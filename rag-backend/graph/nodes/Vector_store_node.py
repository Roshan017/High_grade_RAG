from graph.state import RAG_State
from services.Vector_store.Add_to_Chroma import add_chunks_to_chroma

def Vector_store_node(state: RAG_State):
    
    fixed_chunks = state.get('embedded_fixed_chunks', [])
    semantic_chunks = state.get('embedded_semantic_chunks',[])

    all_chunks = fixed_chunks + semantic_chunks

    if not all_chunks:
        print("No chunks to add to Vector Store.")
        return {
            "indexing_complete": True
        }
        
    print(f"Adding {len(all_chunks)} total chunks to Chroma DB...")
    res = add_chunks_to_chroma(all_chunks)
       

    
    if res['status'] =='success':
        print(f"Successfully added {res['inserted_count']} new chunks to Chroma DB")
        print('Indexing Complete')
        return {
            "indexing_complete": True
        }
    else:
        print(f"Error adding chunks to Chroma DB: {res['message']}")
        return {
            "indexing_complete": False
        }

    

   