"""
Features of voice assistant:
1. can search for things on google
2. can open apps on your device
3. can open websites like whatsapp, instagram, outlook and gmail
4. can close apps on your device
5. can provide information you ask for
6. can set reminders
"""

import speech_recognition as sr
import pyttsx3
import webbrowser
import AppOpener
import json

# configuration of google gemini

import google.generativeai as generativeai

generativeai.configure(api_key="AIzaSyAzsqBT9wCN03wqE3T3FtbfI11Pe1W71H0")

model = generativeai.GenerativeModel("gemini-pro")

conversation = model.start_chat(history=[])

r = sr.Recognizer()

Reminders = []

# remove * from the answers given by gemini


def removeUnwanted(string):
    while "*" in string:
        string = string.replace("*", "")

    return string


# makes computer speak words


def SpeakText(command):
    engine = pyttsx3.init()
    engine.say(command)
    print(command)
    engine.runAndWait()


# open google search


def query(q):
    webbrowser.open(f"https://www.google.com/search?q={q}")


# open website


def opensite(site):
    webbrowser.open(site)

SpeakText("Hello Boss, how may I help you?")


while True:

    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.2)

            audio = r.listen(source, timeout=2)

            try:
                myText = r.recognize_google(audio)
                myText = myText.lower().strip()

                if myText == "hello":
                    SpeakText("Hello Boss, how may I help you?")
                    continue

                elif "search " in myText:
                    q = myText.replace("search ", "")
                    try:
                        q = q.replace("for ", "")
                    except:
                        pass

                    query(str(q))

                    SpeakText(f"Searching for {q}")
                    continue

                elif "thank you" in myText:
                    SpeakText("You're welcome.")
                    continue

                elif myText == "exit" or "bye" in myText:
                    SpeakText("Bye")
                    break

                elif "set a reminder" in myText:
                    myText = myText.replace("set a reminder", "")
                    myText = myText.strip()

                    if len(myText) > 0:
                        Reminders.append(myText)

                        with open("./reminders.json", "w") as at:
                            json.dump(Reminders, at)

                    else:
                        recognizer = sr.Recognizer()
                        SpeakText("Say your reminder")
                        with sr.Microphone() as source2:
                            audio2 = recognizer.listen(source2)
                            reminder = r.recognize_google(audio2)
                            Reminders.append(reminder)

                        with open("./reminders.json", "w") as at:
                            json.dump(Reminders, at)

                    SpeakText("Reminder has been added.")
                    print("")
                    continue

                elif "open" in myText:
                    myText = myText.replace("open", "")
                    myText = myText.strip()
                    # open app

                    if "my reminder" in myText:
                        with open("./reminders.json", "r") as at:
                            reminders = json.load(at)
                        if len(reminders) > 0:
                            SpeakText("Your reminders are: ")
                            for i in reminders:
                                SpeakText(i)

                        else:
                            SpeakText("You have no reminders")

                    # open the websites
                    elif "gmail" in myText:
                        SpeakText("Opening gmail.")
                        opensite("https://mail.google.com/mail/u/0/#inbox")
                        continue

                    elif "outlook" in myText:
                        SpeakText("Opening outlook.")
                        opensite("https://outlook.office.com/mail/")
                        continue

                    elif "whatsapp" in myText:
                        SpeakText("Opening Whatsapp")
                        opensite("https://web.whatsapp.com")
                        continue

                    elif "insta" in myText:
                        SpeakText("Opening instagram.")
                        opensite("https://www.instagram.com")
                        continue

                    else:
                        try:
                            AppOpener.open(myText)
                            SpeakText(f"Opening {myText}")
                        except:
                            SpeakText("Sorry I am not able to execute your command.")

                elif "close" in myText:
                    myText = myText.replace("close", "")
                    myText = myText.strip()

                    try:
                        AppOpener.close(myText)
                        SpeakText(f"Closing {myText}")

                    except:
                        SpeakText("Sorry I am not able to execute your command.")

                else:
                    response = conversation.send_message(myText)
                    response.resolve()
                    SpeakText(removeUnwanted(response.text))

            except:
                SpeakText("Sorry I couldn't recognise your command.")

    except:
        pass

