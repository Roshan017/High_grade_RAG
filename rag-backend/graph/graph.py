from langgraph.graph import StateGraph , END, START
from graph.state import RAG_State
from graph.nodes.Doc_Uploader_node import Doc_Uploader_node
from graph.nodes.Chunking_node import Chunking_node
from graph.nodes.Embedder_node import Embedder_node
from graph.nodes.Vector_store_node import Vector_store_node
from graph.nodes.Query_Embedder_node import Query_Embedder_node
from graph.nodes.Retrieval_node import Retrieval_node
from graph.nodes.Response_gen_node import Response_gen_node

from services.Vector_store.Check_collection import get_collections


def entry_route_check(state: RAG_State):
    """
    Check the starting point of the graph
    """
    index_complete = get_collections()
    print("Indexing Complete: ",index_complete)
    if index_complete:
        print('Straight to Query_Embedder_node')
        return True
    else:
        print('Straight to Doc_Uploader_node')
        return False

def query_route_check(state: RAG_State):
    """
    Check if query is present in the flow
    """
    isquery = state.get('query') and state.get('query').strip()
    if isquery:
        print('Query Present')
        return True
    else:
        print('No Query Present')
        return False
         


def build_RAG_State_Graph():
    graph = StateGraph(RAG_State)
    
    graph.add_node("Doc_Uploader_node",Doc_Uploader_node)
    graph.add_node("Chunking_node",Chunking_node)
    graph.add_node("Embedder_node", Embedder_node)
    graph.add_node("Vector_store_node", Vector_store_node)
    graph.add_node("Query_Embedder_node", Query_Embedder_node)
    graph.add_node("Retrieval_node", Retrieval_node)
    graph.add_node("Response_gen_node", Response_gen_node)
    

    graph.add_conditional_edges(
        START,
        entry_route_check,
        {
            True: "Query_Embedder_node",
            False: "Doc_Uploader_node"
        }
    )

    graph.add_edge("Doc_Uploader_node","Chunking_node")
    graph.add_edge("Chunking_node","Embedder_node")
    graph.add_edge("Embedder_node","Vector_store_node")

    graph.add_conditional_edges(
        "Vector_store_node",
        query_route_check,
        {
            True: "Query_Embedder_node",
            False: END
        }
    )
    graph.add_edge('Query_Embedder_node','Retrieval_node')
    graph.add_edge('Retrieval_node','Response_gen_node')
    graph.add_edge('Response_gen_node',END)
    

    return graph.compile()

