"""Send a small prompt through LiteLLM, or exercise the client offline."""

import argparse
import os
import sys

# Avoid downloading tokenizer metadata for this small connectivity test.
os.environ.setdefault("LITELLM_LOCAL_MODEL_COST_MAP", "True")

from litellm import completion


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default="gemini/gemini-3.1-flash-lite")
    parser.add_argument("--prompt", default="Say hello in one short sentence.")
    parser.add_argument("--timeout", type=float, default=60, help="Request timeout in seconds (default: 60)")
    parser.add_argument("--mock", action="store_true", help="Run without a key or API request")
    args = parser.parse_args()
    key = os.getenv("LITELLM_API_KEY") or os.getenv("GEMINI_API_KEY")
    if not args.mock and not key:
        parser.error("Set LITELLM_API_KEY or GEMINI_API_KEY, or use --mock.")
    options = {"mock_response": "Hello from LiteLLM!"} if args.mock else {"api_key": key}
    try:
        response = completion(
            model=args.model,
            messages=[{"role": "user", "content": args.prompt}],
            max_tokens=256,
            timeout=args.timeout,
            num_retries=0,
            **options,
        )
    except Exception as exc:
        # Avoid logging exception bodies that may contain request details.
        print(f"Request failed ({type(exc).__name__}). Check your key, billing, model access, and network.", file=sys.stderr)
        return 1
    print(response.choices[0].message.content)
    return 0


if __name__ == "__main__":
    sys.exit(main())
