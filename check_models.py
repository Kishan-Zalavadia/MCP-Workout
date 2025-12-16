# import google.generativeai as genai
# import os
# from dotenv import load_dotenv

# load_dotenv()

# # Hardcoded key from client.py just in case .env is not working or different
api_key = "your api key"
# genai.configure(api_key=api_key)

# print("List of available models:")
# for m in genai.list_models():
#     if 'generateContent' in m.supported_generation_methods:
#         print(m.name)

import google.generativeai as genai
import sys

# 1. SETUP YOUR API KEY
# Paste your actual key inside the quotes below
# api_key = "AIzaSyD..."

# if api_key == "AIzaSyD...":
#     print("❌ STOP: You need to paste your real API key in the code first!")
#     sys.exit(1)

# Configure the library
genai.configure(api_key=api_key)

def check_ai_connection():
    print("📡 Contacting Gemini API...")

    try:
        # 2. SELECT THE MODEL
        # We use 'gemini-1.5-flash' because it is the most reliable free model right now.
        model = genai.GenerativeModel('gemini-2.5-flash')

        # 3. SEND A SIMPLE REQUEST
        # We ask for a very short response to keep it fast.
        response = model.generate_content("Reply with exactly one word: 'Success'.")

        # 4. CHECK RESULT
        print(f"🤖 AI Response: {response.text}")
        print("✅ usage check passed! The API is working correctly.")

    except Exception as e:
        print(f"\n❌ API Call Failed!")
        print(f"Error Message: {e}")
        print("\nPossible reasons:")
        print("1. API Key is wrong.")
        print("2. Quota limit (429) - You might need to wait a few minutes.")

if __name__ == "__main__":
    check_ai_connection()
