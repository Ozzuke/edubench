import os
import json
import asyncio
import click
import braintrust
from braintrust.oai import wrap_openai
from openai import AsyncOpenAI
from src.config import load_config
from src.logger import get_logger
from src.scenarios import load_all_students, load_all_scenarios, load_teacher
from src.generator import generate_conversation
from src.evaluation import (
    evaluate_conversation_with_grader,
    calculate_student_talk_time,
    calculate_average_words_per_turn,
)
from src.reporting import aggregate_results, generate_markdown_report

# Initialize logger
logger = get_logger(__name__)

# Load configuration
config = load_config()

# Initialize Braintrust
braintrust.init_logger(project="EduBench", api_key=config["braintrust"]["api_key"])

# Initialize OpenAI clients and wrap them with Braintrust
student_client = wrap_openai(
    AsyncOpenAI(
        api_key=config["student"]["api_key"], base_url=config["student"]["base_url"]
    )
)
teacher_client = wrap_openai(
    AsyncOpenAI(
        api_key=config["teacher"]["api_key"], base_url=config["teacher"]["base_url"]
    )
)
grader_client = wrap_openai(
    AsyncOpenAI(
        api_key=config["grader"]["api_key"], base_url=config["grader"]["base_url"]
    )
)
moderator_client = wrap_openai(
    AsyncOpenAI(
        api_key=config["moderator"]["api_key"],
        base_url=config["moderator"]["base_url"],
    )
)


@click.group()
def cli():
    pass


async def async_run(output_dir: str):
    """
    Runs the EduBench benchmark pipeline asynchronously.
    """
    os.makedirs(output_dir, exist_ok=True)

    # Load all students and scenarios
    students = load_all_students("data/students")
    scenarios = load_all_scenarios("data/scenarios")
    teacher = load_teacher("data/teacher/teacher.yaml")

    # Generate conversations
    conversations = []
    for student in students:
        for scenario in scenarios:
            logger.info(
                f"Generating conversation for student {student.id} and scenario {scenario.id}..."
            )
            conversation = await generate_conversation(
                student=student,
                scenario=scenario,
                teacher=teacher,
                teacher_model=teacher_client,
                student_model=student_client,
                moderator_model=moderator_client,
                teacher_model_name=config["teacher"]["model"] or "",
                student_model_name=config["student"]["model"] or "",
                moderator_model_name=config["moderator"]["model"] or "",
            )
            conversations.append(conversation)

    # Save conversations to a JSONL file
    conversations_file_jsonl = os.path.join(output_dir, "conversations.jsonl")
    with open(conversations_file_jsonl, "w") as f:
        for conversation in conversations:
            f.write(json.dumps(conversation.dict()) + "\n")
    logger.info(
        f"Generated {len(conversations)} conversations and saved them to {conversations_file_jsonl}"
    )

    # Save conversations to a JSON file for easier use
    conversations_file_json = os.path.join(output_dir, "conversations.json")
    with open(conversations_file_json, "w") as f:
        json.dump([c.dict() for c in conversations], f, indent=4)
    logger.info(
        f"Saved {len(conversations)} conversations to {conversations_file_json}"
    )

    # Evaluate conversations
    evaluation_results = []
    for conversation in conversations:
        logger.info(f"Evaluating conversation {conversation.id}...")
        evaluation_result = await evaluate_conversation_with_grader(
            conversation=conversation,
            grader=grader_client,
            grader_model_name=config["grader"]["model"] or "",
        )
        evaluation_results.append(evaluation_result)

    # Save evaluation results to a JSONL file
    evaluations_file = os.path.join(output_dir, "evaluations.jsonl")
    with open(evaluations_file, "w") as f:
        for result in evaluation_results:
            f.write(json.dumps(result.dict()) + "\n")
    logger.info(
        f"Evaluated {len(evaluation_results)} conversations and saved results to {evaluations_file}"
    )

    # Aggregate results
    aggregated_data = aggregate_results(evaluation_results)

    # Calculate statistical metrics and add to aggregated data
    total_student_talk_time = 0.0
    total_average_words_per_turn = 0.0
    for conversation in conversations:
        total_student_talk_time += calculate_student_talk_time(conversation)
        total_average_words_per_turn += calculate_average_words_per_turn(conversation)

    aggregated_data["metrics"]["student_talk_time"] = total_student_talk_time / len(
        conversations
    )
    aggregated_data["metrics"]["average_words_per_turn"] = (
        total_average_words_per_turn / len(conversations)
    )

    # Generate and save report
    report = generate_markdown_report(aggregated_data)
    report_file = os.path.join(output_dir, "report.md")
    with open(report_file, "w") as f:
        f.write(report)
    logger.info(f"Generated report and saved to {report_file}")


@cli.command()
@click.option("--output-dir", default="results", help="Directory to save results.")
def run(output_dir: str):
    """
    Runs the EduBench benchmark pipeline.
    """
    asyncio.run(async_run(output_dir))


if __name__ == "__main__":
    cli()
