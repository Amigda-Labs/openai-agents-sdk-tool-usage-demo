from __future__ import annotations

import argparse
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


def load_model_name() -> str:
    load_dotenv()

    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is missing. Copy .env.example to .env and fill it in.")

    return os.getenv("OPENAI_MODEL", "gpt-4.1-mini")


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
        raw_type = getattr(raw_item, "type", None)
        raw_name = getattr(raw_item, "name", None)

        if raw_name:
            print(f"- {item_type}: {raw_name}")
        elif raw_type:
            print(f"- {item_type}: {raw_type}")
        else:
            print(f"- {item_type}")
