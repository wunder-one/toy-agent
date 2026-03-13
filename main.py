import os
import sys
import argparse

from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file
from functions.call_function import call_function

from prompts import SYSTEM_PROMPT, available_functions

def call_model(client, messages, verbose=False):
    response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=SYSTEM_PROMPT,
            temperature=0,
        ),
    )
    if not response.usage_metadata:
        raise RuntimeError("Gemini API response appears to be malformed")

    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content)

    # Print Response
    function_responses = []
    if response.function_calls:
        for function_call in response.function_calls:
            function_call_result = call_function(function_call, verbose)
            if (
                not function_call_result.parts
                or not function_call_result.parts[0].function_response
                or not function_call_result.parts[0].function_response.response
            ):
                raise RuntimeError(f"Empty function response for {function_call.name}")
            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
            function_responses.append(function_call_result.parts[0])

    if function_responses:
        messages.append(types.Content(role="user", parts=function_responses))
        is_final = False
    else:
        print(f"Response: {response.text}")
        is_final = True

    # if response.text:
    #     print(f"Response: {response.text}")
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    return messages, is_final


def main():
    print("Loading Environment...")
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key == None:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")

    # Process arguments
    parser = argparse.ArgumentParser(description="Agent Chat")
    parser.add_argument("user_prompt", type=str, help="Your prompt")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    # Send Prompt
    client = genai.Client(api_key=api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    print("Sending First Question...")
    if args.verbose:
        print(f"User prompt: {args.user_prompt}\n")
    for call in range(10):
        # print(f"Messages going in --> {messages}")
        messages, is_final = call_model(client, messages, args.verbose)
        if is_final:
            break
    if not is_final:
        print("Error: Maximum response limit reached")
        sys.exit(1)


if __name__ == "__main__":
    main()
