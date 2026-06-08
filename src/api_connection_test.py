"""
API connection test script.
Verifies connectivity to a model service endpoint.
"""

import argparse
from openai import OpenAI


def test_connection(base_url: str, api_key: str, model_name: str) -> None:
    """
    Test API connectivity with a simple prompt.

    Args:
        base_url: API base URL.
        api_key: API key.
        model_name: Model identifier.
    """
    client = OpenAI(base_url=base_url, api_key=api_key)
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Hello, what model are you?"},
            ],
            stream=False,
        )
        print("Connection successful!")
        print(f"Response: {response.choices[0].message.content}")
    except Exception as e:
        print(f"Connection failed: {e}")


def main():
    parser = argparse.ArgumentParser(description="Test model API connection")
    parser.add_argument("--base_url", required=True, help="API base URL")
    parser.add_argument("--api_key", required=True, help="API key")
    parser.add_argument("--model", required=True, help="Model name")
    args = parser.parse_args()

    test_connection(args.base_url, args.api_key, args.model)


if __name__ == "__main__":
    main()
