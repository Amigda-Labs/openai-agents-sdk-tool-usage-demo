from __future__ import annotations

import argparse
import os

from agents import Agent, Runner
from dotenv import load_dotenv

from course_tools import search_course_faq

DEFAULT_QUESTION = "Can late assignments still receive full credit?"


def build_agent() -> Agent:
    model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

    return Agent(
        name="CourseHelper",
        model=model,
        instructions=(
            "You answer beginner course questions. "
            "Use the search_course_faq tool before answering questions about policies, grading, "
            "schedule, support, assignments, or office hours. "
            "Keep answers short and cite the FAQ title you used."
        ),
        tools=[search_course_faq],
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Ask a course FAQ question using an OpenAI Agents SDK tool."
    )
    parser.add_argument(
        "question",
        nargs="?",
        default=DEFAULT_QUESTION,
        help="Question to ask the CourseHelper agent.",
    )
    return parser.parse_args()


def main() -> None:
    load_dotenv()
    args = parse_args()

    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is missing. Copy .env.example to .env and fill it in.")

    agent = build_agent()
    result = Runner.run_sync(agent, args.question)

    print("\nAssistant answer:")
    print(result.final_output)


if __name__ == "__main__":
    main()
