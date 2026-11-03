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

This project uses the [`weil-ai`](https://pypi.org/project/weil-ai/) package. Run the commands below from the recipe root, `contrib/python/weilliptic-integration`, unless a block starts with `cd`.

### Setup

1. Install the dependencies (`weil-ai` and `weil-wallet` come from PyPI):

   ```bash
   pip install -r requirements.txt
   ```

2. Create this project's env file and fill in the values:

   ```bash
   cp adk_team/adk_knowledge_agent/.env.example adk_team/adk_knowledge_agent/.env
   ```

   Variables it needs: `WEIL_ADK_TEAM_AGENT_IDENTITY`, `OPENAI_API_KEY`, `VERTEXAI_DATASTORE_ID`.

3. `WEIL_ADK_TEAM_AGENT_IDENTITY` must be a real identity registered on WeilChain. The placeholder `weil_xxxx` is rejected at startup. `WEIL_ADK_TEAM_MODEL` (default `openai/gpt-5.1`) can be overridden; it is defined in `adk_team/config.py`.

### Run locally

```bash
adk web adk_team --port 8000
```

ADK loads this project's `.env` automatically. Open <http://localhost:8000> and pick `adk_knowledge_agent` from the agent list.

### Run with Docker

From the recipe root:

```bash
docker build -f adk_team/adk_knowledge_agent/Dockerfile -t adk_knowledge_agent .
docker run --rm --env-file adk_team/adk_knowledge_agent/.env -p 8000:8000 adk_knowledge_agent
```

Credentials are never copied into the image; they come from `--env-file` at run time.

See the [recipe README](../../README.md) for how the Weilliptic integration works.
