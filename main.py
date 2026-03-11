import os
import argparse

from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.get_files_info import schema_get_files_info
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
            print(f"Calling function: {call.name}({call.args})")
    if args.verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        

if __name__ == "__main__":
    main()
