# Resume Intelligence Multi-Agent System (Strands Edition)

An enterprise-grade, deterministic talent analytics application powered by **Strands** agent multi-role orchestrations and backed by **Gemini-2.5-flash**.

## Core System Architecture Design

Unlike typical AI projects that blindly pipe raw context into an LLM and guess scores, this architecture enforces a decoupled, deterministic layout:

1. **Ingestion Layer:** Leverages native LangChain structured document loaders to process inputs while maintaining structure layout.
2. **Deterministic Processing Engines:** Base analytics—including ATS scores, skills extraction, and writing metrics—are computed strictly inside native Python code matrices.
3. **Strands Multi-Agent Orchestration:** Specialized agents ingest these computed analytics and apply cognitive reasoning via Gemini to generate evidence-based optimizations, alternative copy configurations, and actionable insights.

---

## Strategic System Setup Blueprint

### 1. Project Prerequisites Setup

Ensure a clean Python environment installation (Python 3.10+ recommended):

```bash
git clone <repository-url>
cd resume_intelligence
python -m venv venv
source venv/bin/activate  # On Windows run: venv\Scripts\activate
```

## 📂 Project Directory Structure

To run this application successfully, ensure your local directory is structured exactly as follows:

```text
resume_intelligence/
│
├── .env                        # Environment configuration (Gemini API Key)
├── requirements.txt            # Python dependencies configuration
├── README.md                   # Setup and execution instructions
├── app.py                      # Streamlit Enterprise UI Dashboard
│
├── core/
│   ├── __init__.py
│   ├── config.py               # Pydantic environment configuration
│   ├── exceptions.py           # Custom domain exceptions mapping
│   ├── logger.py               # Standard log system bootstrapping
│   └── models.py               # Data architecture typing schemas
│
├── ingestion/
│   ├── __init__.py
│   └── document_loader.py      # LangChain document ingestion framework
│
├── engines/
│   ├── __init__.py
│   ├── ats_engine.py           # Deterministic compliance matrices logic
│   ├── jd_matcher.py           # Technical token vocabulary analytics
│   └── writing_analyser.py     # Deterministic linguistic parsing module
│
└── agents/
    ├── __init__.py
    ├── orchestrator.py         # Central Strands Multi-Agent coordinator
    ├── ats_agent.py            # Strands ATS system context wrapper
    ├── jd_agent.py             # Strands JD extraction profile worker
    ├── writing_agent.py        # Strands linguistic health specialist
    └── reporting_agent.py      # Strands optimization synthesis reporter
