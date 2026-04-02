import pandas as pd
from datetime import datetime
from utils import call_gemini, parse_json_response


def build_eval_prompt(notes, summary):
    """
    Builds a prompt that asks Gemini to score a summary.
    Forces JSON output for easy parsing.
    """
    return f"""You are an expert evaluator of study summaries.

    Rate the following summary based on the original notes.
    Score each dimension from 1 to 5 where:
    1 = very poor, 3 = acceptable, 5 = excellent

    Dimensions:
    - completeness: does the summary cover all main ideas 
                    from the original notes?
    - conciseness: is the summary shorter and tighter 
                   than the original?
    - clarity: is the summary easy to understand for 
               a student studying for an exam?

    Reply ONLY with this exact JSON format.
    No explanation. No extra text. Just the JSON:
    {{"completeness": 4, "conciseness": 3, "clarity": 5}}

    Original notes:
    {notes}

    Summary to evaluate:
    {summary}"""


def evaluate(notes, summary):
    """
    Scores a summary against the original notes.
    Returns a dictionary of scores.
    """
    prompt = build_eval_prompt(notes, summary)
    response = call_gemini(prompt)

    if response is None:
        # Return neutral scores if API call fails
        return {"completeness": 0, "conciseness": 0, "clarity": 0}

    scores = parse_json_response(response)

    if scores is None:
        return {"completeness": 0, "conciseness": 0, "clarity": 0}

    return scores


def evaluate_all(notes, summaries):
    """
    Evaluates all three summaries and returns results
    as a list of dictionaries ready for a DataFrame.
    """
    results = []

    for style, summary in summaries.items():
        scores = evaluate(notes, summary)

        results.append({
            "style": style,
            "summary": summary,
            "summary_length": len(summary),
            "completeness": scores.get("completeness", 0),
            "conciseness": scores.get("conciseness", 0),
            "clarity": scores.get("clarity", 0),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

    return results


def save_results(results, filepath="data/experiment_log.csv"):
    df = pd.DataFrame(results)
    try:
        existing = pd.read_csv(filepath, encoding='utf-8')
        updated = pd.concat([existing, df], ignore_index=True)
        updated.to_csv(filepath, index=False, encoding='utf-8')
    except FileNotFoundError:
        df.to_csv(filepath, index=False, encoding='utf-8')


def get_best_summary(results):
    """
    Finds the summary with the highest average score.
    Returns the style name and summary text.
    """
    df = pd.DataFrame(results)
    df["average"] = df[["completeness", "conciseness", "clarity"]].mean(axis=1)
    best_row = df.loc[df["average"].idxmax()]

    return {
        "style": best_row["style"],
        "summary": best_row["summary"],
        "average_score": round(best_row["average"], 2)
    }