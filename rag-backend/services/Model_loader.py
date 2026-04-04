from sentence_transformers import SentenceTransformer
import nltk


_MODEL_INSTANCE = None

def get_model():
    global _MODEL_INSTANCE
    if _MODEL_INSTANCE is None:
        try:
            nltk.data.find("tokenizers/punkt")
        except LookupError:
            nltk.download("punkt")
        _MODEL_INSTANCE = SentenceTransformer("BAAI/bge-small-en-v1.5")
    return _MODEL_INSTANCE