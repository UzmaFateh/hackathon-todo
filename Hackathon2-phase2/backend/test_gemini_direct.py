import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
print(f"API Key found: {api_key[:5]}...{api_key[-5:] if api_key else 'None'}")

if not api_key or "CHANGE_ME" in api_key:
    print("Error: API Key is invalid or placeholder.")
    exit(1)

try:
    genai.configure(api_key=api_key)
    models_to_try = ['gemini-2.0-flash', 'gemini-1.5-flash', 'gemini-pro']
    
    for model_name in models_to_try:
        print(f"Testing model: {model_name}...")
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content("Hello")
            print(f"✅ Success with {model_name}!")
            print(response.text)
            break
        except Exception as e:
            print(f"❌ Failed with {model_name}: {e}")
except Exception as e:
    print(f"Error: {e}")
