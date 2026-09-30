from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Supported languages
LANGUAGES = {
    "English": "en",
    "Hindi": "hi",
    "Kannada": "kn",
    "Tamil": "ta",
    "Telugu": "te",
    "Malayalam": "ml",
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Japanese": "ja"
}


@app.route("/", methods=["GET", "POST"])
def home():

    translated_text = ""
    original_text = ""
    error = ""

    if request.method == "POST":

        original_text = request.form.get("text", "").strip()
        source = request.form.get("source")
        target = request.form.get("target")

        # Check if text was entered
        if not original_text:
            error = "Please enter some text."

        # If source and target are same
        elif source == target:
            translated_text = original_text

        else:

            try:

                # MyMemory Translation API
                url = "https://api.mymemory.translated.net/get"

                params = {
                    "q": original_text,
                    "langpair": f"{source}|{target}"
                }

                # Send request to API
                response = requests.get(
                    url,
                    params=params,
                    timeout=10
                )

                # Convert response to JSON
                data = response.json()

                # Get translated text
                translated_text = data["responseData"]["translatedText"]

            except Exception as e:

                print("Translation error:", e)

                error = "Translation service is temporarily unavailable."

    return render_template(
        "index.html",
        languages=LANGUAGES,
        translated_text=translated_text,
        original_text=original_text,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True)