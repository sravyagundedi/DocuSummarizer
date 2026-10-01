from rouge_score import rouge_scorer

def rouge_scores(reference, candidate):
    scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=True)
    return {
        k: {"precision": v.precision, "recall": v.recall, "fmeasure": v.fmeasure}
        for k, v in scorer.score(reference, candidate).items()
    }

def manual_rubric_score(values):
    total = sum(values.values())
    return {"total": total, "max": 10, "percentage": total * 10}
