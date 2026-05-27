from __future__ import annotations

from agents import Agent, Runner, WebSearchTool

from demo_helpers import load_model_name, parse_question, print_run_result

DEFAULT_QUESTION = "Search the web and summarize the latest OpenAI Agents SDK tool categories."


def build_agent() -> Agent:
    return Agent(
        name="WebSearchDemo",
        model=load_model_name(),
        instructions=(
            "You are demonstrating the hosted WebSearchTool. "
            "Use web search for current or external facts. "
            "Keep the answer short and mention the sources you used when available."
        ),
        tools=[WebSearchTool(search_context_size="low")],
    )


def main() -> None:
    args = parse_question(
        "Ask an agent that can use the hosted WebSearchTool.",
        DEFAULT_QUESTION,
    )
    result = Runner.run_sync(build_agent(), args.question)
    print_run_result(result)


if __name__ == "__main__":
    main()
