# Context Caching

ADK's [`examples/contextcaching`](https://github.com/google/adk-java/tree/main/examples/contextcaching), with a Weil wallet identity. An agent with a large, fixed reference prompt, cached by the model provider so later turns are cheaper and faster.

## What Weil adds

- **An audit trail on chain:** every model call, tool call and agent step is recorded under the agent's wallet.
- **Permission checks:** a tool marked `@WeilSecured` runs only when the wallet is permitted in its subgroup (`engg.weil` here), checked on chain.
- **Prompt caching on any provider:** with Anthropic, the fixed start of the prompt is cached (`CLAUDE_PROMPT_CACHE`); the token counts in the audit trail show the cached share.

## Prerequisites

- JDK 17 and Maven 3.9
- A Weil Agent Registry key, and a Sentinel your machine can reach
- A model key: Anthropic, or OpenAI (or any OpenAI-compatible server)
- Docker, only to run it in a container

## Setup

Copy the example environment file and fill in your keys:

```bash
cp .env.example .env
```

Set at least `WEIL_AGENT_KEY` and your model's key: `ANTHROPIC_API_KEY`, or `MODEL_PROVIDER=openai` with `OPENAI_API_KEY` and `OPENAI_MODEL`. `.env.example` lists every setting this example reads. `.env` holds keys; never commit it.

Your wallet must be permitted in the subgroup `engg.weil`, or the agent's tool calls are refused. For a local development Sentinel, trust its certificate, or set `WEIL_TLS_VERIFY=0` for local testing only.

## Run

From this folder, load `.env` and run the example:

```bash
(set -a; source .env; set +a; mvn -q compile exec:java -Dexec.mainClass=com.weilliptic.weilwallet.examples.contextcaching.ContextCachingAgent)
```

With no question it runs a default conversation:

- "Ask about the weather reference it holds, then ask again: the second answer reuses the cached prompt."

Pass your own with `-Dexec.args="..."`.

## Run in Docker

```bash
docker build -t weil-contextcaching .
```

```bash
docker run -it --rm --env-file .env weil-contextcaching
```
