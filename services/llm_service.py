import os
from dotenv import load_dotenv
import google.generativeai as genai

# 🔹 Load environment variables
load_dotenv()

# 🔹 Get API key from .env
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

# 🔹 Configure Gemini
genai.configure(api_key=API_KEY)

# 🔹 Load model
model = genai.GenerativeModel("gemini-2.5-flash")


def ask_llm(query: str) -> str:
    try:
        response = model.generate_content(query)

        # ✅ Safe response handling
        if response and hasattr(response, "text") and response.text:
            return response.text.strip()

        return "No response from AI"

    except Exception as e:
        print("Gemini Error:", e)
        return "AI service is currently unavailable"