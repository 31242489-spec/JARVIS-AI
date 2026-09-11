"""JARVIS Cloud Backend.

This service handles text-based AI requests.
Microphone access, speech, and Windows controls remain
on the user's local computer.
"""

from datetime import UTC, datetime
import os

from flask import Flask, jsonify, request
from google import genai


app = Flask(__name__)


# =========================================================
# HOME
# =========================================================

@app.get("/")
def index():
    return jsonify(
        service="JARVIS cloud backend",
        status="online",
        message="Send a POST request to /api/chat to test the cloud AI.",
    )


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health")
def health():
    return jsonify(
        status="ok",
        service="jarvis-cloud-backend",
        timestamp=datetime.now(UTC).isoformat(),
    )


# =========================================================
# CLOUD AI CHAT
# =========================================================

@app.post("/api/chat")
def chat():

    payload = request.get_json(silent=True)

    if not isinstance(payload, dict):
        return jsonify(
            error="Please send a JSON request body."
        ), 400

    message = payload.get("message")

    if not isinstance(message, str) or not message.strip():
        return jsonify(
            error="'message' must be a non-empty string."
        ), 400

    # -----------------------------------------------------
    # Get Gemini API key from environment
    # -----------------------------------------------------

    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        return jsonify(
            error="GEMINI_API_KEY is not configured."
        ), 500

    # -----------------------------------------------------
    # Ask Gemini
    # -----------------------------------------------------

    try:

        client = genai.Client(
            api_key=api_key
        )

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=message.strip(),
        )

        reply = response.text

        if not reply:
            reply = "I could not generate a response."

        return jsonify(
            reply=reply,
            provider="gemini",
        )


    except Exception as e:

        print(

            "GEMINI ERROR:",

            repr(e)

        )

        return jsonify(

            error="Cloud AI request failed.",

            details=repr(e)

        ), 500


# =========================================================
# START SERVER
# =========================================================

if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            "5000"
        )
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=True
    )