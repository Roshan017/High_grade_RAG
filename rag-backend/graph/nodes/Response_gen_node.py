from graph.state import RAG_State
from llm.gemini_llm_call import Gemini_LLM_Call
from services.Reranking.MMR import mmr  
from langfuse import observe

@observe(name='RAG_Response_Generation')
def Response_gen_node(state: RAG_State):

    query = state.get('query', "")

    query_emb = state.get('query_embedding', [])

    ret_chunks = state.get('retrieved_chunks', [])

    context = []
    for doc in ret_chunks:
        context.append({
            "content": doc["document"],
            "metadata": doc["metadata"],
            "score": doc["distance"],
            "embedding": doc["embeddings"]
        })


    context = sorted(context, key=lambda x: x["score"])

    context = mmr(query_emb, context, k=5, lambda_param=0.7, relevance_threshold=0.4)


    ranked_context = []
    for chunk in context:
        ranked_context.append({
            "content": chunk["content"],
            "metadata": chunk["metadata"],
            "score": chunk["score"],
        })

   

    ids_to_metadata = {}
    formatted_context = ""


    for i , chunk in enumerate(ranked_context):
        cid = i + 1

        ids_to_metadata[cid] = {
            "chunk_id": chunk['metadata'].get('chunk_id'),
            "filename": chunk['metadata'].get('filename')
        }

        formatted_context +=f"[{cid}] {chunk['content']}\n\n"
    
    print("Res Node: Formatted Context:", formatted_context)
    print("Res Node: IDs to Metadata:", ids_to_metadata)

    system_prompt = """
    You are a retrieval-augmented generation (RAG) assistant.

    Answer the user's question using ONLY the provided context.

    Strict Rules:
    1. Do NOT use any external knowledge.
    2. If the answer is not clearly present in the context, respond with:
    "I cannot answer this question based on the provided documents."
    3. If multiple parts of the context are relevant, combine them into a single answer.
    4. Cite the source of information using [number] (e.g., [1], [2]).
    5. Every factual statement MUST be supported by at least one citation.
    6. Only use citation numbers that exist in the provided context. Do not invent or guess citations.
    7. Avoid redundant citations; prefer the most relevant sources.
    8. Place citations immediately after the relevant sentence or claim.
    9. Do not include information that is not supported by the context.
    10. Base your answer strictly on the meaning of the provided context without adding interpretation.
    11. Keep the answer concise (3–5 sentences maximum), unless more detail is clearly required.
    """
    user_prompt = f"""
    Question:
    {query}

    Context:
    {formatted_context}

    Answer:
    """

    response = Gemini_LLM_Call(system_prompt, user_prompt, metadata='RAG_Response_Generation')
    if not response:
        response = "Under Dev"
    print("Final Answer: ", response)
    
    return {
        'ids_to_metadata': ids_to_metadata,
        'final_answer': response,
        'final_answer_complete': True
    }