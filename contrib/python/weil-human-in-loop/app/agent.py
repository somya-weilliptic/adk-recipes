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

from typing import Any

import weil_ai
from google.adk import Agent
from google.adk.apps import App
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.long_running_tool import LongRunningFunctionTool
from google.adk.tools.tool_context import ToolContext
from google.genai import types

from app.config import AGENT_MODEL, WEIL_AGENT_IDENTITY, WEIL_SERVICE


@weil_ai.secured_user(WEIL_SERVICE)
def reimburse(purpose: str, amount: float) -> dict[str, str]:
    """Reimburse the amount of money to the employee."""
    return {
        "status": "ok",
    }


@weil_ai.secured_user(WEIL_SERVICE)
def ask_for_approval(
    purpose: str, amount: float, tool_context: ToolContext
) -> dict[str, Any]:
    """Ask for approval for the reimbursement."""
    return {
        "status": "pending",
        "amount": amount,
        "ticketId": "reimbursement-ticket-001",
    }


@weil_ai.agent(identity=WEIL_AGENT_IDENTITY, verify=False)
def create_root_agent() -> Agent:
    return Agent(
        name="reimbursement_agent",
        model=LiteLlm(model=AGENT_MODEL),
        instruction="""
      You are an agent whose job is to handle the reimbursement process for
      the employees. If the amount is less than $100, you will automatically
      approve the reimbursement.

      If the amount is greater than $100, you will
      ask for approval from the manager. If the manager approves, you will
      call reimburse() to reimburse the amount to the employee. If the manager
      rejects, you will inform the employee of the rejection.
""",
        tools=[reimburse, LongRunningFunctionTool(func=ask_for_approval)],
        generate_content_config=types.GenerateContentConfig(temperature=0.1),
    )


weil_root_agent = create_root_agent()
weil_root_agent.setup_secure_a2a()
root_agent = weil_root_agent.inner_agent
a2a_app = weil_root_agent.to_secure_a2a(host="127.0.0.1", port=8007)

app = App(root_agent=root_agent, name="app")
