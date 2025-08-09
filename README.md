# CodeAlpha_Chatbot_For_FAQs
A user-friendly chat bot of a product based company.

# 🤖 FAQ Bot API with Flask, SpaCy, and RapidFuzz

This is a simple yet powerful FAQ chatbot API that uses **NLP (Natural Language Processing)** techniques to match user questions with a set of predefined FAQs. It combines **SpaCy's semantic similarity** and **RapidFuzz's fuzzy string matching** to provide accurate and robust answers.

---

## 📌 Features

- Accepts user questions and returns the best-matching FAQ answer.
- Combines **semantic similarity** (SpaCy) and **fuzzy matching** (RapidFuzz) for better accuracy.
- Returns confidence score and top 3 closest matches.
- Simple RESTful API with **CORS enabled**.
- Built-in logging for easier debugging.

---

## 🚀 Getting Started

### 🔧 Prerequisites

Ensure Python 3.7+ is installed. Then install the required packages:

```bash
pip install flask flask-cors spacy rapidfuzz
python -m spacy download en_core_web_md
```

---

## 🧑‍💻 Running the Application

```bash
python faq-bot.py
```

The API will start on:

```
http://localhost:8800/ask
```

---

## 📨 API Endpoint

### **POST** `/ask`

**Request Body (JSON):**

```json
{
  "question": "How do I track my order?"
}
```

**Successful Response (JSON):**

```json
{
  "answer": "Once shipped, you will receive a tracking number via email.",
  "confidence": 0.89,
  "top_matches": [
    {
      "question": "How can I track my order?",
      "answer": "Once shipped, you will receive a tracking number via email.",
      "score": 0.89
    },
    {
      "question": "Can I change or cancel my order?",
      "answer": "Orders can be changed or cancelled within 2 hours of placing them.",
      "score": 0.52
    },
    {
      "question": "How long does shipping take?",
      "answer": "Shipping usually takes 5-7 business days.",
      "score": 0.47
    }
  ]
}
```

**Low Confidence Response (JSON):**

```json
{
  "answer": "Sorry, I don't understand your question. Please try rephrasing."
}
```

---

## 💡 How It Works

- **SpaCy** (`en_core_web_md`) is used to compute semantic similarity between user question and FAQ entries.
- **RapidFuzz** computes character-level fuzzy matching on preprocessed (cleaned) text.
- A weighted score (`0.7 * SpaCy + 0.3 * Fuzzy`) is used to find the best match.
- Returns top 3 matches with scores for better insight or frontend display.

---

## ⚠️ Notes

- Designed for English language queries using `en_core_web_md`. You can switch to other SpaCy models if needed.
- Performance and accuracy can be tuned by adjusting similarity weights or preprocessing steps.
- Not intended for production-scale loads without optimization (e.g., async handling, caching, DB support).

---

Happy coding! 🚀
