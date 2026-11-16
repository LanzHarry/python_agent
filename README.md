# Boot.dev Python Coding Agent

The code in this repo was generated for the
[boot.dev](https://www.boot.dev/dashboard) python AI agent project. It uses the
OpenAI sdk to build a basic harness for a coding agent that can:

- List files in a working directory
- Read file contents
- Write to files
- Run Python files

The LLM inference is accessed via OpenRouter on their free tier so this
harness/model combination is simply a proof of concept rather than any serious
attempt at making a useful agent.

This whole repo is just a proof of concept and a quick learning tool, therefore
the structure can be somewhat in violation of concepts like DRY and some
refactoring could clean it up. However, it serves its purpose and the agent is
able to handle basic tasks and refactors of the toy calculator app that comes as
part of the guided project.
