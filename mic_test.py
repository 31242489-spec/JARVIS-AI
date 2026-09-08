import speech_recognition as sr

print("Testing microphones...\n")

for i, name in enumerate(sr.Microphone.list_microphone_names()):

    if "Microphone" in name and "Stereo Mix" not in name:

        print(f"\nTesting microphone {i}: {name}")

        try:

            recognizer = sr.Recognizer()

            with sr.Microphone(device_index=i) as source:

                print("Speak something for 3 seconds...")

                audio = recognizer.record(
                    source,
                    duration=3
                )

                print("Audio captured.")

                try:
                    text = recognizer.recognize_google(audio)
                    print("SUCCESS:", text)

                except sr.UnknownValueError:
                    print("No speech detected.")

                except sr.RequestError as e:
                    print("Google recognition error:", e)

        except Exception as e:

            print("MIC ERROR:", e)