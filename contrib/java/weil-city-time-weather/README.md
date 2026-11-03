# City Time and Weather

ADK's city time and weather quickstart, with a Weil wallet identity. An agent that tells the current time and the weather in a city.

## What Weil adds

- **An audit trail on chain:** every model call, tool call and agent step is recorded under the agent's wallet.
- **Permission checks:** a tool marked `@WeilSecured` runs only when the wallet is permitted in its subgroup (`engg.weil` here), checked on chain.

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
(set -a; source .env; set +a; mvn -q compile exec:java -Dexec.mainClass=com.weilliptic.weilwallet.examples.city_time_weather.CityTimeWeather)
```

With no question it runs a default conversation:

- "I live in New York. What's the weather there?"
- "What time is it in my city?"

Pass your own with `-Dexec.args="..."`.

## Run in Docker

```bash
docker build -t weil-city-time-weather .
```

```bash
docker run -it --rm --env-file .env weil-city-time-weather
```
