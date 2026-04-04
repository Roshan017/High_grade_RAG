from services.Model_loader import get_model
from typing import Dict, List, Any


def embed_texts(texts: List[str]) -> List[List[float]]:
    """
    Embedd a List of Texts using BGE Model.
    """
    model = get_model()
    
    formatted_texts =  [text.strip().replace("\n", " ") for text in texts]

    embeddings = model.encode(formatted_texts, normalize_embeddings=True, show_progress_bar=True)

    return embeddings.tolist()
   

def embed_query(query: str) -> List[float]:
    """
    Embedd a Query using BGE Model.
    """
    model = get_model()
    instruction = "Represent this sentence for searching relevant passages: "
    embedding = model.encode(instruction + query, normalize_embeddings=True)
    return embedding.tolist()