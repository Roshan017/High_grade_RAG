import json
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
FILE = os.path.join(CURRENT_DIR, "data.json")


def log_interaction(user_input, response, retrieved_contexts, reference=None):
    # load existing data
    if os.path.exists(FILE):
        try:
            with open(FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            data = []
    else:
        data = []

    # create entry
    entry = {
        "user_input": user_input,
        "response": response,
        "retrieved_contexts": retrieved_contexts
    }

    # optional reference
    if reference:
        entry["reference"] = reference

    # append and save
    data.append(entry)

    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)