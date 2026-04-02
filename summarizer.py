from utils import call_gemini


def build_prompt(notes, style):
    """
    Builds a prompt string based on the chosen strategy.
    Same notes, different instructions = different outputs.
    """

    role = """You are an expert study assistant helping a 
    university student prepare for an exam. Your job is to 
    create clear, accurate summaries from raw study notes."""

    if style == "direct":
        task = f"""Summarize the following study notes into 
        clear bullet points. Cover all the main concepts.

        Notes:
        {notes}"""

    elif style == "concise":
        task = f"""Summarize the following notes in exactly 
        3 sentences. Be as concise as possible. Every word 
        must be essential. No examples, just core concepts.

        Notes:
        {notes}"""

    elif style == "chain_of_thought":
        task = f"""Follow these steps carefully:
        Step 1: Identify the 3 most important concepts 
                in the notes
        Step 2: For each concept, write one clear 
                explanation sentence
        Step 3: Combine into a structured summary with 
                a header for each concept

        Notes:
        {notes}"""

    return f"{role}\n\n{task}"


def summarize(notes, style):
    """
    Generates a summary using the specified prompt style.
    Returns the summary text or an error message.
    """
    prompt = build_prompt(notes, style)
    result = call_gemini(prompt)

    if result is None:
        return "Summary generation failed. Please try again."

    return result


def run_all_styles(notes):
    """
    Runs all three prompt styles on the same notes.
    Returns a dictionary with style names as keys 
    and summaries as values.
    """
    styles = ["direct", "concise", "chain_of_thought"]
    summaries = {}

    for style in styles:
        summaries[style] = summarize(notes, style)

    return summaries