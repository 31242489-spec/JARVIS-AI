import pyttsx3

print("Starting voice test...")

engine = pyttsx3.init()

voices = engine.getProperty("voices")

print("Voices found:", len(voices))

for i, voice in enumerate(voices):
    print(i, voice.name)

engine.setProperty("rate", 165)
engine.setProperty("volume", 1.0)

if voices:
    engine.setProperty("voice", voices[0].id)

print("Speaking now...")

engine.say("Hello. I am Jarvis. Voice test successful.")
engine.runAndWait()

print("Finished.")