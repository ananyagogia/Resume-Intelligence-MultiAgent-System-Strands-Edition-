import logging
from core.models import ATSAnalysisResult
from engines.ats_engine import ATSEngine

logger = logging.getLogger("resume_intel.ats_agent")

class ATSAnalysisAgent:
    """
    Strands Agent wrapper for the deterministic ATS Scoring Engine.
    """
    def __init__(self):
        self.name = "ATS_Analyst"
        self.role = "Expert ATS Systems Optimization Engineer"
        
    def execute(self, resume_text: str) -> dict:
        logger.info(f"[{self.name}] starting deterministic resume structural analysis.")
        try:
            analysis_result: ATSAnalysisResult = ATSEngine.analyze(resume_text)
            return analysis_result.model_dump()
        except Exception as e:
            logger.error(f"[{self.name}] failed during execution: {str(e)}")
            raise