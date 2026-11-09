"""Shared Weil configuration for the ported ADK team examples."""

import os

WEIL_ADK_TEAM_AGENT_IDENTITY = os.getenv(
    "WEIL_ADK_TEAM_AGENT_IDENTITY",
    "weil_xxxx",
)
WEIL_ADK_TEAM_SERVICE = os.getenv("WEIL_ADK_TEAM_SERVICE", "engg.acme")
WEIL_ADK_TEAM_MODEL = os.getenv("WEIL_ADK_TEAM_MODEL", "openai/gpt-5.1")
