from dotenv import load_dotenv
from openai import OpenAI
from google import genai
from anthropic import Anthropic
import os
load_dotenv()

azureKey = os.getenv("OPENAI_API_KEY")
geminiKey = os.getenv("GOOGLE_API_KEY")
claudekey = os.getenv("ANTHROPIC_API_KEY")

openai_client = OpenAI()
gemini_client = genai.Client(api_key= geminiKey)
clade_client = Anthropic(api_key= claudekey )

openai_response = openai_client.responses.create(
    model = "gpt-5.4-mini",
    input = "Who won the IPL 2026?"
)

gemini_response = gemini_client.models.generate_content(
    model="gemini-3.5-flash",
    contents="Who won the IPL 2025?"
)

claude_response = clade_client.messages.create(
    model="claude-sonnet-4-5-20250929",
    messages=[{"role": "user", "content": "Hello, Claude"}]
)

print(openai_response.output_text)
print (gemini_response.text)
print(claude_response.content)

