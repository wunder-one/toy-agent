import os
from dotenv import load_dotenv
from google import genai

def main():
    print("Loading Environment...")
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key == None:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")

    client = genai.Client(api_key=api_key)

    print("Sending Question...")
    response = client.models.generate_content(
        model='gemini-2.5-flash', 
        contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
    )
    print(f"[Answer]:{response.text}")

if __name__ == "__main__":
    main()
