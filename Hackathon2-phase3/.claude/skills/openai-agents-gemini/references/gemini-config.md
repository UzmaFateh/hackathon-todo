# OpenAI Agents SDK with Gemini Backend

## Configuration
- **Backend:** Gemini via `AsyncOpenAI` client.
- **Base URL:** `https://generativelanguage.googleapis.com/v1beta/openai/`
- **Model:** `gemini-2.5-flash`
- **API Key:** `GEMINI_API_KEY` environment variable.

## Models vs Clients
- **External Client:** `AsyncOpenAI` instance configured with the Gemini endpoint.
- **Model Wrapper:** `OpenAIChatCompletionsModel` wraps the external client.
- **Agent Integration:** Pass the wrapper to the `Agent(model=llm_model)` constructor.

## Tool Definitions
- Use `@function_tool` decorator.
- Tools must have type hints and docstrings (critical for Gemini to understand them).
- Tools are synchronous functions (in this example) but the Agent runner handles them.

## Running the Agent
- Use `Runner.run_sync(agent, input)` for synchronous execution (simplest for CLI/Scripts).
- Use `Runner.run(agent, input)` for async contexts.

## Important Constraints
- **Tracing:** `OPENAI_API_KEY` may be needed for internal SDK tracing even if using Gemini for inference. Set it to a dummy value if strict tracing isn't required but SDK demands it.
- **Tool Use Behavior:** Gemini 2.x supports tool calling, but precise control (`tool_choice`) might behave differently than GPT-4. We use `tool_use_behavior` to control execution flow.
