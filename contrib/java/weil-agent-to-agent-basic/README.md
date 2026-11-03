# A2A Basic (dice agent)

ADK's [`examples/a2a_basic`](https://github.com/google/adk-java/tree/main/examples/a2a_basic), with a Weil wallet identity. A root agent that rolls dice locally and asks the remote prime agent (`a2a_server`) over A2A which rolls are prime.

## What Weil adds

- **An audit trail on chain:** every model call, tool call and agent step is recorded under the agent's wallet.
- **Permission checks:** a tool marked `@WeilSecured` runs only when the wallet is permitted in its subgroup (`engg.weil` here), checked on chain.
- **Signed A2A calls:** every call to the prime agent is signed with this agent's wallet, so the prime agent knows who is calling and checks its permission.

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

It calls the prime agent, so start [`weil-agent-to-agent-server`](../weil-agent-to-agent-server) first, with its own wallet key, and set `PRIME_URL` if it does not serve at http://127.0.0.1:8003.

## Run

From this folder, load `.env` and run the example:

```bash
(set -a; source .env; set +a; mvn -q compile exec:java -Dexec.mainClass=com.weilliptic.weilwallet.examples.a2a_basic.A2AAgent)
```

With no question it runs a default conversation:

- "Roll a 20-sided die."
- "Is that number prime?"

Pass your own with `-Dexec.args="..."`.

## Run in Docker

```bash
docker build -t weil-a2a-basic .
```

```bash
docker run -it --rm --env-file .env -e PRIME_URL=http://<prime host>:8003 weil-a2a-basic
```

`compose.yaml` runs both agents together, each with its own `.env`, the dice agent reaching the prime agent at `http://prime:8003`:

```bash
docker compose up -d --build prime
```

```bash
docker compose run --rm --build dice
```
