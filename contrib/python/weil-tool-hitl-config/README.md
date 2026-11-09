# Config-based Agent Sample - Human-In-The-Loop

From contributing/samples/human_in_loop/

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
docker build -t weil-tool-hitl-config .
docker run --rm --env-file .env -p 8080:8080 weil-tool-hitl-config
```

The image serves the app on port 8080 (`/list-apps` lists it). Credentials are never copied into the image; they come from `--env-file` at run time.

### A2A server

The agent also builds a Weil-secured A2A app, `a2a_app`, which rejects requests that do not carry valid Weil signature headers. It advertises port 8011:

```bash
docker run --rm --env-file .env -p 8011:8011 weil-tool-hitl-config \
  uv run uvicorn app.agent:a2a_app --host 0.0.0.0 --port 8011
```

See the [Weilliptic integration guide](../weilliptic-integration/README.md) for how the security hooks work.
