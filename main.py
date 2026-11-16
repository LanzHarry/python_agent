import argparse
import os
import sys

from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam

from functions.messages import convert_message_to_param, handle_tool_call, message_model
from prompts import system_prompt


def main() -> None:
    parser = argparse.ArgumentParser(description="AI-agent")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    _ = load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("Api key environment variable not set")

    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)

    messages: list[ChatCompletionMessageParam] = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    for _ in range(20):
        # call the model, handle responses etc.
        response = message_model(client, messages, args.verbose)
        messages.append(convert_message_to_param(response))

        if response.tool_calls is not None:
            for tool_call in response.tool_calls:
                if tool_call.type == "function":
                    tool_call_result = handle_tool_call(tool_call, args.verbose)
                    messages.append(tool_call_result)
        else:
            print(f"Final response:\n{response.content}")
            return

    sys.exit(1)


if __name__ == "__main__":
    main()
