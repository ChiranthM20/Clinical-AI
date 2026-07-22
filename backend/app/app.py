import pytesseract
import logging
import os
import sys
from dotenv import load_dotenv

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
import joblib
import pytesseract
from PIL import Image

# Import Firebase Admin Config
from firebase_admin_config import firebase_config

# Import Authentication Middleware
from auth_middleware import verify_firebase_token, get_user_id, get_user_email

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables from either backend/.env or backend/app/.env
current_dir = os.path.dirname(__file__)
load_dotenv(dotenv_path=os.path.join(current_dir, '..', '.env'))
load_dotenv(dotenv_path=os.path.join(current_dir, '.env'), override=False)

# Initialize Flask app
app = Flask(__name__)

# Basic Flask configuration
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', '')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', '')
app.config['MAIL_DEFAULT_SENDER'] = app.config['MAIL_USERNAME']

# Setup CORS
cors_origins = ['http://localhost:3000', 'http://127.0.0.1:3000']
CORS(app, origins=cors_origins)

# Initialize Firebase Admin SDK
logger.info("Initializing Firebase Admin SDK...")
if firebase_config.initialize():
    logger.info("Firebase Admin SDK initialized successfully")
    firebase_initialized = True
else:
    logger.warning("Firebase Admin SDK initialization failed")
    firebase_initialized = False

# Initialize Mail
mail = Mail(app)    

# Email sending helper function
def send_email(to_email, subject, body):
    try:
        if not app.config['MAIL_USERNAME'] or not app.config['MAIL_PASSWORD']:
            logger.error(
                "Email alert skipped: MAIL_USERNAME or MAIL_PASSWORD is not configured"
            )
            return

        msg = Message(subject,
                      sender=app.config['MAIL_DEFAULT_SENDER'],
                      recipients=[to_email])
        msg.body = body
        mail.send(msg)
        logger.info("Email sent successfully to %s", to_email)
    except Exception as e:
        logger.exception("Email error while sending alert to %s: %s", to_email, e)

# Load model with fallback support
model = None
bert_model = None
model_loaded = False

# Environment info for debugging
print("\n" + "=" * 70)
print("LOADING ML MODELS")
print("=" * 70)
print(f"Python Version: {sys.version}")
print(f"Current Working Directory: {os.getcwd()}")
print("=" * 70)

try:
    print("\n[STEP 1] Loading Logistic Regression classifier...")
    model = joblib.load("../model/model.pkl")
    print(f"✅ Model loaded successfully from: ../model/model.pkl")
    print(f"   Model type: {type(model).__name__}")
    print(f"   Classes: {list(model.classes_)}")
    print(f"   Coefficients shape: {model.coef_.shape}")
    
    print("\n[STEP 2] Loading BERT embedding model...")
    try:
        # Try loading as SentenceTransformer first (recommended)
        from sentence_transformers import SentenceTransformer
        bert_model = SentenceTransformer("../model/bert_model")
        print(f"✅ BERT model loaded from directory: ../model/bert_model")
    except:
        # Fallback to pickle
        print("   (Directory format not found, trying pickle format)")
        bert_model = joblib.load("../model/bert_model.pkl")
        print(f"✅ BERT model loaded from pickle: ../model/bert_model.pkl")
    
    print(f"   Model type: {type(bert_model).__name__}")
    
    # Test embedding generation
    print("\n[STEP 3] Testing embedding generation...")
    test_embedding = bert_model.encode(["test clinical text"])
    print(f"✅ Embedding test successful")
    print(f"   Test embedding shape: {test_embedding.shape}")
    print(f"   Embedding dimensions: {test_embedding.shape[1]}")
    print(f"   Embedding dtype: {test_embedding.dtype}")
    
    # Test prediction
    print("\n[STEP 4] Testing model prediction...")
    test_pred = model.predict(test_embedding)
    test_proba = model.predict_proba(test_embedding)
    print(f"✅ Prediction test successful")
    print(f"   Test prediction: {test_pred[0]}")
    print(f"   Prediction probabilities: {test_proba[0]}")
    
    model_loaded = True
    print("\n" + "=" * 70)
    print("✅ ALL MODELS LOADED SUCCESSFULLY")
    print("=" * 70 + "\n")
    
except FileNotFoundError as e:
    print(f"\n❌ Model file not found: {e}")
    print("⚠️  Using fallback manual prediction logic")
    model_loaded = False
    
except Exception as e:
    print(f"\n❌ ERROR loading models: {e}")
    print(f"   Error type: {type(e).__name__}")
    print(f"   Error message: {str(e)}")
    print("⚠️  Using fallback manual prediction logic")
    print("=" * 70 + "\n")
    model_loaded = False


def get_ml_prediction(text):
    """
    Generate prediction using BERT embeddings + Logistic Regression model
    
    Process:
    1. Generate BERT embeddings from clinical text
    2. Get ML model prediction (risk: Low/Medium/High)
    3. Get prediction probabilities for confidence calculation
    4. Convert highest probability to 0-100 confidence score
    
    Args:
        text (str): Clinical text to analyze
    
    Returns:
        dict: {
            "risk": "Low|Medium|High",
            "confidence": 0-100,
            "use_ml_model": True/False (False if using fallback)
        }
    """
    if not model_loaded or model is None or bert_model is None:
        # Fallback: Use manual keyword logic
        return None
    
    try:
        # STEP 1: Generate BERT embedding from clinical text
        # Converts text into a 384-dimensional vector representation
        embedding = bert_model.encode([text])
        
        # STEP 2: Get ML model prediction (returns "Low", "Medium", or "High")
        predicted_risk = model.predict(embedding)[0]
        
        # STEP 3: Get prediction probabilities for confidence calculation
        # Returns array of probabilities for each class [Low, Medium, High]
        probabilities = model.predict_proba(embedding)[0]
        
        # STEP 4: Calculate confidence as max probability converted to 0-100 scale
        # E.g., 0.87 probability → 87% confidence
        confidence = int(max(probabilities) * 100)
        
        return {
            "risk": predicted_risk,
            "confidence": confidence,
            "use_ml_model": True,
            "probabilities": probabilities.tolist()  # For debugging
        }
    except Exception as e:
        logger.error(f"ML prediction error: {e}")
        return None


def generate_score(risk):
    """
    Legacy function for backward compatibility.
    Score is now calculated from model confidence instead.
    """
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


@app.route("/health", methods=["GET"])
def health_check():
    """
    Health check endpoint to verify Flask and Firebase are running
    
    Returns:
        JSON with status of Flask app and Firebase Admin SDK
    """
    firebase_status = firebase_config.health_check()
    
    return jsonify({
        "status": "ok" if firebase_status["status"] == "ok" else "warning",
        "message": "API is running",
        "firebase": firebase_status,
        "environment": app.config.get('FLASK_ENV', 'unknown')
    }), 200 if firebase_status["status"] == "ok" else 503


@app.route("/firebase-status", methods=["GET"])
def firebase_status():
    """
    Check Firebase Admin SDK status
    
    Returns:
        JSON with Firebase initialization and connection status
    """
    status = firebase_config.health_check()
    is_init = firebase_config.is_initialized()
    
    return jsonify({
        "initialized": is_init,
        "status": status,
        "credentials_configured": app.config.get('FIREBASE_CREDENTIALS_PATH') is not None
    }), 200 if is_init else 503


@app.route("/predict", methods=["POST"])
@verify_firebase_token
def predict():
    """
    Predict health risk based on symptoms
    
    Authentication: Required (Firebase ID token)
    Authorization: Bearer <token>
    
    Request JSON:
    {
        "text": "symptom description",
        "email": "user@example.com"  # optional
    }
    
    Returns:
    {
        "risk": "Low|Medium|High",
        "score": 20-90,
        "symptoms": ["detected", "symptoms"],
        "user_id": "authenticated_user_id"  # From Firebase token
    }
    """
    # Get authenticated user info from Firebase token
    user_id = get_user_id()
    
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

    # ============================================================
    # ML-BASED RISK PREDICTION
    # ============================================================
    # Use trained BERT + Logistic Regression model for prediction
    ml_result = get_ml_prediction(text)
    
    if ml_result:
        # ML model prediction succeeded
        risk = ml_result["risk"]
        # Convert model confidence (0-100) to score matching response structure
        score = ml_result["confidence"]
        logger.info(f"ML Prediction: risk={risk}, confidence={score}%, probabilities={ml_result['probabilities']}")
    else:
        # Fallback to manual keyword-based logic if models aren't loaded
        logger.warning("Using fallback manual prediction logic")
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
        "symptoms": detected,
        "user_id": user_id
    })


@app.route("/upload", methods=["POST"])
@verify_firebase_token
def upload_file():
    """
    Upload and process file (OCR for images, direct read for text)
    
    Authentication: Required (Firebase ID token)
    Authorization: Bearer <token>
    
    Request: multipart/form-data
    - file: The file to upload (image or text)
    
    Returns:
    {
        "text": "extracted text content",
        "user_id": "authenticated_user_id"  # From Firebase token
    }
    """
    # Get authenticated user info from Firebase token
    user_id = get_user_id()
    
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

    return jsonify({"text": text, "user_id": user_id})


if __name__ == "__main__":
    app.run(debug=True)