import speech_recognition as sr
import pyttsx3
import requests

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak...")
        audio = r.listen(source)

    try:
        return r.recognize_google(audio)
    except:
        return ""

while True:
    query = listen()

    if not query:
        continue

    print("You:", query)

    res = requests.post(
        "http://127.0.0.1:5000/chat",
        json={"query": query}
    )

    data = res.json()

    if "answer" in data:
        answer = data["answer"]
    elif "balance" in data:
        answer = f"Your balance is {data['balance']} rupees"
    else:
        answer = str(data)

    print("Bot:", answer)
    speak(answer)