# ADK Issue Formatting Agent

A Weilliptic-secured agent that keeps GitHub issues consistent. For an issue in the configured repository (`OWNER`/`REPO`) it decides whether the issue is a bug report or a feature request, compares the body against the matching issue template, and, when required sections are missing or empty, posts a single polite comment asking the author to fill them in. It ignores questions, discussions and closed issues, and adds at most one comment per invocation.

With `INTERACTIVE=1` (the default) the agent asks for approval before it comments; set `INTERACTIVE=0` to let it act without confirmation. The GitHub calls are the agent's tools, and each is wrapped in `@weil_ai.secured_user(...)` so it only runs for a wallet that holds the right permission.

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

   Variables you must set: `WEIL_ADK_TEAM_AGENT_IDENTITY`, `OPENAI_API_KEY`, `GITHUB_TOKEN`. The other variables in the file have working defaults.

3. `WEIL_ADK_TEAM_AGENT_IDENTITY` must be a real Weilliptic identity; the placeholder `weil_xxxx` is rejected at startup. See [Generate an agent identity](../weilliptic-integration/README.md#generate-an-agent-identity). `WEIL_ADK_TEAM_SERVICE` (default `engg.acme`) and `WEIL_ADK_TEAM_MODEL` (default `openai/gpt-5.1`) can be overridden; they are read in `app/config.py`.

### Run locally

```bash
uv run adk web
```

Open <http://localhost:8000> and pick `app` from the agent list.

### Run with Docker

```bash
docker build -t weil-adk-issue-format .
docker run --rm --env-file .env -p 8080:8080 weil-adk-issue-format
```

The image serves the app on port 8080 (`/list-apps` lists it). Credentials are never copied into the image; they come from `--env-file` at run time.

See the [Weilliptic integration guide](../weilliptic-integration/README.md) for how the security hooks work.
