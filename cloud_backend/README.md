# JARVIS cloud backend

This is a text-only Flask API for demonstrating cloud deployment. The desktop
JARVIS app continues to own the microphone, text-to-speech, Ollama, browser,
and Windows-control features.

## Run locally

From this folder, install the dependencies and run `python app.py`. Then open
`http://127.0.0.1:5000/health` in a browser. A successful response contains
`"status":"ok"`.

## Deploy to Render

1. Put the project in a GitHub repository, keeping the root-level `render.yaml`
   file and this `cloud_backend` folder.
2. In Render, select **New > Blueprint**, connect the GitHub repository, then
   deploy it. The configuration sets `cloud_backend` as the service root.
3. Copy the public `https://...` URL after deployment finishes.

The desktop client will be connected only after the local API test succeeds.
