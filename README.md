## Friday - Python Voice Assistant (CLI)

A simple voice assistant written in Python.

Previously, I built a more responsive version using OpenAI, but decided to stick to this lightweight approach for now, as the OpenAI version hit usage limits.

---

## Features

- Voice activation with wake word: “Friday”
- Weather info via OpenWeatherMap API
- Time lookup in cities like Tokyo, London, Delhi, etc.
- Text-to-speech responses using `pyttsx3`
- Opens websites like Google, YouTube, Facebook, LinkedIn, etc., through voice

---

## Tech Stack

- Python 3.11+
- `speech_recognition`
- `pyttsx3`
- `pyaudio`
- `requests`
- `pytz`
- `webbrowser` (built-in)

---

## API Key Setup

Create a file called `weather_key.py` in the root of the project, and add:

```python
API_KEY = "your_openweather_api_key_here"
