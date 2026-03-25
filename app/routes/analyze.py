from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.gemini_service import analyze_food_label

router = APIRouter()


@router.post("/analyze")
async def analyze_food(file: UploadFile = File(...)):
    try:
        # ✅ Validate file type
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="File must be an image")

        # ✅ Read file bytes
        image_bytes = await file.read()

        if not image_bytes:
            raise HTTPException(status_code=400, detail="Empty file")

        # ✅ Call Gemini service
        result = analyze_food_label(
            image_bytes=image_bytes,
            mime_type=file.content_type
        )

        return {
            "success": True,
            "data": result
        }

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))