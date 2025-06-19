import speech_recognition as sr
import webbrowser
import pyttsx3
import time
import requests
from weather_key import API_KEY
from datetime import datetime
import pytz


recognizer = sr.Recognizer()
engine = pyttsx3.init()

""" RATE"""
rate = engine.getProperty('rate')   # getting details of current speaking rate
engine.setProperty('rate', 160)     # setting up new voice rate

"""VOLUME"""
volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
engine.setProperty('volume',1.0)    # setting up volume level  between 0 and 1

"""VOICE"""
voices = engine.getProperty('voices')       #getting details of current voice
#engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female


# Text-to-speech function
def speak(text):
    print("🗣️ ", text)
    engine.say(text)
    engine.runAndWait()

# Handle commands after wake word
def process_command(command):
    command = command.lower()

    if "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://www.google.com/")
    elif "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")
    elif "open facebook" in command:
        speak("Opening Facebook")
        webbrowser.open("https://facebook.com")
    elif "open instagram" in command:
        speak("Opening Instagram")
        webbrowser.open("https://instagram.com")
    elif "open profile" in command:
        speak("Opening your LinkedIn profile")
        webbrowser.open("https://www.linkedin.com/in/nastel-rodrigues-3aa91525a/?originalSubdomain=in")
        
    elif "time" in command:
        speak("Which city's time should I check?")
        city = listen_for_command()
        tz_map = {
            "new york": "America/New_York",
            "london": "Europe/London",
            "tokyo": "Asia/Tokyo",
            "delhi": "Asia/Kolkata",
            "mumbai": "Asia/Kolkata",
            "sydney": "Australia/Sydney",
            "paris": "Europe/Paris",
            "dubai": "Asia/Dubai",
            "toronto": "America/Toronto"
        }
        city_lower = city.lower()
        if city_lower in tz_map:
            time_info = get_time_in_location(tz_map[city_lower])
            speak(time_info)
        else:
            speak("Sorry, I don't know the timezone for that city.")
    elif "weather" in command:
        speak("Which city's weather should I check?")
        city = listen_for_command()
        if city:
            weather_info = get_weather(city)
            speak(weather_info)
    else:
        speak("Sorry, I didn't understand that command.")


#Time
def get_time_in_location(location_name):
    try:
        timezone = pytz.timezone(location_name)
        time_in_location = datetime.now(timezone).strftime('%I:%M %p')
        return f"The current time in {location_name.split('/')[-1].replace('_', ' ')} is {time_in_location}."
    except Exception as e:
        return "Sorry, I couldn't find the time for that location."


#Weather
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()
        calls_per_minute = response.headers.get("X-RateLimit-Limit-minute")
        calls_remaining = response.headers.get("X-RateLimit-Remaining-minute")

        if data["cod"] != 200:
            return f"City '{city}' not found."
        temp = data["main"]["temp"]
        weather_desc = data["weather"][0]["description"]
        weather_info = f"The weather in {city} is {weather_desc} with a temperature of {temp}°C."

        if calls_per_minute and calls_remaining:
            quota_info = f" You have used {int(calls_per_minute) - int(calls_remaining)} of {calls_per_minute} calls this minute."
            weather_info += quota_info
        
        else:
            weather_info += " (Quota info unavailable — may depend on your plan.)"
        return weather_info

    except Exception as e:
        return f"Could not fetch weather data: {e}"


# Main assistant logic
def listen_for_friday():
    with sr.Microphone() as source:
        print("🔊 Listening for wake word....")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
            trigger = recognizer.recognize_google(audio)
            if trigger.lower() == "friday":
                speak("Friday Active....")
                return True
        except sr.WaitTimeoutError:
            pass
        except sr.UnknownValueError:
            pass
        except sr.RequestError as e:
            speak(f"API Error: {e}")
    return False


#Listening for Command
def listen_for_command():
    with sr.Microphone() as source:
        print("🎤 Listening for command....")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            command = recognizer.recognize_google(audio)
            print("🧠 You said:", command)
            return command
        except sr.WaitTimeoutError:
            speak("Listening timed out.")
        except sr.UnknownValueError:
            speak("Could not understand your command.")
        except sr.RequestError as e:
            speak(f"API Error: {e}")
    return ""


# Entry point
if __name__ == "__main__":
    speak("Initializing Friday....")
    while True:
        if listen_for_friday():
            break
        time.sleep(2)
    speak("I'm listening....")
    while True:
        command = listen_for_command()
        if command:
            if any(exit_word in command.lower() for exit_word in ["exit", "goodbye", "shutdown", "stop"]):
                speak("Goodbye. Shutting down.")
                break
            else:
                process_command(command)
        time.sleep(1)

