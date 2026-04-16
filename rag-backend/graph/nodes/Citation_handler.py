from graph.state import RAG_State
from services.ID_extractor import extract_ids, remove_ids
from services.Vector_store.Retrive_from_chroma import retrive_by_id


def Citation_handler(state: RAG_State):

    ans = state.get('final_answer', "")
    ids_to_metadata = state.get('ids_to_metadata', {})


    cited_ids = list(set(extract_ids(ans)))
    ans  = remove_ids(ans)
    chunk_ids = []

    for ids in cited_ids:
        chunk_ids.append(ids_to_metadata[ids]['chunk_id'])


    citations = []

    for ids in chunk_ids:
        citations.append(retrive_by_id(ids))
    
    # print("Citations: ",citations)

    unique_citations = []
    seen = set()
    for cit in citations:
        if not cit.get('metadatas'):
            continue
        for m in cit['metadatas']:
            page = m.get('page_number')
            file = m.get('filename')
            if file and page is not None:
                pair = (file, page)
                if pair not in seen:
                    unique_citations.append({'file': file, 'page': page})
                    seen.add(pair)
    
    return {
        'final_answer': ans,
        'citations': unique_citations
    }