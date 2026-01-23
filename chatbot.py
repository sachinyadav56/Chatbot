# import json
# import pickle
# import random

# # Load files
# model = pickle.load(open("model.pkl", "rb"))
# vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# with open("intents.json") as file:
#     intents = json.load(file)

# def chatbot_response(user_input):
#     X = vectorizer.transform([user_input])
#     tag = model.predict(X)[0]

#     for intent in intents["intents"]:
#         if intent["tag"] == tag:
#             return random.choice(intent["responses"])

#     return "Sorry, I didn't understand."

# # Chat loop
# print("Chatbot is running! (type 'quit' to exit)")

# while True:
#     msg = input("You: ")
#     if msg.lower() == "quit":
#         break
#     print("Bot:", chatbot_response(msg))


import json, pickle, random
from deep_translator import GoogleTranslator

# Load files
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))
with open("intents.json") as file:
    intents = json.load(file)

def chatbot_response(user_input):
    # Translate input to English for model processing
    translated_input = GoogleTranslator(source='auto', target='en').translate(user_input)

    # Predict intent
    X = vectorizer.transform([translated_input])
    tag = model.predict(X)[0]

    for intent in intents["intents"]:
        if intent["tag"] == tag:
            reply = random.choice(intent["responses"])
            # Translate reply back to user’s language
            translated_reply = GoogleTranslator(source='en', target='auto').translate(reply)
            return translated_reply

    return GoogleTranslator(source='en', target='auto').translate("Sorry, I didn't understand.")
    

# Chat loop
print("Chatbot is running! (type 'quit' to exit)")
while True:
    msg = input("You: ")
    if msg.lower() == "quit":
       break
    print("Bot:", chatbot_response(msg))

