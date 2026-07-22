#!/usr/bin/env python
"""
STEP 2: Practical Test Script
Test Firebase JWT verification without needing a real token

Run this after starting Flask:
  python test_step2.py

This script:
1. Tests public routes (no auth required)
2. Tests protected routes with missing token (should fail)
3. Shows how to use the auth middleware
4. Demonstrates all error scenarios
"""

import requests
import json
from colorama import Fore, Style

BASE_URL = "http://localhost:5000"

def print_section(title):
    print(f"\n{Fore.CYAN}{'='*70}")
    print(f"{title:^70}")
    print(f"{'='*70}{Style.RESET_ALL}\n")

def print_request(method, path, headers=None, json_data=None):
    print(f"{Fore.YELLOW}{method} {path}{Style.RESET_ALL}")
    if headers:
        for k, v in headers.items():
            if 'Authorization' in k:
                v = v[:20] + "..." if len(str(v)) > 20 else v
            print(f"  {k}: {v}")
    if json_data:
        print(f"  Body: {json.dumps(json_data, indent=2)}")

def print_response(response):
    status_color = Fore.GREEN if response.status_code == 200 else Fore.RED
    print(f"\n{status_color}Response: {response.status_code}{Style.RESET_ALL}")
    try:
        data = response.json()
        print(json.dumps(data, indent=2))
    except:
        print(response.text)

def test_public_routes():
    """Test public routes (no authentication required)"""
    print_section("TEST 1: PUBLIC ROUTES (No Authentication)")
    
    # Test /health endpoint
    print("Testing GET /health (Should succeed)")
    print_request("GET", "/health")
    response = requests.get(f"{BASE_URL}/health")
    print_response(response)
    assert response.status_code == 200, "Health check should return 200"
    print(f"{Fore.GREEN}✓ PASS{Style.RESET_ALL}")

def test_missing_token():
    """Test protected route without token"""
    print_section("TEST 2: PROTECTED ROUTE WITHOUT TOKEN")
    
    print("Testing POST /predict without Authorization header")
    print("Expected: 401 Unauthorized")
    print_request("POST", "/predict", 
                 json_data={"text": "I have chest pain"})
    
    response = requests.post(
        f"{BASE_URL}/predict",
        headers={"Content-Type": "application/json"},
        json={"text": "I have chest pain"}
    )
    print_response(response)
    assert response.status_code == 401, "Should reject missing token"
    data = response.json()
    assert "Missing Authorization header" in data.get("message", ""), \
        "Should indicate missing header"
    print(f"{Fore.GREEN}✓ PASS - Correctly rejected missing token{Style.RESET_ALL}")

def test_invalid_header_format():
    """Test with invalid Authorization header format"""
    print_section("TEST 3: INVALID HEADER FORMAT")
    
    print("Testing POST /predict with wrong header format")
    print("Expected: 401 Unauthorized")
    print_request("POST", "/predict",
                 headers={"Authorization": "Basic invalid"},
                 json_data={"text": "I have chest pain"})
    
    response = requests.post(
        f"{BASE_URL}/predict",
        headers={
            "Content-Type": "application/json",
            "Authorization": "Basic invalid"
        },
        json={"text": "I have chest pain"}
    )
    print_response(response)
    assert response.status_code == 401, "Should reject invalid format"
    data = response.json()
    assert "Bearer" in data.get("message", ""), \
        "Should indicate Bearer token required"
    print(f"{Fore.GREEN}✓ PASS - Correctly rejected invalid format{Style.RESET_ALL}")

def test_empty_token():
    """Test with empty token"""
    print_section("TEST 4: EMPTY TOKEN")
    
    print("Testing POST /predict with empty Bearer token")
    print("Expected: 401 Unauthorized")
    print_request("POST", "/predict",
                 headers={"Authorization": "Bearer "},
                 json_data={"text": "I have chest pain"})
    
    response = requests.post(
        f"{BASE_URL}/predict",
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer "
        },
        json={"text": "I have chest pain"}
    )
    print_response(response)
    assert response.status_code == 401, "Should reject empty token"
    data = response.json()
    assert "empty" in data.get("message", "").lower(), \
        "Should indicate empty token"
    print(f"{Fore.GREEN}✓ PASS - Correctly rejected empty token{Style.RESET_ALL}")

def test_invalid_token():
    """Test with invalid token"""
    print_section("TEST 5: INVALID TOKEN")
    
    print("Testing POST /predict with invalid token")
    print("Expected: 401 Unauthorized")
    invalid_token = "invalid.token.here"
    print_request("POST", "/predict",
                 headers={"Authorization": f"Bearer {invalid_token}"},
                 json_data={"text": "I have chest pain"})
    
    response = requests.post(
        f"{BASE_URL}/predict",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {invalid_token}"
        },
        json={"text": "I have chest pain"}
    )
    print_response(response)
    assert response.status_code == 401, "Should reject invalid token"
    print(f"{Fore.GREEN}✓ PASS - Correctly rejected invalid token{Style.RESET_ALL}")

def test_upload_without_token():
    """Test /upload without token"""
    print_section("TEST 6: /upload WITHOUT TOKEN")
    
    print("Testing POST /upload without Authorization header")
    print("Expected: 401 Unauthorized")
    print_request("POST", "/upload")
    
    response = requests.post(
        f"{BASE_URL}/upload",
        files={"file": ("test.txt", "test content")}
    )
    print_response(response)
    assert response.status_code == 401, "Should reject missing token"
    print(f"{Fore.GREEN}✓ PASS - Correctly rejected missing token{Style.RESET_ALL}")

def test_auth_middleware_present():
    """Verify auth middleware is properly installed"""
    print_section("TEST 7: VERIFY AUTH MIDDLEWARE INSTALLED")
    
    print("Checking if auth_middleware module can be imported...")
    try:
        from app.auth_middleware import verify_firebase_token
        print(f"{Fore.GREEN}✓ verify_firebase_token decorator found{Style.RESET_ALL}")
        print(f"✓ Decorator docstring: {verify_firebase_token.__doc__[:100]}...")
        print(f"{Fore.GREEN}✓ PASS - Auth middleware properly installed{Style.RESET_ALL}")
    except ImportError as e:
        print(f"{Fore.RED}✗ FAIL - Could not import auth middleware: {e}{Style.RESET_ALL}")
        return False
    
    return True

def main():
    print(f"\n{Fore.CYAN}{Style.BRIGHT}")
    print("╔" + "="*68 + "╗")
    print("║" + " "*10 + "STEP 2: Firebase JWT Verification Tests" + " "*18 + "║")
    print("╚" + "="*68 + "╝")
    print(Style.RESET_ALL)
    
    print(f"\n{Fore.YELLOW}Testing against: {BASE_URL}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Make sure Flask backend is running!{Style.RESET_ALL}")
    
    try:
        # Test 1: Verify imports
        if not test_auth_middleware_present():
            return
        
        # Test 2: Public routes
        test_public_routes()
        
        # Test 3-6: Protected routes without valid token
        test_missing_token()
        test_invalid_header_format()
        test_empty_token()
        test_invalid_token()
        test_upload_without_token()
        
        print_section("ALL TESTS PASSED ✓")
        print(f"{Fore.GREEN}{Style.BRIGHT}")
        print("Summary:")
        print("  ✓ Public routes work without authentication")
        print("  ✓ Protected routes correctly reject missing tokens")
        print("  ✓ Protected routes correctly reject invalid tokens")
        print("  ✓ Auth middleware is properly installed")
        print("  ✓ All error responses are properly formatted")
        print(f"\n{Style.RESET_ALL}")
        
        print(f"{Fore.CYAN}Next steps:")
        print(f"  1. Get a real Firebase token from your React frontend")
        print(f"  2. Test with: curl -H 'Authorization: Bearer YOUR_TOKEN' \\")
        print(f"               http://localhost:5000/predict -d '{{\"text\": \"...\"}}' -H 'Content-Type: application/json'")
        print(f"  3. See STEP2_TESTING_GUIDE.md for more examples{Style.RESET_ALL}\n")
        
    except AssertionError as e:
        print(f"\n{Fore.RED}{Style.BRIGHT}✗ TEST FAILED: {e}{Style.RESET_ALL}\n")
        return False
    except Exception as e:
        print(f"\n{Fore.RED}{Style.BRIGHT}✗ ERROR: {e}{Style.RESET_ALL}")
        print(f"Make sure Flask backend is running at {BASE_URL}\n")
        print(f"Start with: cd 'd:\\Clinical app\\backend\\app' && python -m flask run")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
