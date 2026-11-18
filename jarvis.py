
import vosk
import sounddevice as sd
import requests
import json
import subprocess
import base64
import time

# ==========================================
# CONFIGURATION
# ==========================================

MODEL_NAME = "qwen2.5:3b"
MODEL_PATH = "model"
OLLAMA_URL = "http://localhost:11434/api/chat"

SAMPLE_RATE = 16000
BLOCK_SIZE = 4000

# ==========================================
# LOAD VOSK MODEL
# ==========================================

print("JARVIS: Loading speech recognition model...")

vosk.SetLogLevel(-1)
speech_model = vosk.Model(MODEL_PATH)

print("JARVIS: Speech model loaded!")

# ==========================================
# HTTP SESSION
# ==========================================

session = requests.Session()

# ==========================================
# WINDOWS OFFLINE TEXT TO SPEECH
# ==========================================

def speak(text):

    print("JARVIS: Speaking...")

    try:

        encoded_text = base64.b64encode(
            text.encode("utf-8")
        ).decode("ascii")

        powershell_script = f"""
        Add-Type -AssemblyName System.Speech

        $bytes = [Convert]::FromBase64String('{encoded_text}')
        $text = [System.Text.Encoding]::UTF8.GetString($bytes)

        $speaker = New-Object System.Speech.Synthesis.SpeechSynthesizer
        $speaker.Rate = 0
        $speaker.Volume = 100
        $speaker.Speak($text)
        $speaker.Dispose()
        """

        result = subprocess.run(
            [
                "powershell.exe",
                "-NoProfile",
                "-NonInteractive",
                "-Command",
                powershell_script
            ],
            capture_output=True,
            text=True,
            timeout=120
        )

        if result.returncode != 0:
            print("VOICE ERROR:", result.stderr)
            return False

        return True

    except Exception as error:

        print("VOICE ERROR:", error)
        return False


# ==========================================
# MICROPHONE AND SPEECH RECOGNITION
# ==========================================

def listen_to_jarvis():

    recognizer = vosk.KaldiRecognizer(
        speech_model,
        SAMPLE_RATE
    )

    print("\nJARVIS: Listening... Speak naturally.")

    try:

        with sd.RawInputStream(
            samplerate=SAMPLE_RATE,
            blocksize=BLOCK_SIZE,
            dtype="int16",
            channels=1
        ) as stream:

            while True:

                audio_data, overflowed = stream.read(BLOCK_SIZE)

                if overflowed:
                    print("WARNING: Audio buffer overflow.")

                audio_bytes = bytes(audio_data)

                if recognizer.AcceptWaveform(audio_bytes):

                    result = json.loads(
                        recognizer.Result()
                    )

                    question = result.get("text", "").strip()

                    if question:
                        print("\nYOU:", question)
                        return question

    except KeyboardInterrupt:

        print("\nJARVIS: Listening interrupted.")
        return None

    except Exception as error:

        print("MICROPHONE ERROR:", error)
        return None


# ==========================================
# OLLAMA AI CONNECTION
# ==========================================


def ask_jarvis(question, speak_output=True):
    data = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are Rudra, a helpful personal AI assistant. "
                    "Speak naturally and give direct, concise answers."
                )
            },
            {
                "role": "user",
                "content": question
            }
        ],
        "stream": False,
        "keep_alive": "10m",
        "options": {
            "num_predict": 120,
            "temperature": 0.5
        }
    }

    try:
        print("\nRUDRA: Thinking...")

        response = session.post(
            OLLAMA_URL,
            json=data,
            timeout=180
        )
        response.raise_for_status()

        answer = response.json()["message"]["content"].strip()

        print("\nRUDRA:", answer)

        if answer and speak_output:
            speak(answer)

        return answer

    except requests.exceptions.ConnectionError:
        return "Ollama is not running."

    except requests.exceptions.Timeout:
        return "Qwen response timed out."

    except Exception as error:
        print("AI ERROR:", error)
        return f"AI Error: {error}"



# ==========================================
# MAIN PROGRAM
# ==========================================

def main():

    print("\n================================")
    print("       JARVIS AI SYSTEM")
    print("================================")

    print("Say exit to close JARVIS.")

    speak("Jarvis is online. How can I help you?")

    try:

        while True:

            question = listen_to_jarvis()

            if question is None:
                break

            if not question:
                continue

            if question.lower().strip() in [
                "exit",
                "quit",
                "stop"
            ]:

                print("\nJARVIS: Shutting down.")

                speak("Goodbye!")

                break

            ask_jarvis(question)

    except KeyboardInterrupt:

        print("\nJARVIS: Shutting down.")

    finally:

        session.close()

        print("JARVIS: Offline.")


# ==========================================
# START JARVIS
# ==========================================

if __name__ == "__main__":
    main()
