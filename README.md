# NutritionLens

> AI-powered food label analyzer that turns complex ingredient lists and nutrition labels into clear, actionable health insights.

<table>
  <tr>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/3cbf07db-c24a-4610-868e-23d73697e069" width="250">
    </td>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/1da2d339-f97e-454d-b837-767507f9b5c0" width="250">
    </td>
  </tr>
  <tr>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/b82ca557-5d6f-4a75-800b-1490eff8a546" width="250">
    </td>
    <td align="center">
      <img src="https://github.com/user-attachments/assets/c78a86db-8ced-40a9-be04-90cd03dffeb7" width="250">
    </td>
  </tr>
</table>

## Overview

NutritionLens is an intelligent system designed to help users make better food choices by analyzing product labels. Users simply upload images of ingredient lists and nutrition labels, and the system processes them using computer vision and AI to generate easy-to-understand health insights.

The system bridges the gap between raw food label data and consumer understanding, enabling smarter, healthier decisions in real time.

The frontend of the system is built on Telegram using a bot named NutritionLensBot.

## Problem Statement

Modern food labels are:

* Hard to read
* Filled with complex chemical names
* Misleading due to marketing tactics

Most consumers:

* Don’t understand ingredient impact
* Can’t quickly evaluate healthiness
* Lack time to research every product

NutritionLens solves this by automating label interpretation using AI.

## Solution

NutritionLens provides:

* Image-based input (ingredients + nutrition labels)
* AI-driven analysis of food content
* Structured health insights
* Detection of harmful or controversial ingredients

All delivered via a Telegram bot interface (NutritionLensBot).

## System Architecture

```
User (Telegram)
      ↓
Telegram Bot Interface (NutritionLensBot)
      ↓
FastAPI Backend
      ↓
Vision + OCR Layer
      ↓
LLM Analysis Engine
      ↓
Structured Health Output
```

## Tech Stack

### Backend

* FastAPI (high-performance API framework)
* Python (core logic)

### AI & ML

* Vision-Language Model (Gemini API)
* OCR via multimodal model
* LLM-based reasoning

### Integration

* Telegram Bot API (NutritionLensBot)

### Utilities

* Logging and retry mechanisms
* Structured prompt engineering

## How to Run

### 1. Create Conda Environment

```bash
conda create -n NutriLens python=3.10 -y
conda activate NutriLens
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Setup Environment Variables

Create a `.env` file in the root directory and add the following:

```env
GEMINI_API_KEY=your_gemini_ai_studio_api_key
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
```

### 4. Start Backend

```bash
uvicorn app.main:app --reload
```

### 5. Start Telegram Bot

```bash
python -m bot.telegram_bot
```

## Pipeline (End-to-End Flow)

### 1. User Interaction

* User starts bot with /start
* Bot requests:

  * Ingredients image
  * Nutrition label image

### 2. Image Input Handling

* Accepts:

  * Ingredients image
  * Nutrition label image
* Rejects irrelevant inputs

### 3. Text Extraction

* Images processed using Vision-Language Model
* Extracts:

  * Ingredient list
  * Nutritional values

### 4. Data Structuring

* Parsed into structured format
* Cleaned and normalized

### 5. AI Analysis

* LLM evaluates:

  * Ingredient safety
  * Additives and preservatives
  * Nutritional balance

### 6. Insight Generation

* Generates:

  * Health summary
  * Warnings
  * Recommendations

### 7. Response Delivery

* Structured output sent back to user via Telegram

## Core Approach

### 1. Multimodal Intelligence

Instead of traditional OCR and rules, NutritionLens uses a Vision-Language Model, enabling:

* Better text extraction
* Context-aware understanding

### 2. LLM-Based Reasoning

Rather than static rules, the system uses AI to:

* Interpret ingredient impact
* Provide human-like explanations

### 3. Prompt Engineering

Carefully designed prompts ensure:

* Consistent output format
* Reliable health evaluation

### 4. Robust Error Handling

* Retry logic for API failures
* Graceful fallback for unreadable images

## Features

* Image-based food label analysis
* Ingredient safety detection
* Nutrition breakdown interpretation
* Telegram bot interface (NutritionLensBot)
* Real-time AI insights
* Intelligent error handling

## Challenges and Solutions

### Challenge: Poor Image Quality

Solution: Robust parsing and fallback messaging

### Challenge: API Failures

Solution: Retry logic and logging system

### Challenge: Unstructured Data

Solution: Structured prompt-based extraction

## Future Enhancements

* Barcode scanning support
* Health scoring system
* Personalized diet recommendations
* Product comparison engine
* Web dashboard

## Use Cases

* Everyday grocery shopping
* Fitness and diet tracking
* Health-conscious consumers
* Parents evaluating packaged food

## Contribution

Contributions are welcome. Fork the repository and submit pull requests.

## License

This project is open-source and available under the MIT License.

## Final Note

NutritionLens is a step toward making food transparency accessible to everyone.
