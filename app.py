import streamlit as st
from ingestion.document_loader import DocumentIngestionLayer
from agents.orchestrator import StrandsOrchestrator
from core.exceptions import ResumeIntelException

st.set_page_config(
    page_title="Resume Intel Core AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom enterprise UI stylings application
st.markdown("""
    <style>
    .metric-card {
        background-color: #1E293B;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #3B82F6;
        margin-bottom: 15px;
    }
    .score-text {
        font-size: 36px;
        font-weight: bold;
        color: #F8FAFC;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 Resume Intelligence Multi-Agent System")
st.subheader("Enterprise-Grade Agentic Recruiting Analytics Framework")
st.markdown("---")

# Main Application Configuration Sidebar Layout Context
with st.sidebar:
    st.header("📋 System Ingestion Panel")
    st.markdown("Upload target profile files below to invoke processing agents.")
    
    resume_file = st.file_uploader("Upload Candidate Resume", type=["pdf", "docx"])
    jd_file = st.file_uploader("Upload Target Job Specification", type=["pdf", "docx", "txt"])
    
    st.markdown("---")
    analyze_btn = st.button("⚡ Run Agentic Pipeline Analysis", type="primary", use_container_width=True)

if analyze_btn:
    if not resume_file or not jd_file:
        st.error("❌ Critical Validation Failure: Both Candidate Resume and Job Specification files are required.")
    else:
        with st.spinner("🧠 Orchestrating Specialist Agents & Analysis Engines..."):
            try:
                # 1. Ingestion Execution Routing Phase
                resume_bytes = resume_file.read()
                jd_bytes = jd_file.read()
                
                resume_text = DocumentIngestionLayer.load_document(resume_bytes, resume_file.name)
                jd_text = DocumentIngestionLayer.load_document(jd_bytes, jd_file.name)
                
                # 2. Multi-Agent Pipeline Orchestration Invocation
                orchestrator = StrandsOrchestrator()
                report = orchestrator.run_analysis_pipeline(resume_text, jd_text)
                
                # 3. Dynamic UI Component Presentation Layer Execution
                st.balloons()
                
                # Top Score Summary Dashboard Row Layout Elements - Fixed with Dot Notation
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"""
                    <div class="metric-card" style="border-left-color: #10B981;">
                        <p style="color: #94A3B8; margin:0;">DETERMINISTIC ATS SCORE</p>
                        <p class="score-text">{report.ats_analysis.score} <span style="font-size:18px;">/ 100</span></p>
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    st.markdown(f"""
                    <div class="metric-card" style="border-left-color: #3B82F6;">
                        <p style="color: #94A3B8; margin:0;">JD MATCH COMPLIANCE</p>
                        <p class="score-text">{report.jd_match.match_percentage} <span style="font-size:18px;">%</span></p>
                    </div>
                    """, unsafe_allow_html=True)
                with col3:
                    st.markdown(f"""
                    <div class="metric-card" style="border-left-color: #8B5CF6;">
                        <p style="color: #94A3B8; margin:0;">WRITING HEALTH INDEX</p>
                        <p class="score-text">{report.writing_quality.ai_heuristic_score} <span style="font-size:18px;">/ 100</span></p>
                    </div>
                    """, unsafe_allow_html=True)

                st.markdown("---")
                
                # Main Dashboard Columns Presentation
                left_col, right_col = st.columns(2)
                
                with left_col:
                    st.header("🎯 Evidence-Based Strategic Analysis")
                    
                    st.subheader("🟢 Core Strengths")
                    for s in report.strengths:
                        st.markdown(f"* ✅ {s}")
                        
                    st.subheader("🔴 Missing Gaps & Weaknesses")
                    for w in report.weaknesses:
                        st.markdown(f"* ⚠️ {w}")
                        
                    st.markdown("---")
                    st.header("🔍 Job Specification Skills Coverage Mapping")
                    
                    s_col1, s_col2 = st.columns(2)
                    with s_col1:
                        st.subheader("Matching Technical Skillsets")
                        if report.jd_match.matching_skills:
                            for m_s in report.jd_match.matching_skills:
                                st.caption(f"🧬 {m_s}")
                        else:
                            st.write("None.")
                    with s_col2:
                        st.subheader("Missing Technical Skillsets")
                        if report.jd_match.missing_skills:
                            for mi_s in report.jd_match.missing_skills:
                                st.markdown(f"<span style='color:#EF4444;'>❌ {mi_s}</span>", unsafe_allow_html=True)
                        else:
                            st.write("None detected.")

                with right_col:
                    st.header("🛠️ Actionable Adjustments & Refactoring Suggestions")
                    for imp in report.actionable_improvements:
                        with st.expander(f"📍 [{imp.category}] - {imp.finding}"):
                            st.markdown(f"**Optimization Instruction:** {imp.actionable_fix}")
                            if imp.example:
                                st.info(f"💡 **Production Standard Example:**\n\n*{imp.example}*")
                                
                    st.markdown("---")
                    st.header("📈 Scoring Systems Explanatory Methodology Matrix")
                    with st.expander("ATS Engine Breakdown Matrix Detail"):
                        st.json(report.ats_analysis.score_breakdown)
                    with st.expander("Job Matching Allocation Logic Detail"):
                        st.json(report.jd_match.calculation_breakdown)
                    with st.expander("Linguistic Health Index Notes"):
                        st.warning("⚠️ **System Advisory Policy:** Writing analysis scores use deterministic linguistic indicators (such as passive voice frequency and cliché counts) as structural optimization heuristics. They are not absolute indicators of AI usage.")
                        st.write(report.writing_quality.ai_heuristic_explanation)

            except ResumeIntelException as error:
                st.error(f"Execution Error within Core Engine Domain Layer: {str(error)}")
            except Exception as severe_err:
                st.error(f"Unmanaged System Platform Failure: {str(severe_err)}")
else:
    st.info("💡 Application Dashboard Initialized. Upload your Candidate Resume and Target Job Specification to trigger the Multi-Agent optimization engine.")