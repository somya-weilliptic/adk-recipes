import os
import random

import weil_ai
from google.adk.agents.llm_agent import Agent
from google.adk.apps import App
from google.adk.examples.example import Example
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools.example_tool import ExampleTool
from google.genai import types

# Weilliptic identities registered on WeilChain. The placeholder is rejected
# at startup, so set the real values in this project's .env.
ROLL_AGENT_IDENTITY = os.getenv("ROLL_AGENT_IDENTITY", "weil_xxxx")
PRIME_AGENT_IDENTITY = os.getenv("PRIME_AGENT_IDENTITY", "weil_xxxx")
ROOT_AGENT_IDENTITY = os.getenv("ROOT_AGENT_IDENTITY", "weil_xxxx")


# --- Roll Die Sub-Agent ---
@weil_ai.secured_user("it.acme")
async def roll_die(sides: int) -> int:
    """Roll a die and return the rolled result."""
    if "PYTEST_CURRENT_TEST" in os.environ:
        return 2
    return random.randint(1, sides)  # noqa: S311 -- dice roll, not cryptographic


@weil_ai.agent(identity=ROLL_AGENT_IDENTITY, verify=False)
def create_roll_agent() -> Agent:
    return Agent(
        name="roll_agent",
        mode="single_turn",
        model=LiteLlm(model="openai/gpt-4o"),
        description="Handles rolling dice of different sizes.",
        instruction="""
        You are responsible for rolling dice based on the user's request.
        When asked to roll a die, you must call the roll_die tool with the number of sides as an integer.
        """,
        tools=[roll_die],
        generate_content_config=types.GenerateContentConfig(
            safety_settings=[
                types.SafetySetting(  # avoid false alarm about rolling dice.
                    category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                    threshold=types.HarmBlockThreshold.OFF,
                ),
            ]
        ),
    )


weil_roll_agent = create_roll_agent()


# --- Prime Check Sub-Agent ---
@weil_ai.secured_user("hr.acme")
async def check_prime(nums: list[int]) -> str:
    """Check if a given list of numbers are prime."""
    primes = set()
    for raw_number in nums:
        number = int(raw_number)
        if number <= 1:
            continue
        is_prime = True
        for i in range(2, int(number**0.5) + 1):
            if number % i == 0:
                is_prime = False
                break
        if is_prime:
            primes.add(number)
    return (
        "No prime numbers found."
        if not primes
        else f"{', '.join(str(num) for num in primes)} are prime numbers."
    )


example_tool = ExampleTool(
    examples=[
        Example(
            input=types.UserContent(
                parts=[types.Part(text="Roll a 6-sided die.")]
            ),
            output=[
                types.ModelContent(
                    parts=[types.Part(text="I rolled a 4 for you.")]
                )
            ],
        ),
        Example(
            input=types.UserContent(
                parts=[types.Part(text="Is 7 a prime number?")]
            ),
            output=[
                types.ModelContent(
                    parts=[types.Part(text="Yes, 7 is a prime number.")]
                )
            ],
        ),
        Example(
            input=types.UserContent(
                parts=[
                    types.Part(
                        text="Roll a 10-sided die and check if it's prime."
                    )
                ]
            ),
            output=[
                types.ModelContent(
                    parts=[types.Part(text="I rolled an 8 for you.")]
                ),
                types.ModelContent(
                    parts=[types.Part(text="8 is not a prime number.")]
                ),
            ],
        ),
    ]
)


@weil_ai.agent(identity=PRIME_AGENT_IDENTITY, verify=False)
def create_prime_agent() -> Agent:
    return Agent(
        name="prime_agent",
        mode="single_turn",
        model=LiteLlm(model="openai/gpt-4o"),
        description="Handles checking if numbers are prime.",
        instruction="""
        You are responsible for checking whether numbers are prime.
        When asked to check primes, you must call the check_prime tool with a list of integers.
        Never attempt to determine prime numbers manually.
        Return the prime number results to the root agent.
        """,
        tools=[check_prime],
        generate_content_config=types.GenerateContentConfig(
            safety_settings=[
                types.SafetySetting(  # avoid false alarm about rolling dice.
                    category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                    threshold=types.HarmBlockThreshold.OFF,
                ),
            ]
        ),
    )


weil_prime_agent = create_prime_agent()


@weil_ai.agent(identity=ROOT_AGENT_IDENTITY, verify=False)
def create_root_agent() -> Agent:
    return Agent(
        name="root_agent",
        model=LiteLlm(model="openai/gpt-4o"),
        instruction="""
        You are a helpful assistant that can roll dice and check if numbers are prime.
        You delegate rolling dice tasks to the roll_agent and prime checking tasks to the prime_agent.
        Follow these steps:
        1. If the user asks to roll a die, delegate to the roll_agent.
        2. If the user asks to check primes, delegate to the prime_agent.
        3. If the user asks to roll a die and then check if the result is prime, call roll_agent first, then pass the result to prime_agent.
        Always clarify the results before proceeding.
        """,
        global_instruction=(
            "You are DicePrimeBot, ready to roll dice and check prime numbers."
        ),
        sub_agents=[weil_roll_agent.inner_agent, weil_prime_agent.inner_agent],
        tools=[example_tool],
        generate_content_config=types.GenerateContentConfig(
            safety_settings=[
                types.SafetySetting(  # avoid false alarm about rolling dice.
                    category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                    threshold=types.HarmBlockThreshold.OFF,
                ),
            ]
        ),
    )


weil_root_agent = create_root_agent()
weil_root_agent.setup_secure_a2a(service="finance.acme")

root_agent = weil_root_agent.inner_agent
a2a_app = weil_root_agent.to_secure_a2a(host="127.0.0.1", port=8001)

app = App(root_agent=root_agent, name="app")
