import json
import re

from google import genai
from google.genai import types

from app.config import settings
from app.utils.prompts import get_food_analysis_prompt
from app.services.image_service import save_image


# Initialize Gemini client
client = genai.Client(api_key=settings.GEMINI_API_KEY)


def extract_json(text: str) -> dict:
    """
    Extract valid JSON safely from model output
    """
    try:
        # Remove markdown formatting if present
        text = text.strip().replace("```json", "").replace("```", "")

        # Extract JSON using regex
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


def analyze_food_label(image_bytes: bytes, mime_type: str = "image/jpeg") -> dict:
    """
    Main pipeline:
    Image → OCR → Prompt → Analysis → JSON
    """
    try:
        # ✅ Step 0: Save image locally
        save_image(image_bytes)

        # ✅ Step 1: Normalize MIME type (important fix)
        if mime_type not in ["image/jpeg", "image/png", "image/webp"]:
            mime_type = "image/jpeg"

        # ✅ Step 2: Extract text using Gemini Vision
        vision_response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                "Extract all readable text from this food label image.",
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type=mime_type
                )
            ]
        )

        extracted_text = getattr(vision_response, "text", None)

        if not extracted_text:
            return {"error": "Could not extract text from image"}

        # ✅ Step 3: Build prompt
        prompt = get_food_analysis_prompt(extracted_text)

        # ✅ Step 4: Analyze food label
        analysis_response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        raw_output = getattr(analysis_response, "text", None)

        if not raw_output:
            return {"error": "Empty response from Gemini"}

        # ✅ Step 5: Parse JSON safely
        parsed_output = extract_json(raw_output)

        return parsed_output

    except Exception as e:
        return {
            "error": str(e)
        }