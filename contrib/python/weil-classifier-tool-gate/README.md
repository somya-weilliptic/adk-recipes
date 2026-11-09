# Classifier Tool Gate Sample

## Overview

This sample demonstrates how to gate tool calls with a classifier from `google.adk.labs.classifiers`.

The agent manages a small customer database through two tools: `run_sql` and `send_email`. Before each tool call, a `before_tool_callback` asks a classifier a `Binary` question about the call: "Would this tool call delete or change data, or contact a customer?" Calls the classifier rates below the threshold run right away. The rest pause until the user approves them through ADK's tool confirmation flow.

`FunctionTool(require_confirmation=...)` decides per tool, or with code you write for each tool. A classifier decides from the arguments, so one question covers every tool: a `SELECT` through `run_sql` runs, and a `DELETE` through the same tool asks first.

This sample uses `LlmClassifier`, which answers with any `BaseLlm`. A dedicated decision model answers faster, which matters for a check that runs before every tool call, and can be swapped in without other changes.

## Sample Inputs

- `Which customers are on the pro plan?`

- `Move Alan Turing to the pro plan.`

  *The gate asks for confirmation before the `UPDATE` runs.*

- `Delete every customer on the free plan.`

- `Email Grace Hopper to thank her for renewing.`

## How To

1. Create the callback with `create_tool_gate_callback` from [`tool_gate.py`](tool_gate.py) and pass it as the agent's `before_tool_callback`:

   ```python
   tool_gate = create_tool_gate_callback(
       classifier=LlmClassifier(model="gemini-3.5-flash"),
       instructions="Would this tool call delete or change data, or contact a customer?",
       on_threshold_exceeded="confirm",
   )

   root_agent = Agent(..., before_tool_callback=tool_gate)
   ```

1. Choose what happens when a call's probability is at or above `threshold` (default `0.5`):

   - `on_threshold_exceeded="block"` (default) skips the call and returns an error to the model.
   - `on_threshold_exceeded="confirm"` asks the user with `tool_context.request_confirmation()` and runs the call only if they approve. When the user answers, the call comes back through the callback with `tool_context.tool_confirmation` set, and the callback runs or rejects it without asking the classifier again.

1. By default the classifier sees the tool's name, description and arguments. To classify something else, such as recent conversation or session state, pass a `state_extractor(tool, args, tool_context)` that returns the classifier input.

If the classifier raises, the gate treats the call as risky and blocks it or asks the user, so an outage can't let a risky call through.

`LlmClassifier` probabilities are the model's stated values, not measured frequencies, and the right threshold differs between classifiers. Pick `threshold` from an evaluation set of calls you expect to pass and to stop.

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

   Variables you must set: `WEIL_AGENT_IDENTITY`, `OPENAI_API_KEY`, `GOOGLE_API_KEY`. The other variables in the file have working defaults.

3. Put your values in `.env`. Only these need to change; leave the rest as they are:

   ```dotenv
   WEIL_AGENT_IDENTITY=weil_<your-identity>
   OPENAI_API_KEY=<your-openai-api-key>
   GOOGLE_API_KEY=<your-google-api-key>
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
| `GOOGLE_API_KEY` | Gemini API key, used by the classifier model (`MODEL_NAME`). |

### Run locally

```bash
uv run adk web
```

Open <http://localhost:8000> and pick `app` from the agent list.

### Run with Docker

```bash
docker build -t weil-classifier-tool-gate .
grep -vE '^\s*(#|$)|<TODO' .env | sed -E 's/[[:space:]]+#.*$//' > .env.docker
docker run --rm --env-file .env.docker -p 8080:8080 weil-classifier-tool-gate
```

Open <http://localhost:8080/dev-ui/> and pick `app`. `.env.docker` is `.env` without comments (Docker's `--env-file` does not strip them) and is git-ignored. Credentials are never copied into the image; they come from `--env-file` at run time.

### A2A server

The agent also builds a Weil-secured A2A app, `a2a_app`, which rejects requests that do not carry valid Weil signature headers. It advertises port 8006:

```bash
docker run --rm --env-file .env.docker -p 8006:8006 weil-classifier-tool-gate \
  uv run uvicorn app.agent:a2a_app --host 0.0.0.0 --port 8006
```
