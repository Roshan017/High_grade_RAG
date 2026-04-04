from typing import List , Dict , Any

def File_writer(chunks: List[Dict[str, Any]], filename: str, strategy: str):
    if strategy == 'fixed':
        with open(f'files/Fixed_chunks.txt', 'w') as f:
            for idx ,chunk in enumerate(chunks):
                f.write(f"Chunk {idx+1}:\n")
                f.write(chunk['text'] + '\n\n')
    elif strategy == 'semantic':
        with open(f'files/Semantic_chunks.txt', 'w') as f:
            for idx ,chunk in enumerate(chunks):
                f.write(f"Chunk {idx+1}:\n")
                f.write(chunk['text'] + '\n\n')
    else:
        raise ValueError('Invalid strategy')
    