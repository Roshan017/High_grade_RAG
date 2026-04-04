from langgraph.graph import StateGraph , END
from graph.state import RAG_State

from graph.nodes.Doc_Uploader_node import Doc_Uploader_node
from graph.nodes.Chunking_node import Chunking_node
from graph.nodes.Embedder_node import Embedder_node


def build_RAG_State_Graph():
    graph = StateGraph(RAG_State)

    graph.add_node("Doc_Uploader_node",Doc_Uploader_node)
    graph.add_node("Chunking_node",Chunking_node)
    graph.add_node("Embedder_node", Embedder_node)

    graph.set_entry_point('Doc_Uploader_node')

    graph.add_edge("Doc_Uploader_node","Chunking_node")
    graph.add_edge("Chunking_node","Embedder_node")
    graph.add_edge("Embedder_node",END)

    return graph.compile()

