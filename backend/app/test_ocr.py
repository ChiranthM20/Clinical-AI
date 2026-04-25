from PIL import Image
import pytesseract
import re

# IMPORTANT: set path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

img = Image.open("test.png")
text = pytesseract.image_to_string(img)

# Clean extracted text
cleaned = text.lower()
cleaned = re.sub(r'[^a-z\s]', ' ', cleaned)
cleaned = re.sub(r'\s+', ' ', cleaned)

print("Raw text:")
print(text)
print("\nCleaned text:")
print(cleaned)