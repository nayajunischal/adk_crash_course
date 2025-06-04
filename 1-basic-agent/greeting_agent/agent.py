from google.adk.agents import Agent

root_agent = Agent(
    model="gemini-2.0-flash",
    name="greeting_agent",
    description="A helpful assistant for greeting user",
    instruction="""
    You are a helpful assistant that greets the user.
    Ask for the user's name and greet them by name.    
    """,
)
