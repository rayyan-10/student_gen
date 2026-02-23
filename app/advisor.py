import re
import json
import time
import logging
from groq import Groq, RateLimitError
from app.config import get_settings
from app.ml_service import (
    get_high_risk_students,
    get_student_analysis,
    predict_all_students,
)
from app.schemas import AdvisorResponse

logger = logging.getLogger(__name__)
settings = get_settings()

# ── Groq Client ────────────────────────────────────────────────────────

_client = None


def _get_client():
    global _client
    if _client is None:
        _client = Groq(api_key=settings.GROQ_API_KEY)
    return _client


def _call_llm(prompt: str, max_retries: int = 3) -> str:
    """Send a prompt to Groq with retry logic for rate limits."""
    client = _get_client()
    wait_times = [15, 30, 60]  # seconds between retries

    for attempt in range(max_retries + 1):
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=2048,
            )
            return response.choices[0].message.content
        except RateLimitError:
            if attempt < max_retries:
                wait = wait_times[attempt]
                logger.warning(f"Rate limited. Retrying in {wait}s (attempt {attempt + 1}/{max_retries})")
                time.sleep(wait)
            else:
                raise RuntimeError(
                    "Groq API rate limit exceeded after retries. "
                    "Please wait a minute and try again."
                )


# ── Query Classification ──────────────────────────────────────────────

def _classify_query(query: str) -> str:
    """Determine intent from the user query string."""
    q = query.lower()

    if any(kw in q for kw in ["quiz", "generate quiz", "mcq", "practice"]):
        return "generate_quiz"

    if any(kw in q for kw in ["intervention", "need help", "at risk students",
                               "who need", "struggling", "which students"]):
        return "intervention"

    if any(kw in q for kw in ["why is", "risk of", "analyze student",
                               "student s", "student "]):
        # Check if a specific student ID is mentioned
        if _extract_student_id(query) is not None:
            return "student_risk"

    return "general"


def _extract_student_id(query: str) -> int | None:
    """Extract a student ID number from the query."""
    # Match patterns like S101, s101, student 101, #101, id 101
    patterns = [
        r"[Ss](\d+)",
        r"student\s*#?\s*(\d+)",
        r"id\s*#?\s*(\d+)",
        r"#(\d+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, query)
        if match:
            return int(match.group(1))
    return None


# ── Handlers ──────────────────────────────────────────────────────────

def _handle_intervention() -> AdvisorResponse:
    """List all HIGH risk students with their weak topics."""
    high_risk = get_high_risk_students()

    if not high_risk:
        return AdvisorResponse(
            response_type="intervention",
            message="No students are currently at HIGH risk. All students are performing adequately.",
            data=[],
        )

    summary_lines = []
    for s in high_risk:
        weak = ", ".join(s["weak_topics"]) if s["weak_topics"] else "None below 50"
        summary_lines.append(
            f"• Student {s['student_id']} — Pass Prob: {s['pass_probability']:.2%}, "
            f"Weak Topics: {weak}"
        )

    message = (
        f"Found {len(high_risk)} HIGH-risk students who need immediate intervention:\n\n"
        + "\n".join(summary_lines)
    )

    return AdvisorResponse(
        response_type="intervention",
        message=message,
        data=high_risk,
    )


def _handle_student_risk(student_id: int) -> AdvisorResponse:
    """Explain why a specific student is at risk."""
    analysis = get_student_analysis(student_id)

    if analysis is None:
        return AdvisorResponse(
            response_type="student_risk",
            message=f"Student with ID {student_id} was not found in the dataset.",
            data=None,
        )

    # Build a structured JSON explanation via LLM
    prompt = f"""You are an academic advisor AI. Analyze this student data and respond in ONLY valid JSON (no markdown, no extra text).

Student Data:
- Student ID: {analysis['student_id']}
- Attendance: {analysis['attendance']}%
- Internal Marks: {analysis['internal_marks']}/100
- Assignment Marks: {analysis['assignment_marks']}/100
- Previous GPA: {analysis['previous_gpa']}/10
- Topic Scores: {json.dumps(analysis['topic_scores'])}
- Pass Probability: {analysis['pass_probability']:.2%}
- Risk Level: {analysis['risk_level']}
- Weak Topics (below 50): {', '.join(analysis['weak_topics']) if analysis['weak_topics'] else 'None'}

Return ONLY this JSON structure:
{{
  "summary": "One-line summary of the student's situation",
  "risk_factors": [
    {{"factor": "Short title", "detail": "Brief explanation", "severity": "HIGH/MEDIUM/LOW"}}
  ],
  "recommendations": [
    {{"action": "Short action title", "detail": "Specific step to take", "priority": 1}}
  ]
}}"""

    raw = _call_llm(prompt)

    # Parse the structured response
    try:
        cleaned = raw.strip()
        if cleaned.startswith("```"):
            cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
            cleaned = re.sub(r"\s*```$", "", cleaned)
        ai_analysis = json.loads(cleaned)
    except json.JSONDecodeError:
        ai_analysis = {"summary": raw, "risk_factors": [], "recommendations": []}

    # Merge student data + AI analysis into one structured response
    analysis["ai_analysis"] = ai_analysis

    return AdvisorResponse(
        response_type="student_risk",
        message=ai_analysis.get("summary", "Analysis complete."),
        data=analysis,
    )


def _handle_generate_quiz(student_id: int) -> AdvisorResponse:
    """Generate a personalized quiz for a student based on their weak topics."""
    analysis = get_student_analysis(student_id)

    if analysis is None:
        return AdvisorResponse(
            response_type="generate_quiz",
            message=f"Student with ID {student_id} was not found in the dataset.",
            data=None,
        )

    if analysis["risk_level"] != "HIGH":
        return AdvisorResponse(
            response_type="generate_quiz",
            message=(
                f"Student {student_id} is at {analysis['risk_level']} risk "
                f"(pass probability: {analysis['pass_probability']:.2%}). "
                "Quiz generation is designed for HIGH risk students. "
                "This student does not require immediate intervention."
            ),
            data=analysis,
        )

    # Determine weakest 2 topics
    topic_scores = analysis["topic_scores"]
    sorted_topics = sorted(topic_scores.items(), key=lambda x: x[1])
    weakest_two = sorted_topics[:2]
    weakest_names = [t[0] for t in weakest_two]

    # Difficulty based on internal marks
    internal = analysis["internal_marks"]
    if internal < 40:
        difficulty = "Easy"
    elif internal < 60:
        difficulty = "Medium"
    else:
        difficulty = "Hard"

    prompt = f"""You are an academic quiz generator for a Data Structures & Algorithms course.

Generate a Predictive Learning Intervention quiz for a student struggling with: {', '.join(weakest_names)}.

Student context:
- Internal Marks: {internal}/100
- Required Difficulty: {difficulty}
- Weakest topic scores: {json.dumps(dict(weakest_two))}

Generate EXACTLY the following in valid JSON (no markdown fences, pure JSON):
{{
  "mcqs": [
    {{
      "question": "...",
      "options": ["A) ...", "B) ...", "C) ...", "D) ..."],
      "correct_answer": "A/B/C/D",
      "difficulty": "{difficulty}"
    }},
    // 3 MCQs total covering the weak topics
  ],
  "coding_problem": "A clear coding problem related to {weakest_names[0]} with input/output examples",
  "conceptual_explanation": "A clear, concise explanation of the core concept of {weakest_names[0]} and {weakest_names[1]} that the student should review"
}}

Make questions relevant, educational, and at {difficulty} difficulty.
Return ONLY valid JSON, no extra text."""

    raw_response = _call_llm(prompt)

    # Parse the JSON response
    try:
        # Strip markdown code fences if present
        cleaned = raw_response.strip()
        if cleaned.startswith("```"):
            cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
            cleaned = re.sub(r"\s*```$", "", cleaned)
        quiz_data = json.loads(cleaned)
    except json.JSONDecodeError:
        quiz_data = {"raw_response": raw_response}

    quiz_data["target_student"] = f"S{student_id}"
    quiz_data["risk_level"] = analysis["risk_level"]
    quiz_data["weakest_topics"] = weakest_names

    return AdvisorResponse(
        response_type="generate_quiz",
        message=(
            f"Generated {difficulty}-level quiz for Student {student_id} "
            f"targeting weak topics: {', '.join(weakest_names)}."
        ),
        data=quiz_data,
    )


def _handle_general(query: str) -> AdvisorResponse:
    """Use Gemini to answer a free-form academic query with student context."""
    all_students = predict_all_students()
    high_risk = [s for s in all_students if s["risk_level"] == "HIGH"]
    medium_risk = [s for s in all_students if s["risk_level"] == "MEDIUM"]

    context_summary = (
        f"Total students: {len(all_students)}\n"
        f"HIGH risk: {len(high_risk)}\n"
        f"MEDIUM risk: {len(medium_risk)}\n"
        f"LOW risk: {len(all_students) - len(high_risk) - len(medium_risk)}\n"
    )

    if high_risk:
        top_risk = sorted(high_risk, key=lambda x: x["pass_probability"])[:5]
        context_summary += "\nTop 5 most at-risk students:\n"
        for s in top_risk:
            context_summary += (
                f"  - Student {s['student_id']}: "
                f"Pass Prob {s['pass_probability']:.2%}, "
                f"Weak: {', '.join(s['weak_topics'])}\n"
            )

    prompt = f"""You are a GenAI Academic Advisor for a university's Student Result 
Analysis & Pass Prediction System. You have access to the following class overview:

{context_summary}

The user asks: "{query}"

Provide a helpful, structured, and actionable response based on the data available. 
If the query is about a specific student and you have data, reference it. 
Keep your response concise and practical."""

    response_text = _call_llm(prompt)

    return AdvisorResponse(
        response_type="general",
        message=response_text,
        data={"total_students": len(all_students),
              "high_risk_count": len(high_risk),
              "medium_risk_count": len(medium_risk)},
    )


# ── Main Entry Point ──────────────────────────────────────────────────

def handle_query(query: str) -> AdvisorResponse:
    """Route the user query to the appropriate handler."""
    intent = _classify_query(query)

    if intent == "intervention":
        return _handle_intervention()

    elif intent == "student_risk":
        student_id = _extract_student_id(query)
        if student_id is None:
            return AdvisorResponse(
                response_type="student_risk",
                message="Could not extract a student ID from your query. "
                        "Please specify a student like 'S101' or 'student 101'.",
                data=None,
            )
        return _handle_student_risk(student_id)

    elif intent == "generate_quiz":
        student_id = _extract_student_id(query)
        if student_id is None:
            return AdvisorResponse(
                response_type="generate_quiz",
                message="Please specify which student to generate a quiz for. "
                        "Example: 'Generate quiz for student S101'.",
                data=None,
            )
        return _handle_generate_quiz(student_id)

    else:
        return _handle_general(query)
