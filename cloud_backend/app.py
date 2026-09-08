"""Small cloud API used by the JARVIS desktop client.

This service deliberately handles text only. Microphone access, speech, and
Windows controls remain on the user's local computer.
"""

from datetime import UTC, datetime
import os

from flask import Flask, jsonify, request


app = Flask(__name__)


@app.get("/")
def index():
    return jsonify(
        service="JARVIS cloud backend",
        status="online",
        message="Send a POST request to /api/chat to test the cloud connection.",
    )


@app.get("/health")
def health():
    return jsonify(
        status="ok",
        service="jarvis-cloud-backend",
        timestamp=datetime.now(UTC).isoformat(),
    )


@app.post("/api/chat")
def chat():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify(error="Please send a JSON request body."), 400

    message = payload.get("message")
    if not isinstance(message, str) or not message.strip():
        return jsonify(error="'message' must be a non-empty string."), 400

    # This deterministic response is sufficient for the first deployment.
    # A hosted LLM can be added later through an environment key.
    reply = (
        "Your message reached the JARVIS cloud backend successfully: "
        f"{message.strip()}"
    )
    return jsonify(reply=reply, provider="cloud-backend")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=True)
