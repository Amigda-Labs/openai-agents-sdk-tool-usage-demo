from __future__ import annotations

import os
from typing import Annotated

from dotenv import load_dotenv

from agents import Agent, Runner, ToolSearchTool, function_tool, tool_namespace

from demo_helpers import parse_question, print_run_result

DEFAULT_QUESTION = (
    "For student stu_202, check progress, find the tool-usage resources they need, "
    "and recommend what they should do next."
)
DEFAULT_TOOL_SEARCH_MODEL = "gpt-5.5"


def load_tool_search_model() -> str:
    load_dotenv()

    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is missing. Copy .env.example to .env and fill it in.")

    model = os.getenv("TOOL_SEARCH_MODEL")
    if model:
        return model

    configured_model = os.getenv("OPENAI_MODEL")
    if configured_model and configured_model != "gpt-4.1-mini":
        return configured_model

    print(
        f"[setup] ToolSearchTool is not supported with gpt-4.1-mini; "
        f"using {DEFAULT_TOOL_SEARCH_MODEL} for this demo."
    )
    return DEFAULT_TOOL_SEARCH_MODEL


@function_tool(defer_loading=True)
def get_student_progress(
    student_id: Annotated[str, "Student id, for example stu_101 or stu_202."],
) -> str:
    """Fetch a student's course progress summary."""
    print(f"[tool] get_student_progress called with student_id: {student_id}")

    progress = {
        "stu_101": "Maya completed weeks 1 and 2, missed the week 3 tool-usage exercise, and has strong participation.",
        "stu_202": "Leo completed week 1, submitted week 2 late, and has not started the week 3 tool-usage exercise.",
    }
    return progress.get(student_id, f"No progress record found for {student_id}.")


@function_tool(defer_loading=True)
def list_course_resources(
    topic: Annotated[str, "Course topic to find resources for, such as tools or structured outputs."],
) -> str:
    """List course resources for a topic."""
    print(f"[tool] list_course_resources called with topic: {topic}")

    topic_lower = topic.lower()
    if "tool" in topic_lower:
        return "Resources: Agents SDK tools guide, course FAQ week 3 notes, and the local function-tool demo."
    if "structured" in topic_lower:
        return "Resources: structured outputs primer, validation checklist, and week 2 examples."
    return "Resources: course FAQ, weekly slides, and instructor office hours."


@function_tool(defer_loading=True)
def get_week_topic(
    week_number: Annotated[int, "Course week number, for example 1, 2, 3, or 4."],
) -> str:
    """Fetch the main topic for a course week."""
    print(f"[tool] get_week_topic called with week_number: {week_number}")

    schedule = {
        1: "Week 1 covers setup and prompt basics.",
        2: "Week 2 covers structured outputs and validation.",
        3: "Week 3 covers tool usage with the OpenAI Agents SDK.",
        4: "Week 4 covers final project demos and feedback.",
    }
    return schedule.get(week_number, f"No topic is configured for week {week_number}.")


@function_tool(defer_loading=True)
def recommend_next_step(
    student_id: Annotated[str, "Student id, for example stu_101 or stu_202."],
    topic: Annotated[str, "Topic the recommendation should focus on."],
) -> str:
    """Recommend the next course action for a student."""
    print(f"[tool] recommend_next_step called with student_id: {student_id}, topic: {topic}")

    return (
        f"For {student_id}, assign a short catch-up task on {topic}: run the demo, "
        "identify which tool was called, and write a 3-sentence reflection."
    )


course_progress_tools = tool_namespace(
    name="course_progress",
    description="Student progress and next-step recommendation tools.",
    tools=[get_student_progress, recommend_next_step],
)

course_content_tools = tool_namespace(
    name="course_content",
    description="Course content tools for weekly topics and learning resources.",
    tools=[get_week_topic, list_course_resources],
)


def build_agent() -> Agent:
    return Agent(
        name="ToolSearchDemo",
        model=load_tool_search_model(),
        instructions=(
            "You are demonstrating ToolSearchTool. "
            "First search for and load the right tool namespaces, then call the loaded tools. "
            "Use course_progress for student status and recommendations. "
            "Use course_content for week topics and learning resources. "
            "Explain which tools were useful in one short final answer."
        ),
        tools=[*course_progress_tools, *course_content_tools, ToolSearchTool()],
    )


def main() -> None:
    args = parse_question(
        "Ask an agent that can use ToolSearchTool to load deferred tools.",
        DEFAULT_QUESTION,
    )
    result = Runner.run_sync(build_agent(), args.question)
    print_run_result(result)


if __name__ == "__main__":
    main()
