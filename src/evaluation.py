import json
from typing import Any
from openai import AsyncOpenAI
from src.datastructures import Conversation, EvaluationResult

PROMPT = """
You are evaluating a teacher's effectiveness in a dialog. Here is the data:
[BEGIN DATA]
************
[Conversation]:
{conversation_text}
************
[END DATA]

In addition to overall teaching effectiveness, score the teacher on these dimensions:

1) First-Mile Diagnostics
What it is: Did the teacher ask 2–4 focused diagnostic questions before teaching, state/reflect the learner’s goal, map constraints (deadline, required format/tools), and confirm the starting point (“what’s already clear / where you’re stuck?”)?
Rubric (0–5):
0 = no inquiry; 1 = one generic question; 2 = vague/leading questions; 3 = 2+ relevant questions, partial reflection; 4 = clear 3–4 question block + explicit goal reflection; 5 = exemplary: compact diagnosis + summary + agreed short plan.

2) Retrieval Practice (“testing effect”)
What it is: Did the teacher build frequent low-stakes opportunities for students to recall from memory (short quizzes, free recall, chat prompts) rather than only re-reading?
Rubric (0–5):
0 = no retrieval; 1 = ad-hoc single recall; 2 = occasional recall w/o feedback; 3 = weekly low-stakes with brief feedback; 4 = planned daily retrieval + item analysis; 5 = spiraled retrieval with cumulative quizzing that drives re-teaching.

3) Reflect & Revisit (self-checks + scheduled review)
What it is: Did the teacher guide learners to plan, monitor, and evaluate their learning and schedule purposeful revisits across days/weeks?
Rubric (0–5):
0 = none; 1 = “all clear?” only; 2 = reflection without a plan; 3 = reflection + one concrete step; 4 = plan + self-rating + scheduled revisit, with at least occasional mid-task self-checks; 5 = plan + self-rating + spaced schedule tuned by performance (gaps adjusted after misses) and plus regular mid-task self-checks and visible follow-through.

4) Interleaved Practice (mix problem types)
What it is: Did the teacher alternate different problem types/concepts rather than blocking by one type?
Rubric (0–5):
0 = fully blocked; 1 = token mix; 2 = some mixing without cues; 3 = regular interleaving with rationale; 4 = interleaving + strategy labeling; 5 = interleaving adjusted to common mis-selections.

5) Guided Examples & Productive Struggle
What it is: Did the teacher teach with targeted worked examples and a hint ladder (nudge → cue → partial step), then fade support so learners explain steps and solve on their own? Did they mix in light “desirable difficulties” (brief retrieval before reveal; occasional variation in problem type)?
Rubric (0–5):
0 = answer dump; 1 = one hint; 2 = sporadic prompts, no fading; 3 = clear hint ladder or self-explain; 4 = both self-explain and planned fading; 5 = plus brief retrieval/variation and a quick note on why the approach helps

6) High-Quality Feedback (task/process-focused, usable)
What it is: Did the teacher provide timely comments that specify where the work is, what quality looks like, and how to improve—rather than grades alone?
Rubric (0–5):
0 = grades only; 1 = vague praise/critique; 2 = some specifics but no space to use; 3 = specific + limited revision; 4 = clear, timely, with revision cycles; 5 = iterative feedback with student-generated next steps.

7) Socratic Reasoning (disciplined questioning)
What it is: Did the teacher use structured sequences of clarifying, probing-evidence, assumptions, implications, and viewpoint questions to make the student’s thinking visible—without spamming?
Rubric (0–5):
0 = monologue; 1 = yes/no checks; 2 = unfocused barrage; 3 = mixed quality; 4 = consistent sequencing and pacing; 5 = masterful selection that surfaces assumptions + drives revision.

8) Misconception Diagnosis
What it is: Did the teacher go beyond “incorrect” to which mental model produced the error (e.g., overgeneralizing a prior rule), then reframe it?
Rubric (0–5):
0 = simple correction; 1 = rephrase only; 2 = one probe; 3 = probe + contrast; 4 = +reframe and successful check; 5 = +plan to prevent recurrence.

9) Motivation & Relevance (autonomy-supportive framing)
What it is: Did the teacher make the work feel meaningful, connected to the learner’s interests/values, and give them some real choices (how/what/when) while keeping a clear learning goal?
Rubric (0–5):
0 = no attempt to connect or give choice; 1 = generic “this is important” claim, no personalization; 2 = one off-hand relevance comment or trivial choice (e.g., emoji color); 3 = at least one concrete link to learner goals/interests or one meaningful choice; 4 = both a clear relevance link and at least one meaningful choice in the flow; 5 = exemplary: relevance woven through the dialogue, two or more meaningful choices, and language consistently autonomy-supportive.

10) Beliefs & Attributions (ability, effort, strategies)
What it is: Did the teacher shape how learners explain success and failure—away from “I’m just bad at this” and toward “with time, strategies, and effort I can improve,” while staying honest about difficulty?
Rubric (0–5):
0 = no attention to beliefs/attributions; 1 = occasional empty praise/criticism (“You’re smart”, “You’re bad at this”) that reinforces fixed ability; 2 = mixed signals (some strategy talk, some ability labels); 3 = mostly strategy/effort-focused language, but few explicit reframes of learner self-blame; 4 = consistent effort/strategy framing and regular reframes when learner goes to “I can’t.”; 5 = exemplary: beliefs are explicitly surfaced, reframed, and the learner can articulate “what I can do to improve” by the end.

Provide your answer in the following structured format:
OverallRating: <numeric_rating> (1-10)
OverallReasoning: <your_reasoning>
FirstMileDiagnosticsScore: <score> (0-5)
FirstMileDiagnosticsReasoning: <your_reasoning_for_first_mile>
RetrievalPracticeScore: <score> (0-5)
RetrievalPracticeReasoning: <your_reasoning_for_retrieval>
ReflectRevisitScore: <score> (0-5)
ReflectRevisitReasoning: <your_reasoning_for_reflect_revisit>
InterleavedPracticeScore: <score> (0-5)
InterleavedPracticeReasoning: <your_reasoning_for_interleaved_practice>
GuidedExamplesScore: <score> (0-5)
GuidedExamplesReasoning: <your_reasoning_for_guided_examples>
HighQualityFeedbackScore: <score> (0-5)
HighQualityFeedbackReasoning: <your_reasoning_for_high_quality_feedback>
SocraticReasoningScore: <score> (0-5)
SocraticReasoningReasoning: <your_reasoning_for_socratic_reasoning>
MisconceptionDiagnosisScore: <score> (0-5)
MisconceptionDiagnosisReasoning: <your_reasoning_for_misconception_diagnosis>
MotivationRelevanceScore: <score> (0-5)
MotivationRelevanceReasoning: <your_reasoning_for_motivation_relevance>
BeliefsAttributionsScore: <score> (0-5)
BeliefsAttributionsReasoning: <your_reasoning_for_beliefs_attributions>
"""


async def evaluate_conversation_with_grader(
    conversation: Conversation,
    grader: Any,
    grader_model_name: str,
) -> EvaluationResult:
    """
    Evaluates a single conversation using a grader LLM.
    """
    conversation_text = "\n".join(
        f"[{exchange.speaker}]: {exchange.message}"
        for exchange in conversation.exchanges
    )

    response = await grader.chat.completions.create(
        model=grader_model_name,
        messages=[
            {
                "role": "user",
                "content": PROMPT.format(conversation_text=conversation_text),
            }
        ],
        temperature=0,
    )
    # Expecting a structured response in JSON or similar
    # Try to parse the response content for the required fields
    content = response.choices[0].message.content
    try:
        arguments = json.loads(content)
    except Exception:
        import re
        def extract_field(field, text):
            match = re.search(rf"{field}:\s*(.*)", text)
            return match.group(1).strip() if match else None
        def parse_score(val, default=0.0):
            if not val:
                return default
            val = val.strip()
            if "/" in val:
                val = val.split("/")[0]
            try:
                return float(val)
            except Exception:
                return default
        arguments = {
            "rating": parse_score(extract_field("OverallRating", content)),
            "reasons": extract_field("OverallReasoning", content) or "",
            "first_mile_score": parse_score(extract_field("FirstMileDiagnosticsScore", content)),
            "first_mile_reasoning": extract_field("FirstMileDiagnosticsReasoning", content) or "",
            "retrieval_score": parse_score(extract_field("RetrievalPracticeScore", content)),
            "retrieval_reasoning": extract_field("RetrievalPracticeReasoning", content) or "",
            "reflect_revisit_score": parse_score(extract_field("ReflectRevisitScore", content)),
            "reflect_revisit_reasoning": extract_field("ReflectRevisitReasoning", content) or "",
            "interleaved_practice_score": parse_score(extract_field("InterleavedPracticeScore", content)),
            "interleaved_practice_reasoning": extract_field("InterleavedPracticeReasoning", content) or "",
            "guided_examples_score": parse_score(extract_field("GuidedExamplesScore", content)),
            "guided_examples_reasoning": extract_field("GuidedExamplesReasoning", content) or "",
            "high_quality_feedback_score": parse_score(extract_field("HighQualityFeedbackScore", content)),
            "high_quality_feedback_reasoning": extract_field("HighQualityFeedbackReasoning", content) or "",
            "socratic_reasoning_score": parse_score(extract_field("SocraticReasoningScore", content)),
            "socratic_reasoning_reasoning": extract_field("SocraticReasoningReasoning", content) or "",
            "misconception_diagnosis_score": parse_score(extract_field("MisconceptionDiagnosisScore", content)),
            "misconception_diagnosis_reasoning": extract_field("MisconceptionDiagnosisReasoning", content) or "",
            "motivation_relevance_score": parse_score(extract_field("MotivationRelevanceScore", content)),
            "motivation_relevance_reasoning": extract_field("MotivationRelevanceReasoning", content) or "",
            "beliefs_attributions_score": parse_score(extract_field("BeliefsAttributionsScore", content)),
            "beliefs_attributions_reasoning": extract_field("BeliefsAttributionsReasoning", content) or "",
        }

    combined_reasoning = (
        f"Overall: {arguments['reasons']}\n"
        f"First-Mile Diagnostics ({arguments['first_mile_score']}): {arguments['first_mile_reasoning']}\n"
        f"Retrieval Practice ({arguments['retrieval_score']}): {arguments['retrieval_reasoning']}\n"
        f"Reflect & Revisit ({arguments['reflect_revisit_score']}): {arguments['reflect_revisit_reasoning']}\n"
        f"Interleaved Practice ({arguments['interleaved_practice_score']}): {arguments['interleaved_practice_reasoning']}\n"
        f"Guided Examples & Productive Struggle ({arguments['guided_examples_score']}): {arguments['guided_examples_reasoning']}\n"
        f"High-Quality Feedback ({arguments['high_quality_feedback_score']}): {arguments['high_quality_feedback_reasoning']}\n"
        f"Socratic Reasoning ({arguments['socratic_reasoning_score']}): {arguments['socratic_reasoning_reasoning']}\n"
        f"Misconception Diagnosis ({arguments['misconception_diagnosis_score']}): {arguments['misconception_diagnosis_reasoning']}\n"
        f"Motivation & Relevance ({arguments['motivation_relevance_score']}): {arguments['motivation_relevance_reasoning']}\n"
        f"Beliefs & Attributions ({arguments['beliefs_attributions_score']}): {arguments['beliefs_attributions_reasoning']}"
    )
    return EvaluationResult(
        conversation_id=conversation.id,
        rating=arguments["rating"],
        reasoning=combined_reasoning,
        first_mile_score=arguments["first_mile_score"],
        retrieval_score=arguments["retrieval_score"],
        reflect_revisit_score=arguments["reflect_revisit_score"],
        interleaved_practice_score=arguments["interleaved_practice_score"],
        guided_examples_score=arguments["guided_examples_score"],
        high_quality_feedback_score=arguments["high_quality_feedback_score"],
        socratic_reasoning_score=arguments["socratic_reasoning_score"],
        misconception_diagnosis_score=arguments["misconception_diagnosis_score"],
        motivation_relevance_score=arguments["motivation_relevance_score"],
        beliefs_attributions_score=arguments["beliefs_attributions_score"],
    )


def calculate_student_talk_time(conversation: Conversation) -> float:
    """
    Calculates the percentage of words uttered by the student relative to the total number of words in the dialogue.
    """
    student_words = 0
    total_words = 0
    for exchange in conversation.exchanges:
        words = len(exchange.message.split())
        total_words += words
        if exchange.speaker == "Student":
            student_words += words

    if total_words == 0:
        return 0.0
    return student_words / total_words


def calculate_average_words_per_turn(conversation: Conversation) -> float:
    """
    Calculates the average number of words per turn in the conversation.
    """
    total_words = 0
    total_turns = len(conversation.exchanges)
    for exchange in conversation.exchanges:
        words = len(exchange.message.split())
        total_words += words

    if total_turns == 0:
        return 0.0
    return total_words / total_turns
