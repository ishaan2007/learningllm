"""Send an OpenAI-compatible request to the local LiteLLM gateway."""

import argparse
import sys

from openai import OpenAI


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prompt", default="Explain what an LLM gateway does in one sentence.")
    parser.add_argument("--model", default="gemini-learning")
    args = parser.parse_args()
    # This is a dummy client key for our loopback-only, unauthenticated gateway.
    # The Gemini key stays in the gateway process.
    client = OpenAI(base_url="http://127.0.0.1:4000/v1", api_key="local-learning", timeout=90, max_retries=0)
    try:
        response = client.chat.completions.create(
            model=args.model,
            messages=[{"role": "user", "content": args.prompt}],
            max_tokens=256,
        )
    except Exception as exc:
        # Classify the provider's error without printing request details or keys.
        if "prepayment credits are depleted" in str(exc).lower():
            print("Gemini credits are depleted. Add credits in Google AI Studio, then retry.", file=sys.stderr)
            return 1
        print(f"Gateway request failed ({type(exc).__name__}). Check gateway startup and provider access.", file=sys.stderr)
        return 1
    print(response.choices[0].message.content)
    return 0


if __name__ == "__main__":
    sys.exit(main())
