import os

from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("GEMINI_API_KEY must be set")


client = genai.Client(api_key=api_key)

prompt = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)

print(f"User prompt: {prompt}")

if response.usage_metadata:
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
else:
    raise RuntimeError("request failed")

print("Response:")
print(response.text)
