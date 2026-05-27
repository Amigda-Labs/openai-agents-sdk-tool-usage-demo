# OpenAI Agents SDK Tool Usage Demo

This is a beginner demo of an OpenAI Agents SDK agent that can call a Python function as a tool.

The agent answers course FAQ questions. When the question needs course-specific information, the model can call the `search_course_faq` tool, read the matching local FAQ entry, and then answer the user.

## Mental Model

```text
You
  -> Python script
  -> Agents SDK Runner
  -> CourseHelper agent
  -> search_course_faq tool
  -> sample_docs/course_faq.json
```

The important idea: the model does not already know the local course policy. The tool gives the agent a controlled way to fetch that information.

## Setup

```bash
uv sync
cp .env.example .env
```

Then edit `.env` and set:

```bash
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4.1-mini
```

## Run

Ask the default question:

```bash
uv run python src/course_assistant.py
```

Ask your own question:

```bash
uv run python src/course_assistant.py "Can late assignments still receive full credit?"
uv run python src/course_assistant.py "What happens in week 3?"
uv run python src/course_assistant.py "How is the final grade calculated?"
```

When the tool is used, you will see a line like:

```text
[tool] search_course_faq called with query: late assignments full credit
```

That print statement is only for teaching. It makes tool usage visible in the terminal.

## Files

- `src/course_assistant.py` creates and runs the agent.
- `src/course_tools.py` defines the `search_course_faq` tool with `@function_tool`.
- `sample_docs/course_faq.json` contains the local knowledge base.

## Verify Syntax

```bash
uv run python -m compileall src
```
