import os
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

def main():
    print("Loading Environment...")
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key == None:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")

    client = genai.Client(api_key=api_key)

    # Process arguments
    parser = argparse.ArgumentParser(description="Agent Chat")
    parser.add_argument("user_prompt", type=str, help="Your prompt")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    # Send Prompt
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    print("Sending Question...")
    response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=SYSTEM_PROMPT,
            temperature=0,
        ),
    )

    # Print Response
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
    if response.text:
        print(f"Response: {response.text}")
    if response.function_calls:
        for call in response.function_calls:
            function_call_result = call_function(call, args.verbose)
            if not function_call_result.parts:
                raise Exception("Error: Function didn't return anything")
            if not function_call_result.parts[0].function_response:
                raise Exception("Error: Function response incorrect type")
            if not function_call_result.parts[0].function_response.response:
                raise Exception("Error: Function response empty")
            function_results = function_call_result.parts[0]
            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
        
    if args.verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        

if __name__ == "__main__":
    main()
