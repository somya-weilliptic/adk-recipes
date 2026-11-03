# Financial Advisor

The adk-recipes Java recipe [`contrib/java/financial-advisor`](https://github.com/google/adk-recipes/tree/main/contrib/java/financial-advisor), with a Weil wallet identity. A coordinator that analyses a stock ticker with four specialist agents: data analysis (web search), trading strategies, an execution plan and a risk assessment.

## What changes for Weil

- **Model**: `Models` uses `WeilAgentSetup.model()`, so `MODEL_PROVIDER`
  (anthropic or openai) picks the model instead of Gemini's `MODEL_NAME`.
- **Search**: Gemini's `GoogleSearchTool` runs on Google's side, where no
  permission check sees it. The data analyst uses `web_search`
  (`WebSearchTools.java`) instead. Any model can call it, and it runs
  through the organisation's search applet (`websearch::<org>`, or
  `WEIL_SEARCH_APPLET`). Its method carries `@WeilSecured("engg.weil")`, so only
  a wallet with Execution or Management in `engg.weil` can search.
- **Audit**: `main` runs the coordinator with `Weil.chat`. Each specialist runs
  as an `AgentTool` made by `Weil.agentTool`, with the coordinator's plugins
  (`includePlugins`, which ADK
  leaves off by default). So every model call, agent-tool call and search, the
  specialists' included, is audited under the agent's wallet, and `web_search`'s
  `@WeilSecured` gate applies inside the data analyst.
- **Specialist gates**: an agent has no Java method to carry `@WeilSecured`, so
  each specialist is made with `Weil.agentTool(agent, service)`, and the tool
  carries its service instead. `SPECIALIST_SERVICES` in `FinancialAdvisorAgent`
  maps each one to its service (all `engg.weil` here).
  A wallet without Execution or Management there is refused before the
  specialist runs, and the coordinator gets "Permission denied" as the result.
  Each verdict is published to `security`, as for any gated tool.

The agents:

- `FinancialAdvisorAgent`: the coordinator, `financial_coordinator`. It calls
  the four specialists as `AgentTool`s.
- `DataAnalystAgent` (`market_data_analysis_output`): searches the web for a ticker.
- `TradingAnalystAgent` (`proposed_trading_strategies_output`)
- `ExecutionAnalystAgent` (`execution_plan_output`)
- `RiskAnalystAgent` (`final_risk_assessment_output`)
- `LegalDisclaimer`, `Models`

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
(set -a; source .env; set +a; mvn -q compile exec:java -Dexec.mainClass=com.weilliptic.weilwallet.examples.financialadvisor.FinancialAdvisorAgent)
```

With no question it runs a default conversation:

- "Analyze the market ticker NVDA."

Pass your own with `-Dexec.args="..."`.

## Run in Docker

```bash
docker build -t weil-financialadvisor .
```

```bash
docker run -it --rm --env-file .env weil-financialadvisor
```
