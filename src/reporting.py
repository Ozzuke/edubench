from typing import List, Dict, Any
from src.datastructures import EvaluationResult


def aggregate_results(evaluation_results: List[EvaluationResult]) -> Dict[str, Any]:
    """
    Aggregates evaluation results and statistical metrics.
    """
    total_rating = 0.0
    for result in evaluation_results:
        total_rating += result.rating

    average_rating = (
        total_rating / len(evaluation_results) if evaluation_results else 0.0
    )

    # Placeholder for other metrics, will be added later
    metrics = {
        "student_talk_time": 0.0,
        "average_words_per_turn": 0.0,
    }

    return {
        "average_rating": average_rating,
        "num_evaluations": len(evaluation_results),
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
    report += (
        f"- Student Talk Time: {aggregated_data['metrics']['student_talk_time']:.2%}\n"
    )
    report += f"- Average Words per Turn: {aggregated_data['metrics']['average_words_per_turn']:.2f}\n"

    return report
