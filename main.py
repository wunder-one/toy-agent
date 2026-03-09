import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types



def main():
    print("Loading Environment...")
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key == None:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")

    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="Agent Chat")
    parser.add_argument("user_prompt", type=str, help="Your prompt")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    print("Sending Question...")
    response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents=messages
    )
    if args.verbose == True:
        print(f"User prompt: {args.user_prompt}")
    print(f"Response: {response.text}")
    if args.verbose == True:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        

if __name__ == "__main__":
    main()
