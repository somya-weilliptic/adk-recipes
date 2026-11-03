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

# adk_pr_triaging_agent: one image for this project only.
# Build from the recipe root (the directory holding requirements.txt):
#   docker build -f adk_team/adk_pr_triaging_agent/Dockerfile -t adk_pr_triaging_agent .
#   docker run --rm --env-file adk_team/adk_pr_triaging_agent/.env -p 8000:8000 adk_pr_triaging_agent
#   docker run --rm --env-file adk_team/adk_pr_triaging_agent/.env adk_pr_triaging_agent python -m adk_pr_triaging_agent.main
FROM python:3.11-slim

WORKDIR /code/agents

# Dependencies first so this layer is cached across code changes.
# Shared dependencies are installed from requirements.txt.
COPY ./requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY ./adk_team/adk_pr_triaging_agent /code/agents/adk_pr_triaging_agent
COPY ./adk_team/config.py /code/agents/config.py
COPY ./adk_team/component_owners.py /code/agents/component_owners.py

# Pass credentials with --env-file at run time; they are not copied in.
ENV PYTHONPATH="/code/agents" \
    PYTHONUNBUFFERED=1

RUN useradd --create-home --uid 1000 appuser && \
    chown -R appuser /code

USER appuser

# adk web UI.
EXPOSE 8000

CMD ["adk", "web", "--host", "0.0.0.0", "--port", "8000", "/code/agents"]
