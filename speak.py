import pyttsx3

print("Starting TTS test...")

engine = pyttsx3.init()

engine.setProperty("rate", 165)
engine.setProperty("volume", 1.0)

voices = engine.getProperty("voices")

print("Number of voices:", len(voices))

for i, voice in enumerate(voices):
    print(i, voice.name)

if voices:
    engine.setProperty("voice", voices[0].id)

text = "Hello Deep. I am Jarvis. Can you hear me?"

print("ABOUT TO SPEAK:", text)

engine.say(text)
engine.runAndWait()

print("SPEECH FINISHED")

engine.stop()