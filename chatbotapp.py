from flask import Flask, render_template, request, jsonify
import pickle, json, random
from deep_translator import GoogleTranslator
from langdetect import detect, DetectorFactory, LangDetectException

DetectorFactory.seed = 0  

app = Flask(__name__)

model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))
intents = json.load(open("intents.json", encoding="utf-8"))

@app.route("/chatbot", methods=["GET", "POST"])
def chat():
    if request.method == "GET":
        return render_template("index.html")

    data = request.get_json()
    user_input = data.get("message", "").strip()

    # language detection
    try:
        if len(user_input) < 10:
            user_lang = "en"   
        else:
            user_lang = detect(user_input)
    except LangDetectException:
        user_lang = "en"

    # Translate user input → English
    translated_input = GoogleTranslator(source='auto', target='en').translate(user_input)

    # Machin Learnning processing
    X = vectorizer.transform([translated_input])
    tag = model.predict(X)[0]

    for intent in intents["intents"]:
        if intent["tag"] == tag:
            reply_en = random.choice(intent["responses"])

            # reply in user language
            if user_lang != "en":
                final_reply = GoogleTranslator(source='en', target=user_lang).translate(reply_en)
            else:
                final_reply = reply_en

            return jsonify({"reply": final_reply})

    return jsonify({"reply": "Sorry, I didn't understand that."})

@app.route("/")
def home():
    return render_template("start.html")

if __name__ == "__main__":
    app.run(debug=True)

