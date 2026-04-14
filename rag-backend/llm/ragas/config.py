from google import genai
from ragas.llms import llm_factory
from dev_actions.get_gemini_key import get_gemini_key
from ragas.embeddings import GoogleEmbeddings
from typing import List
from langfuse import observe

# Bridge the gap between modern Ragas embeddings and legacy metric expectations
class CompatibleGoogleEmbeddings(GoogleEmbeddings):
    def embed_query(self, text: str) -> List[float]:
        return self.embed_text(text)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return self.embed_texts(texts)

    async def aembed_query(self, text: str) -> List[float]:
        return await self.aembed_text(text)

    async def aembed_documents(self, texts: List[str]) -> List[List[float]]:
        return await self.aembed_texts(texts)

def get_embeddings():
    api_key = get_gemini_key()
    client = genai.Client(api_key=api_key)

    embeddings = CompatibleGoogleEmbeddings(
        model="gemini-embedding-001",
        client=client
    )

    return embeddings
def get_llm():
    api_key = get_gemini_key()

    client = genai.Client(api_key=api_key)
    llm = llm_factory(
        model="gemini-3.1-flash-lite-preview",
        provider="google",
        client=client
    )

    return llm
