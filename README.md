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
