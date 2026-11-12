# ADK Issue Monitoring Agent 🛡️

An intelligent, cost-optimized, automated moderation agent built with the **Google Agent Development Kit (ADK)**.

This agent automatically audits GitHub repository issues to detect SEO spam, unsolicited promotional links, and irrelevant third-party endorsements. If spam is detected, it automatically applies a `spam` label and alerts the repository maintainers.

## ✨ Key Features & Optimizations

- **Zero-Waste LLM Invocations:** Fetches issue comments via REST APIs and pre-filters them in Python. It automatically ignores comments from maintainers, `[bot]` accounts, and the official `adk-bot`. The Gemini LLM is never invoked for safe threads, saving 100% of the token cost.
- **Dual-Mode Scanning:** Can perform a **Deep Clean** (auditing the entire history of all open issues) or a **Daily Sweep** (only fetching issues updated within the last 24 hours).
- **Token Truncation:** Uses Regular Expressions to strip out Markdown code blocks (```` ``` ````) replacing them with `[CODE BLOCK REMOVED]`, and truncates unusually long text to 1,500 characters before sending it to the AI.
- **Idempotency (Anti-Double-Posting):** The bot reads the comment history for its own signature. If it has already flagged an issue, it instantly skips it, preventing infinite feedback loops.

______________________________________________________________________

## Configuration

The agent is configured via environment variables, typically set as secrets in GitHub Actions.

### Required Secrets

| Secret Name      | Description                                                                                          |
| :--------------- | :--------------------------------------------------------------------------------------------------- |
| `GITHUB_TOKEN`   | A GitHub Personal Access Token (PAT) or Service Account Token with `repo` and `issues: write` scope. |
| `GOOGLE_API_KEY` | An API key for the Google AI (Gemini) model used for reasoning.                                      |

### Optional Configuration

These variables control the scanning behavior, thresholds, and model selection.

| Variable Name          | Description                                                                                                        | Default                 |
| :--------------------- | :----------------------------------------------------------------------------------------------------------------- | :---------------------- |
| `INITIAL_FULL_SCAN`    | If `true`, audits every open issue in the repository. If `false`, only audits issues updated in the last 24 hours. | `false`                 |
| `SPAM_LABEL_NAME`      | The exact text of the label applied to flagged issues.                                                             | `spam`                  |
| `BOT_NAME`             | The GitHub username of your official bot to ensure its comments are ignored.                                       | `adk-bot`               |
| `CONCURRENCY_LIMIT`    | The number of issues to process concurrently.                                                                      | `3`                     |
| `SLEEP_BETWEEN_CHUNKS` | Time in seconds to sleep between batches to respect GitHub API rate limits.                                        | `1.5`                   |
| `LLM_MODEL_NAME`       | The specific Gemini model version to use.                                                                          | `gemini-3.5-flash`      |
| `OWNER`                | Repository owner (auto-detected in Actions).                                                                       | (Environment dependent) |
| `REPO`                 | Repository name (auto-detected in Actions).                                                                        | (Environment dependent) |

______________________________________________________________________

## Deployment

To deploy this agent, a GitHub Actions workflow file (`.github/workflows/issue-monitor.yml`) is recommended.

### Directory Structure Note

Because this agent resides within the `adk-python` package structure, the workflow must ensure the script is executed correctly to handle imports. It must be run as a module from the parent directory.

### Example Workflow Execution

```yaml
      - name: Run ADK Issue Monitoring Agent
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          GOOGLE_API_KEY: ${{ secrets.GOOGLE_API_KEY }}
          OWNER: ${{ github.repository_owner }}
          REPO: ${{ github.event.repository.name }}
          # Mapped to the manual trigger checkbox in the GitHub UI
          INITIAL_FULL_SCAN: ${{ github.event.inputs.full_scan == 'true' }}
          PYTHONPATH: contributing/samples/adk_team
        run: python -m adk_issue_monitoring_agent.main
```

## Weilliptic setup and usage

This recipe uses the [`weil-ai`](https://pypi.org/project/weil-ai/) package. Run the commands below from this folder.

### Prerequisites

Before you run this recipe you need to set up your organization, create a subgroup and generate an agent identity. This is a one-time setup; follow the [Org onboarding guide](https://docs.weilliptic.ai/docs/org-onboarding/) and keep these steps in order:

1. **Set up your org and identity** ([guide](https://docs.weilliptic.ai/docs/org-onboarding/identity-setup)). Log in at console.weilliptic.ai with a connected wallet, open **Admin Panel** and the **Setup Identity** tab. Enter your org's TLD (the guide uses `acme`), keep the default **Key Management** and **Identity** applets, pick the pods (SENATE is always included) and click **Register Organization**, approving each wallet prompt. Then, in the WeilWallet extension, open **Account Details**, click **Link Organization**, select your org, and click **I've linked it — Continue** back in the console.
2. **Create a subgroup** ([guide](https://docs.weilliptic.ai/docs/org-onboarding/team-onboarding)). On the master pod's **Onboard Team** tab, click **Create Subgroup** and fill in the team name, team admin address, admin name and designation. You get a subgroup such as `engg.acme`.
3. **Add an agent** ([guide](https://docs.weilliptic.ai/docs/org-onboarding/add-agents)). With your org selected as the active organization in WeilWallet, click **Add Agent**, enter a name, a description and a purpose (the guide uses "Execution"), and pick the subgroup. When registration finishes, the agent's identity and wallet address are shown **once**; copy the identity.

Put the identity in `WEIL_ADK_TEAM_AGENT_IDENTITY` (see [Setup](#setup)). `WEIL_ADK_TEAM_SERVICE` defaults to `engg.acme`, the example subgroup in the guide; set it to your own subgroup if you named it differently.

The identity is a live credential: anyone who has it can sign as the agent. Keep it in `.env` and never commit it.

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
| `GITHUB_TOKEN` | GitHub personal access token with `repo` and `issues: write` scope. |

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
docker build -t weil-adk-issue-monitor .
grep -vE '^\s*(#|$)|<TODO' .env | sed -E 's/[[:space:]]+#.*$//' > .env.docker
docker run --rm --env-file .env.docker -p 8080:8080 weil-adk-issue-monitor
```

Open <http://localhost:8080/dev-ui/> and pick `app`. `.env.docker` is `.env` without comments (Docker's `--env-file` does not strip them) and is git-ignored. Credentials are never copied into the image; they come from `--env-file` at run time.

One-off jobs use the same image with a different command:

```bash
docker run --rm --env-file .env.docker weil-adk-issue-monitor uv run python -m app.main
```
