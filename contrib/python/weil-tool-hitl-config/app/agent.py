import weil_ai
from google.adk import Agent
from google.adk.apps import App
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.long_running_tool import LongRunningFunctionTool
from google.genai import types

from app.tools import ask_for_approval, reimburse


@weil_ai.agent(identity="weil_xxxx", verify=False)
def create_root_agent() -> Agent:
    return Agent(
        name="reimbursement_agent",
        model=LiteLlm(model="openai/gpt-4o"),
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
a2a_app = weil_root_agent.to_secure_a2a(host="127.0.0.1", port=8011)

app = App(root_agent=root_agent, name="app")
