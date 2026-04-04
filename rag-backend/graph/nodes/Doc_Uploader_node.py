import fitz
import docx
import io
from graph.state import RAG_State


def Doc_Uploader_node(state: RAG_State):
    """
    This node is responsible for uploading the documents to the RAG system.
    """
    raw_docs = state.get('raw_docs',[])

    # print("Doc Uploader Node: ",raw_docs)
    
    extracted_docs = []

    for doc_item in raw_docs:
        filename = doc_item.get('filename')
        content = doc_item.get('content')
        file_type = doc_item.get('file_type')
        text = ""

        try:
            if file_type == 'pdf':
                pdf_doc = fitz.open(stream = content , filetype = 'pdf')
                text = "\n".join([page.get_text() for page in pdf_doc])
                pdf_doc.close()

            elif file_type == 'docx':
                doc = docx.Document(io.BytesIO(content))
                text = "\n".join([ptr.text for ptr in doc.paragraphs])
            elif file_type in ["txt", "md"]:
                text = content.decode("utf-8")
            extracted_docs.append({
                "filename": filename,
                "content": text,
                "file_type": file_type
            })

        except Exception as e:
            print(f"Error parsing {filename}: {str(e)}")
            continue

        # print("Doc Uploader Node: ",extracted_docs)
        
    return {
        "raw_docs": extracted_docs,
        "uploaded_files": [doc["filename"] for doc in extracted_docs]
    }
    
    