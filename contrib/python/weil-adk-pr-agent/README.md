# ADK Pull Request Description Agent

A Weilliptic-secured agent that writes pull request descriptions. Given a pull request number, its tool fetches the pull request details and commit list from the GitHub API for the configured repository (`OWNER`/`REPO`), and the agent turns them into a description with a summary, the motivation and the notable changes.

The GitHub call is the agent's only tool and is wrapped in `@weil_ai.secured_user(...)`, so it only runs for a wallet that holds the right permission. A small `main.py` runs the agent once from the command line.

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

To run it as a one-off job instead of in the web UI:

```bash
uv run python -m app.main
```

### Run with Docker

```bash
docker build -t weil-adk-pr-agent .
docker run --rm --env-file .env -p 8080:8080 weil-adk-pr-agent
```

The image serves the app on port 8080 (`/list-apps` lists it). Credentials are never copied into the image; they come from `--env-file` at run time.

One-off jobs use the same image with a different command:

```bash
docker run --rm --env-file .env weil-adk-pr-agent uv run python -m app.main
```

See the [Weilliptic integration guide](../weilliptic-integration/README.md) for how the security hooks work.
