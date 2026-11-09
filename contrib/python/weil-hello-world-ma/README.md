# Hello World Multi-Agent

A small Weilliptic-secured multi-agent recipe. The root agent greets the user and delegates to two sub-agents: `roll_agent`, which rolls dice of any size, and `prime_agent`, which checks whether numbers are prime. Each of the three agents has its own Weilliptic identity (`ROOT_AGENT_IDENTITY`, `ROLL_AGENT_IDENTITY` and `PRIME_AGENT_IDENTITY`), and each tool is gated with `@weil_ai.secured_user(...)` on a different service (`it.acme` for the dice, `hr.acme` for the prime check), so the same user can be allowed to use one sub-agent and not the other.

The recipe also shows how an agent-to-agent (A2A) app is built with `to_secure_a2a()`, which verifies signed requests on the way in.

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

   Variables you must set: `OPENAI_API_KEY`, `ROLL_AGENT_IDENTITY`, `PRIME_AGENT_IDENTITY`, `ROOT_AGENT_IDENTITY`. The other variables in the file have working defaults.

3. The three `*_AGENT_IDENTITY` values must be real Weilliptic identities; the placeholder `weil_xxxx` is rejected at startup. See [Generate an agent identity](../weilliptic-integration/README.md#generate-an-agent-identity).

### Run locally

```bash
uv run adk web
```

Open <http://localhost:8000> and pick `app` from the agent list.

### Run with Docker

```bash
docker build -t weil-hello-world-ma .
docker run --rm --env-file .env -p 8080:8080 weil-hello-world-ma
```

The image serves the app on port 8080 (`/list-apps` lists it). Credentials are never copied into the image; they come from `--env-file` at run time.

### A2A server

The agent also builds a Weil-secured A2A app, `a2a_app`, which rejects requests that do not carry valid Weil signature headers. It advertises port 8001:

```bash
docker run --rm --env-file .env -p 8001:8001 weil-hello-world-ma \
  uv run uvicorn app.agent:a2a_app --host 0.0.0.0 --port 8001
```

See the [Weilliptic integration guide](../weilliptic-integration/README.md) for how the security hooks work.
