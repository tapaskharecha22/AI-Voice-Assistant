import pyttsx3
import requests
import json

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[1].id)
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def latestnews():
    api_dict = {"business":"https://newsapi.org/v2/top-headlines?country=in&category=business&apiKey= ENTER_YOUR_API_KEY",
                "entertainment":"https://newsapi.org/v2/top-headlines?country=in&category=entertainment&apiKey=ENTER_YOUR_API_KEY",
                "medical":"https://newsapi.org/v2/top-headlines?country=in&category=health&apiKey=ENTER_YOUR_API_KEY",
                "science":"https://newsapi.org/v2/top-headlines?country=in&category=science&apiKey=ENTER_YOUR_API_KEY",
                "sports":"https://newsapi.org/v2/top-headlines?country=in&category=sports&apiKey=ENTER_YOUR_API_KEY",
                "technology":"https://newsapi.org/v2/top-headlines?country=in&category=technology&apiKey=ENTER_YOUR_API_KEY"
               }
    content = None
    url = None
    speak("which feild news do you want, [business] , [medical] , [sports] , [technology] , [entertainment] , [science]")
    field = input("typee feild news that you want: ")
    for key ,value in api_dict.items():
        if key.lower() in field.lower():
            url = value
            print(url)
            print("url was not found")
            break
        else:
            url = True
    if url is True:
         print("url not found")

    news = requests.get(url).text
    news = json.loads(news)
    speak("here is the news you want")

    arts = news["articles"]
    for articles in arts:
        article = articles["title"]
        print(article)
        speak(article)
        news_url = articles["url"]
        print(f"for more information visit: {news_url}")

        a = input("[press 1 to continue] and [press 2 to stop]")
        if str(a) == "1":
            pass
        elif str(a) == "2":
            break

    speak("that's all")
