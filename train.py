import json
import nltk
import numpy as np
import pickle
import re

from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

# Download NLTK data
nltk.download('punkt')
nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()

# Text  function
def clean_text(text):
    text = text.lower()                     
    text = re.sub(r"[^a-zA-Z\s]", "", text) 
    tokens = word_tokenize(text)           
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    return " ".join(tokens)

# Load intents
with open("intents.json", encoding="utf-8") as file:
    data = json.load(file)

sentences = []
labels = []

# Prepare training data
for intent in data["intents"]:
    for pattern in intent["patterns"]:
        cleaned_pattern = clean_text(pattern)
        sentences.append(cleaned_pattern)
        labels.append(intent["tag"])

# Convert text to vectors
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(sentences)

# Train ML model
model = LogisticRegression(max_iter=1000)
model.fit(X, labels)

# Save trained model and vectorizer
pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

print(" Model trained and saved successfully!")
