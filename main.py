import speech_recognition as sr
import os
import webbrowser
import openai
from config import apikey
import datetime
import random
import numpy as np
import win32com.client
# from AppOpener import open, close

speaker = win32com.client.Dispatch("SAPI.SpVoice")
chatStr = ""

# https://youtu.be/Z3ZAJoi4x6Q
def chat(query):
    global chatStr
    print(chatStr)
    openai.api_key = apikey
    chatStr += f"Saket: {query}\n Helper A.I.: "
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=chatStr,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # todo: Wrap this inside of a  try catch block
    print(response["choices"][0]["text"])
    chatStr += f"{response['choices'][0]['text']}\n"
    return response["choices"][0]["text"]


def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # todo: Wrap this inside of a  try catch block
    # print(response["choices"][0]["text"])
    text += response["choices"][0]["text"]
    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    # with open(f"Openai/prompt- {random.randint(1, 2343434356)}", "w") as f:
    with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip()}.txt", "w") as f:
        f.write(text)


def say(text):
    speaker.Speak(text)


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 0.6
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "Some Error Occurred. Sorry from Helper A.I."


if __name__ == '__main__':
    print('Welcome to Helper A.I.')
    say("Helper A.I.")
    while True:
        print("Listening...")
        query = takeCommand()
        # todo: Add more sites
        sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"],
                 ["google", "https://www.google.com"],["codeforces", "https://codeforces.com/"] ]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])
        # todo: Add a feature to play a specific song
        if "play music" in query:
            musicPath = "let-it-go-12279.mp3"
            import playsound
            playsound.playsound(musicPath)

        elif "the time" in query:
            hour = datetime.datetime.now().strftime("%H")
            min = datetime.datetime.now().strftime("%M")
            say(f"Sir time is {hour} bajke {min} minutes")

        elif "open".lower() in query.lower():
            app_name = query.lower().replace("open ", "")
            open(app_name, match_closest=True)  # App will be open be it matches little bit too

        elif "close".lower() in query.lower():
            app_name = query.lower().replace("close ", "").strip()
            close(app_name, match_closest=True, output=False)  # App will be close be it matches little bit too (Without printing context (like CLOSING <app_name>))

        elif "Using artificial intelligence".lower() in query.lower():
            ai(prompt=query)

        elif "Helper A.I. Quit".lower() in query.lower():
            exit()

        elif "reset chat".lower() in query.lower():
            chatStr = ""

        else:
            print("Chatting...")
            chat(query)
