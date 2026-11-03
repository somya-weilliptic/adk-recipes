# Config-based Agent Sample - Human-In-The-Loop

From contributing/samples/human_in_loop/

## Weilliptic setup and usage

This project uses the [`weil-ai`](https://pypi.org/project/weil-ai/) package. Run the commands below from the recipe root, `contrib/python/weilliptic-integration`, unless a block starts with `cd`.

### Setup

1. Install the dependencies (`weil-ai` and `weil-wallet` come from PyPI):

   ```bash
   pip install -r requirements.txt
   ```

2. Create this project's env file and fill in the values:

   ```bash
   cp hitl/tool_human_in_the_loop_config/.env.example hitl/tool_human_in_the_loop_config/.env
   ```

   Variables it needs: `OPENAI_API_KEY`.

3. Replace the placeholder `identity="weil_xxxx"` in `hitl/tool_human_in_the_loop_config/agent.py` with your own Weilliptic identity. It is hardcoded there, not read from the environment, and WeilChain rejects the placeholder at startup.

### Run locally

```bash
adk web hitl --port 8000
```

ADK loads this project's `.env` automatically. Open <http://localhost:8000> and pick `tool_human_in_the_loop_config` from the agent list.

### Run with Docker

From the recipe root:

```bash
docker build -f hitl/tool_human_in_the_loop_config/Dockerfile -t tool_human_in_the_loop_config .
docker run --rm --env-file hitl/tool_human_in_the_loop_config/.env -p 8000:8000 -p 8011:8011 tool_human_in_the_loop_config
```

Credentials are never copied into the image; they come from `--env-file` at run time.

### A2A server (port 8011)

The agent also exposes a Weil-secured A2A app, `a2a_app`. Inbound requests must carry Weil signature headers; unsigned requests are rejected.

```bash
docker run --rm --env-file hitl/tool_human_in_the_loop_config/.env -p 8011:8011 tool_human_in_the_loop_config \
  uvicorn tool_human_in_the_loop_config.agent:a2a_app --host 0.0.0.0 --port 8011
```

See the [recipe README](../../README.md) for how the Weilliptic integration works.
