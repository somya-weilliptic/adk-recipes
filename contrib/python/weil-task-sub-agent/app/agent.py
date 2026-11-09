from __future__ import annotations

import weil_ai
from google.adk import Agent
from google.adk.apps import App
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.function_tool import FunctionTool
from pydantic import BaseModel, Field

from app.config import AGENT_MODEL, WEIL_AGENT_IDENTITY, WEIL_SERVICE


class OrderItem(BaseModel):
    name: str = Field(description="Name of the food item ordered")
    quantity: int = Field(description="Quantity ordered")


class PaymentInfo(BaseModel):
    """Output schema for the payment collection task."""

    credit_card_number: str
    cvv: str


@weil_ai.secured_user(WEIL_SERVICE)
def place_order(orders: list[OrderItem], payment_info: PaymentInfo) -> str:
    """Mock an order placement operation."""
    total_items = sum(item.quantity for item in orders)
    return f"Successfully placed order for {total_items} items."


@weil_ai.secured_user(WEIL_SERVICE)
def confirmation() -> str:
    """Confirm proceeding with the order."""
    return "Proceeding with order."


order_collector = Agent(
    name="order_collector",
    model=LiteLlm(model=AGENT_MODEL),
    mode="task",
    output_schema=list[OrderItem],
    instruction=(
        """\
You are an order collection assistant for a food delivery service.
Our menu today has exactly 3 items: 1. Pizza, 2. Burger, 3. Salad.
Ask the user what they would like to order and collect their choice and quantity.
Do not offer anything else.
If the combined quantity of items exceeds 5, you MUST use the `confirmation` tool to get user's confirmation before proceeding.
Do not ask for confirmation in natural language, always use the confirmation tool.
Once you have their final order and confirmation if needed, finish your task.
    """
    ),
    description="Collects the food order from the user.",
    tools=[FunctionTool(confirmation, require_confirmation=True)],
)

payment_collector = Agent(
    name="payment_collector",
    model=LiteLlm(model=AGENT_MODEL),
    mode="task",
    output_schema=PaymentInfo,
    instruction=(
        """\
You are a payment collection assistant.
Ask the user for their credit card number and CVV.
Once you have both pieces of information, finish your task.
    """
    ),
    description="Collects credit card and CVV from the user.",
)


@weil_ai.agent(identity=WEIL_AGENT_IDENTITY, verify=False)
def create_root_agent() -> Agent:
    return Agent(
        name="coordinator",
        model=LiteLlm(model=AGENT_MODEL),
        sub_agents=[order_collector, payment_collector],
        tools=[place_order],
        instruction="""\
You are a helpful coordinator for a food delivery service.
You need both order and payment information to place an order.
    """,
    )


weil_root_agent = create_root_agent()
weil_root_agent.setup_secure_a2a()
root_agent = weil_root_agent.inner_agent
a2a_app = weil_root_agent.to_secure_a2a(host="127.0.0.1", port=8004)

app = App(root_agent=root_agent, name="app")
