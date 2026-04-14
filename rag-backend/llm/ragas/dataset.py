import json
import os
from ragas import EvaluationDataset

def load_dataset():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, "data.json")
    
    with open(data_path, "r") as f:
        data = json.load(f)
    
    return EvaluationDataset.from_list(data)