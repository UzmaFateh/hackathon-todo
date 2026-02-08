from agents import Agent, Runner, AsyncOpenAI, ModelSettings, OpenAIChatCompletionsModel, function_tool
import os
from dotenv import load_dotenv, find_dotenv

# Load environment variables
load_dotenv(find_dotenv())

# --- Configuration (User Provided Logic) ---
# ONLY FOR TRACING (Dummy key if not used for real OpenAI)
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")

gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")

if not gemini_api_key:
    print("Warning: GEMINI_API_KEY not found in .env")

# 1. Which LLM Service? (Gemini via OpenAI-compatible API)
external_client: AsyncOpenAI = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# 2. Which LLM Model?
llm_model: OpenAIChatCompletionsModel = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=external_client
)

# --- Tool Definitions ---

@function_tool
def get_weather(city: str) -> str:
    """A simple function to get the weather for a user."""
    return f"Sunny in {city} (Mock Data)"

@function_tool
def get_travel_plan(city: str) -> str:
    """Plan Travel for your city"""
    return f"Travel Plan for {city}: Visit downtown, see the park. (Mock Data)"

# --- Agent Definitions ---

# 1. Check Agent: Forces a specific tool call via ModelSettings
check_agent: Agent = Agent(
    name="Weather Agent",
    tools=[get_travel_plan, get_weather],
    model=llm_model,
    model_settings=ModelSettings(tool_choice="auto") # Let Gemini decide, or enforce specific tool
)

# 2. Base Agent: General purpose
base_agent: Agent = Agent(
    name="TravelAssistant",
    instructions="You are a helpful travel assistant. Use tools to answer questions.",
    model=llm_model,
    tools=[get_weather, get_travel_plan],
)

# --- Execution ---

if __name__ == "__main__":
    print("--- Running Check Agent (Weather in Lahore) ---")
    res = Runner.run_sync(check_agent, "What is weather in Lahore")
    print(f"Final Output: {res.final_output}")

    print("\n--- Running Base Agent (Travel Plan for Tokyo) ---")
    res_base = Runner.run_sync(base_agent, "Give me a travel plan for Tokyo")
    print(f"Final Output: {res_base.final_output}")
