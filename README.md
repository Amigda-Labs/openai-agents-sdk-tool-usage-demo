# OpenAI Agents SDK Tool Usage Demo

This is a beginner demo of OpenAI Agents SDK agents that can use different tool types.

The first agent answers course FAQ questions with a local Python function tool. The other demos let you try hosted tools: web search, code interpreter, and tool search.

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

Hosted tools work a little differently:

```text
You
  -> Python script
  -> Agents SDK Runner
  -> Agent
  -> hosted OpenAI tool
```

Those tools run through the OpenAI Responses API. `WebSearchTool` searches the web, `CodeInterpreterTool` runs code in a hosted sandbox, and `ToolSearchTool` lets the model load deferred tools only when needed.

## Setup

```bash
uv sync
cp .env.example .env
```

Then edit `.env` and set:

```bash
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4.1-mini
TOOL_SEARCH_MODEL=gpt-5.5
```

If a hosted tool returns a model-support error, switch `OPENAI_MODEL` to a current OpenAI Responses model that supports hosted tools.
`ToolSearchTool` is stricter than the other demos, so `src/tool_search_demo.py` uses `TOOL_SEARCH_MODEL` and defaults to `gpt-5.5` when `OPENAI_MODEL` is still `gpt-4.1-mini`.

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

## Hosted Tool Demos

Try web search:

```bash
uv run python src/web_search_demo.py "Search the web and summarize the latest OpenAI Agents SDK tool categories."
```

Try code interpreter:

```bash
uv run python src/code_interpreter_demo.py "Use code to analyze these quiz scores: 78, 92, 88, 73, 95, 84."
```

Try tool search:

```bash
uv run python src/tool_search_demo.py "For student stu_202, check progress, find the tool-usage resources they need, and recommend what they should do next."
```

`ToolSearchTool` is different from the other two. It does not answer the user by itself. It searches for deferred tools that the agent can load. In this demo, the searchable tools are grouped into the `course_progress` and `course_content` namespaces.

For a fuller explanation of run items, namespaces, and when to use tool search, open `docs/tool_search_explained.html` in a browser.

## Files

- `src/course_assistant.py` creates and runs the agent.
- `src/course_tools.py` defines the `search_course_faq` tool with `@function_tool`.
- `src/web_search_demo.py` demonstrates `WebSearchTool`.
- `src/code_interpreter_demo.py` demonstrates `CodeInterpreterTool`.
- `src/tool_search_demo.py` demonstrates `ToolSearchTool` with deferred function tools.
- `src/demo_helpers.py` contains shared setup and terminal output helpers.
- `sample_docs/course_faq.json` contains the local knowledge base.

## Verify Syntax

```bash
uv run python -m compileall src
```
