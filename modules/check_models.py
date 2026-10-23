import google.generativeai as genai

# Replace with your actual Gemini API key
api_key = "AQ.Ab8RN6KA2X6-7-MHlrw24kwxnTAqtHM6rk3sti0wewiEThaD1Q"
genai.configure(api_key=api_key)

print("Available Models supporting generateContent:")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)
