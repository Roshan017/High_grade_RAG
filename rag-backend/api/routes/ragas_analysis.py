from fastapi import APIRouter, HTTPException
from llm.ragas.evals import run_evaluation
from llm.ragas.dataset import load_dataset

router = APIRouter()

@router.post('/analyze')
def analyze_ragas():

    data = load_dataset()

    if len(data) < 5:
        return {
            "message": "Not enough data for evaluation"
        }

    try:
        result = run_evaluation()
        
        faithfulness = result.get("faithfulness", 0)
        answer_relevancy = result.get("answer_relevancy", 0)
        
      
        if type(faithfulness) is list:
            faithfulness = sum(faithfulness) / len(faithfulness) if faithfulness else 0
        if type(answer_relevancy) is list:
            answer_relevancy = sum(answer_relevancy) / len(answer_relevancy) if answer_relevancy else 0
            
        return {
            "faithfulness": faithfulness,
            "answer_relevancy": answer_relevancy
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))