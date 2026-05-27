from __future__ import annotations

from typing import Annotated

from agents import Agent, Runner, ToolSearchTool, function_tool, tool_namespace

from demo_helpers import load_model_name, parse_question, print_run_result

DEFAULT_QUESTION = (
    "For student stu_101, check progress and recommend what they should do next."
)


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


course_admin_tools = tool_namespace(
    name="course_admin",
    description="Course administration tools for student progress, resources, and next-step recommendations.",
    tools=[get_student_progress, list_course_resources, recommend_next_step],
)


def build_agent() -> Agent:
    return Agent(
        name="ToolSearchDemo",
        model=load_model_name(),
        instructions=(
            "You are demonstrating ToolSearchTool. "
            "First search for and load the right course_admin tools, then call the loaded tools. "
            "Explain which tools were useful in one short final answer."
        ),
        tools=[*course_admin_tools, ToolSearchTool()],
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
