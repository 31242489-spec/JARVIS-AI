import speech_recognition as sr
import pyttsx3
import webbrowser
import urllib.parse
import urllib.request
import json
import datetime
import subprocess
import os


# =========================================================
# JARVIS VOICE ENGINE
# =========================================================



def speak(text):
    print("JARVIS:", text)

    try:
        engine = pyttsx3.init()

        engine.setProperty("rate", 165)
        engine.setProperty("volume", 1.0)

        voices = engine.getProperty("voices")

        if voices:
            engine.setProperty("voice", voices[0].id)

        print("SPEAKING:", text)

        engine.say(str(text))
        engine.runAndWait()

        print("SPEECH FINISHED")

        engine.stop()

    except Exception as e:
        print("VOICE ERROR:", repr(e))

# =========================================================
# SPEECH RECOGNITION
# =========================================================

recognizer = sr.Recognizer()

recognizer.energy_threshold = 300
recognizer.dynamic_energy_threshold = True
recognizer.pause_threshold = 0.8
recognizer.phrase_threshold = 0.3
recognizer.non_speaking_duration = 0.5


def find_microphone():
    """
    Automatically find a working microphone.

    Priority:
    1. ZEB-THUNDER NEO if actually available
    2. Laptop Realtek microphone #1
    3. Other Realtek microphones
    """

    print("\nSearching for microphone...")

    microphones = sr.Microphone.list_microphone_names()

    # -----------------------------------------------------
    # Try ZEB headset first
    # -----------------------------------------------------

    for index, name in enumerate(microphones):

        if "ZEB-THUNDER NEO" in name.upper():

            print(f"Trying ZEB microphone #{index}: {name}")

            try:
                with sr.Microphone(device_index=index) as source:
                    print("ZEB microphone is available.")
                    return index

            except Exception as e:
                print("ZEB unavailable:", e)

    # -----------------------------------------------------
    # Prefer laptop Realtek microphone
    # -----------------------------------------------------

    for index, name in enumerate(microphones):

        if name.strip() == "Microphone (Realtek(R) Audio)":

            print(f"Using laptop microphone #{index}: {name}")

            try:
                with sr.Microphone(device_index=index) as source:
                    return index

            except Exception as e:
                print("Laptop microphone failed:", e)

    # -----------------------------------------------------
    # Try any Realtek microphone
    # -----------------------------------------------------

    for index, name in enumerate(microphones):

        if "microphone (realtek" in name.lower():

            print(f"Trying microphone #{index}: {name}")

            try:
                with sr.Microphone(device_index=index) as source:
                    return index

            except Exception:
                pass

    print("No working microphone found.")

    return None


MIC_INDEX = find_microphone()

if MIC_INDEX is None:
    print("ERROR: No microphone available.")
    exit()


# =========================================================
# LISTEN
# =========================================================

def listen():

    with sr.Microphone(device_index=MIC_INDEX) as source:

        print("\nListening...")

        try:

            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=10
            )

        except sr.WaitTimeoutError:

            print("No speech detected.")
            return ""

    try:

        print("Recognizing...")

        text = recognizer.recognize_google(audio)

        print("YOU:", text)

        return text.lower()

    except sr.UnknownValueError:

        print("Could not understand audio.")
        return ""

    except sr.RequestError as e:

        print("Speech recognition error:", e)
        return ""


# =========================================================
# COMPUTER TOOLS
# =========================================================

def open_website(url):

    webbrowser.open(url)

    return f"Opening {url}"


def search_google(query):

    encoded_query = urllib.parse.quote(query)

    url = f"https://www.google.com/search?q={encoded_query}"

    webbrowser.open(url)

    return f"Searching Google for {query}"


def get_time():

    now = datetime.datetime.now()

    return now.strftime("The time is %I:%M %p")


def get_date():

    today = datetime.datetime.now()

    return today.strftime(
        "Today is %A, %B %d, %Y"
    )


def open_calculator():

    try:

        subprocess.Popen("calc.exe")

        return "Opening Calculator."

    except Exception as e:

        return f"Could not open Calculator: {e}"


def open_notepad():

    try:

        subprocess.Popen("notepad.exe")

        return "Opening Notepad."

    except Exception as e:

        return f"Could not open Notepad: {e}"


def open_chrome():

    chrome_paths = [

        r"C:\Program Files\Google\Chrome\Application\chrome.exe",

        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",

        os.path.expandvars(
            r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"
        )
    ]

    for path in chrome_paths:

        if os.path.exists(path):

            subprocess.Popen([path])

            return "Opening Google Chrome."

    webbrowser.open("https://www.google.com")

    return "Chrome was not found, so I opened your default browser."


# =========================================================
# TOOL DEFINITIONS
# =========================================================

available_functions = {

    "open_website": open_website,

    "search_google": search_google,

    "get_time": get_time,

    "get_date": get_date,

    "open_calculator": open_calculator,

    "open_notepad": open_notepad,

    "open_chrome": open_chrome
}


tools = [

    {
        "type": "function",
        "function": {

            "name": "open_website",

            "description":
                "Open a website in the user's default browser.",

            "parameters": {

                "type": "object",

                "properties": {

                    "url": {
                        "type": "string",
                        "description":
                            "The complete website URL."
                    }

                },

                "required": ["url"]
            }
        }
    },

    {
        "type": "function",
        "function": {

            "name": "search_google",

            "description":
                "Search Google for something.",

            "parameters": {

                "type": "object",

                "properties": {

                    "query": {
                        "type": "string",
                        "description":
                            "The search query."
                    }

                },

                "required": ["query"]
            }
        }
    },

    {
        "type": "function",
        "function": {

            "name": "get_time",

            "description":
                "Get the current time.",

            "parameters": {

                "type": "object",

                "properties": {}
            }
        }
    },

    {
        "type": "function",
        "function": {

            "name": "get_date",

            "description":
                "Get today's date.",

            "parameters": {

                "type": "object",

                "properties": {}
            }
        }
    },

    {
        "type": "function",
        "function": {

            "name": "open_calculator",

            "description":
                "Open the Windows Calculator application.",

            "parameters": {

                "type": "object",

                "properties": {}
            }
        }
    },

    {
        "type": "function",
        "function": {

            "name": "open_notepad",

            "description":
                "Open Windows Notepad.",

            "parameters": {

                "type": "object",

                "properties": {}
            }
        }
    },

    {
        "type": "function",
        "function": {

            "name": "open_chrome",

            "description":
                "Open Google Chrome.",

            "parameters": {

                "type": "object",

                "properties": {}
            }
        }
    }

]


# =========================================================
# OLLAMA CONNECTION
# =========================================================

OLLAMA_URL = "http://127.0.0.1:11434/api/chat"

MODEL = "gemma4:latest"
CLOUD_URL = "https://jarvis-cloud-backend-inzd.onrender.com/api/chat"

def ollama_chat(messages, use_tools=True):

    """
    Send a chat request directly to Ollama.

    This avoids the Python ollama.chat() issue
    that was causing JARVIS to get stuck.
    """

    data = {

        "model": MODEL,

        "messages": messages,

        "stream": False
    }

    if use_tools:

        data["tools"] = tools

    request = urllib.request.Request(

        OLLAMA_URL,

        data=json.dumps(data).encode("utf-8"),

        headers={
            "Content-Type": "application/json"
        }
    )

    try:

        response = urllib.request.urlopen(
            request,
            timeout=120
        )

        result = json.loads(
            response.read().decode("utf-8")
        )

        return result

    except Exception as e:

        print("OLLAMA ERROR:", e)

        return None
def cloud_chat(message):

    data = {
        "message": message
    }

    request = urllib.request.Request(
        CLOUD_URL,
        data=json.dumps(data).encode("utf-8"),
        headers={
            "Content-Type": "application/json"
        }
    )

    try:

        response = urllib.request.urlopen(
            request,
            timeout=30
        )

        result = json.loads(
            response.read().decode("utf-8")
        )

        return result.get(
            "reply",
            "No response from cloud."
        )

    except Exception as e:

        print("CLOUD ERROR:", e)

        return None

# =========================================================
# ASK JARVIS
# =========================================================

def ask_jarvis(command):

    messages = [

        {
            "role": "system",

            "content":
            """
You are JARVIS, a helpful desktop AI assistant.

You are running locally on the user's Windows computer.

Be concise and natural when answering.

You can control the computer using the available tools.

Use tools when the user asks you to:
- open websites
- search Google
- get the time
- get the date
- open Calculator
- open Notepad
- open Chrome

For normal conversation, answer naturally without using tools.

Do not explain tool calls to the user.

Keep responses short because your responses will be spoken aloud.
"""
        },

        {
            "role": "user",

            "content": command
        }

    ]

    print("Thinking...")

    # -----------------------------------------------------
    # First request
    # -----------------------------------------------------

    result = ollama_chat(
        messages,
        use_tools=True
    )

    if result is None:

        return "I'm having trouble connecting to my AI system."

    message = result.get("message", {})

    # -----------------------------------------------------
    # Check whether Gemma requested a tool
    # -----------------------------------------------------

    tool_calls = message.get("tool_calls", [])

    if tool_calls:

        # Add assistant's tool request
        messages.append(message)

        for tool_call in tool_calls:

            function = tool_call.get("function", {})

            function_name = function.get("name")

            arguments = function.get(
                "arguments",
                {}
            )

            print(
                f"Tool requested: {function_name}"
            )

            print(
                f"Arguments: {arguments}"
            )

            # ---------------------------------------------
            # Execute tool
            # ---------------------------------------------

            if function_name in available_functions:

                try:

                    # Ollama may return arguments as JSON string
                    if isinstance(arguments, str):

                        arguments = json.loads(arguments)

                    function_result = available_functions[
                        function_name
                    ](**arguments)

                except Exception as e:

                    function_result = (
                        f"Tool error: {e}"
                    )

            else:

                function_result = (
                    f"Unknown tool: {function_name}"
                )

            print(
                "Tool result:",
                function_result
            )

            # ---------------------------------------------
            # Send result back to Gemma
            # ---------------------------------------------

            messages.append({

                "role": "tool",

                "content": str(function_result),

                "name": function_name

            })

        # -------------------------------------------------
        # Ask Gemma for final natural response
        # -------------------------------------------------

        print("Getting final response...")

        final_result = ollama_chat(
            messages,
            use_tools=False
        )

        if final_result is None:

            return "The command was completed."

        final_message = final_result.get(
            "message",
            {}
        )

        return final_message.get(
            "content",
            "Done."
        )

    # -----------------------------------------------------
    # Normal AI response
    # -----------------------------------------------------

    return message.get(
        "content",
        "I'm not sure how to respond to that."
    )


# =========================================================
# START JARVIS
# =========================================================

print("\n====================================")
print("        JARVIS AI ASSISTANT")
print("====================================")
print("Model:", MODEL)
print("Microphone:", MIC_INDEX)
print("Ollama:", OLLAMA_URL)
print("====================================\n")


speak("JARVIS is online. How may I assist you?")


# =========================================================
# MAIN LOOP
# =========================================================

while True:

    command = listen()

    if not command:

        continue

    # -----------------------------------------------------
    # Exit commands
    # -----------------------------------------------------

    exit_words = [

        "exit",

        "quit",

        "goodbye",

        "shutdown",

        "shut down",

        "go offline"

    ]

    if any(word in command for word in exit_words):

        speak("Going offline. Goodbye.")

        break

    # -----------------------------------------------------
    # AI
    # -----------------------------------------------------

    # -----------------------------------------------------
    # AI
    # -----------------------------------------------------

    if command.startswith("ask the cloud"):

        cloud_message = command.replace(
            "ask the cloud",
            "",
            1
        ).strip()

        if cloud_message:

            cloud_answer = cloud_chat(cloud_message)

            if cloud_answer is None:
                answer = "I could not connect to the cloud."

            else:
                answer = cloud_answer

        else:

            answer = "What would you like me to ask the cloud?"cd

    else:

        answer = ask_jarvis(command)

    print("JARVIS:", answer)

    speak(answer)
