from __future__ import annotations

import argparse
import json
import os
from typing import Any

from dotenv import load_dotenv


def parse_question(description: str, default_question: str) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "question",
        nargs="?",
        default=default_question,
        help="Question or task to send to the agent.",
    )
    return parser.parse_args()


def load_model_name(default_model: str = "gpt-4.1-mini") -> str:
    load_dotenv()

    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is missing. Copy .env.example to .env and fill it in.")

    return os.getenv("OPENAI_MODEL", default_model)


def _raw_item_data(raw_item: Any) -> dict[str, Any]:
    if isinstance(raw_item, dict):
        return raw_item
    if hasattr(raw_item, "model_dump"):
        return raw_item.model_dump(exclude_unset=True)
    return {}


def _short_text(value: Any, max_length: int = 120) -> str:
    text = value if isinstance(value, str) else json.dumps(value, default=str)
    if len(text) <= max_length:
        return text
    return f"{text[: max_length - 3]}..."


def _format_tool_search_output(tools: list[dict[str, Any]]) -> str:
    loaded = []
    for tool in tools:
        tool_name = tool.get("name", "unknown")
        child_tools = tool.get("tools")
        if isinstance(child_tools, list):
            child_names = [child.get("name", "unknown") for child in child_tools]
            loaded.append(f"{tool_name} -> {', '.join(child_names)}")
        else:
            loaded.append(tool_name)
    return "; ".join(loaded)


def print_run_result(result: Any) -> None:
    print("\nAssistant answer:")
    print(result.final_output)

    new_items = getattr(result, "new_items", [])
    if not new_items:
        return

    print("\nRun items:")
    for item in new_items:
        item_type = getattr(item, "type", type(item).__name__)
        raw_item = getattr(item, "raw_item", None)
        raw_data = _raw_item_data(raw_item)
        raw_type = raw_data.get("type") or getattr(raw_item, "type", None)
        raw_name = raw_data.get("name") or getattr(raw_item, "name", None)
        namespace = raw_data.get("namespace")

        if item_type == "tool_search_call_item":
            arguments = raw_data.get("arguments", {})
            execution = raw_data.get("execution", "unknown")
            print(f"- {item_type}: execution={execution}, arguments={_short_text(arguments)}")
            continue

        if item_type == "tool_search_output_item":
            tools = raw_data.get("tools", [])
            if isinstance(tools, list):
                print(f"- {item_type}: loaded {_format_tool_search_output(tools)}")
            else:
                print(f"- {item_type}: loaded {_short_text(tools)}")
            continue

        if item_type == "tool_call_item" and raw_name:
            qualified_name = f"{namespace}.{raw_name}" if namespace else raw_name
            arguments = raw_data.get("arguments")
            suffix = f" args={_short_text(arguments)}" if arguments else ""
            print(f"- {item_type}: {qualified_name}{suffix}")
            continue

        if item_type == "tool_call_output_item":
            output = raw_data.get("output")
            suffix = f": {_short_text(output)}" if output else ""
            print(f"- {item_type}{suffix}")
            continue

        if raw_name:
            print(f"- {item_type}: {raw_name}")
        elif raw_type:
            print(f"- {item_type}: {raw_type}")
        else:
            print(f"- {item_type}")
