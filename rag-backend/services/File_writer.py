from typing import List , Dict , Any
import os

def File_writer(chunks: List[Dict[str, Any]],  strategy: str):
    os.makedirs('files', exist_ok=True)
    if strategy == 'fixed':
        with open(f'files/Fixed_chunks.txt', 'w', encoding='utf-8') as f:
            for idx ,chunk in enumerate(chunks):
                f.write(f"Chunk {idx+1}:\n")
                f.write(chunk['text'] + '\n\n')
    elif strategy == 'semantic':
        with open(f'files/Semantic_chunks.txt', 'w', encoding='utf-8') as f:
            for idx ,chunk in enumerate(chunks):
                f.write(f"Chunk {idx+1}:\n")
                f.write(chunk['text'] + '\n\n')
    else:
        raise ValueError('Invalid strategy')
    