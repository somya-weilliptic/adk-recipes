# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Weil and model settings, read from the environment (.env)."""

import os

# Weilliptic identity registered on WeilChain (weil_<token>). The
# weil_xxxx placeholder is rejected at startup; set the real one in .env.
WEIL_AGENT_IDENTITY = os.getenv("WEIL_AGENT_IDENTITY", "weil_xxxx")

# Weil service the secured tools are registered under.
WEIL_SERVICE = os.getenv("WEIL_SERVICE", "engg.acme")

# LiteLLM model id the agent runs on.
AGENT_MODEL = os.getenv("AGENT_MODEL", "openai/gpt-4o")
