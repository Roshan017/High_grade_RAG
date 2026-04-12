from langgraph.graph import StateGraph , END, START
from graph.state import RAG_State
from graph.nodes.Doc_Uploader_node import Doc_Uploader_node
from graph.nodes.Chunking_node import Chunking_node
from graph.nodes.Embedder_node import Embedder_node
from graph.nodes.Vector_store_node import Vector_store_node
from graph.nodes.Query_Embedder_node import Query_Embedder_node
from graph.nodes.Retrieval_node import Retrieval_node
from graph.nodes.Response_gen_node import Response_gen_node
from graph.nodes.Citation_handler import Citation_handler

from services.Vector_store.Check_collection import get_collections


def entry_route_check(state: RAG_State):
    """
    Check the starting point of the graph based on the input state and DB status
    """
    if state.get('raw_docs'):
        print('New documents detected. Routing to Doc_Uploader_node.')
        return False
    
    index_complete = get_collections()
    if index_complete:
        print('Collection exists. Routing to Query_Embedder_node.')
        return True
    
    print('No documents provided and no collection exists. Routing to Doc_Uploader_node.')
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
    graph.add_node("Citation_handler", Citation_handler)
    

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
    graph.add_edge('Response_gen_node','Citation_handler')
    graph.add_edge('Citation_handler',END)
    

    return graph.compile()

