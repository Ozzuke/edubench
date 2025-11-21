from typing import List, Dict, Any
from src.datastructures import EvaluationResult


def aggregate_results(evaluation_results: List[EvaluationResult]) -> Dict[str, Any]:
    """
    Aggregates evaluation results and statistical metrics.
    """
    total_rating = 0.0
    total_first_mile = 0.0
    total_retrieval = 0.0
    total_reflect_revisit = 0.0
    total_interleaved_practice = 0.0
    total_guided_examples = 0.0
    total_high_quality_feedback = 0.0
    total_socratic_reasoning = 0.0
    total_misconception_diagnosis = 0.0
    total_motivation_relevance = 0.0
    total_beliefs_attributions = 0.0
    for result in evaluation_results:
        total_rating += result.rating
        total_first_mile += getattr(result, "first_mile_score", 0.0)
        total_retrieval += getattr(result, "retrieval_score", 0.0)
        total_reflect_revisit += getattr(result, "reflect_revisit_score", 0.0)
        total_interleaved_practice += getattr(result, "interleaved_practice_score", 0.0)
        total_guided_examples += getattr(result, "guided_examples_score", 0.0)
        total_high_quality_feedback += getattr(result, "high_quality_feedback_score", 0.0)
        total_socratic_reasoning += getattr(result, "socratic_reasoning_score", 0.0)
        total_misconception_diagnosis += getattr(result, "misconception_diagnosis_score", 0.0)
        total_motivation_relevance += getattr(result, "motivation_relevance_score", 0.0)
        total_beliefs_attributions += getattr(result, "beliefs_attributions_score", 0.0)

    n = len(evaluation_results)
    average_rating = total_rating / n if n else 0.0
    average_first_mile = total_first_mile / n if n else 0.0
    average_retrieval = total_retrieval / n if n else 0.0
    average_reflect_revisit = total_reflect_revisit / n if n else 0.0
    average_interleaved_practice = total_interleaved_practice / n if n else 0.0
    average_guided_examples = total_guided_examples / n if n else 0.0
    average_high_quality_feedback = total_high_quality_feedback / n if n else 0.0
    average_socratic_reasoning = total_socratic_reasoning / n if n else 0.0
    average_misconception_diagnosis = total_misconception_diagnosis / n if n else 0.0
    average_motivation_relevance = total_motivation_relevance / n if n else 0.0
    average_beliefs_attributions = total_beliefs_attributions / n if n else 0.0

    metrics = {
        "student_talk_time": 0.0,
        "average_words_per_turn": 0.0,
        "average_first_mile_score": average_first_mile,
        "average_retrieval_score": average_retrieval,
        "average_reflect_revisit_score": average_reflect_revisit,
        "average_interleaved_practice_score": average_interleaved_practice,
        "average_guided_examples_score": average_guided_examples,
        "average_high_quality_feedback_score": average_high_quality_feedback,
        "average_socratic_reasoning_score": average_socratic_reasoning,
        "average_misconception_diagnosis_score": average_misconception_diagnosis,
        "average_motivation_relevance_score": average_motivation_relevance,
        "average_beliefs_attributions_score": average_beliefs_attributions,
    }

    return {
        "average_rating": average_rating,
        "num_evaluations": n,
        "metrics": metrics,
    }


def generate_markdown_report(aggregated_data: Dict[str, Any]) -> str:
    """
    Generates a summary report in Markdown.
    """
    report = "# EduBench Evaluation Report\n\n"
    report += "## Summary\n"
    report += f"- Average Rating: {aggregated_data['average_rating']:.2f}\n"
    report += f"- Number of Evaluations: {aggregated_data['num_evaluations']}\n\n"

    report += "## Statistical Metrics\n"
    report += f"- Student Talk Time: {aggregated_data['metrics']['student_talk_time']:.2%}\n"
    report += f"- Average Words per Turn: {aggregated_data['metrics']['average_words_per_turn']:.2f}\n"
    report += f"- Average First-Mile Diagnostics Score: {aggregated_data['metrics']['average_first_mile_score']:.2f}\n"
    report += f"- Average Retrieval Practice Score: {aggregated_data['metrics']['average_retrieval_score']:.2f}\n"
    report += f"- Average Reflect & Revisit Score: {aggregated_data['metrics']['average_reflect_revisit_score']:.2f}\n"
    report += f"- Average Interleaved Practice Score: {aggregated_data['metrics']['average_interleaved_practice_score']:.2f}\n"
    report += f"- Average Guided Examples & Productive Struggle Score: {aggregated_data['metrics']['average_guided_examples_score']:.2f}\n"
    report += f"- Average High-Quality Feedback Score: {aggregated_data['metrics']['average_high_quality_feedback_score']:.2f}\n"
    report += f"- Average Socratic Reasoning Score: {aggregated_data['metrics']['average_socratic_reasoning_score']:.2f}\n"
    report += f"- Average Misconception Diagnosis Score: {aggregated_data['metrics']['average_misconception_diagnosis_score']:.2f}\n"
    report += f"- Average Motivation & Relevance Score: {aggregated_data['metrics']['average_motivation_relevance_score']:.2f}\n"
    report += f"- Average Beliefs & Attributions Score: {aggregated_data['metrics']['average_beliefs_attributions_score']:.2f}\n"
    return report
