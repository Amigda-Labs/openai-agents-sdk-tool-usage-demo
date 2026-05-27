from __future__ import annotations

import json
from pathlib import Path

from agents import function_tool

ROOT_DIR = Path(__file__).resolve().parents[1]
FAQ_PATH = ROOT_DIR / "sample_docs" / "course_faq.json"


def _load_course_faq() -> list[dict[str, str]]:
    with FAQ_PATH.open(encoding="utf-8") as file:
        return json.load(file)


def _score_entry(query: str, entry: dict[str, str]) -> int:
    query_words = {word.strip(".,?!:;").lower() for word in query.split()}
    text = f"{entry['topic']} {entry['title']} {entry['content']}".lower()
    return sum(1 for word in query_words if word and word in text)


@function_tool
def search_course_faq(query: str) -> str:
    """Search the course FAQ for policies, schedule details, grading rules, or support options."""
    print(f"[tool] search_course_faq called with query: {query}")

    entries = _load_course_faq()
    ranked_entries = sorted(entries, key=lambda entry: _score_entry(query, entry), reverse=True)
    matches = [entry for entry in ranked_entries if _score_entry(query, entry) > 0][:2]

    if not matches:
        return "No matching course FAQ entry was found."

    formatted_matches = []
    for entry in matches:
        formatted_matches.append(
            f"Topic: {entry['topic']}\n"
            f"Title: {entry['title']}\n"
            f"Content: {entry['content']}"
        )

    return "\n\n---\n\n".join(formatted_matches)
