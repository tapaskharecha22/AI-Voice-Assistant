import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import requests
import json
import random
from google.generativeai import generate_text
from google.cloud import storage
from googleapiclient.discovery import build
import google.auth
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials
import google.generativeai as genai
import operator
import pyautogui
import speedtest
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from contextlib import closing
import pyjokes


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[1].id)
engine.setProperty('voice', voices[1].id)

# google gemini api key
os.environ["GOOGLE_API_KEY"] = "YOUR_API_KEY"

load_dotenv()

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >=0 and hour < 12:
        speak("Good Morning !")

    elif hour >= 12 and hour < 18:
        speak("Good Afternoon !")

    else:
        speak("Good Evening !")

    speak("i am Jarvis, how may i help you ")

def takeCommand():

    #It takes micro phone input from the user and returns the output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        # print(e)
        print("Say that again please..")
        return "none"
    return query

    try:
        text = r.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Could not understand audio")

        return "I didn't get that"
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return "Something went wrong"

def ai(query):
    genai.configure(api_key=os.getenv("YOUR_API_KEY"))
    generation_config = {
        "temperature": 0.9,
        "top_p": 1, "top_k": 1,
        "max_output_tokens": 2048,
        "response_mime_type": "text/plain"
    }
    model = genai.GenerativeModel("gemini-1.5-flash", generation_config=generation_config)
    response = model.generate_content(query)
    print(response.text)
    speak("here is the result you want")

def alarm(query):
    timehere = open("Alarmtext.txt","a")
    timehere.write(query)
    timehere.close()
    os.startfile("alarm.py")

if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()

        # Logic foe executing tasks based on query
        if 'wikipedia' in query:
            speak('searching wikipedia...')
            query = query.replace("wikipedia","")
            results = wikipedia.summary(query, sentences = 2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif "hello" in query:
            speak("Hello sir, how are you ?")
        elif "i am fine" in query:
            speak("that's great, sir")
        # elif "how are you" or "how r u " or "how are you doing" in query:
            # speak("Perfect, sir")
        elif "what are you doing" in query:
            speak("Answering your question, sir")
        elif "thank you" in query:
            speak("you are welcome, sir")

        elif 'open youtube' in query:
            webbrowser.open("youtube.com")
            speak("Here are the search results for " + query)

        elif "close youtube" in query:
            speak("closing youtube")
            pyautogui.hotkey('alt', 'f4')

        elif 'open google' in query:
            webbrowser.open("google.com")
            speak("Here are the search results for " + query)

        elif "close google" in query:
            speak("closing google")
            pyautogui.hotkey('alt', 'f4')

        elif 'open w3schools' in query:
            webbrowser.open("w3schools.com")
            speak("Here are the search results for " + query)

        elif "close w3schools" in query:
            speak("closing w3schools")
            pyautogui.hotkey('alt', 'f4')

        elif 'open microsoft edge' in query:
            webbrowser.open("microsoft.com")
            speak("Here are the search results for " + query)

        elif "close microsoft edge" in query:
            speak("closing microsoft edge")
            pyautogui.hotkey('alt', 'f4')

        elif 'open googlemeet' in query:
            webbrowser.open("meet.google.com")
            speak("Here are the search results for " + query)

        elif "close google meet" in query:
            speak("closing google meet")
            pyautogui.hotkey('alt', 'f4')

        elif 'open linkedin' in query:
            webbrowser.open("linkedin.com")
            speak("Here are the search result for " + query)

        elif "close linkedin" in query:
            speak("closing linkedin")
            pyautogui.hotkey('alt', 'f4')

        elif 'open python.org' in query:
            webbrowser.open("www.python.org")
            speak("here are the search result for " + query)

        elif "close python.org" in query:
            pyautogui.hotkey('alt', 'f4')

        elif "hello jarvis" in query:
            chat(query)

        elif 'play music' in query:
            music_dir = "ENTER_YOUR_PATH"  #enter your music dir path
            songs = os.listdir(music_dir)
            print(songs)
            speak("Here are the search result for " + query)
            os.startfile(os.path.join(music_dir, songs[2]))

        elif "pause music" in query:
            speak("pausing music")
            pyautogui.hotkey('ctrl', 'p')

        elif "start music" in query:
            speak("resuming music")
            pyautogui.hotkey('ctrl', 'p')

        elif "close music" in query:
            speak("closing music")
            pyautogui.hotkey('alt', 'f4')

        elif "translate" in query:
            from translator import translategl
            query = query.replace("jarvis", "")
            query = query.replace("translate", "")
            translategl(query)

        elif 'what time it is' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            print(strTime)
            speak(f"Sir, the time is {strTime}")

        elif "set an alarm" in query:
            print("input time example:- 10 and 10 and 10")
            speak("Set the time")
            a = input("Please tell the time :- ")
            alarm(a)
            speak("Done,sir")

        elif "internet speed" in query:
            wifi =  speedtest.Speedtest()
            download_net = wifi.download() / 1048576  # Megabyte = 1024*1024 Bytes
            upload_net = wifi.upload() / 1048576
            print(f"Wifi download speed is {download_net:.2f} Mbps")
            print(f"Wifi upload speed is {upload_net:.2f} Mbps")
            speak(f"Wifi download speed is {download_net:.2f} megabits per second")
            speak(f"Wifi upload speed is {upload_net:.2f} megabits per second")

        elif "take screenshot" in query:
             # pip install pyautogui
            im = pyautogui.screenshot()
            im.save("ss.jpg")

        elif "calculate" in query:
            from calculator import calculate
            from calculator import calculate
            query = query.replace("calculate", "")
            query = query.replace("jarvis", "")
            calculate(query)

        elif "remember that" in query:
            speak("What should i remember sir")
            data = takeCommand()
            speak("You asked me to remember that" + data)
            remember = open("data.txt", "w")
            remember.write(data)
            remember.close()

        elif "do you remember anything" in query:
            remember = open("data.txt", "r")
            speak("You asked me to remember that" + remember.read())

        elif 'open vs code' in query:
            path = "ENTER_YOUR_PATH"
            os.startfile(path)
            speak("Here are the search result for " + query)

        elif "close vs code" in query:
            speak("closing vs code")
            pyautogui.hotkey('alt', 'f4')

        elif 'open steam' in query:
            apppath = "ENTER_YOUR_PATH"
            os.startfile(apppath)
            speak("Here are the search result for " + query)

        elif "close steam" in query:
            speak("closing steam")
            pyautogui.hotkey('alt', 'f4')

        elif 'open pycharm' in query:
            codepath = "ENTER_YOUR_PATH"
            os.startfile(codepath)
            speak("Here are the search result for " + query)

        elif "close pycharm" in query:
            speak("closing pycharm")
            pyautogui.hotkey('alt', 'f4')

        elif 'open word' in query:
            wordpath = "ENTER_YOUR_PATH"
            os.startfile(wordpath)
            speak("Here are the search result for " + query)

        elif "close word" in query:
            speak("closing word")
            pyautogui.hotkey('alt', 'f4')

        elif 'open excel' in query:
            excelpath = "ENTER_YOUR_PATH"
            os.startfile(excelpath)
            speak("Here are the search result for " + query)

        elif "close excel" in query:
            speak("closing excel")
            pyautogui.hotkey('alt', 'f4')

        elif 'open powerpoint' in query:
            pppath = "ENTER_YOUR_PATH"
            os.startfile(pppath)
            speak("Here are the search result for " + query)

        elif "close powerpoint" in query:
            speak("closing powerpoint")
            pyautogui.hotkey('alt', 'f4')

        elif 'open onenote' in query:
            notepath = "ENTER_YOUR_PATH"
            os.startfile(notepath)
            speak("Here are the search result for " + query)

        elif "close onenote" in query:
            speak("closing onenote")
            pyautogui.hotkey('alt', 'f4')

        elif 'open outlook' in query:
            outpath = "ENTER_YOUR_PATH"
            os.startfile(outpath)
            speak("Here are the search result for " + query)

        elif "close outlook" in query:
            speak("closing outlook")
            pyautogui.hotkey('alt', 'f4')

        elif 'open publisher' in query:
            pubpath = "ENTER_YOUR_PATH"
            os.startfile(pubpath)
            speak("Here are the search result for " + query)

        elif "close publisher" in query:
            speak("closing publisher")
            pyautogui.hotkey('alt', 'f4')

        elif 'open notepad2' in query:
            nopath = "ENTER_YOUR_PATH"
            os.startfile(nopath)
            speak("Here are the search result for " + query)

        elif "close notepad2" in query:
            speak("closing notepad")
            pyautogui.hotkey('alt', 'f4')

        elif"volume up" in query:
            pyautogui.press("volumeup")
            speak("volume up")

        elif"volume down" in query:
            pyautogui.press ("volumedown")
            speak("volume down")

        elif"volume mute" in query:
            pyautogui.press ("volumemute")
            speak("volume mute")

        elif"pause video" in query:
            pyautogui.press ("space")
            speak("video paused")

        elif "play video" in query:
            pyautogui.press("space")
            speak("video played")

        elif "tell me a joke" in query:
            my_joke = pyjokes.get_joke(language="en", category="all")
            print(my_joke)
            speak(my_joke)

        elif "weather report" in query:
            search = "weather in ahmedabad"
            url = f"https://www.google.com/search?q={search}"
            r = requests.get(url)
            data = BeautifulSoup(r.text, "html.parser")
            temp = data.find("div", class_="BNeawe").text
            speak(f"current{search} is {temp}")

        elif 'switch the window' in query:
            speak("switching the window")
            pyautogui.keyDown("alt")
            pyautogui.press("tab")
            pyautogui.keyUp("alt")

        elif 'open command prompt' in query:
            os.system("start cmd")

        elif "close command prompt" in query:
            pyautogui.hotkey('alt', 'f4')

        elif 'what is current news' in query:
            from Newsread import latestnews
            latestnews()

        elif 'using artificial intelligence' in query:
                response = ai(query)
                speak(response)

        elif "shutdown the system" in query:
            speak("are you want to shutdown")
            shutdown = input("Do you want ot shutdown your system ? (yes/no)")
            if shutdown == "yes":
                os.system("shutdown /s /t 1")

            elif shutdown == "no":
                break

        elif "restart the system" in query:
            speak("are you want to restart")
            restart = input("Do you want to restart your system ? (yes/no)")
            if restart == "yes":
                os.system("shutdown /r /t 1")

            elif restart == "no":
                break

        elif 'exit' in query:
            speak("thanks for using me")
            break

