# learningllm

Try a small Gemini request through LiteLLM:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python test_litellm.py --mock
```

Create your own Gemini API key at https://aistudio.google.com/apikey
(model access and available quota are required). Never commit it or paste it into chat.
In this cloud environment, add the `LITELLM_API_KEY` secret in environment
settings with destination `generativelanguage.googleapis.com`. The program also accepts
`GEMINI_API_KEY` when running locally.

For a local terminal, enter the key without displaying it or saving it in shell history:

```bash
read -rsp 'Gemini API key: ' LITELLM_API_KEY
export LITELLM_API_KEY
echo
.venv/bin/python test_litellm.py
```

Use `--prompt 'Explain LiteLLM in one sentence'` or `--model gemini/gemini-3.1-flash-lite`
to customize the request. A live request uses your API credits. `--mock` runs
without credentials or an API request and does not verify Gemini connectivity.
Use `--timeout 60` to set the request timeout in seconds.

The prepared cloud Python environment is `/workspace/.venvs/learningllm`;
use its `bin/python` in place of `.venv/bin/python` there.

## Run LiteLLM as a gateway

The request path is: Python client → local LiteLLM gateway → Gemini.
The gateway exposes an OpenAI-compatible API and maps the `gemini-learning`
alias to `gemini/gemini-3.1-flash-lite` in `gateway.yaml`. The client needs
only the alias; the Gemini key stays in the gateway.

Install the dependencies above, then start the gateway in one terminal:

```bash
PYTHON=.venv/bin/python bash start_gateway.sh
```

In the cloud environment, use:

```bash
PYTHON=/workspace/.venvs/learningllm/bin/python bash start_gateway.sh
```

From a second terminal in this repository, check readiness, list aliases,
and make a live request (uses your Gemini quota):

```bash
curl --fail http://127.0.0.1:4000/health/liveliness
curl --fail http://127.0.0.1:4000/v1/models
.venv/bin/python test_gateway.py
.venv/bin/python test_gateway.py --prompt 'Explain model routing simply'
```

Use `/workspace/.venvs/learningllm/bin/python` for the client in the cloud.
Stop the foreground gateway with Ctrl+C. Edit `gateway.yaml` and restart
to experiment with aliases or other models available to your Gemini key.
The gateway binds to loopback with no client authentication, for local learning.
Keep it on loopback; shared deployments need authentication and access controls.
No database is needed for this basic routing example.

If a request reports depleted prepayment credits, add credits to the Gemini
project in Google AI Studio. LiteLLM may wrap that provider billing error
in an HTTP 500 response; the gateway client prints a clearer explanation.
