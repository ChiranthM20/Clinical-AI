# =========================
# IMPORT LIBRARIES
# =========================
import os
os.environ["TRANSFORMERS_NO_TF"] = "1"
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import joblib

# =========================
# LOAD DATA
# =========================
df = pd.read_csv("../data/cleaned_data.csv")
df['clean_text'] = df['clean_text'].fillna("")

# =========================
# CREATE LABELS
# =========================
def assign_risk(text):
    text = str(text).lower()

    score = 0

    high = [
        "cancer","tumor","heart attack","stroke",
        "chest pain","breathlessness","respiratory failure",
        "cardiac arrest","bleeding","unconscious"
    ]

    medium = [
        "fever","cough","infection","fatigue",
        "vomiting","diarrhea","headache","dizziness",
        "nausea","weakness","pain"
    ]

    for word in high:
        if word in text:
            score += 3

    for word in medium:
        if word in text:
            score += 1

    if score >= 3:
        return "High"
    elif score >= 1:
        return "Medium"
    else:
        return "Low"

df['risk'] = df['clean_text'].apply(assign_risk)

# =========================
# LOAD PRETRAINED MODEL
# =========================
bert_model = SentenceTransformer('all-MiniLM-L6-v2')

# Convert text → embeddings
X = bert_model.encode(df['clean_text'].tolist())

y = df['risk']

# =========================
# SPLIT DATA
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# =========================
# TRAIN CLASSIFIER
# =========================
clf = LogisticRegression(max_iter=200)
clf.fit(X_train, y_train)

# =========================
# EVALUATE
# =========================
pred = clf.predict(X_test)
print("Accuracy:", accuracy_score(y_test, pred))

# =========================
# SAVE EVERYTHING
# =========================
joblib.dump(clf, "model.pkl")
joblib.dump(bert_model, "bert_model.pkl")

print("BERT-based model trained successfully!")