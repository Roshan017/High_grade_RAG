from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List , Dict , Any


def Fixed_Chunker(docs_list: List[Dict[str, Any]], chunk_size: int = 1000, chunk_overlap: int = 200 ) -> List[Dict[str,Any]]:
    """
    This function is responsible for chunking the documents to fixed Chunks.
    """
    chunks = []
    splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ".", " "]
        )
    for docs in docs_list:
        text = docs.get('text', '')
        metadata = docs.get('metadata', {})
        doc_id = docs.get('doc_id', 'unknown')
        filename = docs.get('filename', 'unknown')

        raw_chunks = splitter.split_text(text)
        total_chunks = len(raw_chunks)

        for idx , chunk in enumerate(raw_chunks):
            chunks.append(
                {
                    'chunk_id': f"{doc_id}_fixed_chunk_{idx+1}",
                    'text': chunk,
                    'metadata': {
                        **metadata,
                        "user_id":"dev_user_001",
                        "doc_id": doc_id,
                        "filename": filename,
                        "chunk_index": idx + 1,
                        "chunking_type": 'fixed',
                        "chunk_id": f"{doc_id}_fixed_chunk_{idx+1}",
                        "total_chunks": total_chunks
                    }
                }
            )


    return chunks