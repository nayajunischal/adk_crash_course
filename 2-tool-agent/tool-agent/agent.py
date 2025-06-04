from datetime import datetime
from google.adk.agents import Agent
# from google.adk.tools import google_search


def get_current_time() -> dict:
    """
    Get the current time in the format YYYY-MM-DD HH:MM:SS
    """
    return {
        "current_time": datetime.now().strftime("%Y-%m-%df %H:%M:%S"),
    }


root_agent = Agent(
    model="gemini-2.0-flash",
    name="tool_agent",
    description="Tool agent",
    instruction="""
    You are a helpful assistant that can use the following tools:
    - get current time
    """,
    # tools=[google_search]
    tools=[get_current_time],
)
