from flask import Flask, request, jsonify
from flask_cors import CORS
import spacy
from rapidfuzz import fuzz
import logging

app = Flask(__name__)
CORS(app)

# Setup logging
logging.basicConfig(level=logging.INFO)

# Load SpaCy model
nlp = spacy.load("en_core_web_md")

# FAQ data
faqs = [
    {"question": "What is your return policy?", "answer": "You can return any item within 30 days of purchase."},
    {"question": "How long does shipping take?", "answer": "Shipping usually takes 5-7 business days."},
    {"question": "Do you offer international shipping?", "answer": "Yes, we ship to most countries worldwide."},
    {"question": "How can I track my order?", "answer": "Once shipped, you will receive a tracking number via email."},
    {"question": "What payment methods do you accept?", "answer": "We accept credit cards, PayPal, and Apple Pay."},
    {"question": "Can I change or cancel my order?", "answer": "Orders can be changed or cancelled within 2 hours of placing them."},
    {"question": "Are your products covered by warranty?", "answer": "Yes, all products come with a one-year warranty."},
    {"question": "How do I contact customer support?", "answer": "You can reach customer support via email at support@example.com or call 123-456-7890."},
    {"question": "Do you offer gift wrapping?", "answer": "Yes, gift wrapping is available for an additional fee at checkout."},
    {"question": "Is my personal information secure?", "answer": "We use industry-standard encryption to protect your data."},
    {"question": "Can I get a discount on bulk orders?", "answer": "Yes, please contact sales@example.com for bulk order discounts."},
    {"question": "What should I do if I receive a damaged product?", "answer": "Please contact customer support immediately with your order details and photos of the damage."},
    {"question": "Do you have a physical store location?", "answer": "Currently, we operate only online, but we plan to open stores soon."},
    {"question": "What are your business hours?", "answer": "Our customer support is available Monday to Friday, 9 AM to 6 PM EST."},
    {"question": "Can I update my shipping address after ordering?", "answer": "Shipping address can be updated within 1 hour of placing the order."},
    {"question": "How do I create an account?", "answer": "Click the 'Sign Up' button on the top right and fill in your details."},
    {"question": "What should I do if I forgot my password?", "answer": "Click on 'Forgot Password' at login to reset your password via email."},
    {"question": "Are your products eco-friendly?", "answer": "Yes, we are committed to sustainable and eco-friendly products."}
]


# Precompute SpaCy docs for questions
faq_docs = [nlp(faq["question"]) for faq in faqs]

def preprocess_text(text):
    """
    Basic text cleanup:
    - Lowercase
    - Remove stopwords and punctuation for better fuzzy matching
    """
    doc = nlp(text.lower())
    tokens = [token.text for token in doc if not (token.is_stop or token.is_punct)]
    return " ".join(tokens)

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    user_question = data.get("question", "").strip()
    if not user_question:
        return jsonify({"answer": "Please ask a question."})

    logging.info(f"User question: {user_question}")

    user_doc = nlp(user_question)

    # Calculate SpaCy similarity for each FAQ
    sim_scores = []
    for faq_doc in faq_docs:
        sim = user_doc.similarity(faq_doc)
        sim_scores.append(sim)

    # Calculate fuzzy ratio on preprocessed text for robustness
    user_processed = preprocess_text(user_question)
    faq_processed = [preprocess_text(faq['question']) for faq in faqs]
    fuzzy_scores = [fuzz.ratio(user_processed, fp) / 100 for fp in faq_processed]

    # Combine scores with weights (adjust weights to your liking)
    combined_scores = []
    for spa, fz in zip(sim_scores, fuzzy_scores):
        combined = (0.7 * spa) + (0.3 * fz)
        combined_scores.append(combined)

    # Get top 3 matches by combined score
    top_matches = sorted(
        enumerate(combined_scores),
        key=lambda x: x[1],
        reverse=True
    )[:3]

    # If top score is low, respond no match
    if top_matches[0][1] < 0.6:
        logging.info(f"No good match found. Top score: {top_matches[0][1]:.2f}")
        return jsonify({"answer": "Sorry, I don't understand your question. Please try rephrasing."})

    # Prepare detailed results (optional)
    results = []
    for idx, score in top_matches:
        results.append({
            "question": faqs[idx]["question"],
            "answer": faqs[idx]["answer"],
            "score": round(score, 2)
        })

    # Return best answer and optionally top 3 matches
    best_idx = top_matches[0][0]
    best_answer = faqs[best_idx]["answer"]
    best_score = top_matches[0][1]

    logging.info(f"Best match: {faqs[best_idx]['question']} with score {best_score:.2f}")

    return jsonify({
        "answer": best_answer,
        "confidence": round(best_score, 2),
        "top_matches": results  # optional: send top matches for frontend to display or debug
    })


if __name__ == "__main__":
    app.run(debug=True, port=8800)
