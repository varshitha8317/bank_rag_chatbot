import google.generativeai as genai

# 🔐 Paste your API key here
genai.configure(api_key="AIzaSyC8F7MPCgRvrvC4FZ9ZPjoxdpV8TeG2g3g")

model = genai.GenerativeModel("gemini-2.5-flash")   # ✅ updated model


def ask_llm(query):
    try:
        response = model.generate_content(query)

        if response and hasattr(response, "text"):
            return response.text

        return "No response from AI"

    except Exception as e:
        print("Gemini Error:", e)   # 👈 IMPORTANT (see error in terminal)
        return "AI service is currently unavailable"