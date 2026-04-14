from ragas import evaluate
from ragas.metrics import faithfulness, answer_relevancy
from .config import get_llm, get_embeddings
from .dataset import load_dataset
from langfuse import observe
from llm.langfuse import init_langfuse

# Initialize OpenTelemetry and Langfuse integration
init_langfuse()

@observe(name="ragas_evaluation")
def run_evaluation():
    llm = get_llm()
    embeddings = get_embeddings()
    
    data = load_dataset()

    metrics = [
        faithfulness,
        answer_relevancy
    ]

    res = evaluate(
        dataset=data,
        metrics=metrics,
        llm=llm,
        embeddings=embeddings
    )

    return res

if __name__ == "__main__":
    result = run_evaluation()
    print("\n--- Evaluation Results ---")
    print({
        "faithfulness": result.get("faithfulness", 0),
        "answer_relevancy": result.get("answer_relevancy", 0)
    })