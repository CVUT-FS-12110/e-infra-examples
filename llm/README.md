# CESNET LLM API example

This minimal example sends a chat request to the e-INFRA CZ LLM API using the
OpenAI Python SDK and prints the model's text response.

## Setup

Create and activate a virtual environment, then install the dependencies:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On PowerShell, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

Store your API token in `llm/.env`:

```dotenv
LLM_TOKEN=your_token_here
```

The `.env` file is ignored by Git. Do not commit or share your token.

## Run the request

From the `llm` directory, run:

```bash
python example.py
```

[`example.py`](./example.py) loads `LLM_TOKEN`, creates an asynchronous client
for `https://llm.ai.e-infra.cz/v1`, and sends a message with
`client.chat.completions.create()`. The returned text is available as:

```python
response.choices[0].message.content
```

The example uses `deepseek-v3.2`. Available models can change; list the current
model identifiers with:

```bash
curl -H "Authorization: Bearer $LLM_TOKEN" \
  https://llm.ai.e-infra.cz/v1/models
```

See the [e-INFRA CZ LLM API documentation](https://docs.cerit-sc.cz/en/docs/ai-as-a-service/ai-api)
for authentication, model discovery, and other supported features.
