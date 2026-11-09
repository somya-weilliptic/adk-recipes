# Agent Knowledge Agent

An intelligent assistant for performing Vertex AI Search to find ADK knowledge
and documentation.

## Deployment

This agent is deployed to Google Cloud Run as an A2A agent, which is used by
the parent ADK Agent Builder Assistant.

Here are the steps to deploy the agent:

1. Set environment variables

```bash
export GOOGLE_CLOUD_PROJECT=your-project-id
export GOOGLE_CLOUD_LOCATION=us-central1 # Or your preferred location
export GOOGLE_GENAI_USE_ENTERPRISE=True
export VERTEXAI_DATASTORE_ID=your-datastore-id
```

`VERTEXAI_DATASTORE_ID` is required, and is the full resource name of the
Vertex AI Search data store the agent queries, with the format
`projects/{project_number}/locations/{location}/collections/{collection}/dataStores/{datastore_id}`.
The agent refuses to start without it.

2. Run the deployment command

```bash
$ adk deploy cloud_run --project=your-project-id --region=us-central1 --service_name=adk-agent-builder-knowledge-service --with_ui --a2a ./adk_knowledge_agent
```

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

   Variables you must set: `WEIL_ADK_TEAM_AGENT_IDENTITY`, `OPENAI_API_KEY`, `VERTEXAI_DATASTORE_ID`. The other variables in the file have working defaults.

3. Put your values in `.env`. Only these need to change; leave the rest as they are:

   ```dotenv
   WEIL_ADK_TEAM_AGENT_IDENTITY=weil_<your-identity>
   OPENAI_API_KEY=<your-openai-api-key>
   VERTEXAI_DATASTORE_ID=<your-value>
   ```

   `WEIL_ADK_TEAM_AGENT_IDENTITY` must be a real Weilliptic identity; the placeholder `weil_xxxx` is rejected. `WEIL_ADK_TEAM_SERVICE` (default `engg.acme`) and `WEIL_ADK_TEAM_MODEL` (default `openai/gpt-5.1`) can be overridden; they are read in `app/config.py`.

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
| `WEIL_ADK_TEAM_AGENT_IDENTITY` | Weilliptic identity of the agent (`weil_<token>`). |
| `OPENAI_API_KEY` | OpenAI API key, read by LiteLLM for `openai/...` models. |
| `VERTEXAI_DATASTORE_ID` | Full Vertex AI Search datastore ID of the knowledge base: `projects/{project_number}/locations/{location}/collections/{collection}/dataStores/{datastore_id}`. |

### Run locally

```bash
uv run adk web
```

Open <http://localhost:8000> and pick `app` from the agent list.

### Run with Docker

```bash
docker build -t weil-adk-knowledge-agent .
grep -vE '^\s*(#|$)|<TODO' .env | sed -E 's/[[:space:]]+#.*$//' > .env.docker
docker run --rm --env-file .env.docker -p 8080:8080 weil-adk-knowledge-agent
```

Open <http://localhost:8080/dev-ui/> and pick `app`. `.env.docker` is `.env` without comments (Docker's `--env-file` does not strip them) and is git-ignored. Credentials are never copied into the image; they come from `--env-file` at run time.
