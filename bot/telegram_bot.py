import requests
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from app.config import settings

# Backend API URL
API_URL = "http://127.0.0.1:8000/api/analyze"

# In-memory user state
user_data_store = {}


# 🟢 START COMMAND
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    user_data_store[user_id] = {
        "nutrition": None,
        "ingredients": None
    }

    await update.message.reply_text(
        "👋 Welcome to *NutriLens!*\n\n"
        "Send me:\n"
        "1️⃣ Nutrition label image\n"
        "2️⃣ Ingredients label image\n\n"
        "You can send one or both.\n\n"
        "⚠️ Only images are supported right now.",
        parse_mode="Markdown"
    )


# 🖼️ HANDLE IMAGE
async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if user_id not in user_data_store:
        user_data_store[user_id] = {
            "nutrition": None,
            "ingredients": None
        }

    photo = update.message.photo[-1]  # highest resolution
    file = await photo.get_file()
    file_bytes = await file.download_as_bytearray()

    # 🧠 Basic classification (very simple heuristic for MVP)
    caption = update.message.caption.lower() if update.message.caption else ""

    if "ingredient" in caption:
        user_data_store[user_id]["ingredients"] = file_bytes
        await update.message.reply_text("✅ Ingredients image received.")

    elif "nutrition" in caption or "facts" in caption:
        user_data_store[user_id]["nutrition"] = file_bytes
        await update.message.reply_text("✅ Nutrition label received.")

    else:
        # If no caption → try anyway as nutrition (MVP simplification)
        user_data_store[user_id]["nutrition"] = file_bytes
        await update.message.reply_text(
            "📷 Image received. Trying to analyze..."
        )

    # 🚀 If at least one image exists → process
    await process_images(update, context, user_id)


# 🚀 PROCESS IMAGES
async def process_images(update, context, user_id):
    data = user_data_store[user_id]

    # Use nutrition image as primary (MVP)
    image_bytes = data.get("nutrition") or data.get("ingredients")

    if not image_bytes:
        return

    try:
        files = {
            "file": ("image.jpg", image_bytes, "image/jpeg")
        }

        response = requests.post(API_URL, files=files)

        result = response.json()

        if not result.get("success"):
            raise Exception("API failed")

        analysis = result["data"]

        if "error" in analysis:
            await update.message.reply_text("❌ Unable to read contents.")
            return

        # 🧾 Format response
        msg = (
            f"🟢 *Health Score:* {analysis.get('health_score', 'N/A')}/10\n\n"
            f"*Verdict:* {analysis.get('verdict', 'N/A')}\n\n"
            f"⚠️ *Issues:*\n- " + "\n- ".join(analysis.get("issues", [])) + "\n\n"
            f"💡 *Summary:*\n{analysis.get('summary', '')}"
        )

        await update.message.reply_text(msg, parse_mode="Markdown")

    except Exception as e:
        await update.message.reply_text("❌ Unable to read contents.")


# 🚫 HANDLE NON-IMAGE INPUT
async def handle_invalid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "❌ Only images are supported right now.\n"
        "Please upload nutrition or ingredients label."
    )


# 🚀 MAIN
def main():
    app = ApplicationBuilder().token(settings.TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_image))
    app.add_handler(MessageHandler(~filters.PHOTO, handle_invalid))

    print("🤖 NutriLens Bot Running...")
    app.run_polling()


if __name__ == "__main__":
    main()