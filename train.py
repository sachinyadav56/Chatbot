
import json
import nltk
import pickle
import re

from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

nltk.download('punkt')
nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()

# Clean + lemmatize function
def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z ]', '', text)
    tokens = nltk.word_tokenize(text)
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    return " ".join(tokens)

# Load intents
with open("intents.json") as file:
    data = json.load(file)

sentences = []
labels = []

for intent in data["intents"]:
    for pattern in intent["patterns"]:
        sentences.append(preprocess(pattern))
        labels.append(intent["tag"])

# Vectorization
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(sentences)

# Train model
model = LogisticRegression(max_iter=1000)
model.fit(X, labels)

# Save
pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

print("Model trained with preprocessing & saved successfully!")

