from flask import Flask, render_template, request, jsonify
import pickle, json, random

app = Flask(__name__)

model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))
intents = json.load(open("intents.json"))

@app.route("/chatbot", methods=["GET", "POST"])
def chat():
    if request.method == "GET":
        return render_template("index.html")

    user_input = request.json["message"]
    X = vectorizer.transform([user_input])
    tag = model.predict(X)[0]

    for intent in intents["intents"]:
        if intent["tag"] == tag:
            return jsonify({"reply": random.choice(intent["responses"])})

    return jsonify({"reply": "I don't understand"})

@app.route("/")
def home():
    return render_template("start.html")




if __name__ == "__main__":
    app.run(debug=True)
