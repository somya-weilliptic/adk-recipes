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

3. Put your values in `.env`. Only these need to change; leave the rest as they are:

   ```dotenv
   WEIL_ADK_TEAM_AGENT_IDENTITY=weil_<your-identity>
   OPENAI_API_KEY=<your-openai-api-key>
   GITHUB_TOKEN=<your-github-token>
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
| `GITHUB_TOKEN` | GitHub personal access token used for the GitHub API calls. |

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
grep -vE '^\s*(#|$)|<TODO' .env | sed -E 's/[[:space:]]+#.*$//' > .env.docker
docker run --rm --env-file .env.docker -p 8080:8080 weil-adk-documentation
```

Open <http://localhost:8080/dev-ui/> and pick `app`. `.env.docker` is `.env` without comments (Docker's `--env-file` does not strip them) and is git-ignored. Credentials are never copied into the image; they come from `--env-file` at run time.

One-off jobs use the same image with a different command:

```bash
docker run --rm --env-file .env.docker weil-adk-documentation uv run python -m app.adk_docs_updater.main --issue_number 123
docker run --rm --env-file .env.docker weil-adk-documentation uv run python -m app.adk_release_analyzer.main --start-tag v1.26.0 --end-tag v1.27.0
```
