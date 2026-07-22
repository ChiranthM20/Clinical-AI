# 🏥 AI Clinical Text Analysis System

A premium full-stack web application for converting unstructured clinical text into actionable health insights using AI-powered analysis. This system provides healthcare professionals with intelligent risk assessment, symptom extraction, and OCR capabilities for patient records and medical reports.

**Status**: ✅ Production-Ready | **Last Updated**: May 27, 2026

---

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [Deployment](#deployment)
- [API Documentation](#api-documentation)
- [Screenshots](#screenshots)
- [Technical Highlights](#technical-highlights)
- [Future Improvements](#future-improvements)

---

## 🎯 Project Overview

The **AI Clinical Support System** is a full-stack application designed to analyze clinical notes and medical records. The system combines:

- **Frontend**: React-based premium UI with dark/light/gold theme
- **Backend**: Python Flask API with ML/AI analysis engines
- **Database**: Firebase for real-time data and authentication
- **ML/AI**: Scikit-learn + BERT models for risk assessment and symptom extraction
- **OCR**: Pytesseract for processing scanned medical documents

### Core Capabilities

- 🔍 **Risk Assessment**: Evaluates patient health risk (High/Medium/Low) from clinical text
- 📊 **Health Scoring**: Calculates comprehensive health scores (0-100 scale)
- 🏷️ **Symptom Extraction**: Identifies and categorizes symptoms from unstructured text
- 📸 **OCR Processing**: Extracts text from scanned documents (PDF, PNG, JPG)
- 👥 **Multi-User Support**: Firebase authentication with email/password and Google OAuth
- 🎨 **Premium Theme**: Responsive dark/light mode with gold accents
- 📈 **Analysis Dashboard**: Visual history with priority-based sorting

---

## ✨ Key Features

### 1. Authentication & Security
- ✅ Firebase Email/Password authentication
- ✅ Google OAuth integration
- ✅ JWT token verification on backend
- ✅ Secure Bearer token implementation
- ✅ Protected API endpoints
- ✅ Session persistence across app reloads
- ✅ See [AUTH_README.md](AUTH_README.md) for detailed auth documentation

### 2. Premium User Interface
- ✅ **Dark Mode**: Black background with white text
- ✅ **Light Mode**: White background with black text
- ✅ **Gold Accents**: Premium #D4AF37 gold color
- ✅ **Smooth Transitions**: 0.3s ease animations
- ✅ **System Theme Detection**: Auto-detect user preferences
- ✅ **Persistent Theme**: Saves to localStorage
- ✅ **Responsive Design**: Desktop, tablet, mobile compatible
- ✅ **Floating Theme Toggle**: Easy mode switching (top-right corner)

### 3. Clinical Text Analysis
- ✅ Direct text input via textarea
- ✅ File upload with drag-and-drop
- ✅ Multiple format support (.txt, .pdf, .png, .jpg, .jpeg)
- ✅ OCR for scanned documents
- ✅ Real-time processing
- ✅ Batch analysis support

### 4. Analysis Dashboard
- ✅ Risk level color coding (Red/Orange/Green)
- ✅ Health score visualization
- ✅ Symptom list with categorization
- ✅ Analysis history with timestamps
- ✅ Priority-based sorting
- ✅ Patient ranking system

### 5. Data Visualization
- ✅ Bar charts for risk distribution
- ✅ Line charts for trend analysis
- ✅ Statistics cards for summary data
- ✅ Chart.js integration
- ✅ Responsive chart scaling

---

## 🛠️ Technology Stack

### Frontend
| Technology | Version | Purpose |
|-----------|---------|---------|
| **React** | 19.2.5 | UI framework |
| **React Router** | v6 | Client-side routing |
| **Firebase SDK** | 12.12.1 | Auth & Firestore database |
| **Chart.js** | 4.5.1 | Data visualization |
| **React Context** | Built-in | Theme state management |
| **Create React App** | 5.0.1 | Build tooling |
| **CSS3** | ES6+ | Styling with CSS variables |

### Backend
| Technology | Version | Purpose |
|-----------|---------|---------|
| **Python** | 3.x | Core language |
| **Flask** | Latest | Web framework |
| **Firebase Admin SDK** | 6.0+ | Backend auth & database |
| **Scikit-learn** | Latest | ML classification models |
| **BERT/Transformers** | Latest | NLP embeddings |
| **Pytesseract** | Latest | OCR text extraction |
| **Pillow** | Latest | Image processing |
| **Pandas** | Latest | Data processing |
| **Joblib** | Latest | Model serialization |
| **Flask-CORS** | Latest | Cross-origin requests |
| **Flask-Mail** | Latest | Email notifications |

### Database & Authentication
- **Firebase Firestore**: Real-time document database
- **Firebase Authentication**: Multi-provider auth (Email, Google)
- **Firebase Storage**: File uploads and documents

### Deployment
- **Frontend**: GitHub Pages / Vercel / Netlify
- **Backend**: Heroku / AWS / Railway / Google Cloud
- **CI/CD**: GitHub Actions (optional)

---

## 🏗️ Architecture

### System Design

```
┌─────────────────────────────────────────────────────────────────────┐
│                         React Frontend (clinical-app)               │
│  ┌──────────┬──────────┬──────────┬──────────┬──────────────┐     │
│  │ Login    │ Register │Dashboard │Analyze  │ Theme Toggle │     │
│  │ Page     │ Page     │ (Charts) │ Results │ (Dark/Light) │     │
│  └──────────┴──────────┴──────────┴──────────┴──────────────┘     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │         Firebase Auth + Context API State Management         │  │
│  └──────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────┬────────────────────────┘
                                           │
                                 HTTPS/Bearer Token
                                           │
┌──────────────────────────────────────────▼────────────────────────┐
│                      Flask Backend (backend/app)                   │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │  ⚙️ JWT Verification Middleware (@verify_firebase_token)     │ │
│  └──────────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │  Public Routes                   Protected Routes          │   │
│  │  ├─ GET /                       ├─ POST /predict          │   │
│  │  ├─ GET /health                 └─ POST /upload           │   │
│  │  └─ GET /firebase-status                                  │   │
│  └────────────────────────────────────────────────────────────┘   │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │         ML/AI Analysis Engine                              │   │
│  │  ├─ Scikit-learn Classifier (Risk Assessment)             │   │
│  │  ├─ BERT Embeddings (Symptom Extraction)                  │   │
│  │  └─ Pytesseract OCR (Document Processing)                 │   │
│  └────────────────────────────────────────────────────────────┘   │
└─────────────┬─────────────────────────┬────────────────────────────┘
              │                         │
         Firebase Auth              Firebase Firestore
              │                         │
              └─────────────┬───────────┘
                            │
            ┌───────────────▼──────────────┐
            │  Firebase Cloud Services     │
            │  ├─ Authentication          │
            │  ├─ Real-time Database      │
            │  ├─ Cloud Storage           │
            │  └─ Admin Verification      │
            └────────────────────────────┘
```

### Data Flow

1. **User Authentication**
   - User signs up/logs in via Firebase
   - Frontend stores JWT token in localStorage
   - Token sent with each API request in Authorization header

2. **Clinical Text Analysis**
   - User inputs text or uploads file
   - Frontend sends to Flask backend with Bearer token
   - Middleware verifies JWT token
   - ML models analyze text
   - Results returned to frontend
   - Dashboard displays results with visualizations

3. **Document Processing (OCR)**
   - User uploads scanned document (PDF/PNG/JPG)
   - Pytesseract extracts text
   - Text passed to analysis models
   - Results returned

4. **Data Persistence**
   - Analysis results saved to Firestore
   - User-specific data isolation
   - Historical analysis tracking
   - Timestamp-based sorting

---

## 📁 Project Structure

```
Clinical app/
├── 📄 README.md                          (This file)
├── 📄 AUTH_README.md                     (Authentication docs)
│
├── backend/                              (Python Flask API)
│   ├── app/
│   │   ├── 📄 app.py                     (Flask application - 350 lines)
│   │   ├── 📄 auth_middleware.py         (Firebase JWT verification)
│   │   ├── 📄 firebase_admin_config.py   (Firebase initialization)
│   │   ├── 📄 utils.py                   (Helper functions)
│   │   ├── 📄 requirements.txt           (Python dependencies)
│   │   ├── 📄 serviceAccountKey.json     (Firebase credentials)
│   │   ├── 📄 model.pkl                  (Trained classifier model)
│   │   ├── 📄 bert_model.pkl             (BERT embeddings)
│   │   ├── 📄 test_step2.py              (Auth middleware tests)
│   │   ├── config/                       (Configuration)
│   │   │   ├── 📄 __init__.py
│   │   │   └── 📄 settings.py
│   │   └── logs/                         (Application logs)
│   ├── model/
│   │   └── 📄 train_model.py             (ML model training)
│   └── data/
│       └── 📄 cleaned_data.csv           (Training dataset)
│
├── clinical-app/                         (React Frontend)
│   ├── 📄 package.json                   (Dependencies & scripts)
│   ├── 📄 package-lock.json
│   ├── public/
│   │   ├── 📄 index.html                 (HTML template)
│   │   ├── 📄 manifest.json              (PWA manifest)
│   │   └── 📄 robots.txt
│   ├── src/
│   │   ├── 📄 App.js                     (Main router)
│   │   ├── 📄 index.js                   (React entry point)
│   │   ├── 📄 firebase.js                (Firebase config)
│   │   ├── 📄 Dashboard.js               (Main dashboard)
│   │   ├── 📄 Login.js                   (Login page)
│   │   ├── 📄 Register.js                (Registration page)
│   │   ├── 📄 LandingPage.js             (Landing page)
│   │   ├── 📄 ThemeContext.js            (Theme provider)
│   │   ├── 📄 ThemeToggle.js             (Theme toggle button)
│   │   ├── 📄 *.css                      (Stylesheets)
│   │   ├── 📄 reportWebVitals.js         (Performance metrics)
│   │   ├── 📄 setupTests.js              (Jest config)
│   │   └── config/
│   ├── build/                            (Production build)
│   └── node_modules/                     (Dependencies)
│
└── src/                                  (Shared config)
    └── 📄 firebase.js                    (Shared Firebase config)
```

---

## 🚀 Setup Instructions

### Prerequisites
- **Node.js** 14+ and npm
- **Python** 3.8+
- **Firebase Project** (free tier works)
- **Tesseract OCR** (for document processing)
- **Git** (optional but recommended)

### Backend Setup

#### 1. Install Python Dependencies

```bash
cd backend/app
pip install -r requirements.txt
```

**Dependencies include**:
- Flask (web framework)
- firebase-admin (Firebase backend SDK)
- scikit-learn (ML models)
- pytesseract (OCR)
- pandas (data processing)
- flask-cors (cross-origin requests)

#### 2. Set Up Firebase Credentials

Place your Firebase service account key as `serviceAccountKey.json`:

```bash
# Download from Firebase Console → Project Settings → Service Accounts
# Copy to: backend/app/serviceAccountKey.json
```

#### 3. Environment Variables

Create `.env` file in `backend/app/`:

```env
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

#### 4. Install Tesseract OCR

**Windows**:
```bash
# Download from: https://github.com/UB-Mannheim/tesseract/wiki
# Install to: C:\Program Files\Tesseract-OCR
# Installer will set PATH automatically
```

**macOS**:
```bash
brew install tesseract
```

**Linux**:
```bash
sudo apt-get install tesseract-ocr
```

#### 5. Start Backend Server

```bash
cd backend/app
python -m flask run
```

Server runs at: `http://localhost:5000`

---

### Frontend Setup

#### 1. Install Node Dependencies

```bash
cd clinical-app
npm install
```

#### 2. Configure Firebase

Edit `src/firebase.js` with your Firebase project credentials:

```javascript
const firebaseConfig = {
  apiKey: "YOUR_API_KEY",
  authDomain: "YOUR_PROJECT.firebaseapp.com",
  projectId: "YOUR_PROJECT_ID",
  storageBucket: "YOUR_PROJECT.appspot.com",
  messagingSenderId: "YOUR_SENDER_ID",
  appId: "YOUR_APP_ID"
};
```

#### 3. Start Development Server

```bash
cd clinical-app
npm start
```

Frontend runs at: `http://localhost:3000`

#### 4. Build for Production

```bash
npm run build
```

Creates optimized build in `clinical-app/build/`

---

## 📡 API Documentation

### Authentication

All protected endpoints require Firebase JWT token in Authorization header:

```
Authorization: Bearer <firebase_id_token>
```

See [AUTH_README.md](AUTH_README.md) for detailed authentication flow.

### Public Endpoints

#### GET /
Health check endpoint.

**Response**:
```json
{
  "message": "API is running"
}
```

#### GET /health
Service status.

**Response**:
```json
{
  "status": "healthy",
  "firebase": "connected"
}
```

#### GET /firebase-status
Firebase connection status.

**Response**:
```json
{
  "firebase_initialized": true,
  "admin_sdk": "operational"
}
```

### Protected Endpoints

#### POST /predict
Analyze clinical text and extract health insights.

**Headers**:
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Request Body**:
```json
{
  "text": "Patient presents with persistent chest pain and shortness of breath"
}
```

**Response**:
```json
{
  "risk": "High",
  "score": 85,
  "symptoms": ["chest pain", "shortness of breath"],
  "recommendation": "Immediate medical attention recommended",
  "user_id": "firebase_uid_here"
}
```

#### POST /upload
Process uploaded document (OCR + analysis).

**Headers**:
```
Authorization: Bearer <token>
Content-Type: multipart/form-data
```

**Request Body**:
```
file: <binary_file_data>
```

**Response**:
```json
{
  "text_extracted": "Extracted text from document via OCR",
  "analysis": {
    "risk": "Medium",
    "score": 65,
    "symptoms": ["..."],
  },
  "user_id": "firebase_uid_here"
}
```

---

## 🖼️ Screenshots

### Coming Soon
- Dashboard with theme toggle
- Dark mode view
- Light mode view
- Analysis results display
- Login/Register screens
- OCR document upload

*Screenshots to be added for project documentation*

---

## 💡 Technical Highlights

### 1. Modern React Architecture
- Functional components with hooks
- React Router v6 for navigation
- Context API for global state (theme)
- Firebase SDK integration
- Real-time Firestore updates

### 2. Secure Backend Design
- Firebase JWT token verification
- Decorator-based middleware (`@verify_firebase_token`)
- Protected route endpoints
- CORS configuration for security
- Request-scoped user context

### 3. ML/AI Implementation
- Scikit-learn classifier for risk assessment
- BERT embeddings for symptom extraction
- Pre-trained models (model.pkl, bert_model.pkl)
- Model serialization with Joblib
- Real-time prediction pipeline

### 4. OCR Processing
- Pytesseract integration
- Multi-format document support
- Automatic text extraction
- Pipeline integration with ML models

### 5. Premium UI/UX
- CSS variables for theming
- Dark/light/gold color schemes
- Smooth 0.3s transitions
- System preference detection
- localStorage persistence
- Responsive mobile design

### 6. Database Architecture
- Firestore real-time database
- User-scoped data isolation
- Timestamp indexing
- Scalable document structure

---

## 🔮 Future Improvements

### Phase 2: Enhanced Analysis
- [ ] Multi-language support
- [ ] Advanced symptom categorization
- [ ] Predictive health trending
- [ ] Comparative patient analysis
- [ ] Custom risk weights

### Phase 3: Clinical Features
- [ ] HIPAA compliance enhancements
- [ ] Audit logging
- [ ] Role-based access (Admin/Doctor/Patient)
- [ ] Prescription integration
- [ ] Lab results integration

### Phase 4: Advanced ML
- [ ] Transfer learning models
- [ ] Custom model fine-tuning
- [ ] Federated learning for privacy
- [ ] Model explainability (SHAP/LIME)
- [ ] Ensemble methods

### Phase 5: Infrastructure
- [ ] Containerization (Docker)
- [ ] Kubernetes deployment
- [ ] Microservices architecture
- [ ] GraphQL API
- [ ] Caching layer (Redis)

### Phase 6: Analytics & Insights
- [ ] Admin dashboard
- [ ] Usage analytics
- [ ] Performance monitoring
- [ ] A/B testing framework
- [ ] Error tracking (Sentry)

---

## 📊 Resume-Worthy Technical Accomplishments

✅ **Full-Stack Development**: React + Flask + Firebase (modern MERN-style stack with Python)

✅ **AI/ML Integration**: Scikit-learn classifier + BERT embeddings in production

✅ **Authentication Security**: Firebase JWT tokens + backend verification middleware

✅ **OCR Pipeline**: Multi-format document processing with Tesseract

✅ **Real-time Database**: Firestore integration with user data isolation

✅ **Premium UI/UX**: Dark/light theme with smooth animations and responsive design

✅ **API Design**: RESTful endpoints with proper HTTP status codes and error handling

✅ **Secure Backend**: Decorator-based authentication middleware and protected routes

✅ **Performance**: Optimized build pipeline, code splitting, lazy loading

✅ **Scalability**: User-scoped data, efficient queries, model serialization

---

## 📝 Notes

- **Database**: Firebase Firestore (real-time, scalable, free tier available)
- **Deployment**: Frontend on GitHub Pages/Vercel, Backend on Heroku/Railway
- **Testing**: Auth middleware includes test suite (test_step2.py)
- **Monitoring**: Performance metrics with reportWebVitals.js

For authentication-specific documentation, see [AUTH_README.md](AUTH_README.md).

---

## 📞 Support & Troubleshooting

### Common Issues

**Frontend won't start**
```bash
cd clinical-app
rm -rf node_modules
npm install
npm start
```

**Backend won't connect to Firebase**
- Verify `serviceAccountKey.json` is in `backend/app/`
- Check Firebase project is active
- Ensure credentials are not expired

**OCR not working**
- Verify Tesseract is installed
- Check path: `C:\Program Files\Tesseract-OCR\tesseract.exe` (Windows)
- Restart Flask server after installation

**Auth token errors**
- Clear browser localStorage
- Log out and log back in
- Check Firebase project settings

---

## 📄 License

This project is proprietary. All rights reserved.

---

**Last Updated**: May 27, 2026  
**Status**: ✅ Production Ready  
**Version**: 2.0 (Step 2 - Authentication Complete)
