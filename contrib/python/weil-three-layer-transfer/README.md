# Three Layer Transfer Sample

## Overview

This sample demonstrates a three-layer multi-agent system built with the ADK Python toolkit, showcasing structured double-round-trip hierarchical transfers.

## Sample Inputs

- `Hello, who are you?`
- `Can you write a short story about a lost kitten?`
- `Please translate it into Spanish.`
- `Looks great! Let's return to the project coordinator.`

## Graph

```mermaid
graph TD
    root_agent[root_agent] --> writer_agent[writer_agent]
    writer_agent --> translator_agent[translator_agent]
```

## How To

This sample demonstrates:

1. Root delegating to middle-child node `writer_agent`.
1. `writer_agent` delegating to leaf-grandchild node `translator_agent`.
1. Grandchild returning back to the parent `writer_agent`.
1. Parent returning back to the root coordinator `root_agent`.

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

   `WEIL_AGENT_IDENTITY` must be a real Weilliptic identity; the placeholder `weil_xxxx` is rejected. `AGENT_MODEL` (default `openai/gpt-4o`) can be overridden in `.env`; they are read in `app/config.py`.

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
docker build -t weil-three-layer-transfer .
grep -vE '^\s*(#|$)|<TODO' .env | sed -E 's/[[:space:]]+#.*$//' > .env.docker
docker run --rm --env-file .env.docker -p 8080:8080 weil-three-layer-transfer
```

Open <http://localhost:8080/dev-ui/> and pick `app`. `.env.docker` is `.env` without comments (Docker's `--env-file` does not strip them) and is git-ignored. Credentials are never copied into the image; they come from `--env-file` at run time.

### A2A server

The agent also builds a Weil-secured A2A app, `a2a_app`, which rejects requests that do not carry valid Weil signature headers. It advertises port 8005:

```bash
docker run --rm --env-file .env.docker -p 8005:8005 weil-three-layer-transfer \
  uv run uvicorn app.agent:a2a_app --host 0.0.0.0 --port 8005
```
