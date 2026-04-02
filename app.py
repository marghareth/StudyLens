import streamlit as st
from summarizer import run_all_styles
from evaluator import evaluate_all, save_results, get_best_summary
from quiz_generator import generate_quiz
from dashboard import generate_dashboard
from utils import validate_input

# --- Page config ---
st.set_page_config(
    page_title="StudyLens",
    page_icon="🔬",
    layout="wide"
)

# --- Header ---
st.title("🔬 StudyLens")
st.markdown(
    "Paste your study notes → get a summary, quiz, "
    "and prompt evaluation dashboard."
)
st.divider()

# --- Input section ---
notes = st.text_area(
    "Paste your study notes here",
    height=200,
    placeholder="e.g. Photosynthesis is the process by which "
                "plants convert sunlight into glucose..."
)

col1, col2 = st.columns([1, 4])
with col1:
    run_button = st.button("Generate", type="primary",
                           use_container_width=True)

# --- Processing ---
if run_button:

    # Validate input first
    is_valid, error_msg = validate_input(notes)

    if not is_valid:
        st.error(error_msg)

    else:
        # Show progress to the user
        with st.spinner("Running experiment — this takes 15-20 seconds..."):

            # Step 1: Generate all summaries
            st.caption("Generating summaries with 3 prompt strategies...")
            summaries = run_all_styles(notes)

            # Step 2: Evaluate all summaries
            st.caption("Evaluating summary quality...")
            results = evaluate_all(notes, summaries)

            # Step 3: Generate quiz
            st.caption("Generating quiz questions...")
            quiz = generate_quiz(notes)

            # Step 4: Save to experiment log
            save_results(results)

            # Step 5: Find best summary
            best = get_best_summary(results)

            # Step 6: Generate dashboard
            chart = generate_dashboard(results)

        # --- Display results ---
        st.success("Done! Here are your results.")
        st.divider()

        # Row 1: Best summary + Quiz
        col_summary, col_quiz = st.columns(2)

        with col_summary:
            st.subheader("Best Summary")
            st.caption(
                f"Strategy: **{best['style'].replace('_', ' ').title()}** "
                f"— Average score: **{best['average_score']}/5**"
            )
            st.markdown(best["summary"])

        with col_quiz:
            st.subheader("Quiz Questions")
            st.text(quiz)

        st.divider()

        # Row 2: Dashboard
        st.subheader("Evaluation Dashboard")
        st.caption(
            "Each summary was scored 1–5 on completeness, "
            "conciseness, and clarity by the LLM itself."
        )
        st.image(chart, use_column_width=True)

        st.divider()

        # Row 3: Scores table
        st.subheader("Scores Breakdown")
        import pandas as pd
        df = pd.DataFrame(results)
        display_df = df[["style", "completeness",
                          "conciseness", "clarity",
                          "summary_length"]].copy()
        display_df.columns = ["Prompt Style", "Completeness",
                               "Conciseness", "Clarity",
                               "Summary Length (chars)"]
        display_df["Prompt Style"] = display_df["Prompt Style"].str.replace(
            "_", " ").str.title()
        st.dataframe(display_df, use_container_width=True)

        # Row 4: All summaries expandable
        st.divider()
        st.subheader("All Summaries")

        for result in results:
            style_label = result["style"].replace("_", " ").title()
            avg = round((result["completeness"] +
                         result["conciseness"] +
                         result["clarity"]) / 3, 2)
            with st.expander(f"{style_label} — avg score: {avg}/5"):
                st.markdown(result["summary"])