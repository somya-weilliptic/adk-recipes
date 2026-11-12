# Agent with Long-Running Tools

This example demonstrates an agent using a long-running tool (`ask_for_approval`).

## Key Flow for Long-Running Tools

1. **Initial Call**: The agent calls the long-running tool (e.g., `ask_for_approval`).

1. **Initial Tool Response**: The tool immediately returns an initial response, typically indicating a "pending" status and a way to track the request (e.g., a `ticket-id`). This is sent back to the agent as a `types.FunctionResponse` (usually processed internally by the runner and then influencing the agent's next turn).

1. **Agent Acknowledges**: The agent processes this initial response and usually informs the user about the pending status.

1. **External Process/Update**: The long-running task progresses externally (e.g., a human approves the request).

1. **❗️Crucial Step: Provide Updated Tool Response❗️**:

   - Once the external process completes or updates, your application **must** construct a new `types.FunctionResponse`.
   - This response should use the **same `id` and `name`** as the original `FunctionCall` to the long-running tool.
   - The `response` field within this `types.FunctionResponse` should contain the *updated data* (e.g., `{'status': 'approved', ...}`).
   - Send this `types.FunctionResponse` back to the agent as a part within a new message using `role="user"`.

   ```python
   # Example: After external approval
   updated_tool_output_data = {
       "status": "approved",
       "ticketId": ticket_id,  # from original call
       # ... other relevant updated data
   }

   updated_function_response_part = types.Part(
       function_response=types.FunctionResponse(
           id=long_running_function_call.id,  # Original call ID
           name=long_running_function_call.name,  # Original call name
           response=updated_tool_output_data,
       )
   )

   # Send this back to the agent
   async for _ in runner.run_async(
       # ... session_id, user_id ...
       new_message=types.Content(
           parts=[updated_function_response_part], role="user"
       ),
   ):
       pass  # exhaust generator (or handle events)
   ```

1. **Agent Acts on Update**: The agent receives this message containing the `types.FunctionResponse` and, based on its instructions, proceeds with the next steps (e.g., calling another tool like `reimburse`).

**Why is this important?** The agent relies on receiving this subsequent `types.FunctionResponse` (provided in a message with `role="user"` containing the specific `Part`) to understand that the long-running task has concluded or its state has changed. Without it, the agent will remain unaware of the outcome of the pending task.

## Weilliptic setup and usage

This recipe uses the [`weil-ai`](https://pypi.org/project/weil-ai/) package. Run the commands below from this folder.

### Prerequisites

Before you run this recipe you need to set up your organization, create a subgroup and generate an agent identity. This is a one-time setup; follow the [Org onboarding guide](https://docs.weilliptic.ai/docs/org-onboarding/) and keep these steps in order:

1. **Set up your org and identity** ([guide](https://docs.weilliptic.ai/docs/org-onboarding/identity-setup)). Log in at console.weilliptic.ai with a connected wallet, open **Admin Panel** and the **Setup Identity** tab. Enter your org's TLD (the guide uses `acme`), keep the default **Key Management** and **Identity** applets, pick the pods (SENATE is always included) and click **Register Organization**, approving each wallet prompt. Then, in the WeilWallet extension, open **Account Details**, click **Link Organization**, select your org, and click **I've linked it — Continue** back in the console.
2. **Create a subgroup** ([guide](https://docs.weilliptic.ai/docs/org-onboarding/team-onboarding)). On the master pod's **Onboard Team** tab, click **Create Subgroup** and fill in the team name, team admin address, admin name and designation. You get a subgroup such as `engg.acme`.
3. **Add an agent** ([guide](https://docs.weilliptic.ai/docs/org-onboarding/add-agents)). With your org selected as the active organization in WeilWallet, click **Add Agent**, enter a name, a description and a purpose (the guide uses "Execution"), and pick the subgroup. When registration finishes, the agent's identity and wallet address are shown **once**; copy the identity.

Put the identity in `WEIL_AGENT_IDENTITY` (see [Setup](#setup)). `WEIL_SERVICE` defaults to `engg.acme`, the example subgroup in the guide; set it to your own subgroup if you named it differently.

The identity is a live credential: anyone who has it can sign as the agent. Keep it in `.env` and never commit it.

### Setup

1. Install the dependencies:

   ```bash
   uv sync
   ```

2. Create the env file and fill in the values:

   ```bash
   cp .env.example .env
   ```

   Variables you must set: `WEIL_AGENT_IDENTITY`, `OPENAI_API_KEY`. The other variables in the file have working defaults.

3. Put your values in `.env`. Only these need to change; leave the rest as they are:

   ```dotenv
   WEIL_AGENT_IDENTITY=weil_<your-identity>
   OPENAI_API_KEY=<your-openai-api-key>
   ```

   `WEIL_AGENT_IDENTITY` must be a real Weilliptic identity; the placeholder `weil_xxxx` is rejected. `WEIL_SERVICE` (default `engg.acme`) and `AGENT_MODEL` (default `openai/gpt-4o`) can be overridden in `.env`; they are read in `app/config.py`.

4. If your Sentinel node is not at the default address, also add its URL to `.env`:

   ```dotenv
   SENTINEL_HOST=<your-sentinel-url>
   ```

5. Enable the agent import. In `app/__init__.py`, uncomment `from . import agent` and add a noqa for E402:

   ```python
   load_dotenv()
   from . import agent  # noqa: E402 -- must come after load_dotenv()
   ```

### Environment variables

Set these in `.env`; everything else has a working default.

| Variable | Description |
| :-- | :-- |
| `WEIL_AGENT_IDENTITY` | Weilliptic identity of the agent (`weil_<token>`). |
| `OPENAI_API_KEY` | OpenAI API key, read by LiteLLM for `openai/...` models. |

### Run locally

```bash
uv run adk web
```

Open <http://localhost:8000> and pick `app` from the agent list.

### Run with Docker

```bash
docker build -t weil-human-in-loop .
grep -vE '^\s*(#|$)|<TODO' .env | sed -E 's/[[:space:]]+#.*$//' > .env.docker
docker run --rm --env-file .env.docker -p 8080:8080 weil-human-in-loop
```

Open <http://localhost:8080/dev-ui/> and pick `app`. `.env.docker` is `.env` without comments (Docker's `--env-file` does not strip them) and is git-ignored. Credentials are never copied into the image; they come from `--env-file` at run time.

### A2A server

The agent also builds a Weil-secured A2A app, `a2a_app`, which rejects requests that do not carry valid Weil signature headers. It advertises port 8007:

```bash
docker run --rm --env-file .env.docker -p 8007:8007 weil-human-in-loop \
  uv run uvicorn app.agent:a2a_app --host 0.0.0.0 --port 8007
```
