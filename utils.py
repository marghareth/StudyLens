import os
import json
import re
import google.generativeai as genai
from dotenv import load_dotenv

# Load the .env file so os.environ can read it
load_dotenv()

try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception:
    API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini with the key
genai.configure(api_key=API_KEY)

# Create the model object — everything uses this
model = genai.GenerativeModel("gemini-2.5-flash")


def call_gemini(prompt):
    """
    Sends a prompt to Gemini and returns the response text.
    Returns None if the call fails.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Gemini API error: {e}")
        return None


def parse_json_response(text):
    """
    Extracts a JSON object from Gemini's response text.
    Handles cases where Gemini adds extra text around the JSON.
    """
    try:
        # Try direct parsing first
        return json.loads(text)
    except json.JSONDecodeError:
        # If that fails, find JSON pattern inside the text
        match = re.search(r'\{.*?\}', text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                return None
    return None


def validate_input(notes):
    """
    Checks if the user's notes are usable.
    Returns (is_valid, error_message).
    """
    if not notes or notes.strip() == "":
        return False, "Please paste some notes first."

    if len(notes.strip()) < 50:
        return False, "Notes are too short. Please paste more content."

    if len(notes) > 15000:
        return False, "Notes are too long. Please paste a smaller section (under 15,000 characters)."

    return True, None