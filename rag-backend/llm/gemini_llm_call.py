from dev_actions.get_gemini_key import get_gemini_key
from google import genai

GEMINI_KEY = get_gemini_key()
client = genai.Client(api_key=GEMINI_KEY)


def Gemini_LLM_Call(system_prompt: str, user_prompt: str, metadata: str = None, model="gemini-3.1-flash-lite-preview", config=None):
    """
    Synchronous call to Gemini LLM with Langfuse tracing.
    """
    if not client:
        raise RuntimeError("GenAI Client not initialized")

    response = client.models.generate_content(
        model=model,
        contents=user_prompt,
        config={
            'system_instruction': system_prompt,
            **(config or {})
        }
    )

    if not response or not response.text:
        raise RuntimeError("Response not generated or empty")

    
   
    return response.text.strip()

async def Gemini_LLM_Call_Async(system_prompt: str, user_prompt: str, metadata: str = None, model="gemini-3.1-flash-lite-preview", config=None):
    """
    Asynchronous call to Gemini LLM with Langfuse tracing.
    """
    if not client:
        raise RuntimeError("GenAI Client not initialized")

    response = await client.aio.models.generate_content(
        model=model,
        contents=user_prompt,
        config={
            'system_instruction': system_prompt,
            **(config or {})
        }
    )

    if not response or not response.text:
        raise RuntimeError("Response not generated or empty")

    
    
    return response.text.strip()

