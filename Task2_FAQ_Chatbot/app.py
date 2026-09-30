from flask import Flask, render_template, request
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json
import re

app = Flask(__name__)


# Load FAQ data
with open("faqs.json", "r", encoding="utf-8") as file:
    faqs = json.load(file)


# Separate questions and answers
questions = [faq["question"] for faq in faqs]
answers = [faq["answer"] for faq in faqs]


# Text preprocessing function
def preprocess(text):

    # Convert text to lowercase
    text = text.lower()

    # Remove special characters
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    return text


# Preprocess all FAQ questions
processed_questions = [
    preprocess(question)
    for question in questions
]


# Convert FAQ questions into TF-IDF vectors
vectorizer = TfidfVectorizer()

question_vectors = vectorizer.fit_transform(
    processed_questions
)


# Find the most similar FAQ
def find_answer(user_question):

    # Preprocess user's question
    cleaned_question = preprocess(user_question)

    # Convert user's question into TF-IDF vector
    user_vector = vectorizer.transform(
        [cleaned_question]
    )

    # Calculate cosine similarity
    similarities = cosine_similarity(
        user_vector,
        question_vectors
    )

    # Find highest similarity
    best_match = similarities.argmax()

    # Get similarity score
    best_score = similarities[0][best_match]

    # Minimum similarity threshold
    if best_score < 0.15:

        return "Sorry, I don't have an answer for that question."

    # Return matching FAQ answer
    return answers[best_match]


@app.route("/", methods=["GET", "POST"])
def home():

    user_question = ""

    response = ""

    if request.method == "POST":

        user_question = request.form.get(
            "question",
            ""
        ).strip()

        if user_question:

            response = find_answer(
                user_question
            )

    return render_template(
        "index.html",
        question=user_question,
        response=response
    )


if __name__ == "__main__":

    app.run(debug=True)