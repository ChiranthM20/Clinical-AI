# 🔐 Authentication System

Complete Firebase + JWT authentication for the AI Clinical Support System.

---

## 📋 Overview

- **Frontend Auth**: Firebase Authentication (Email/Password + Google OAuth)
- **Backend Verification**: Firebase Admin SDK with JWT tokens
- **Communication**: Bearer tokens in Authorization header
- **User Isolation**: All data scoped to authenticated user UID

---

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | Firebase SDK 12.x | Email/Password/OAuth login |
| **Backend** | Firebase Admin SDK 6.0+ | JWT token verification |
| **API Auth** | Bearer Tokens (JWT) | Stateless request authentication |
| **Data Storage** | Firestore | User-scoped collections |

---

## 🔄 Authentication Flow

```
Frontend (React)           Backend (Flask)         Firebase
     │                          │                      │
     ├─ Sign up/Login ─────────>│                      │
     │                          ├─ Verify ────────────>│
     │                          │<─ Issue JWT ─────────┤
     │<─ Get JWT token ─────────┤                      │
     │                          │                      │
     ├─ POST /predict ─────────>│                      │
     │   + Bearer token         ├─ Verify token ──────>│
     │                          │<─ Verified ──────────┤
     │                          │ Process & isolate    │
     │<─ 200 OK + results ──────┤                      │
     │   + user_id              │                      │
```

---

## ✨ Features Implemented

✅ **Email/Password Authentication**
- Sign up with email validation
- Secure password storage
- Email verification flow

✅ **Google OAuth Integration**
- One-click Google sign-in
- Auto user creation/login
- Email auto-populated

✅ **Session Management**
- localStorage persistence
- Auto-login on page refresh
- Logout clears session

✅ **Protected API Endpoints**
- /predict - Requires authentication
- /upload - Requires authentication
- Both endpoints verify Bearer tokens

✅ **User Data Isolation**
- Each user sees only their data
- Firestore scoped by user UID
- Backend enforces user_id from token

---

## 🔒 Backend Security Architecture

### JWT Verification Middleware

**File**: `backend/app/auth_middleware.py`

```python
@verify_firebase_token
def predict():
    # Middleware verifies token before route executes
    user_id = g.user_id  # Extracted from token
    # Process request with user isolation
    return jsonify({"risk": "...", "user_id": user_id}), 200
```

### Verification Flow

1. **Extract**: Get Authorization header - "Bearer token"
2. **Verify**: Firebase Admin SDK validates signature using RSA public key
3. **Decode**: Extract claims (uid, email, exp)
4. **Validate**: Check expiration, issuer, audience
5. **Store**: Place user_id in Flask g object (request-scoped)
6. **Process**: Route handler uses g.user_id for queries
7. **Return**: Send response with user_id included

### Error Handling

| Status | Reason |
|--------|--------|
| **401** | Missing header, invalid format, expired token |
| **503** | Firebase service unavailable |

---

## 🔐 Protected Routes

| Endpoint | Method | Auth | Purpose |
|----------|--------|------|---------|
| `/predict` | POST | ✅ Required | Analyze clinical text |
| `/upload` | POST | ✅ Required | Process document (OCR) |
| `/health` | GET | ❌ Public | Backend status check |
| `/` | GET | ❌ Public | API health endpoint |

**Request Format**:
```
Authorization: Bearer <firebase_id_token>
Content-Type: application/json (for /predict)
Content-Type: multipart/form-data (for /upload)
```

---

## 📱 Firestore Security

### Collections & User Isolation

```
firestore/
├── reports/
│   ├── doc1 { userId: "uid123", data: {...} }
│   ├── doc2 { userId: "uid456", data: {...} }
│   └── doc3 { userId: "uid123", data: {...} }
```

### Security Rules

```javascript
match /reports/{document=**} {
  allow read, write: if request.auth.uid == resource.data.userId;
  allow create: if request.auth.uid == request.resource.data.userId;
}
```

**Effect**: Users can only access their own data

---

## 🧪 Testing Summary

### Test 1: Analyze Text (Requires Token)

```bash
# With valid token - 200 OK
curl -X POST http://localhost:5000/predict \
  -H "Authorization: Bearer token_here" \
  -H "Content-Type: application/json" \
  -d '{"text": "chest pain"}'

# Response:
# {"risk": "High", "score": 85, "symptoms": [...], "user_id": "uid123"}

# Without token - 401 Unauthorized
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "chest pain"}'

# Response:
# {"error": "Unauthorized", "message": "Missing Authorization header"}
```

### Test 2: Upload File (Requires Token)

Same flow - token required, 401 without it.

### Test 3: Browser Console

1. Sign in to Dashboard
2. Click "Analyze" or upload file
3. Open DevTools (F12 → Console):
   ```
   Retrieving Firebase JWT token...
   ✅ Firebase JWT Token retrieved successfully
   Token length: 1050
   Calling backend...
   Response: {risk: "High", score: 85, ...}
   ```

4. Network Tab shows:
   - Request headers include Authorization: Bearer token
   - Response status: 200 OK

---

## 🔑 Key Security Improvements

| Improvement | Implementation |
|-------------|-----------------|
| **Token Verification** | Backend verifies every request |
| **User Isolation** | Data queries scoped to user UID |
| **No Passwords** | Backend never sees passwords |
| **Token Expiration** | Firebase auto-refreshes after 1 hour |
| **HTTPS Enforced** | Production requires SSL/TLS |
| **Stateless API** | No server sessions needed |
| **Error Handling** | 401 status codes with clear messages |

---

## 📊 Architecture Summary

```
┌─────────────────────────┐
│ React Frontend          │
│ (clinical-app/)         │
│ ├─ Login.js             │
│ ├─ Register.js          │
│ └─ Dashboard.js         │
└────────────┬────────────┘
             │
      Authorization Header
      Bearer JWT Token
             │
             ▼
┌─────────────────────────┐
│ Flask Backend           │
│ (backend/app/)          │
│ ├─ verify_firebase_     │
│ │  token decorator      │
│ ├─ /predict            │
│ └─ /upload             │
└────────────┬────────────┘
             │
    Firebase Admin SDK
    (Token Verification)
             │
             ▼
┌─────────────────────────┐
│ Firebase Services       │
│ ├─ Authentication       │
│ ├─ Admin SDK            │
│ └─ Firestore            │
└─────────────────────────┘
```

---

## 🚀 Future Improvements

- [ ] Refresh token rotation for enhanced security
- [ ] Rate limiting on authentication endpoints
- [ ] MFA (Multi-Factor Authentication) support
- [ ] Device fingerprinting for suspicious activity
- [ ] Session timeout on inactivity
- [ ] Audit logging for security events

---

## ✅ Implementation Status

| Feature | Status | Notes |
|---------|--------|-------|
| Email/Password Auth | ✅ Complete | Firebase managed |
| Google OAuth | ✅ Complete | Social login working |
| JWT Verification | ✅ Complete | Backend validated |
| Protected Routes | ✅ Complete | /predict, /upload secured |
| User Isolation | ✅ Complete | Firestore scoped by UID |
| Error Handling | ✅ Complete | 401 errors caught |

---

**Last Updated**: May 27, 2026  
**Status**: Production Ready  
**Security Level**: Secure with industry best practices

For project overview, see [README.md](README.md).
