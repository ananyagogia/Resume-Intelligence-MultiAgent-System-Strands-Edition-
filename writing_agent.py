import logging
from core.models import WritingQualityResult
from engines.writing_analyser import WritingAnalyserEngine

logger = logging.getLogger("resume_intel.writing_agent")

class WritingQualityAgent:
    """
    Strands Agent wrapping the deterministic structural linguistics engine.
    """
    def __init__(self):
        self.name = "Linguistic_Analyst"
        self.role = "Executive Copywriter and Technical Resume Reviewer"
        
    def execute(self, resume_text: str) -> dict:
        logger.info(f"[{self.name}] assessing linguistic patterns and bullet quality.")
        try:
            writing_result: WritingQualityResult = WritingAnalyserEngine.analyze(resume_text)
            return writing_result.model_dump()
        except Exception as e:
            logger.error(f"[{self.name}] failed during execution: {str(e)}")
            raise