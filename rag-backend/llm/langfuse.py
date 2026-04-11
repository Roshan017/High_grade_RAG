import os
from langfuse import get_client
import base64
from openinference.instrumentation.google_genai import GoogleGenAIInstrumentor

_initialized = False


def init_langfuse():
    """
    Initializes Langfuse client and instruments Google GenAI.
    """
    global _initialized

    if _initialized:
        return get_client()

    sk = os.getenv("LANGFUSE_SECRET_KEY")
    pk = os.getenv("LANGFUSE_PUBLIC_KEY")
    host = os.getenv(
        "LANGFUSE_BASE_URL",
        "https://cloud.langfuse.com"
    )
    if not pk or not sk:
        print("⚠️ Langfuse keys missing in .env. Tracing may be limited.")
        return None
    
    auth = base64.b64encode(f"{pk}:{sk}".encode()).decode()
    os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = f"{host}/api/public/otel"
    os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = f"Authorization=Basic {auth}"
    os.environ["OTEL_EXPORTER_OTLP_PROTOCOL"] = "http/protobuf"
    os.environ["OTEL_SERVICE_NAME"] = "rag-app"

    GoogleGenAIInstrumentor().instrument()

    langfuse = get_client()

    if langfuse.auth_check():
        print("✅ Langfuse: Authentication successful.")
    else:
        print("❌ Langfuse: Authentication failed. Check your keys in .env")

    _initialized = True
    return langfuse