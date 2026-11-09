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

3. `WEIL_ADK_TEAM_AGENT_IDENTITY` must be a real Weilliptic identity; the placeholder `weil_xxxx` is rejected at startup. See [Generate an agent identity](../weilliptic-integration/README.md#generate-an-agent-identity). `WEIL_ADK_TEAM_SERVICE` (default `engg.acme`) and `WEIL_ADK_TEAM_MODEL` (default `openai/gpt-5.1`) can be overridden; they are read in `app/config.py`.

### Run locally

```bash
uv run adk web
```

Open <http://localhost:8000> and pick `app` from the agent list.

### Run with Docker

```bash
docker build -t weil-adk-knowledge-agent .
docker run --rm --env-file .env -p 8080:8080 weil-adk-knowledge-agent
```

The image serves the app on port 8080 (`/list-apps` lists it). Credentials are never copied into the image; they come from `--env-file` at run time.

See the [Weilliptic integration guide](../weilliptic-integration/README.md) for how the security hooks work.
