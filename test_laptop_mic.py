import speech_recognition as sr

recognizer = sr.Recognizer()

# Test Realtek microphone #1
MIC_INDEX = 1

print("Testing microphone:")
print(sr.Microphone.list_microphone_names()[MIC_INDEX])
print()
print("Speak something after 'Listening...'")
print()

try:
    with sr.Microphone(device_index=MIC_INDEX) as source:

        print("Adjusting for background noise...")
        recognizer.adjust_for_ambient_noise(source, duration=1)

        print("Listening...")
        audio = recognizer.listen(
            source,
            timeout=5,
            phrase_time_limit=5
        )

    print("Audio captured!")
    print("Recognizing...")

    text = recognizer.recognize_google(audio)

    print()
    print("YOU SAID:", text)

except sr.WaitTimeoutError:
    print("❌ No speech detected.")

except sr.UnknownValueError:
    print("❌ Audio was captured, but speech could not be understood.")

except sr.RequestError as e:
    print("❌ Google recognition error:", e)

except Exception as e:
    print("❌ MICROPHONE ERROR:", repr(e))