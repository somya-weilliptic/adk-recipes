from __future__ import annotations

import weil_ai
from google.adk.agents import Agent
from google.adk.apps import App
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.function_tool import FunctionTool

from app.config import AGENT_MODEL, WEIL_AGENT_IDENTITY, WEIL_SERVICE


@weil_ai.secured_user(WEIL_SERVICE)
def get_account_status(account_id: str) -> str:
    """Gets the status of a bank account.

    Args:
        account_id: The account ID to check.

    Returns:
        The status of the account.
    """
    return f"Account {account_id} is active."


@weil_ai.secured_user(WEIL_SERVICE)
def close_account(account_id: str) -> str:
    """Closes a bank account. This action requires user confirmation.

    Args:
        account_id: The account ID to close.

    Returns:
        A confirmation message.
    """
    return f"Account {account_id} has been closed."


info_agent = Agent(
    name="info_agent",
    model=LiteLlm(model=AGENT_MODEL),
    description="An agent that can check account status.",
    tools=[get_account_status],
)

close_agent = Agent(
    name="close_agent",
    model=LiteLlm(model=AGENT_MODEL),
    description="An agent that can close accounts.",
    tools=[FunctionTool(func=close_account, require_confirmation=True)],
)


@weil_ai.agent(identity=WEIL_AGENT_IDENTITY, verify=False)
def create_root_agent() -> Agent:
    return Agent(
        name="sub_agents",
        model=LiteLlm(model=AGENT_MODEL),
        description=(
            "A root agent that can check accounts and close them by delegating to"
            " sub-agents."
        ),
        sub_agents=[info_agent, close_agent],
    )


weil_root_agent = create_root_agent()
weil_root_agent.setup_secure_a2a()
root_agent = weil_root_agent.inner_agent
a2a_app = weil_root_agent.to_secure_a2a(host="127.0.0.1", port=8002)

app = App(root_agent=root_agent, name="app")
