import os
import random

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

model = LiteLlm(
    model="openrouter/openai/gpt-4o-mini", api_key=os.getenv("OPENROUTER_API_KEY")
)


def dad_joke_generator() -> list[dict]:
    """
    Generates a list of 5 dad jokes with randomly selected punchlines.

    Returns:
        list: A list of dictionaries, where each dictionary represents a joke
              with 'setup' and 'punchline' keys.
    """
    jokes_data = [
        {
            "setup": "Why don't scientists trust atoms?",
            "punchline_options": [
                "Because they make up everything!",
                "They're just too shifty.",
                "You can't see them anyway.",
            ],
        },
        {
            "setup": "I told my wife she was drawing her eyebrows too high.",
            "punchline_options": [
                "She looked surprised.",
                "She said she was aiming for the stars.",
                "I guess I'll have to deal with it.",
            ],
        },
        {
            "setup": "What do you call a fish with no eyes?",
            "punchline_options": [
                "Fsh!",
                "Blind fish, obviously.",
                "A very confused swimmer.",
            ],
        },
        {
            "setup": "How do you organize a space party?",
            "punchline_options": [
                "You planet!",
                "With a lot of enthusiasm.",
                "Very carefully, so nothing floats away.",
            ],
        },
        {
            "setup": "My dad always said, 'Before you criticize someone, walk a mile in their shoes.'",
            "punchline_options": [
                "That way, when you criticize them, you're a mile away and you have their shoes.",
                "It makes you appreciate their journey.",
                "And then you realize how uncomfortable their shoes are.",
            ],
        },
    ]

    generated_jokes = []
    for joke in jokes_data:
        setup = joke["setup"]
        punchline = random.choice(joke["punchline_options"])
        generated_jokes.append({"setup": setup, "punchline": punchline})

    return generated_jokes


root_agent = Agent(
    model=model,
    name="dad_joke_agent",
    description="Dad Joke Agent",
    instruction="""
    You are a helpful assistant that can tell dad jokes, only use the following tools to generate dad jokes
    - dad_joke_generator
    """,
    tools=[dad_joke_generator],
)
