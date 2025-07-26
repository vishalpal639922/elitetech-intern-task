import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Load the dataset
df = pd.read_csv("E:\Silon\python2025\spam.csv", encoding="latin-1")
df = df.drop(["Unnamed: 2", "Unnamed: 3", "Unnamed: 4"], axis=1)
df = df.rename(columns={"v1": "label", "v2": "text"})

# Preprocess text data
df["text"] = df["text"].str.lower()
df["text"] = df["text"].apply(word_tokenize)
stop_words = set(stopwords.words("english"))
df["text"] = df["text"].apply(lambda x: [word for word in x if word not in stop_words])
df["text"] = df["text"].apply(lambda x: " ".join(x))

# Feature extraction
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(df["text"])

# Split the dataset
X_train, X_test, y_train, y_test = train_test_split(X, df["label"], test_size=0.2, random_state=42)

# Train the classification model
classifier = MultinomialNB()
classifier.fit(X_train, y_train)

# Evaluate the model
y_pred = classifier.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)

print("Accuracy:", accuracy)
print("Classification Report:")
print(report)

# Save the model
import joblib
joblib.dump(classifier, 'email_spam_model.pkl')

# Load and use the model for predictions
loaded_model = joblib.load('email_spam_model.pkl')
new_email = ["Congratulations! You've won a prize. Claim it now."]
new_email = vectorizer.transform(new_email)  # Transform the new email
prediction = loaded_model.predict(new_email)

if prediction[0] == "spam":
    print("This email is spam.")
else:
    print("This email is not spam.")
