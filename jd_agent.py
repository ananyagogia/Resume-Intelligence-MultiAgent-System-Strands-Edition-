import logging
from core.models import JDMatchResult
from engines.jd_matcher import JDMatcherEngine

logger = logging.getLogger("resume_intel.jd_agent")

class JDMatchingAgent:
    """
    Strands Agent wrapper for the deterministic Job Description Matcher.
    """
    def __init__(self):
        self.name = "JD_Matcher"
        self.role = "Technical Recruitment Match Optimizer"
        
    def execute(self, resume_text: str, jd_text: str) -> dict:
        logger.info(f"[{self.name}] executing structural keyword and gap comparison.")
        try:
            match_result: JDMatchResult = JDMatcherEngine.analyze(resume_text, jd_text)
            return match_result.model_dump()
        except Exception as e:
            logger.error(f"[{self.name}] failed during execution: {str(e)}")
            raise