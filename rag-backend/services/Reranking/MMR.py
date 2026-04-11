from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def mmr(query_emb, chunks, k=4, lambda_param=0.7, relevance_threshold=0.4):
    
    
    embeddings = [chunk["embedding"] for chunk in chunks]
    
    selected = []
    selected_indices = []
    
    sim_to_query = cosine_similarity([query_emb], embeddings)[0]
    first_idx = np.argmax(sim_to_query)
    selected.append(chunks[first_idx])
    selected_indices.append(first_idx)
    
    while len(selected) < k:
        mmr_scores = []
        
        for i in range(len(chunks)):
            if i in selected_indices:
                continue
            relevance = sim_to_query[i]

            if relevance < relevance_threshold:
                continue
            diversity = max([
                cosine_similarity([embeddings[i]], [embeddings[j]])[0][0]
                for j in selected_indices
            ])
            score = lambda_param * relevance - (1 - lambda_param) * diversity
            mmr_scores.append((score, i))
        _, best_idx = max(mmr_scores)
        selected.append(chunks[best_idx])
        selected_indices.append(best_idx)
    return selected