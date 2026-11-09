# Agent with Long-Running Tools

This example demonstrates an agent using a long-running tool (`ask_for_approval`).

## Key Flow for Long-Running Tools

1. **Initial Call**: The agent calls the long-running tool (e.g., `ask_for_approval`).

1. **Initial Tool Response**: The tool immediately returns an initial response, typically indicating a "pending" status and a way to track the request (e.g., a `ticket-id`). This is sent back to the agent as a `types.FunctionResponse` (usually processed internally by the runner and then influencing the agent's next turn).

1. **Agent Acknowledges**: The agent processes this initial response and usually informs the user about the pending status.

1. **External Process/Update**: The long-running task progresses externally (e.g., a human approves the request).

1. **❗️Crucial Step: Provide Updated Tool Response❗️**:

   - Once the external process completes or updates, your application **must** construct a new `types.FunctionResponse`.
   - This response should use the **same `id` and `name`** as the original `FunctionCall` to the long-running tool.
   - The `response` field within this `types.FunctionResponse` should contain the *updated data* (e.g., `{'status': 'approved', ...}`).
   - Send this `types.FunctionResponse` back to the agent as a part within a new message using `role="user"`.

   ```python
   # Example: After external approval
   updated_tool_output_data = {
       "status": "approved",
       "ticketId": ticket_id,  # from original call
       # ... other relevant updated data
   }

   updated_function_response_part = types.Part(
       function_response=types.FunctionResponse(
           id=long_running_function_call.id,  # Original call ID
           name=long_running_function_call.name,  # Original call name
           response=updated_tool_output_data,
       )
   )

   # Send this back to the agent
   async for _ in runner.run_async(
       # ... session_id, user_id ...
       new_message=types.Content(
           parts=[updated_function_response_part], role="user"
       ),
   ):
       pass  # exhaust generator (or handle events)
   ```

1. **Agent Acts on Update**: The agent receives this message containing the `types.FunctionResponse` and, based on its instructions, proceeds with the next steps (e.g., calling another tool like `reimburse`).

**Why is this important?** The agent relies on receiving this subsequent `types.FunctionResponse` (provided in a message with `role="user"` containing the specific `Part`) to understand that the long-running task has concluded or its state has changed. Without it, the agent will remain unaware of the outcome of the pending task.

## Weilliptic setup and usage

This recipe uses the [`weil-ai`](https://pypi.org/project/weil-ai/) package. Run the commands below from this folder.

### Setup

1. Install the dependencies:

   ```bash
   uv sync
   ```

2. Create the env file and fill in the values:

   ```bash
   cp .env.example .env
   ```

   Variables you must set: `OPENAI_API_KEY`. The other variables in the file have working defaults.

3. Replace the placeholder `identity="weil_xxxx"` in `app/agent.py` with your own Weilliptic identity. It is hardcoded there, and WeilChain rejects the placeholder at startup. See [Generate an agent identity](../weilliptic-integration/README.md#generate-an-agent-identity).

### Run locally

```bash
uv run adk web
```

Open <http://localhost:8000> and pick `app` from the agent list.

### Run with Docker

```bash
docker build -t weil-human-in-loop .
docker run --rm --env-file .env -p 8080:8080 weil-human-in-loop
```

The image serves the app on port 8080 (`/list-apps` lists it). Credentials are never copied into the image; they come from `--env-file` at run time.

### A2A server

The agent also builds a Weil-secured A2A app, `a2a_app`, which rejects requests that do not carry valid Weil signature headers. It advertises port 8007:

```bash
docker run --rm --env-file .env -p 8007:8007 weil-human-in-loop \
  uv run uvicorn app.agent:a2a_app --host 0.0.0.0 --port 8007
```

See the [Weilliptic integration guide](../weilliptic-integration/README.md) for how the security hooks work.
