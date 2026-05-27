from __future__ import annotations

from agents import Agent, CodeInterpreterTool, ModelSettings, Runner

from demo_helpers import load_model_name, parse_question, print_run_result

DEFAULT_QUESTION = (
    "Use code to analyze these quiz scores: 78, 92, 88, 73, 95, 84. "
    "Return the mean, median, highest score, lowest score, and a short interpretation."
)


def build_agent() -> Agent:
    return Agent(
        name="CodeInterpreterDemo",
        model=load_model_name(),
        instructions=(
            "You are demonstrating the hosted CodeInterpreterTool. "
            "For the first step, call the code interpreter and do not write a text preamble. "
            "In the code you run, always print the computed values so they appear as tool output. "
            "After the tool finishes, use the printed output to give the final answer."
        ),
        model_settings=ModelSettings(tool_choice="required"),
        tools=[
            CodeInterpreterTool(
                tool_config={
                    "type": "code_interpreter",
                    "container": {"type": "auto"},
                }
            )
        ],
    )


def main() -> None:
    args = parse_question(
        "Ask an agent that can use the hosted CodeInterpreterTool.",
        DEFAULT_QUESTION,
    )
    result = Runner.run_sync(build_agent(), args.question)
    print_run_result(result)


if __name__ == "__main__":
    main()
