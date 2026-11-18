
import pyttsx3

try:
    engine = pyttsx3.init("sapi5")

    engine.setProperty("rate", 150)
    engine.setProperty("volume", 1.0)

    voices = engine.getProperty("voices")
    print("Available voices:", len(voices))

    engine.say("Hello! I am JARVIS. My voice system is working.")
    engine.runAndWait()

    print("Speech test completed.")

except Exception as e:
    print("Voice error:", e)
