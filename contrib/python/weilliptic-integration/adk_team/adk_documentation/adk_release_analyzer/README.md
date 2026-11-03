# ADK Release Analyzer Agent

The ADK Release Analyzer Agent is a Python-based agent designed to help keep
documentation up-to-date with code changes. It analyzes the differences between
two releases of the `google/adk-python` repository, identifies required updates
in the `google/adk-docs` repository, and automatically generates a GitHub issue
with detailed instructions for documentation changes.

This agent can be operated in two distinct modes:

- an interactive mode for local use
- a fully automated mode for integration into workflows.

______________________________________________________________________

## Interactive Mode

This mode allows you to run the agent locally to review its recommendations in
real-time before any changes are made.

### Features

- **Web Interface**: The agent's interactive mode can be rendered in a web
  browser using the ADK's `adk web` command.
- **User Approval**: In interactive mode, the agent is instructed to ask for
  your confirmation before creating an issue on GitHub with the documentation
  update instructions.
- **Question & Answer**: You ask questions about the releases and code changes.
  The agent will provide answers based on related information.

### Running in Interactive Mode

To run the agent in interactive mode, first set the required environment
variables, ensuring `INTERACTIVE` is set to `1` or is unset. Then, execute the
following command in your terminal:

```bash
adk web contributing/samples/adk_team/adk_documentation
```

This will start a local server and provide a URL to access the agent's web
interface in your browser.

______________________________________________________________________

## Automated Mode

For automated, hands-off analysis, the agent can be run as a script (`main.py`),
for example as part of a CI/CD pipeline. The workflow is configured in
`.github/workflows/analyze-releases-for-adk-docs-updates.yml` and automatically
checks the most recent two releases for docs updates.

### Workflow Triggers

The GitHub workflow is configured to run on specific triggers:

- **Release Events**: The workflow executes automatically whenever a new release
  is `published`.

- **Manual Dispatch**: The workflow also runs when manually triggered for
  testing and retrying.

### Automated Issue Creation

When running in automated mode, the agent operates non-interactively. It creates
a GitHub issue with the documentation update instructions directly without
requiring user approval. This behavior is configured by setting the
`INTERACTIVE` environment variable to `0`.

______________________________________________________________________

## Setup and Configuration

Whether running in interactive or automated mode, the agent requires the
following setup.

### Dependencies

The agent requires the following Python libraries.

```bash
pip install --upgrade pip
pip install google-adk[db]
```

### Environment Variables

The following environment variables are required for the agent to connect to
the necessary services.

- `GITHUB_TOKEN`: **(Required)** A GitHub Personal Access Token with issues:write permissions for the documentation repository.
- `GOOGLE_API_KEY`: **(Required)** Your API key for the Gemini API.
- `DOC_OWNER`: The GitHub organization or username that owns the documentation repository (defaults to `google`).
- `CODE_OWNER`: The GitHub organization or username that owns the code repository (defaults to `google`).
- `DOC_REPO`: The name of the documentation repository (defaults to `adk-docs`).
- `CODE_REPO`: The name of the code repository (defaults to `adk-python`).
- `LOCAL_REPOS_DIR_PATH`: The local directory to clone the repositories into (defaults to `/tmp`).
- `INTERACTIVE`: Controls the agent's interaction mode. Set to 1 for interactive mode (default), and 0 for automated mode.

For local execution, you can place these variables in a `.env` file in the
project's root directory. For automated workflows, they should be configured as
environment variables or secrets.

## Weilliptic setup and usage

This project uses the [`weil-ai`](https://pypi.org/project/weil-ai/) package. Run the commands below from the recipe root, `contrib/python/weilliptic-integration`, unless a block starts with `cd`.

### Setup

1. Install the dependencies (`weil-ai` and `weil-wallet` come from PyPI):

   ```bash
   pip install -r requirements.txt
   ```

2. Create this project's env file and fill in the values:

   ```bash
   cp adk_team/adk_documentation/.env.example adk_team/adk_documentation/.env
   ```

   Variables it needs: `WEIL_ADK_TEAM_AGENT_IDENTITY`, `OPENAI_API_KEY`, `GITHUB_TOKEN`.

3. `WEIL_ADK_TEAM_AGENT_IDENTITY` must be a real identity registered on WeilChain. The placeholder `weil_xxxx` is rejected at startup. `WEIL_ADK_TEAM_SERVICE` (default `engg.acme`) and `WEIL_ADK_TEAM_MODEL` (default `openai/gpt-5.1`) can be overridden; they are defined in `adk_team/config.py`.

### Run locally

```bash
adk web adk_team --port 8000
```

ADK loads this project's `.env` automatically. Open <http://localhost:8000> and pick `adk_documentation.adk_release_analyzer` or `adk_documentation.adk_docs_updater` from the agent list.

To run it as a one-off job instead of in the web UI:

```bash
cd adk_team
python -m adk_documentation.adk_release_analyzer.main --start-tag v1.26.0 --end-tag v1.27.0
python -m adk_documentation.adk_docs_updater.main --issue_number 123
```

### Run with Docker

From the recipe root:

```bash
docker build -f adk_team/adk_documentation/Dockerfile -t adk_documentation .
docker run --rm --env-file adk_team/adk_documentation/.env -p 8000:8000 adk_documentation
```

Credentials are never copied into the image; they come from `--env-file` at run time.

One-off jobs use the same image with a different command:

```bash
docker run --rm --env-file adk_team/adk_documentation/.env adk_documentation python -m adk_documentation.adk_release_analyzer.main --start-tag v1.26.0 --end-tag v1.27.0
docker run --rm --env-file adk_team/adk_documentation/.env adk_documentation python -m adk_documentation.adk_docs_updater.main --issue_number 123
```

See the [recipe README](../../../README.md) for how the Weilliptic integration works.
