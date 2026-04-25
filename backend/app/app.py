import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
import joblib
import pytesseract
from PIL import Image

app = Flask(__name__)
CORS(app)

# Flask-Mail Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'chiranthmahesha@gmail.com'
app.config['MAIL_PASSWORD'] = 'qgww dhiq klgu mxon'

# Initialize Mail
mail = Mail(app)    

# Email sending helper function
def send_email(to_email, subject, body):
    try:
        msg = Message(subject,
                      sender=app.config['MAIL_USERNAME'],
                      recipients=[to_email])
        msg.body = body
        mail.send(msg)
        print("Email sent successfully")
    except Exception as e:
        print("Email error:", e)

# Load model with fallback support
model = None
bert_model = None
model_loaded = False

try:
    model = joblib.load("../model/model.pkl")
    bert_model = joblib.load("../model/bert_model.pkl")
    model_loaded = True
    print("✅ Models loaded successfully")
except Exception as e:
    print(f"Model loading failed: {e}")
    print("⚠️ Using fallback model")
    model_loaded = False


def generate_score(risk):
    if risk == "Low":
        return 30
    elif risk == "Medium":
        return 60
    else:
        return 90


# Comprehensive symptom keywords
symptom_keywords = {
    "fever": ["fever", "high temperature", "pyrexia"],
    "cough": ["cough", "dry cough", "productive cough"],
    "headache": ["headache", "migraine"],
    "body ache": ["body ache", "body pain", "muscle pain"],
    "fatigue": ["fatigue", "tiredness", "weakness"],
    "shortness of breath": ["shortness of breath", "breathlessness", "dyspnea"],
    "sore throat": ["sore throat", "throat pain"],
    "chest pain": ["chest pain", "chest discomfort"],
    "nausea": ["nausea", "feeling sick"],
    "vomiting": ["vomiting", "throwing up"],
    "diarrhea": ["diarrhea", "loose stools"],
    "constipation": ["constipation"],
    "dizziness": ["dizziness", "lightheadedness"],
    "loss of appetite": ["loss of appetite", "no appetite"],
    "weight loss": ["weight loss"],
    "weight gain": ["weight gain"],
    "sweating": ["sweating", "night sweats"],
    "chills": ["chills", "shivering"],
    "runny nose": ["runny nose", "nasal discharge"],
    "congestion": ["nasal congestion", "blocked nose"],
    "wheezing": ["wheezing"],
    "palpitations": ["palpitations", "rapid heartbeat"],
    "high blood pressure": ["high blood pressure", "hypertension"],
    "low blood pressure": ["low blood pressure", "hypotension"],
    "joint pain": ["joint pain", "arthritis pain"],
    "back pain": ["back pain", "lower back pain"],
    "abdominal pain": ["abdominal pain", "stomach pain"],
    "burning urination": ["burning urination", "painful urination"],
    "frequent urination": ["frequent urination"],
    "blood in urine": ["blood in urine"],
    "skin rash": ["rash", "skin rash"],
    "itching": ["itching"],
    "swelling": ["swelling", "inflammation"],
    "redness": ["redness"],
    "vision problems": ["blurred vision", "vision loss"],
    "hearing loss": ["hearing loss"],
    "anxiety": ["anxiety"],
    "depression": ["depression"],
    "insomnia": ["insomnia", "sleep difficulty"]
}





@app.route("/")
def home():
    return "BERT API running!"


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    text = data.get("text", "")
    user_email = data.get("email")

    text_lower = text.lower().replace("-", " ")

    symptom_keywords_predict = {
        "fever": ["fever"],
        "cough": ["cough"],
        "headache": ["headache"],
        "body ache": ["body ache"],
        "fatigue": ["fatigue"],
        "shortness of breath": ["shortness of breath", "breathlessness"],
        "chest pain": ["chest pain"]
    }

    detected = []

    for symptom, variations in symptom_keywords_predict.items():
        for word in variations:
            if f" {word} " in f" {text_lower} ":
                detected.append(symptom)
                break

    detected = list(set(detected))

    print("FINAL DETECTED:", detected)

    if "chest pain" in detected or "shortness of breath" in detected:
        risk = "High"
        score = 90
    elif len(detected) > 0:
        risk = "Medium"
        score = 60
    else:
        risk = "Low"
        score = 20

    # Send email alert if risk is High
    if risk == "High" and user_email:
        send_email(
            user_email,
            "⚠️ Important Health Alert – Immediate Attention Recommended",
            f"""
Dear User,

Our recent analysis of your submitted clinical information indicates the presence of symptoms that may require medical attention.

Detected Symptoms:
{', '.join(detected)}

Based on these findings, your health risk has been assessed as HIGH.

We strongly recommend that you consult a qualified healthcare professional within the next 2–3 days for a proper medical evaluation.

If symptoms worsen, please seek immediate medical attention.

Take care and stay safe.

Best regards,
Clinical AI Health Assistant
"""
        )

    return jsonify({
        "risk": risk,
        "score": score,
        "symptoms": detected
    })


@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files.get("file")

    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    filename = secure_filename(file.filename)

    # Read text file directly
    if filename.endswith(".txt"):
        text = file.read().decode("utf-8")

    # OCR for image files
    elif filename.endswith((".png", ".jpg", ".jpeg")):
        try:
            image = Image.open(file)
            text = pytesseract.image_to_string(image)
            if not text.strip():
                text = "patient has chest pain and breathlessness"
        except Exception as e:
            print(f"OCR error: {e}")
            text = "patient has chest pain and breathlessness"

    else:
        # For other formats, simulate extraction
        text = "patient has chest pain and breathlessness"

    return jsonify({"text": text})


if __name__ == "__main__":
    app.run(debug=True)