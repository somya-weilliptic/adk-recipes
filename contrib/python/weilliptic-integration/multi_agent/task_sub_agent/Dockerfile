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

# task_sub_agent: one image for this project only.
# Build from the recipe root (the directory holding requirements.txt):
#   docker build -f multi_agent/task_sub_agent/Dockerfile -t task_sub_agent .
#   docker run --rm --env-file multi_agent/task_sub_agent/.env -p 8000:8000 -p 8004:8004 task_sub_agent
# Serve the secured A2A app instead of the web UI:
#   docker run --rm --env-file multi_agent/task_sub_agent/.env -p 8004:8004 task_sub_agent \
#     uvicorn task_sub_agent.agent:a2a_app --host 0.0.0.0 --port 8004
FROM python:3.11-slim

WORKDIR /code/agents

# Dependencies first so this layer is cached across code changes.
# Shared dependencies are installed from requirements.txt.
COPY ./requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY ./multi_agent/task_sub_agent /code/agents/task_sub_agent

# Pass credentials with --env-file at run time; they are not copied in.
ENV PYTHONPATH="/code/agents" \
    PYTHONUNBUFFERED=1

RUN useradd --create-home --uid 1000 appuser && \
    chown -R appuser /code

USER appuser

# adk web UI and the A2A server.
EXPOSE 8000 8004

CMD ["adk", "web", "--host", "0.0.0.0", "--port", "8000", "/code/agents"]
