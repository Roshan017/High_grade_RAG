import sys
import os
import numpy as np

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.Reranking.MMR import mmr

def test_mmr_robustness():
    # Mock data
    query_emb = [1.0, 0.0, 0.0]
    
    # 1. Test with empty chunks
    print("Test 1: Empty chunks")
    results = mmr(query_emb, [], k=5)
    assert results == []
    print("  Pass")

    # 2. Test with k > len(chunks)
    print("Test 2: k > len(chunks)")
    chunks = [
        {"content": "a", "embedding": [1.0, 0.0, 0.0], "score": 0.1},
        {"content": "b", "embedding": [0.0, 1.0, 0.0], "score": 0.2}
    ]
    # Set threshold to 0 to ensure both are picked despite b having 0 similarity to query
    results = mmr(query_emb, chunks, k=5, relevance_threshold=0.0)
    assert len(results) == 2
    print("  Pass")


    # 3. Test with low relevance threshold
    print("Test 3: Relevance threshold filtering")
    chunks = [
        {"content": "highly relevant", "embedding": [0.99, 0.0, 0.0], "score": 0.01},
        {"content": "not relevant", "embedding": [0.0, 1.0, 0.0], "score": 0.9}
    ]
    # first one is always picked regardless of threshold in current logic
    # second one similarity to query [1,0,0] . [0,1,0] is 0.0
    results = mmr(query_emb, chunks, k=5, relevance_threshold=0.5)
    assert len(results) == 1
    assert results[0]["content"] == "highly relevant"
    print("  Pass")

    print("\nAll MMR robustness tests passed!")

if __name__ == "__main__":
    try:
        test_mmr_robustness()
    except Exception as e:
        print(f"Test failed: {str(e)}")
        sys.exit(1)
