from flask import Flask, render_template, request, jsonify
import pickle, json, random
from deep_translator import GoogleTranslator

app = Flask(__name__)

model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))
intents = json.load(open("intents.json"))

@app.route("/chatbot", methods=["GET", "POST"])
def chat():
    if request.method == "GET":
        return render_template("index.html")

    user_input = request.json["message"]

# Translate input to English
    translated_input = GoogleTranslator(source='auto', target='en').translate(user_input)

# Predict intent
    X = vectorizer.transform([translated_input])
    tag = model.predict(X)[0]

    for intent in intents["intents"]:
        if intent["tag"] == tag:
            reply = random.choice(intent["responses"])
            
            # Translate reply back to user’s language
            translated_reply = GoogleTranslator(source='en', target='auto').translate(reply)
            return jsonify({"reply": translated_reply})

    return jsonify({"reply": GoogleTranslator(source='en', target='auto').translate("I don't understand")})

@app.route("/")
def home():
    return render_template("start.html")

if __name__ == "__main__":
    app.run(debug=True)






