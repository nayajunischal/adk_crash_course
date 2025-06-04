import uuid

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from question_answering_agent.agent import question_answering_agent
import asyncio

import warnings
import logging

# Ignore all warnings
warnings.filterwarnings("ignore")


logging.basicConfig(level=logging.ERROR)

load_dotenv()


async def run_conversation():
    # Create a new session service to store state
    session_service_stateful = InMemorySessionService()

    initial_state = {
        "user_name": "Phineas",
        "user_preferences": """
        I love inventing and building amazing things every day.
        My favorite activities involve grand projects with my stepbrother Ferb, like building a rollercoaster or traveling to the moon.
        My favorite food is whatever makes our adventures even better.
        My favorite TV show is anything that sparks imagination and fun.
    """,
    }

    # Create a NEW session
    APP_NAME = "Brandon Bot"
    USER_ID = "brandon_hancock"
    SESSION_ID = str(uuid.uuid4())

    session = await session_service_stateful.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
        state=initial_state,
    )
    print(
        f"Session created: App='{APP_NAME}', User='{USER_ID}', Session='{SESSION_ID}'"
    )
    runner = Runner(
        agent=question_answering_agent,
        app_name=APP_NAME,
        session_service=session_service_stateful,
    )
    print(f"Runner created for agent '{runner.agent.name}'.")
    await call_agent_async(
        "What does Phineas love to do?",
        runner=runner,
        user_id=USER_ID,
        session_id=session.id,
    )

    await call_agent_async(
        "What is Phineas favorite TV show?",
        runner=runner,
        user_id=USER_ID,
        session_id=SESSION_ID,
    )


async def call_agent_async(query: str, runner, user_id, session_id):
    print(f"\n >>> User query: {query}")

    content = types.Content(role="user", parts=[types.Part(text=query)])

    final_response_text = "Agent did not produce a final response."  # Default

    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=content,
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                # Assuming text response is the first part
                final_response_text = event.content.parts[0].text
            elif event.actions and event.actions.escalate:
                # Handle potential errors/escalations
                final_response_text = (
                    f"Agent escalated: {event.error_message or 'No specific message.'}"
                )
            # Add more checks here if needed (e.g., specific error codes)
            break  # Stop processing events once the final response is found

    print(f"<<< Agent Response: {final_response_text}")


if __name__ == "__main__":
    try:
        asyncio.run(run_conversation())
    except Exception as e:
        print(f" An error occured: {e}")
