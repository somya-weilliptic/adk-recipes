# A2A Server (prime agent)

ADK's [`examples/a2a_server`](https://github.com/google/adk-java/tree/main/examples/a2a_server), with a Weil wallet identity. An agent that checks whether numbers are prime, served to other agents over A2A on port 8003. `a2a_basic` calls it.

## What Weil adds

- **An audit trail on chain:** every model call, tool call and agent step is recorded under the agent's wallet.
- **Permission checks:** a tool marked `@WeilSecured` runs only when the wallet is permitted in its subgroup (`engg.weil` here), checked on chain.
- **Signed callers only:** every A2A request must carry a valid wallet signature (401 otherwise), and the caller's wallet must be permitted in `engg.weil` (403 otherwise), before the agent runs.
- **No hand-written agent card:** the card is generated, with the address callers use set by `WEIL_A2A_PUBLIC_URL`.

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
(set -a; source .env; set +a; mvn -q compile exec:java -Dexec.mainClass=com.weilliptic.weilwallet.examples.a2a_server.agent.Agent)
```

It serves until stopped. Its agent card is at http://127.0.0.1:8003/.well-known/agent-card.json; run [`weil-agent-to-agent-basic`](../weil-agent-to-agent-basic) to call it.

## Run in Docker

```bash
docker build -t weil-a2a-server .
```

```bash
docker run --rm --env-file .env -p 8003:8003 -e WEIL_A2A_PUBLIC_URL=http://localhost:8003/ weil-a2a-server
```

In a container it listens on all interfaces. `WEIL_A2A_PUBLIC_URL` is the address its agent card names, and callers send their calls there, so it must be one they can reach.
