from dotenv import load_dotenv
import os

load_dotenv()


def get_gemini_key():
    api_key = os.getenv('GEMINI_API_KEY')

    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables")
    
    return api_key