import json
import re
import time

from google import genai
from google.genai import types

from app.config import settings
from app.utils.prompts import get_food_analysis_prompt
from app.services.image_service import save_image
from app.utils.logger import get_logger

logger = get_logger("gemini_service")

# Initialize Gemini client
client = genai.Client(api_key=settings.GEMINI_API_KEY)

MAX_RETRIES = 3


# 🧠 Retry Wrapper
def call_gemini_with_retry(func):
    last_error = None

    for attempt in range(MAX_RETRIES):
        try:
            logger.info(f"Gemini call attempt {attempt + 1}")
            return func()

        except Exception as e:
            last_error = str(e)

            if "503" in last_error or "UNAVAILABLE" in last_error:
                logger.warning(f"Gemini overloaded (attempt {attempt+1}), retrying...")
                time.sleep(2)
                continue

            raise e

    raise Exception(f"Gemini failed after retries: {last_error}")


# 🧠 JSON Extractor
def extract_json(text: str) -> dict:
    try:
        text = text.strip().replace("```json", "").replace("```", "")

        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return json.loads(match.group())

        return {
            "error": "No valid JSON found",
            "raw_output": text
        }

    except Exception as e:
        return {
            "error": f"JSON parsing failed: {str(e)}",
            "raw_output": text
        }


# 🚀 MAIN PIPELINE
def analyze_food_label(image_bytes: bytes, mime_type: str = "image/jpeg") -> dict:
    try:
        # ✅ Save image
        save_image(image_bytes)
        logger.info("Image saved")

        # ✅ Normalize MIME
        if mime_type not in ["image/jpeg", "image/png", "image/webp"]:
            logger.warning(f"Unsupported MIME type {mime_type}, defaulting to image/jpeg")
            mime_type = "image/jpeg"

        # =============================
        # 🧠 STEP 1: OCR (with retry)
        # =============================
        def extract_text():
            return client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[
                    "Extract all readable text from this food label image.",
                    types.Part.from_bytes(data=image_bytes, mime_type=mime_type)
                ]
            )

        vision_response = call_gemini_with_retry(extract_text)

        extracted_text = getattr(vision_response, "text", None)

        if not extracted_text:
            return {"error": "Could not extract text from image"}

        logger.info(f"Extracted text length: {len(extracted_text)}")

        # =============================
        # 🧠 STEP 2: Prompt
        # =============================
        prompt = get_food_analysis_prompt(extracted_text)

        # =============================
        # 🧠 STEP 3: Analysis (retry + fallback)
        # =============================
        def analyze_primary():
            return client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

        def analyze_fallback():
            logger.warning("Switching to fallback model (gemini-1.5-flash)")
            return client.models.generate_content(
                model="gemini-1.5-flash",
                contents=prompt
            )

        try:
            analysis_response = call_gemini_with_retry(analyze_primary)
        except Exception as e:
            logger.error(f"Primary model failed: {str(e)}")
            analysis_response = analyze_fallback()

        raw_output = getattr(analysis_response, "text", None)

        if not raw_output:
            return {"error": "Empty response from Gemini"}

        logger.info("Received response from Gemini")

        # =============================
        # 🧠 STEP 4: Parse JSON
        # =============================
        parsed = extract_json(raw_output)

        logger.info("JSON parsed successfully")

        return parsed

    except Exception as e:
        logger.error(f"Gemini processing failed: {str(e)}")

        return {
            "error": str(e),
            "type": "gemini_error"
        }