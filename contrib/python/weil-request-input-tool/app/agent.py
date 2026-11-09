# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import weil_ai
from google.adk import Agent
from google.adk.apps import App
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools import request_input
from google.genai import types
from pydantic import BaseModel, Field


class SupportTicket(BaseModel):
    """Details of the IT support ticket to be created."""

    title: str = Field(description="A brief summary of the issue.")
    description: str = Field(description="Detailed explanation of the problem.")
    priority: str = Field(
        default="MEDIUM",
        description="Ticket priority: LOW, MEDIUM, HIGH, or CRITICAL.",
    )
    category: str = Field(
        description=(
            "Issue category, e.g., billing, technical, account, or database."
        )
    )


@weil_ai.secured_user("engg.acme")
def create_support_ticket(ticket: SupportTicket) -> dict[str, str]:
    """Create a support ticket in the IT ticketing system."""
    return {
        "status": "success",
        "message": (
            f"Successfully created ticket '{ticket.title}'"
            f" [Category: {ticket.category}, Priority: {ticket.priority}]."
        ),
        "ticket_id": "INC-98471",
    }


@weil_ai.agent(identity="weil_xxxx", verify=False)
def create_root_agent() -> Agent:
    return Agent(
        name="support_assistant_agent",
        model=LiteLlm(model="openai/gpt-4o"),
        instruction="""
      You are a helpful IT support assistant responsible for creating support tickets.
      When the user requests to create or file a ticket:
      1. Identify which ticket details (title, description, priority, category) are already provided in the conversation.
      2. If any mandatory details are missing, call the `adk_request_input` tool.
      3. When calling `adk_request_input`, you must construct a dynamic JSON `response_schema` (type: "object") that ONLY requests the missing details, and specify a helpful message explaining what is needed.
      4. Once all details are gathered, call `create_support_ticket` with the complete SupportTicket details.
    """,
        tools=[create_support_ticket, request_input],
        generate_content_config=types.GenerateContentConfig(temperature=0.1),
    )


weil_root_agent = create_root_agent()
weil_root_agent.setup_secure_a2a()
root_agent = weil_root_agent.inner_agent
a2a_app = weil_root_agent.to_secure_a2a(host="127.0.0.1", port=8009)

app = App(root_agent=root_agent, name="app")
