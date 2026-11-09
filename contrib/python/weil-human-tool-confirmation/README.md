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
docker build -t weil-human-tool-confirmation .
grep -vE '^\s*(#|$)|<TODO' .env | sed -E 's/[[:space:]]+#.*$//' > .env.docker
docker run --rm --env-file .env.docker -p 8080:8080 weil-human-tool-confirmation
```

Open <http://localhost:8080/dev-ui/> and pick `app`. `.env.docker` is `.env` without comments (Docker's `--env-file` does not strip them) and is git-ignored. Credentials are never copied into the image; they come from `--env-file` at run time.

### A2A server

The agent also builds a Weil-secured A2A app, `a2a_app`, which rejects requests that do not carry valid Weil signature headers. It advertises port 8008:

```bash
docker run --rm --env-file .env.docker -p 8008:8008 weil-human-tool-confirmation \
  uv run uvicorn app.agent:a2a_app --host 0.0.0.0 --port 8008
```
