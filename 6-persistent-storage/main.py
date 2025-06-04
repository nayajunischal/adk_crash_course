import asyncio
from dotenv import load_dotenv

from pizza_order_agent.agent import pizza_order_agent
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from utils import (
    call_agent_async,
    format_order_state_for_display,
    get_order_status_message,
)
import warnings

# Ignore all warnings
warnings.filterwarnings("ignore")

load_dotenv()


# Create database session service
db_url = "sqlite:///./pizza_order_agent_data.db"
db_session_service = DatabaseSessionService(db_url=db_url)

# Default pizza order state structure
DEFAULT_ORDER_STATE = {
    "status": "START",
    "pizza_type": None,
    "size": None,
    "toppings": [],
    "quantity": 1,
    "address": None,
    "phone_number": None,
    "total_price": 0.0,
}


class CLIRunner:
    def __init__(self, app_name: str, user_id: str, session_service):
        self.app_name = app_name
        self.user_id = user_id
        self.session_service = session_service
        self.session_id = None
        self.runner = Runner(
            agent=pizza_order_agent,
            app_name=app_name,
            session_service=session_service,
        )

    async def start(self):
        # Check if there are any existing session available for the user
        session_state = await self.session_service.list_sessions(
            app_name=self.app_name,
            user_id=self.user_id,
        )
        # if there is an existing session use it else create a new one
        if session_state and len(session_state.sessions) > 0:
            self.session_id = session_state.sessions[0].id
            print(f"\n✅ Using existing session: {self.session_id}")

            # Get the current session data to show order status
            session = session_state.sessions[0]
            if session.state:
                print(format_order_state_for_display(session.state))
                print(get_order_status_message(session.state))
        else:
            session = await self.session_service.create_session(
                app_name=self.app_name,
                user_id=self.user_id,
                state=DEFAULT_ORDER_STATE,
            )
            self.session_id = session.id
            print(f"\n🆕 Created new session: {self.session_id}")
            print(get_order_status_message(DEFAULT_ORDER_STATE))

        print("\n🍕 Welcome to the Pizza Order Assistant!")
        print(
            "Type 'exit' to quit, 'menu' to see the menu, or 'order' to view your current order."
        )
        print("-" * 50)

        while True:
            user_input = input("\n🗣️  You: ").strip()
            if user_input.lower() == "exit":
                break

            if not user_input:
                print("Please enter a message or type 'exit' to quit.")
                continue

            try:
                # Call the agent and get response
                agent_response = await call_agent_async(
                    user_input=user_input,
                    runner=self.runner,
                    user_id=self.user_id,
                    session_id=self.session_id,
                )

                if agent_response:
                    print(f"\n🤖 Pizza Assistant: {agent_response}")
                else:
                    print(
                        "\n❌ Sorry, I didn't understand that. Could you please try again?"
                    )

            except Exception as e:
                print(f"\n❌ An error occurred while processing your request: {e}")
                print("Please try again or type 'exit' to quit.")


async def main():
    # Create database session service
    APP_NAME = "Pizza Agent"
    USER_ID = "Phineas"

    db_url = "sqlite:///./pizza_order_agent_data.db"
    db_session_service = DatabaseSessionService(db_url=db_url)

    cli_runner = CLIRunner(
        app_name=APP_NAME, user_id=USER_ID, session_service=db_session_service
    )

    await cli_runner.start()

    print(
        """
        🍕 Thank you for using Pizza Order Assistant!
        Your order has been saved and you can continue later.
        Have a great day! 🍕
        """
    )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Pizza Order Assistant closed. Goodbye!")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        print("Please check your configuration and try again.")
