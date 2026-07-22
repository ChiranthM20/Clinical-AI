# =========================
# IMPORT LIBRARIES
# =========================
import os
os.environ["TRANSFORMERS_NO_TF"] = "1"
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import joblib
import sys
import numpy as np
import sklearn

print("=" * 70)
print("ML MODEL RETRAINING SCRIPT")
print("=" * 70)
print(f"Python Version: {sys.version}")
print(f"NumPy Version: {np.__version__}")
print(f"Scikit-learn Version: {sklearn.__version__}")
print("=" * 70)

# =========================
# LOAD DATA
# =========================
print("\n[STEP 1] Loading training data...")
try:
    df = pd.read_csv("../data/cleaned_data.csv")
    df['clean_text'] = df['clean_text'].fillna("")
    print(f"✅ Data loaded successfully: {len(df)} records")
    print(f"   Columns: {list(df.columns)}")
except Exception as e:
    print(f"❌ ERROR loading data: {e}")
    sys.exit(1)

# =========================
# CREATE LABELS
# =========================
print("\n[STEP 2] Creating risk labels...")

def assign_risk(text):
    """
    Assign risk level based on keyword scoring.
    Used for creating training labels.
    """
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

# Show class distribution
risk_counts = df['risk'].value_counts()
print(f"✅ Risk labels assigned:")
for risk, count in risk_counts.items():
    print(f"   {risk}: {count} samples ({count/len(df)*100:.1f}%)")


# =========================
# LOAD PRETRAINED MODEL & GENERATE EMBEDDINGS
# =========================
print("\n[STEP 3] Loading BERT model and generating embeddings...")
try:
    bert_model = SentenceTransformer('all-MiniLM-L6-v2')
    print(f"✅ BERT model loaded: 'all-MiniLM-L6-v2'")
except Exception as e:
    print(f"❌ ERROR loading BERT model: {e}")
    sys.exit(1)

print("   Encoding clinical texts to embeddings...")
try:
    X = bert_model.encode(df['clean_text'].tolist(), show_progress_bar=True)
    print(f"✅ Embeddings generated successfully:")
    print(f"   Embedding shape: {X.shape}")
    print(f"   Embedding dimensions: {X.shape[1]}")
    print(f"   Data type: {X.dtype}")
except Exception as e:
    print(f"❌ ERROR generating embeddings: {e}")
    sys.exit(1)

y = df['risk']


# =========================
# SPLIT DATA
# =========================
print("\n[STEP 4] Splitting data into train/test sets...")
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"✅ Train/test split completed:")
print(f"   Training samples: {len(X_train)}")
print(f"   Test samples: {len(X_test)}")
print(f"   Train ratio: {len(X_train)/(len(X_train)+len(X_test))*100:.1f}%")

# =========================
# TRAIN CLASSIFIER
# =========================
print("\n[STEP 5] Training Logistic Regression classifier...")
try:
    clf = LogisticRegression(max_iter=200, random_state=42)
    clf.fit(X_train, y_train)
    print(f"✅ Model training completed")
    print(f"   Classes: {list(clf.classes_)}")
    print(f"   Number of coefficients: {clf.coef_.shape}")
except Exception as e:
    print(f"❌ ERROR during training: {e}")
    sys.exit(1)

# =========================
# EVALUATE
# =========================
print("\n[STEP 6] Evaluating model performance...")
pred_train = clf.predict(X_train)
pred_test = clf.predict(X_test)

train_accuracy = accuracy_score(y_train, pred_train)
test_accuracy = accuracy_score(y_test, pred_test)

print(f"✅ Model evaluation completed:")
print(f"   Training Accuracy: {train_accuracy:.2%}")
print(f"   Test Accuracy: {test_accuracy:.2%}")
print(f"\n   Classification Report (Test Set):")
print(classification_report(y_test, pred_test, target_names=clf.classes_))


# =========================
# SAVE EVERYTHING
# =========================
print("\n[STEP 7] Saving models to disk...")

try:
    # Save Logistic Regression classifier
    joblib.dump(clf, "model.pkl")
    print(f"✅ Classifier saved: model.pkl")
    
    # Save BERT embedding model
    bert_model.save("bert_model")
    print(f"✅ BERT model saved: bert_model/")
    
    # Also save as pickle for compatibility
    joblib.dump(bert_model, "bert_model.pkl")
    print(f"✅ BERT model also saved as pickle: bert_model.pkl")
    
except Exception as e:
    print(f"❌ ERROR saving models: {e}")
    sys.exit(1)

# =========================
# SAVE METADATA
# =========================
print("\n[STEP 8] Saving training metadata...")
metadata = {
    "model_type": "LogisticRegression",
    "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
    "embedding_dimensions": int(X.shape[1]),
    "num_training_samples": len(X_train),
    "num_test_samples": len(X_test),
    "classes": list(clf.classes_),
    "train_accuracy": float(train_accuracy),
    "test_accuracy": float(test_accuracy),
    "python_version": sys.version,
    "numpy_version": np.__version__,
    "sklearn_version": sklearn.__version__,
    "scikit_learn_version": sklearn.__version__,
}

import json
try:
    with open("model_metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)
    print(f"✅ Metadata saved: model_metadata.json")
except Exception as e:
    print(f"⚠️  Warning: Could not save metadata: {e}")

# =========================
# SUMMARY
# =========================
print("\n" + "=" * 70)
print("TRAINING COMPLETE!")
print("=" * 70)
print(f"✅ Model files created:")
print(f"   - model.pkl (Logistic Regression classifier)")
print(f"   - bert_model.pkl (BERT SentenceTransformer)")
print(f"   - model_metadata.json (training metadata)")
print(f"\n✅ Key metrics:")
print(f"   - Embedding dimensions: {X.shape[1]}")
print(f"   - Classes: {', '.join(clf.classes_)}")
print(f"   - Test Accuracy: {test_accuracy:.2%}")
print("=" * 70)
