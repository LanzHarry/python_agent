import json

from openai import OpenAI
from openai.types.chat import (
    ChatCompletionAssistantMessageParam,
    ChatCompletionMessage,
    ChatCompletionMessageFunctionToolCall,
    ChatCompletionMessageParam,
    ChatCompletionToolMessageParam,
)

from functions.call_function import available_functions, call_function


def message_model(
    client: OpenAI, messages: list[ChatCompletionMessageParam], verbose: bool
) -> ChatCompletionMessage:

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions,
    )

    if not response.usage:
        raise RuntimeError("Response may be malformed")

    if verbose:
        prompt_tokens = response.usage.prompt_tokens
        response_tokens = response.usage.completion_tokens
        last_message = messages[-1]
        if "content" in last_message:
            print(f"User prompt: {last_message['content']}")
        print(f"Prompt tokens: {prompt_tokens}\nResponse tokens: {response_tokens}")

    return response.choices[0].message


def handle_tool_call(
    tool_call: ChatCompletionMessageFunctionToolCall, verbose: bool
) -> ChatCompletionToolMessageParam:
    function_args = json.loads(tool_call.function.arguments or "{}")
    print(f"Calling function: {tool_call.function.name}({function_args})")
    result_message = call_function(tool_call, verbose)

    if not result_message["content"]:
        raise RuntimeError("No content in tool result message")

    if verbose:
        print(f"-> {result_message['content']}")

    return result_message


def convert_message_to_param(
    message: ChatCompletionMessage,
) -> ChatCompletionAssistantMessageParam:
    param: ChatCompletionAssistantMessageParam = {"role": "assistant"}
    if message.content is not None:
        param["content"] = message.content
    return param
