# ADK Answering Agent

The ADK Answering Agent is a Python-based agent designed to help answer questions in GitHub discussions for the `google/adk-python` repository. It uses a large language model to analyze open discussions, retrieve information from document store, generate response, and post a comment in the github discussion.

This agent can be operated in three distinct modes:

- An interactive mode for local use.
- A batch script mode for oncall use.
- A fully automated GitHub Actions workflow.

______________________________________________________________________

## Interactive Mode

This mode allows you to run the agent locally to review its recommendations in real-time before any changes are made to your repository's discussions.

### Features

- **Web Interface**: The agent's interactive mode can be rendered in a web browser using the ADK's `adk web` command.
- **User Approval**: In interactive mode, the agent is instructed to ask for your confirmation before posting a comment to a GitHub discussion.
- **Question & Answer**: You can ask ADK related questions, and the agent will provide answers based on its knowledge on ADK.

### Running in Interactive Mode

To run the agent in interactive mode, first set the required environment variables. Then, execute the following command in your terminal:

```bash
adk web
```

This will start a local server and provide a URL to access the agent's web interface in your browser.

______________________________________________________________________

## Batch Script Mode

The `main.py` script supports batch processing for ADK oncall team to process discussions.

### Features

- **Single Discussion**: Process a specific discussion by providing its number.
- **Batch Process**: Process the N most recently updated discussions.
- **Direct Discussion Data**: Process a discussion using JSON data directly (optimized for GitHub Actions).

### Running in Batch Script Mode

To run the agent in batch script mode, first set the required environment variables. Then, execute one of the following commands:

```bash
export PYTHONPATH=contributing/samples/adk_team

# Answer a specific discussion
python -m adk_answering_agent.main --discussion_number 27

# Answer the 10 most recent updated discussions
python -m adk_answering_agent.main --recent 10

# Answer a discussion using direct JSON data (saves API calls)
python -m adk_answering_agent.main --discussion '{"number": 27, "title": "How to...", "body": "I need help with...", "author": {"login": "username"}}'

# Answer a discussion using JSON data read from a file
python -m adk_answering_agent.main --discussion-file discussion.json
```

______________________________________________________________________

## GitHub Workflow Mode

The `main.py` script is automatically triggered by GitHub Actions when new discussions are created in the Q&A category. The workflow is configured in `.github/workflows/discussion_answering.yml` and automatically processes discussions using the `--discussion` flag with JSON data from the GitHub event payload.

### Optimization

The GitHub Actions workflow passes discussion data directly from `github.event.discussion` using `toJson()`, eliminating the need for additional API calls to fetch discussion information that's already available in the event payload. This makes the workflow faster and more reliable.

______________________________________________________________________

## Update the Knowledge Base

The `upload_docs_to_vertex_ai_search.py` is a script to upload ADK related docs to Vertex AI Search datastore to update the knowledge base. It can be executed with the following command in your terminal:

```bash
export PYTHONPATH=contributing/samples/adk_team # If not already exported
python -m adk_answering_agent.upload_docs_to_vertex_ai_search
```

## Setup and Configuration

Whether running in interactive or workflow mode, the agent requires the following setup.

### Dependencies

The agent requires the following Python libraries.

```bash
pip install --upgrade pip
pip install google-adk google-cloud-discoveryengine
```

The agent also requires gcloud login:

```bash
gcloud auth application-default login
```

The upload script requires the following additional Python libraries.

```bash
pip install google-cloud-storage markdown
```

### Environment Variables

The following environment variables are required for the agent to connect to the necessary services.

- `GITHUB_TOKEN=YOUR_GITHUB_TOKEN`: **(Required)** A GitHub Personal Access Token with read and write permissions for Discussions. Needed for both interactive and workflow modes.
- `GOOGLE_GENAI_USE_ENTERPRISE=TRUE`: **(Required)** Use Google Vertex AI for the authentication.
- `GOOGLE_CLOUD_PROJECT=YOUR_PROJECT_ID`: **(Required)** The Google Cloud project ID.
- `GOOGLE_CLOUD_LOCATION=LOCATION`: **(Required)** The Google Cloud region.
- `VERTEXAI_DATASTORE_ID=YOUR_DATASTORE_ID`: **(Required)** The full Vertex AI datastore ID for the document store (i.e. knowledge base), with the format of `projects/{project_number}/locations/{location}/collections/{collection}/dataStores/{datastore_id}`.
- `LLM_MODEL_NAME`: The Gemini model used by the answering agent. Defaults to `gemini-2.5-flash`.
- `OWNER`: The GitHub organization or username that owns the repository (e.g., `google`). Needed for both modes.
- `REPO`: The name of the GitHub repository (e.g., `adk-python`). Needed for both modes.
- `INTERACTIVE`: Controls the agent's interaction mode. For the automated workflow, this is set to `0`. For interactive mode, it should be set to `1` or left unset.

The following environment variables are required to upload the docs to update the knowledge base.

- `GCS_BUCKET_NAME=YOUR_GCS_BUCKET_NAME`: **(Required)** The name of the GCS bucket to store the documents.
- `ADK_DOCS_ROOT_PATH=YOUR_ADK_DOCS_ROOT_PATH`: **(Required)** Path to the root of the downloaded adk-docs repo.
- `ADK_PYTHON_ROOT_PATH=YOUR_ADK_PYTHON_ROOT_PATH`: **(Required)** Path to the root of the downloaded adk-python repo.

For local execution in interactive mode, you can place these variables in a
`.env` file in the project's root directory. For the GitHub workflow, required
credentials should be configured as repository secrets. The workflow also
supports the optional repository variables `ADK_ANSWERING_MODEL` and
`ADK_ANSWERING_LOCATION` to override the default model and location without
changing the workflow file.

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

   Variables you must set: `WEIL_ADK_TEAM_AGENT_IDENTITY`, `OPENAI_API_KEY`, `GITHUB_TOKEN`, `VERTEXAI_DATASTORE_ID`, `GEMINI_API_DATASTORE_ID`, `ADK_GCP_SA_KEY`. The other variables in the file have working defaults.

3. Put your values in `.env`. Only these need to change; leave the rest as they are:

   ```dotenv
   WEIL_ADK_TEAM_AGENT_IDENTITY=weil_<your-identity>
   OPENAI_API_KEY=<your-openai-api-key>
   GITHUB_TOKEN=<your-github-token>
   VERTEXAI_DATASTORE_ID=<your-value>
   GEMINI_API_DATASTORE_ID=<your-value>
   ADK_GCP_SA_KEY=<your-value>
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
| `GITHUB_TOKEN` | GitHub personal access token with read and write permissions for Discussions. |
| `VERTEXAI_DATASTORE_ID` | Full Vertex AI Search datastore ID of the knowledge base: `projects/{project_number}/locations/{location}/collections/{collection}/dataStores/{datastore_id}`. |
| `GEMINI_API_DATASTORE_ID` | Vertex AI Search datastore ID used to search the Gemini API docs. |
| `ADK_GCP_SA_KEY` | Google Cloud service account key (JSON) used to call Vertex AI Search for the Gemini API docs. |

### Run locally

```bash
uv run adk web
```

Open <http://localhost:8000> and pick `app` from the agent list.

To run it as a one-off job instead of in the web UI:

```bash
uv run python -m app.main --recent 10
```

### Run with Docker

```bash
docker build -t weil-adk-answering-agent .
grep -vE '^\s*(#|$)|<TODO' .env | sed -E 's/[[:space:]]+#.*$//' > .env.docker
docker run --rm --env-file .env.docker -p 8080:8080 weil-adk-answering-agent
```

Open <http://localhost:8080/dev-ui/> and pick `app`. `.env.docker` is `.env` without comments (Docker's `--env-file` does not strip them) and is git-ignored. Credentials are never copied into the image; they come from `--env-file` at run time.

One-off jobs use the same image with a different command:

```bash
docker run --rm --env-file .env.docker weil-adk-answering-agent uv run python -m app.main --recent 10
```
