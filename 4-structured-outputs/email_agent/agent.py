from google.adk.agents import Agent
from pydantic import BaseModel, Field


class StructuredEmailSchema(BaseModel):
    subject: str = Field(
        description="The subject line of the email. Should be concise and descriptive"
    )
    body: str = Field(
        description="The mail content of the email, Should be well-formatted with proper greeting, paragraphs"
    )


root_agent = Agent(
    model="gemini-2.0-flash",
    name="email_agent",
    description="Generates a professional emails with structued subject and body",
    instruction="""
    You are an AI assistant designed to write professional and clear emails. Your task is to generate a *new* email (not a reply or forward) based on the user's request.

    Output the email in JSON format with two keys: `subject` and `body`.

    **Input:** The user will provide instructions for the email content, purpose, and any key details.

    **Output Format:**
    ```json
    {
    "subject": "Subject of the email lives here",
    "body": "Body of the email with proper paragraphs and formatting"
    }
    """,
    output_schema=StructuredEmailSchema,
    output_key="email",
)
