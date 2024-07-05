# Harmonix
Harmonix is a Google Chrome Extension which plays Spotify songs according to the sentiment of the user determined on the basis of recent browsing history. The extension uses Gemini Pro to infer the sentiment and javascript for the front-end interaction.

## Contents
1. `llm_interact_v3.py` is the backend of the system, which generates song recommendations using an LLM
2. `Alternative` folder contains other versions of the backend
3. `popup.html`
4. `popup.js`
5. `server.py`
6. `call.py`

To run the model, `.env` must be present locally with the API key to Google Gemini Pro.

## Collaborators
1. BR Parikshit (frontend)
2. Samarth K J (backend)
