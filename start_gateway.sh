#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"
: "${LITELLM_API_KEY:?Set LITELLM_API_KEY to your Gemini API key}"
export LITELLM_LOCAL_MODEL_COST_MAP=True
# Local learning only: bind to loopback because authentication is not configured.
exec "${PYTHON:-python3}" -c 'from litellm import run_server; run_server()' --config gateway.yaml --host 127.0.0.1 --port 4000
