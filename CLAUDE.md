# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## Common Development Commands

**Environment setup**
```bash
# Create and activate a Conda environment (Python 3.10)
conda create -n NutriLens python=3.10 -y
conda activate NutriLens
```

**Install dependencies**
```bash
pip install -r requirements.txt
```

**Configure environment variables**
Create a `.env` file in the repository root with:
```env
GEMINI_API_KEY=your_gemini_api_key
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
```

**Run the FastAPI backend (auto‑reload)**
```bash
uvicorn app.main:app --reload
```

**Start the Telegram bot**
```bash
python -m bot.telegram_bot
```

**Run the Gemini API sanity test**
```bash
python test_gemini.py
```

---

## High‑Level Architecture

1. **Telegram Bot (`bot/telegram_bot.py`)** – Handles user interaction, receives image bytes, forwards them to the backend API, and formats the JSON response for the chat.
2. **FastAPI Backend (`app/main.py`, `app/routes/analyze.py`)** – Exposes a single POST `/api/analyze` endpoint. It validates the uploaded image and delegates processing to the Gemini service.
3. **Gemini Service (`app/services/gemini_service.py`)** –
   * Saves the uploaded image via `save_image` (stores under `data/`).
   * Calls the Google Gemini Vision model to extract raw text from the image.
   * Builds a structured prompt (`app/utils/prompts.get_food_analysis_prompt`).
   * Sends the prompt back to Gemini, receives a textual response, and extracts the JSON payload safely.
4. **Image Service (`app/services/image_service.py`)** – Persists raw image bytes with a timestamped, UUID‑based filename.
5. **Prompt Utilities (`app/utils/prompts.py`)** – Provides the fixed JSON‑only prompt template used for food analysis.
6. **Configuration (`app/config.py`)** – Loads `GEMINI_API_KEY` and `TELEGRAM_BOT_TOKEN` from the `.env` file via `python-dotenv`.
7. **Logging (`app/utils/logger.py`)** – Simple wrapper around Python’s `logging` module.

**Data Flow**
```
User → Telegram Bot → FastAPI /api/analyze → Gemini Service
   ← (image bytes)                ↓
   ← (JSON analysis)            Gemini Vision + LLM
```
The bot stores received images in memory per user, forwards the first available image to the API, and replies with a formatted health score, verdict, issues, and summary extracted from the Gemini JSON output.

---

## Key Files to Know
- `app/main.py` – FastAPI app creation and CORS setup.
- `app/routes/analyze.py` – `/api/analyze` endpoint implementation.
- `app/services/gemini_service.py` – Core OCR → prompt → JSON extraction pipeline.
- `app/services/image_service.py` – `save_image` helper.
- `app/utils/prompts.py` – Prompt template with strict JSON output contract.
- `bot/telegram_bot.py` – Bot command handlers and HTTP request to the backend.
- `app/config.py` – Environment variable loading.
- `requirements.txt` – Dependency list (FastAPI, google‑genai, python‑telegram‑bot, python‑dotenv, etc.).

---

*End of CLAUDE.md*