# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Runnability tests for the recipe."""

import os
from unittest.mock import AsyncMock, patch

from weil_wallet.wallet import PrivateKey, Wallet

# Values the recipe's settings require at import time.
_ENV = {
    "GITHUB_TOKEN": "test-token",
    "VERTEXAI_DATASTORE_ID": "projects/p/locations/global/collections/c/dataStores/d",
}


def test_agent_runnability() -> None:
    """Verify agent.py imports and defines the expected globals."""
    # `@weil_ai.agent(identity=...)` resolves the agent's wallet from the
    # Sentinel node at import time. Stub that lookup with a throwaway offline
    # wallet so the test needs no network and no real identity.
    offline_wallet = Wallet.from_private_key_and_address(
        PrivateKey.from_hex("11" * 32), "0x" + "11" * 20
    )
    with (
        patch.dict(os.environ, _ENV),
        patch(
            "weil_wallet.WeilClient.get_agent_wallet",
            new=AsyncMock(return_value=offline_wallet),
        ),
    ):
        import app.agent

    assert app.agent.root_agent is not None
