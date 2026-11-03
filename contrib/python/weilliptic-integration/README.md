# Weilliptic Integration for Google ADK

These recipes secure Google ADK agents with WeilChain identities, tool
permissions, and signed agent-to-agent (A2A) requests. The `weil-ai` package
wraps an ADK agent and connects it to the wallet and permission APIs in
`weil-wallet`.

## How the security hooks work

| API | What it does |
|---|---|
| `@weil_ai.agent(identity=...)` | Resolves the identity to a WeilChain wallet and wraps the ADK agent. The plain agent is exposed as `root_agent` for `adk web`. |
| `@weil_ai.secured_user("service.name")` | Checks that the calling wallet has an Execution or Management key for the named service before the tool runs. |
| `setup_secure_a2a()` | Adds signing, verification, and audit hooks to the ADK agent tree. |
| `to_secure_a2a(...)` | Creates the secured A2A app and verifies signed headers on incoming requests. |

The `hitl/` and `multi_agent/` agents expose an A2A app as well as the ADK
`root_agent`. The `adk_team/` agents use the security hooks from the ADK web
interface. Each Dockerfile starts `adk web` by default; its header also shows
how to run any project-specific job or A2A app.

## Recipe groups

| Directory | What it contains |
|---|---|
| `hitl/` | Human approval, confirmation, user input, and classifier-gated tools. |
| `multi_agent/` | Sub-agent handoff, task agents, and multi-level transfers. |
| `adk_team/` | GitHub issue and pull request tools, documentation agents, and Vertex AI Search agents. `adk_documentation/` contains a docs updater and a release analyzer. |

## Requirements

- The `weil-ai` and `weil-wallet` packages. `requirements.txt` installs both
  from PyPI; to use Weilliptic's public repository instead, see
  [the alternative below](#alternative-install-the-sdk-from-weilliptics-public-repository).
- A Weilliptic agent identity (a `weil_...` string) registered on WeilChain. See
  [Generate an agent identity](#generate-an-agent-identity).
- Execution (or Management) permission for that identity on every service named
  by a `secured_user(...)` tool. A tool decorated with
  `secured_user("engg.acme")`, for example, needs a key for `engg.acme`.

## Generate an agent identity

Every agent needs an identity string that looks like `weil_...`. You create it
at [marauder.weilliptic.ai](https://marauder.weilliptic.ai), and `weil-ai`
resolves it to the agent's wallet through the Sentinel node. These steps follow
[Weilliptic's documentation](#sources).

### Organization, team and service names

Identities are issued under an organization (and optionally a subgroup), and
the service names the recipes check are built from them as
`<subgroup>.<organization>`. `engg.acme` is the subgroup `engg` of the
organization `acme`, which is what `@weil_ai.secured_user("engg.acme")` checks.

1. Install the **WAuth** browser extension from Weilliptic
   ([Chrome](https://chromewebstore.google.com/detail/wauth/nmdlcegenjnehamofkaaifhgjibdpdag),
   [Firefox](https://addons.mozilla.org/addon/wauth/)). Create a new account in
   it, or import an existing one with its recovery phrase or private key. WAuth
   holds your wallet and approves the transactions below.
2. Sign in at [marauder.weilliptic.ai](https://marauder.weilliptic.ai) with
   WAuth.
3. Register the organization (for example `acme`) in SENATE: open the **Setup
   Identity** tab, enter the organization, and approve the prompts in WAuth.
   Your connected wallet becomes a Management wallet.
4. On the master WeilPod, open **Onboard Team**, select the organization, and
   enter the team name (for example `engg`), which creates the subgroup. Set a
   team admin wallet (Management) and add developer wallets (Execution).

### Create the agent identity

1. In [marauder.weilliptic.ai](https://marauder.weilliptic.ai), create the agent
   identity for that organization and team with the **Execution** purpose, which
   is what these recipes use. Copy the `weil_...` string it gives you.
2. Make sure the identity has **Execution** on the scope its secured tools name
   (here `engg.acme`, or the whole `acme` organization). Without it, tools fail
   with `WalletNotPermittedError`.
3. Give the identity to the recipe:
   - `adk_team/` projects: set `WEIL_ADK_TEAM_AGENT_IDENTITY=weil_...` in the
     project's `.env`.
   - `hitl/` and `multi_agent/` projects: replace `identity="weil_xxxx"` in the
     project's `agent.py`.

One identity can be shared by several recipes, or you can create one per agent.
If the identity's wallet is stored in your own S3 bucket, the process may also
need the `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION` and
`AWS_BUCKET_NAME` environment variables.

### Sources

- [Client SDK: agent identities and secure signing](https://docs.weilliptic.ai/docs/explainers/client-sdk#agent-identities-and-secure-signing)
- [Agentic integrations tutorial](https://docs.weilliptic.ai/docs/tutorials/agentic-integrations)
- [Secured MCP servers: identity and permissions](https://docs.weilliptic.ai/docs/tutorials/mcp_secured#setting-up-identity-and-permissions)

## Alternative: install the SDK from Weilliptic's public repository

By default `requirements.txt` installs `weil-ai` and `weil-wallet` from PyPI.
Weilliptic also publishes the same Python SDK as source in the public
[`weilliptic-public/wadk`](https://github.com/weilliptic-public/wadk)
repository, under `adk/python`:

| Folder | What it is |
|---|---|
| `weil_wallet` | Wallet, signing and transaction primitives. |
| `weil_ai` | The agent, `secured_user` and secure A2A integrations these recipes use. It depends on `weil_wallet`. |
| `examples` | Runnable usage examples, including Google ADK, LangChain and secured-agent examples. |

To use it instead of the PyPI packages, install `weil_wallet` first, then
`weil_ai`, and then the rest of this recipe's requirements. pip keeps the
packages you already installed because they satisfy the `>=0.1.0` pins:

```bash
git clone https://github.com/weilliptic-public/wadk.git
cd wadk/adk/python
python3 -m venv .venv && source .venv/bin/activate   # recommended
pip3 install ./weil_wallet
pip3 install ./weil_ai
cd /path/to/adk-recipes/contrib/python/weilliptic-integration
python3 -m pip install -r requirements.txt
```

On Linux, `weil_wallet` builds a small native extension, so OpenSSL and libcurl
development headers must be installed. The Dockerfiles always install from PyPI
through `requirements.txt`.

## Install and run locally

From this directory, install the shared dependencies with pip:

```bash
python3 -m pip install -r requirements.txt
```

For example, configure and start the human-in-loop recipe:

```bash
cp hitl/human_in_loop/.env.example hitl/human_in_loop/.env
# Edit .env and replace the identity in hitl/human_in_loop/agent.py.
adk web --port 8000 hitl/human_in_loop
```

ADK loads the project's `.env` automatically.

An A2A server does not load `.env` itself, so export it first and run the app
instead of `adk web`:

```bash
set -a && . hitl/human_in_loop/.env && set +a
PYTHONPATH=hitl python3 -m uvicorn human_in_loop.agent:a2a_app \
  --host 0.0.0.0 --port 8007
```

The `adk_team/` projects also provide command-line jobs. For example, after
copying and filling `adk_team/adk_stale_agent/.env.example`, run:

```bash
cd adk_team
python3 -m adk_stale_agent.main
```

The Dockerfile headers include the command-line entrypoints and arguments for
the other jobs.

## Run with Docker

Build from this directory, which is the shared Docker build context. Select
the Dockerfile and `.env` for the recipe you want to run:

```bash
cp hitl/human_in_loop/.env.example hitl/human_in_loop/.env
# Edit .env and replace the identity in hitl/human_in_loop/agent.py.
docker build -f hitl/human_in_loop/Dockerfile -t human_in_loop .
docker run --rm --env-file hitl/human_in_loop/.env \
  -p 8000:8000 human_in_loop
```

To serve its A2A app instead of the web UI, run:

```bash
docker run --rm --env-file hitl/human_in_loop/.env \
  -p 8007:8007 human_in_loop \
  uvicorn human_in_loop.agent:a2a_app --host 0.0.0.0 --port 8007
```