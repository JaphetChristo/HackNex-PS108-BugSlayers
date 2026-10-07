# VERITAS — Proof-Carrying AI Data Analyst

> **"Don't just give an answer. Prove whether the answer deserves to be trusted."**

VERITAS is an AI-powered data analysis system designed to answer natural-language questions about CSV and Excel datasets while providing evidence for whether the generated answer can be trusted.

Unlike a conventional AI chatbot that may confidently generate an answer, VERITAS follows a structured pipeline:

**Dataset → Inspection → AI Analysis Plan → Code Safety → Computation → Verification → Evidence → Final Decision**

---

## 🚀 Key Features

### 1. Dataset Understanding
VERITAS can load:

- CSV files
- Excel `.xlsx` files
- Excel `.xls` files

It automatically inspects:

- Number of rows
- Number of columns
- Column names
- Data types
- Missing values
- Duplicate rows
- Numerical columns
- Categorical columns
- Dataset preview
- Basic statistics

---

### 2. Natural-Language Questions

Users can ask questions such as:

> Which region had the highest revenue?

or:

> What is the average exam score?

The system converts the user's question into a structured analysis plan.

---

### 3. AI Analysis Planning

The AI agent analyzes:

- The user's question
- Dataset schema
- Dataset metadata

It determines whether the question can be answered using the available data.

The AI is instructed to:

- Never invent columns
- Never invent data values
- Never assume unavailable information
- Explain when information is missing
- Generate an analysis plan
- Generate Python/Pandas code for the requested calculation

---

### 4. Code Safety

Before generated Python code is accepted, VERITAS performs a basic AST-based safety check.

Potentially dangerous operations such as:

- `eval`
- `exec`
- `compile`
- `open`
- `input`
- `__import__`

and selected modules such as:

- `os`
- `subprocess`
- `socket`
- `requests`
- `shutil`
- `pathlib`

are blocked.

> **Important:** This is currently a basic first-pass safety checker and is not a true secure sandbox.

---

### 5. Independent Verification

VERITAS is designed around the principle that the AI-generated answer should not automatically be trusted.

The system contains verification functions that can independently check:

- Totals
- Averages
- Counts
- Minimum values
- Maximum values
- Percentage changes
- Required columns
- Result quality

The goal is to compare the generated analysis against independently calculated results.

---

### 6. Evidence

VERITAS can produce evidence describing:

- What operation was performed
- What value was calculated
- What value was expected
- Whether the values matched

Example:

```text
Operation: Total Revenue
Calculated: 636000
Expected: 636000
Status: VERIFIED
```

---

## 🧠 CANNOT DETERMINE

One of VERITAS's most important principles is:

> **If the dataset does not contain enough information to answer the question, VERITAS should refuse to guess.**

For example, if a dataset contains:

```text
region
revenue
```

and the user asks:

> Which product generated the highest revenue?

VERITAS should not invent a product.

Instead:

```text
CANNOT DETERMINE

The dataset does not contain a product column.
Therefore, the question cannot be answered using
the available data.
```

This helps reduce hallucinations and unsupported conclusions.

---

# 🏗️ System Architecture

```text
                    USER
                      │
                      ▼
              ┌───────────────┐
              │ Streamlit UI  │
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │ Dataset Upload│
              └───────┬───────┘
                      │
                      ▼
              ┌───────────────┐
              │  Data Engine  │
              └───────┬───────┘
                      │
                      ▼
            ┌─────────────────────┐
            │ Schema + Metadata   │
            └──────────┬──────────┘
                       │
                       ▼
              ┌────────────────┐
              │  Groq AI Agent │
              └───────┬────────┘
                      │
                      ▼
            ┌─────────────────────┐
            │ Analysis Plan +     │
            │ Python Code         │
            └──────────┬──────────┘
                       │
                       ▼
              ┌────────────────┐
              │  Code Safety   │
              └───────┬────────┘
                      │
                      ▼
             ┌──────────────────┐
             │ Controlled       │
             │ Execution        │
             └────────┬─────────┘
                      │
                      ▼
             ┌──────────────────┐
             │ Actual Result    │
             └────────┬─────────┘
                      │
                      ▼
             ┌──────────────────┐
             │ Independent      │
             │ Verification     │
             └────────┬─────────┘
                      │
                      ▼
             ┌──────────────────┐
             │ Evidence /       │
             │ Provenance       │
             └────────┬─────────┘
                      │
                      ▼
          ┌─────────────────────────┐
          │ VERIFIED / FAILED /     │
          │ CANNOT DETERMINE        │
          └─────────────────────────┘
```

---

# 📁 Project Structure

```text
VERITAS/
│
├── app/
│   ├── __init__.py
│   ├── app.py
│   │
│   ├── config.py
│   ├── models.py
│   ├── prompts.py
│   ├── schema_builder.py
│   ├── llm_agent.py
│   │
│   ├── data_engine.py
│   ├── analysis_engine.py
│   ├── verifier.py
│   ├── code_safety.py
│   └── trust_pipeline.py
│
├── datasets/
│   ├── sales_clean.csv
│   ├── sales_messy.csv
│   ├── sales_limited.csv
│   ├── hospital_operations.csv
│   ├── agriculture_yield.csv
│   └── student_performance.csv
│
├── .env
├── .gitignore
└── README.md
```

---

# 🧩 Main Components

## AI / Agent Layer

### `config.py`

Stores configuration such as:

- Groq API key
- Model name

The API key should be stored in `.env` and should **never be committed to GitHub**.

---

### `models.py`

Defines Pydantic models used to validate the AI's structured response.

Main models:

```text
AnalysisPlan
AgentResponse
```

---

### `prompts.py`

Contains the system prompt that defines VERITAS's AI behavior.

The prompt enforces rules such as:

```text
Never invent dataset columns.
Never invent data values.
Never calculate the final numerical answer.
Only use columns that actually exist.
```

---

### `llm_agent.py`

Connects VERITAS to the Groq API.

Responsibilities:

1. Receive the user question.
2. Receive the dataset schema.
3. Receive dataset metadata.
4. Send them to the AI.
5. Receive structured JSON.
6. Validate the response using Pydantic.
7. Return the validated analysis plan.

---

### `schema_builder.py`

Converts the Pandas DataFrame structure into a schema that can be provided to the AI.

Example:

```text
Columns:

- region: object
- product: object
- quarter: object
- revenue: int64
```

---

# 📊 Data / Analysis Layer

## `data_engine.py`

Responsible for:

- Loading datasets
- Inspecting datasets
- Generating previews
- Generating basic statistics

---

## `analysis_engine.py`

Contains reusable analysis operations such as:

```text
total()
average()
count()
minimum()
maximum()
percentage_change()
group_sum()
sort_descending()
```

---

## `verifier.py`

Provides independent verification functions.

Examples:

```text
verify_total()
verify_average()
verify_count()
verify_minimum()
verify_maximum()
verify_percentage_change()
verify_columns()
```

---

## `code_safety.py`

Performs AST-based inspection of generated Python code.

It identifies selected dangerous functions, imports, and special attributes before execution.

---

## `trust_pipeline.py`

Combines:

1. Code safety
2. Result verification

into a higher-level trust decision.

Possible outcomes include:

```text
VERIFIED
FAILED
```

---

# 🖥️ User Interface

The Streamlit interface provides:

- Dataset upload
- Dataset overview
- Dataset preview
- Schema information
- Natural-language question input
- AI analysis
- Analysis plan
- Generated Python code
- Code safety result
- Verification result
- Final trust decision

---

# 🧪 Example Datasets

The project includes several datasets for testing.

### `sales_clean.csv`

Used for normal analysis.

Example:

```text
Which region had the highest revenue?
```

Expected result:

```text
South
```

---

### `sales_messy.csv`

Contains:

- Missing values
- Duplicate rows

Used to demonstrate dataset-quality inspection.

---

### `sales_limited.csv`

Contains limited information.

Useful for demonstrating:

```text
CANNOT DETERMINE
```

---

### `hospital_operations.csv`

Contains hospital operational data such as:

- Department
- Patients
- Average wait time
- Doctors
- Emergency cases

---

### `agriculture_yield.csv`

Contains agricultural data such as:

- Crop
- Rainfall
- Fertilizer
- Temperature
- Yield

---

### `student_performance.csv`

Contains educational data such as:

- Study hours
- Attendance
- Assignments
- Exam scores

---

# ⚙️ Installation

Create and activate a Python virtual environment.

Then install the required packages:

```bash
python -m pip install streamlit pandas openpyxl groq python-dotenv pydantic
```

---

# 🔑 Environment Variables

Create a `.env` file in the project root:

```text
GROQ_API_KEY=your_groq_api_key_here
```

Never upload `.env` to GitHub.

The `.gitignore` file should contain:

```text
.env
.venv/
__pycache__/
*.pyc
.idea/
```

---

# ▶️ Running VERITAS

From the project root:

```bash
python -m streamlit run app/app.py
```

The Streamlit application will open locally.

---

# 🔄 Current VERITAS Pipeline

The current development pipeline is:

```text
1. Upload dataset
       ↓
2. Load dataset
       ↓
3. Inspect dataset
       ↓
4. Build schema
       ↓
5. Ask natural-language question
       ↓
6. Groq generates analysis plan
       ↓
7. Validate AI response
       ↓
8. Check generated code safety
       ↓
9. Execute analysis
       ↓
10. Independently verify result
       ↓
11. Generate evidence
       ↓
12. Display final trust status
```

---

# 🛡️ Design Philosophy

VERITAS is built around three principles:

### 1. Don't hallucinate

If the data does not contain the required information, the system should not invent it.

### 2. Don't blindly trust AI-generated calculations

AI-generated code should be checked and its output independently verified.

### 3. Show evidence

A result should be accompanied by information explaining how the system arrived at its trust decision.

---

# 🎯 Hackathon Demo

A recommended demonstration consists of three scenarios.

## Demo 1 — Successful Analysis

Dataset:

```text
sales_clean.csv
```

Question:

```text
Which region had the highest revenue?
```

Expected:

```text
VERIFIED
```

---

## Demo 2 — Messy Dataset

Dataset:

```text
sales_messy.csv
```

Question:

```text
How many duplicate rows are present?
```

VERITAS demonstrates that it can inspect the quality of the uploaded data.

---

## Demo 3 — Unsupported Question

Dataset:

```text
sales_limited.csv
```

Question:

```text
Which product generated the highest revenue?
```

Expected:

```text
CANNOT DETERMINE
```

Reason:

```text
The dataset does not contain product-level information.
```

This demonstrates that VERITAS can recognize when an answer is not supported by the available evidence.

---

# 🚧 Development Status

VERITAS is currently under active development.

Implemented components include:

- Dataset loading
- Dataset inspection
- Schema generation
- Groq AI integration
- Structured AI responses
- Pydantic validation
- Analysis functions
- Verification functions
- Basic code-safety checking
- Trust pipeline
- Streamlit interface

Further integration work includes connecting AI-generated analysis code to controlled execution and independent verification.

---

# 👥 Team

VERITAS is being developed by a 3-member student team.

### Member 1 — AI / Agent Engineer

Responsible for:

- Groq integration
- Prompt engineering
- AI response structure
- Pydantic validation
- Analysis planning

### Member 2 — Data / Analysis / Verification Engineer

Responsible for:

- Data engine
- Analysis engine
- Verification
- Code safety
- Trust pipeline

### Member 3 — UI / Integration / Demo Lead

Responsible for:

- Streamlit UI
- System integration
- Dataset management
- User experience
- Demo preparation

---

# 💡 Vision

Traditional AI data analysts focus on:

> **"Can I give you an answer?"**

VERITAS focuses on:

> **"Can I prove that the answer is supported by the data?"**

The goal is to make AI-assisted data analysis more transparent, verifiable, and resistant to unsupported conclusions.

---

## VERITAS

**Analyze. Verify. Prove.**