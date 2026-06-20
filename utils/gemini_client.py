import os
import google.generativeai as genai
from dotenv import load_dotenv

from dotenv import load_dotenv
load_dotenv(dotenv_path=".env")
print("API KEY =", os.getenv("GOOGLE_API_KEY"))
print("CONFIG CALLED")

genai.configure(
    api_key="AQ.Ab8RN6IQrxMkKAPaL6dcAnIsnck2sYO-lD64T03s6NN6dZCAqg"
)

model = genai.GenerativeModel("gemini-2.5-flash")


def get_gemini_response(prompt):
    response = model.generate_content(prompt)
    return response.text