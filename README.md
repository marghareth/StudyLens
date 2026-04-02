# StudyLens 🔬
### LLM-Powered Study Assistant with Prompt Evaluation Dashboard

StudyLens transforms raw, unstructured study notes into clean summaries and quiz questions — but what makes it different from a simple summarizer is its built-in evaluation layer.

Instead of running one prompt and returning one output, StudyLens runs **three different prompt strategies** on the same notes, scores each output using the LLM itself, and visualizes which strategy performed best. This turns a productivity tool into a mini research experiment.

Live demo: https://studylens-jayksf5i2hwyllcmw2xxun.streamlit.app/
Click the link to see how it works.

---

## What It Does

1. Paste any study notes into the app
2. Click Generate
3. StudyLens automatically runs three prompt strategies behind the scenes
4. Each summary is scored on completeness, conciseness, and clarity using LLM-as-judge evaluation
5. The best summary and quiz questions are displayed alongside a dashboard showing which prompt strategy performed best and why

---

## Why This Approach

**Three prompt strategies** — direct, concise, and chain-of-thought — test whether constraining or structuring the LLM's reasoning process produces measurably different quality outcomes on the same input. This mirrors how ML & GenAI engineering teams evaluate prompt strategies for real client deployments.

**LLM-as-judge evaluation** scales without human labeling. The same model that generates summaries is asked to score them against defined criteria, returning structured JSON scores that can be aggregated and visualized across runs.

**Persistent experiment log** saves every run to CSV so patterns can be analyzed across different content types and sessions — not just within a single run.

---

## Demo

```
Input:  Raw study notes (paste any text)
Output: Best summary + quiz questions + evaluation dashboard
Time:   ~15-20 seconds per run
```

---

## Tech Stack

| Layer | Tool |
|---|---|
| Language | Python 3.9+ |
| LLM | Gemini 1.5 Flash (Google AI) |
| UI | Streamlit |
| Data | Pandas |
| Visualization | Matplotlib |
| Storage | CSV (experiment log) |
| Version Control | Git |

---

## Project Structure

```
studylens/
│
├── app.py                  # Streamlit UI — wires everything together
├── summarizer.py           # Prompt builder + summarization logic
├── evaluator.py            # LLM scoring, CSV logging, best summary selection
├── quiz_generator.py       # Multiple choice question generation
├── dashboard.py            # Matplotlib charts
├── utils.py                # Gemini setup, shared API wrapper, input validation
│
├── data/
│   └── experiment_log.csv  # Auto-created on first run
│
├── requirements.txt
├── .env                    # API key (never committed)
└── .gitignore
```

---

## Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/yourusername/studylens.git
cd studylens
```

### 2. Create and activate a virtual environment
```bash
# Windows
py -m venv venv
venv\Scripts\activate

# Mac/Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add your Gemini API key

Get a free API key at [aistudio.google.com](https://aistudio.google.com), then create a `.env` file:

```
GEMINI_API_KEY=your_key_here
```

### 5. Run the app
```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`

---

## How the Experiment Works

Each time you paste notes and click Generate, StudyLens runs this pipeline automatically:

```
Notes input
    ↓
Summarize with 3 prompt strategies (3 API calls)
    ↓
Score each summary on completeness, conciseness, clarity (3 API calls)
    ↓
Generate quiz questions (1 API call)
    ↓
Save results to experiment_log.csv
    ↓
Generate dashboard from log
    ↓
Display best summary + quiz + charts + scores table
```

### Prompt Strategies

| Strategy | Approach | Tends to produce |
|---|---|---|
| Direct | No constraints, model decides format | Balanced, medium-length output |
| Concise | Hard 3-sentence limit | Short, tight, may sacrifice completeness |
| Chain-of-thought | Step-by-step reasoning before summarizing | Thorough, well-structured, longer |

### Evaluation Dimensions

| Dimension | What it measures |
|---|---|
| Completeness (1-5) | Does the summary cover all main ideas? |
| Conciseness (1-5) | Is it shorter and tighter than the original? |
| Clarity (1-5) | Is it easy to understand? |

---

## Findings

One of the core observations from running this experiment across different types of study notes is that **no single prompt strategy consistently wins across all three evaluation dimensions**. The best strategy depends heavily on the content type and the use case.

### The Completeness vs Conciseness Tradeoff

The most consistent pattern across runs is a fundamental tension between completeness and conciseness — they trade off against each other regardless of content type.

- **Chain-of-thought** tends to score highest on completeness and clarity. Forcing the model to identify key concepts before summarizing keeps important ideas from being dropped. The tradeoff is longer output and lower conciseness scores.
- **Concise prompting** reliably produces the shortest summaries and scores highest on conciseness. However, the hard length constraint forces the model to drop ideas — completeness scores suffer as a result.
- **Direct prompting** consistently lands in the middle across all three dimensions. It doesn't win on any single metric but offers the most balanced tradeoff overall.

### Content Type Affects Strategy Performance

Strategy rankings are not stable across content types. Dense, technical notes with many interdependent concepts tend to favor chain-of-thought — there is more reasoning to do before summarizing. Shorter, more narrative content shows smaller differences between strategies, with direct prompting sometimes outperforming chain-of-thought because less structured reasoning is needed.

### LLM Evaluation Is Inherently Variable

Because this project uses LLM-as-judge evaluation, scores vary between runs even on the same input. The model is probabilistic — it doesn't always produce identical outputs for identical inputs. This means individual scores should be interpreted as estimates rather than fixed measurements. Patterns observed across multiple runs are more reliable than any single result.

### Practical Recommendation

| Use Case | Recommended Strategy | Reason |
|---|---|---|
| Exam review | Chain-of-thought | Completeness matters more than brevity |
| Quick reference | Concise | Speed of review matters more than depth |
| General study | Direct | Balanced tradeoff with no extremes |

### What This Suggests for GenAI Systems

These findings reflect a broader principle in GenAI engineering: **prompt design is not one-size-fits-all.** A production system serving real users would need to either select prompt strategies dynamically based on content type and user intent, or expose strategy selection to the user directly. This is why evaluation infrastructure — the ability to measure and compare outputs systematically — is as important as the generation capability itself.

---

## Relevance to ML & GenAI Engineering

This project practices the core workflow of an ML & GenAI engineering team:

| Skill | How This Project Demonstrates It |
|---|---|
| Experiment design | Controlled variables — same notes, same model, different prompts |
| LLM evaluation methodology | LLM-as-judge with structured JSON scoring across defined dimensions |
| GenAI pipeline thinking | Input → prompt strategies → evaluation → aggregation → visualization |
| Prompt engineering | Three distinct strategies with different constraint levels and reasoning structures |
| Research documentation | Persistent CSV log, evaluation dashboard, written findings |
| GenAI tool building | Wraps research functionality in a usable productivity tool |

This directly maps to what ML & GenAI engineering teams do when deploying LLM solutions for clients — design prompts, evaluate outputs, measure quality, and iterate based on findings.

---

## Known Limitations

- **Self-serving bias** — the LLM evaluates its own outputs, which can inflate scores
- **Score variability** — LLM-as-judge produces slightly different scores on repeated runs due to model non-determinism
- **No retry logic** — failed API calls surface as empty outputs rather than error messages
- **CSV grows unbounded** — no cleanup mechanism for the experiment log
- **Single user only** — CSV append mode is not safe for concurrent writes

---

## What's Next

- Add ROUGE scoring as an objective complement to LLM-as-judge evaluation
- Add retry logic with exponential backoff for failed API calls
- Replace CSV with SQLite for better querying across sessions
- Add temperature control so users can test how model randomness affects output consistency
- Expand experiment across more content types to validate whether strategy rankings generalize

---

## Author

Built by Marga
[github.com/yourusername](https://github.com/marghareth) · [linkedin.com/in/yourprofile](https://www.linkedin.com/in/mary-marghareth-bueno-4a654a230/)