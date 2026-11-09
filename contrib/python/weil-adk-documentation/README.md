# ADK Documentation Agents

This recipe holds two Weilliptic-secured agents that keep the ADK documentation in step with the code:

- **Docs updater** (`app/adk_docs_updater`) reads a GitHub issue in the docs repository, works through its numbered suggestions against a local clone of the code repository, and opens a pull request with the documentation changes. It is the recipe's `root_agent`.
- **Release analyzer** (`app/adk_release_analyzer`) compares two release tags of the code repository, analyzes the changed files in groups, and files a GitHub issue listing the documentation updates the release needs.

Both agents clone and pull repositories with `git`, and both read the target repositories from `DOC_OWNER`, `DOC_REPO`, `CODE_OWNER` and `CODE_REPO` (defaults: `google/adk-docs` and `google/adk-python`). The release analyzer keeps its session state in a local SQLite database so a run can be resumed with `--resume`. The longer release analyzer description lives in [`app/adk_release_analyzer/README.md`](app/adk_release_analyzer/README.md).

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
uv run python -m app.adk_docs_updater.main --issue_number 123
uv run python -m app.adk_release_analyzer.main --start-tag v1.26.0 --end-tag v1.27.0
```

### Run with Docker

```bash
docker build -t weil-adk-documentation .
docker run --rm --env-file .env -p 8080:8080 weil-adk-documentation
```

The image serves the app on port 8080 (`/list-apps` lists it). Credentials are never copied into the image; they come from `--env-file` at run time.

One-off jobs use the same image with a different command:

```bash
docker run --rm --env-file .env weil-adk-documentation uv run python -m app.adk_docs_updater.main --issue_number 123
docker run --rm --env-file .env weil-adk-documentation uv run python -m app.adk_release_analyzer.main --start-tag v1.26.0 --end-tag v1.27.0
```

See the [Weilliptic integration guide](../weilliptic-integration/README.md) for how the security hooks work.
