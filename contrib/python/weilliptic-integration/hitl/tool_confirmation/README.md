# Tool Confirmation Sample

## Overview

This sample demonstrates how to use the Tool Confirmation feature in ADK to implement Human-in-the-Loop (HITL) flows. It shows how a tool can dynamically request confirmation from the user before proceeding with a sensitive action (e.g., transferring funds).

## Sample Inputs

- `Transfer $50 to Alice`

- `Transfer $200 to Bob`

- `Close account ACC123`

- `Transfer $500 to Charlie and close account ACC123`

  *This will cause parallel tools being called in a single step*

## How To

### 1. Requesting Confirmation

In your tool function, you can access the `ToolContext` and check if `tool_confirmation` is present. If not, you can call `tool_context.request_confirmation()` to request approval from the user.

```python
def transfer_funds(amount: float, recipient: str, tool_context: ToolContext):
    # Only request confirmation for amounts >= 100
    if amount >= 100:
        if not tool_context.tool_confirmation:
            tool_context.request_confirmation(
                hint=f"Confirm transfer of ${amount} to {recipient}.",
            )
            return {"error": "This tool call requires confirmation, please approve or reject."}
```

### 2. Handling the Response

When the user responds to the confirmation request, the tool will be called again. This time, `tool_context.tool_confirmation` will be populated with the user's decision (`confirmed` boolean).

```python
        elif not tool_context.tool_confirmation.confirmed:
            return {"error": "Transfer rejected by user."}

    return {"result": f"Successfully transferred ${amount} to {recipient}."}
```

### 3. Using `FunctionTool` for Automatic Confirmation

Alternatively, you can specify that a tool always requires confirmation by wrapping it in a `FunctionTool` and setting `require_confirmation=True` when defining the agent's tools. In this case, the runner will automatically handle the confirmation request before calling your function.

```python
from google.adk.tools.function_tool import FunctionTool

def close_account(account_id: str, tool_context: ToolContext):
    # This code only runs if the user approves the confirmation
    return {"result": f"Account {account_id} closed."}

root_agent = Agent(
    ...
    tools=[
        FunctionTool(func=close_account, require_confirmation=True),
    ],
)
```

## Weilliptic setup and usage

This project uses the [`weil-ai`](https://pypi.org/project/weil-ai/) package. Run the commands below from the recipe root, `contrib/python/weilliptic-integration`, unless a block starts with `cd`.

### Setup

1. Install the dependencies (`weil-ai` and `weil-wallet` come from PyPI):

   ```bash
   pip install -r requirements.txt
   ```

2. Create this project's env file and fill in the values:

   ```bash
   cp hitl/tool_confirmation/.env.example hitl/tool_confirmation/.env
   ```

   Variables it needs: `OPENAI_API_KEY`.

3. Replace the placeholder `identity="weil_xxxx"` in `hitl/tool_confirmation/agent.py` with your own Weilliptic identity. It is hardcoded there, not read from the environment, and WeilChain rejects the placeholder at startup.

### Run locally

```bash
adk web hitl --port 8000
```

ADK loads this project's `.env` automatically. Open <http://localhost:8000> and pick `tool_confirmation` from the agent list.

### Run with Docker

From the recipe root:

```bash
docker build -f hitl/tool_confirmation/Dockerfile -t tool_confirmation .
docker run --rm --env-file hitl/tool_confirmation/.env -p 8000:8000 -p 8010:8010 tool_confirmation
```

Credentials are never copied into the image; they come from `--env-file` at run time.

### A2A server (port 8010)

The agent also exposes a Weil-secured A2A app, `a2a_app`. Inbound requests must carry Weil signature headers; unsigned requests are rejected.

```bash
docker run --rm --env-file hitl/tool_confirmation/.env -p 8010:8010 tool_confirmation \
  uvicorn tool_confirmation.agent:a2a_app --host 0.0.0.0 --port 8010
```

See the [recipe README](../../README.md) for how the Weilliptic integration works.
