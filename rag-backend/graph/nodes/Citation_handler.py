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

    details = {
    "pages": set(),
    "filenames": set()
    }

    for cit in citations:
        if not cit.get('metadatas'):
            continue

        for m in cit['metadatas']:
            page = m.get('page_number')
            file = m.get('filename')

            if page is not None:
                details["pages"].add(page)

            if file:
                details["filenames"].add(file)
    details["pages"] = sorted(details["pages"])
    details["filenames"] = list(details["filenames"])
    citations = f"The Content was taken from pages {details['pages']} from file {details['filenames']}"
    return {
        'final_answer': ans,
        'citations': citations
    }