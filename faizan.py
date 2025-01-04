import pyttsx3
import speech_recognition as sr
import datetime
import os
import webbrowser
import wikipedia
import sys
import random
import psutil

# Initialize the text-to-speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# Function to handle text-to-speech
def speak(audio):
    """Function to handle text-to-speech conversion"""
    engine.say(audio)
    print(audio)
    engine.runAndWait()

# Function to take voice command input
def take_command():
    """Function to take voice commands from the user"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 1
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            print("Recognizing...")
            query = recognizer.recognize_google(audio, language='en-in')
            print(f"User said: {query}")
       # except sr.UnknownValueError:
            #speak("I did not understand. Please say that again.")
           # return "none"
        except sr.RequestError:
            speak("Please check your internet connection.")
            return "none"
        except Exception as e:
            speak(f"An error occurred: {e}")
            return "none"
        return query.lower()

# Function to greet the user based on the time
def wish():
    """Function to greet the user based on the time of day"""
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Assalamu Aalaikum! Good morning!")
    elif 12 <= hour < 18:
        speak("Assalamu Aalaikum! Good afternoon!")
    else:
        speak("Assalamu Aalaikum! Good evening!")
    speak("I am Faaizaan, your personal assistant. How can I assist you today?")

# Function to open applications or websites
def open_application_or_website(command, name, path_or_url):
    """Function to handle opening applications or websites"""
    if os.path.exists(path_or_url):
        os.startfile(path_or_url)
        speak(f"Opening {name}.")
    else:
        webbrowser.open(path_or_url)
        speak(f"Opening {name} in your browser.")

# Function to close applications
def close_application(process_name):
    """Function to close an application by its process name"""
    for process in psutil.process_iter():
        try:
            if process_name.lower() in process.name().lower():
                process.terminate()
                speak(f"Closed {process_name}.")
                return
        except Exception as e:
            continue
    speak(f"Could not find {process_name} running.")

# Function to handle Wikipedia searches
def search_wikipedia(query):
    """Search Wikipedia and return results"""
    speak("Searching Wikipedia...")
    query = query.replace("wikipedia", "")
    try:
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia:")
        speak(results)
    except Exception as e:
        speak("Sorry, I couldn't fetch results from Wikipedia.")

# Function to play a song from a predefined list
def play_song():
    """Play a random song from a predefined list"""
    songs = [
        "C:\\Music\\song1.mp3",
        "C:\\Music\\song2.mp3",
        "C:\\Music\\song3.mp3"
    ]
    if songs:
        song = random.choice(songs)
        os.startfile(song)
        speak("Playing a random song for you.")
    else:
        speak("Sorry, I couldn't find any songs to play.")

# Function to tell the current time
def tell_time():
    """Tell the current time"""
    time = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The time is {time}.")

# Function to create a note
def take_note():
    """Take a quick note and save it to a file"""
    speak("What should I write in the note?")
    note = take_command()
    if note != "none":
        with open("notes.txt", "a") as file:
            file.write(f"{datetime.datetime.now()} - {note}\n")
        speak("I have saved the note.")
    else:
        speak("I couldn't save the note. Please try again.")

# Function to read all saved notes
def read_notes():
    """Read all saved notes from the file"""
    try:
        with open("notes.txt", "r") as file:
            notes = file.readlines()
            if notes:
                speak("Here are your saved notes:")
                for note in notes:
                    speak(note.strip())
            else:
                speak("You don't have any saved notes.")
    except FileNotFoundError:
        speak("I couldn't find any saved notes.")

# Main execution block
if __name__ == "__main__":
    wish()

    while True:
        query = take_command()

        # Logic for executing various commands
        if "open notepad" in query:
            open_application_or_website(query, "Notepad", "C:\\Windows\\notepad.exe")

        elif "close notepad" in query:
            close_application("notepad")

        elif "open vs code" in query:
            open_application_or_website(query, "Visual Studio Code", "C:\\Users\\YourUsername\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe")

        elif "close vs code" in query:
            close_application("code")

        elif "open command prompt" in query:
            os.system("start cmd")
            speak("Opening Command Prompt.")

        elif "close command prompt" in query:
            close_application("cmd")

        elif "wikipedia" in query:
            search_wikipedia(query)

        elif "open youtube" in query:
            open_application_or_website(query, "YouTube", "https://www.youtube.com")

        elif "open facebook" in query:
            open_application_or_website(query, "Facebook", "https://www.facebook.com")

        elif "open linkedin" in query:
            open_application_or_website(query, "LinkedIn", "https://www.linkedin.com")

        elif "open github" in query:
            open_application_or_website(query, "GitHub", "https://www.github.com")

        elif "open wix studio" in query:
            open_application_or_website(query, "Wix Studio", "https://www.wix.com/studio")

        elif "open google" in query:
            speak("What should I search on Google?")
            search_query = take_command()
            webbrowser.open(f"https://www.google.com/search?q={search_query}")
            speak(f"Here are the search results for {search_query}.")

        elif "play a song" in query:
            play_song()

        elif "what's the time" in query:
            tell_time()

        elif "take a note" in query or "write a note" in query:
            take_note()

        elif "read notes" in query or "show my notes" in query:
            read_notes()

        elif "nothing" in query or "exit" in query:
            speak("Thank you for using me. Have a great day!")
            sys.exit()

        else:
            speak("I didn't understand that. Please try again or ask for something else.")
