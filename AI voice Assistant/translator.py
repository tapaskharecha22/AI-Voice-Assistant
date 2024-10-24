from googletrans import Translator
import pyttsx3
import googletrans

engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 170)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def translategl(query):
    speak("Sure, sir.")
    print(googletrans.LANGUAGES)
    translator = Translator()
    speak("Choose the language into which you want to translate.")
    b = input("To_Lang: ")

    try:
        text_to_translate = translator.translate(query, dest=b, src="auto")
        translated_text = text_to_translate.text
        print(f"Translated Text: {translated_text}")
        speak(translated_text)
    except Exception as e:
        print(f"An error occurred: {e}")
        speak("Sorry, I couldn't translate that.")
