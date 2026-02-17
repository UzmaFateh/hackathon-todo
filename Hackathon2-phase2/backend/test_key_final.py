import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

print(f"Key: {api_key[:10]}...")

try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("Hi")
    print("SUCCESS")
except Exception as e:
    err = str(e)
    if "403" in err:
        print("ERROR: 403 Forbidden (Invalid Key or API disabled)")
    elif "404" in err:
        print("ERROR: 404 Not Found (Model not available)")
    else:
        print(f"ERROR: {err[:100]}")
