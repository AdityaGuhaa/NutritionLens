# 🥗 NutriLens

> AI-powered food label analyzer that turns complex ingredient lists and nutrition labels into clear, actionable health insights.

---

## 🚀 Overview

NutriLens is an intelligent system designed to help users make better food choices by analyzing product labels. Users simply upload images of ingredient lists and nutrition labels, and NutriLens processes them using computer vision and AI to generate easy-to-understand health insights.

The system bridges the gap between **raw food label data** and **consumer understanding**, enabling smarter, healthier decisions in real time.

---

## 🎯 Problem Statement

Modern food labels are:

* Hard to read
* Filled with complex chemical names
* Misleading due to marketing tactics

Most consumers:

* Don’t understand ingredient impact
* Can’t quickly evaluate healthiness
* Lack time to research every product

👉 NutriLens solves this by **automating label interpretation using AI**.

---

## 💡 Solution

NutriLens provides:

* 📸 Image-based input (ingredients + nutrition labels)
* 🧠 AI-driven analysis of food content
* 📊 Structured health insights
* ⚠️ Detection of harmful or controversial ingredients

All delivered via a simple **Telegram bot interface**.

---

## 🏗️ System Architecture

The system is designed using a modular, scalable architecture:

```
User (Telegram)
      ↓
Telegram Bot Interface
      ↓
FastAPI Backend
      ↓
Vision + OCR Layer
      ↓
LLM Analysis Engine
      ↓
Structured Health Output
```

---

## ⚙️ Tech Stack

### Backend

* FastAPI (high-performance API framework)
* Python (core logic)

### AI & ML

* Vision-Language Model (Gemini API)
* OCR capabilities via multimodal model
* LLM-based reasoning for health analysis

### Integration

* Telegram Bot API (user interface)

### Utilities

* Logging & retry mechanisms
* Structured prompt engineering

---

## 🔄 Pipeline (End-to-End Flow)

### 1. User Interaction

* User starts bot with `/start`
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

---

## 🧠 Core Approach

### 1. Multimodal Intelligence

Instead of traditional OCR + rules, NutriLens uses a **Vision-Language Model**, enabling:

* Better text extraction
* Context-aware understanding

### 2. LLM-Based Reasoning

Rather than static rules, NutriLens uses AI to:

* Interpret ingredient impact
* Provide human-like explanations

### 3. Prompt Engineering

Carefully designed prompts ensure:

* Consistent output format
* Reliable health evaluation

### 4. Robust Error Handling

* Retry logic for API failures
* Graceful fallback for unreadable images

---

## 📦 Features

* ✅ Image-based food label analysis
* ✅ Ingredient safety detection
* ✅ Nutrition breakdown interpretation
* ✅ Telegram bot interface
* ✅ Real-time AI insights
* ✅ Intelligent error handling

---

## 🚧 Challenges & Solutions

### ❗ Challenge: Poor Image Quality

**Solution:** Robust parsing + fallback messaging

### ❗ Challenge: API Failures (e.g., 503 errors)

**Solution:** Retry logic and logging system

### ❗ Challenge: Unstructured Data

**Solution:** Structured prompt-based extraction

---

## 📈 Future Enhancements

* 🔍 Barcode scanning support
* 📊 Health scoring system
* 🧑‍⚕️ Personalized diet recommendations
* 🛒 Product comparison engine
* 🌐 Web dashboard

---

## 🧪 Use Cases

* Everyday grocery shopping
* Fitness and diet tracking
* Health-conscious consumers
* Parents evaluating packaged food

---

## 🤝 Contribution

Contributions are welcome! Feel free to fork the repo and submit pull requests.

---

## 📜 License

This project is open-source and available under the MIT License.

---

## 🌟 Final Note

NutriLens is not just a project — it’s a step toward making **food transparency accessible to everyone**.
