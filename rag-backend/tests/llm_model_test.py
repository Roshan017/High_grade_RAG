import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from llm.gemini_llm_call import Gemini_LLM_Call
from dev_actions.get_gemini_key import get_gemini_key
from google import genai

def test_llm_call():
    print("--- Characterizing Gemini Model ---")
    system_prompt = "You are a helpful assistant."
    user_prompt = "Hello, what model are you?"
    
    try:
        response = Gemini_LLM_Call(system_prompt, user_prompt)
        print(f"Response: {response}")
    except Exception as e:
        print(f"Error calling LLM: {e}")

def list_available_models():
    print("\n--- Listing Available Models ---")
    try:
        client = genai.Client(api_key=get_gemini_key())
        models = list(client.models.list())
        for m in models:
            print(f"- {m.name}")
    except Exception as e:
        print(f"Error listing models: {e}")

if __name__ == "__main__":
    test_llm_call()
    # list_available_models()