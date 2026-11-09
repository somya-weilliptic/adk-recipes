# Human Tool Confirmation

A Weilliptic-secured agent that asks a human before it does something consequential. It handles reimbursements and time-off requests for employees and shows two ways to ask for confirmation:

- `reimburse` is wrapped in `FunctionTool(require_confirmation=...)` with a threshold function, so ADK asks for confirmation only when the amount is above 1000.
- `request_time_off` approves one or two days at once and, for longer requests, calls `request_confirmation()` with a payload so a manager can approve or narrow the number of days.

The agent is wrapped in a resumable `App`, so a conversation can pause for the answer and continue afterwards. Both tools are gated with `@weil_ai.secured_user(...)`.

## Weilliptic setup and usage

This recipe uses the [`weil-ai`](https://pypi.org/project/weil-ai/) package. Run the commands below from this folder.

### Setup

1. Install the dependencies:

   ```bash
   uv sync
   ```

2. Create the env file and fill in the values:

   ```bash
   cp .env.example .env
   ```

   Variables you must set: `OPENAI_API_KEY`. The other variables in the file have working defaults.

3. Replace the placeholder `identity="weil_xxxx"` in `app/agent.py` with your own Weilliptic identity. It is hardcoded there, and WeilChain rejects the placeholder at startup. See [Generate an agent identity](../weilliptic-integration/README.md#generate-an-agent-identity).

### Run locally

```bash
uv run adk web
```

Open <http://localhost:8000> and pick `app` from the agent list.

### Run with Docker

```bash
docker build -t weil-human-tool-confirmation .
docker run --rm --env-file .env -p 8080:8080 weil-human-tool-confirmation
```

The image serves the app on port 8080 (`/list-apps` lists it). Credentials are never copied into the image; they come from `--env-file` at run time.

### A2A server

The agent also builds a Weil-secured A2A app, `a2a_app`, which rejects requests that do not carry valid Weil signature headers. It advertises port 8008:

```bash
docker run --rm --env-file .env -p 8008:8008 weil-human-tool-confirmation \
  uv run uvicorn app.agent:a2a_app --host 0.0.0.0 --port 8008
```

See the [Weilliptic integration guide](../weilliptic-integration/README.md) for how the security hooks work.
