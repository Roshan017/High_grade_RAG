import re
from typing import List

def extract_ids(text: str) -> List[int]:
    matches = re.findall(r'\[(.*?)\]', text)

    ids = [
        int(num.strip())
        for match in matches
        for num in match.split(',')
        if num.strip().isdigit()
    ]

    return ids


def remove_ids(text: str) -> str:
    """
    Removes numeric citations like [1], [2,3], or [1], [2] and handles following punctuation spacing.
    """
    # 1. Remove citations like [1], [2] or [1, 2]
    # This pattern matches one or more brackets separated by commas/spaces
    text = re.sub(r'\s*\[\s*\d+(?:\s*,\s*\d+)*\s*\](?:,\s*\[\s*\d+(?:\s*,\s*\d+)*\s*\])*', '', text)
    
    # 2. Fix spacing before punctuation (e.g., "benefits ." -> "benefits.")
    text = re.sub(r'\s+([.,!?;:])', r'\1', text)
    
    # 3. Collapse multiple spaces and strip
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text