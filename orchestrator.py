import logging
from core.models import FinalReport
from agents.ats_agent import ATSAnalysisAgent
from agents.jd_agent import JDMatchingAgent
from agents.writing_agent import WritingQualityAgent
from agents.reporting_agent import FinalReportAgent

logger = logging.getLogger("resume_intel.orchestrator")

class StrandsOrchestrator:
    """
    Central Nervous System / Orchestrator of the Strands framework.
    Coordinates sequential context flow across isolated domain-specific expert agents.
    """
    def __init__(self):
        logger.info("Initializing multi-agent orchestrator lifecycle workflow engine.")
        self.ats_agent = ATSAnalysisAgent()
        self.jd_agent = JDMatchingAgent()
        self.writing_agent = WritingQualityAgent()
        self.report_agent = FinalReportAgent()
        
    def run_analysis_pipeline(self, resume_text: str, jd_text: str) -> FinalReport:
        logger.info("Starting Multi-Agent analysis execution run.")
        
        # Step 1, 2 & 3: Run the deterministic tools through their specific wrappers
        ats_data = self.ats_agent.execute(resume_text)
        jd_data = self.jd_agent.execute(resume_text, jd_text)
        writing_data = self.writing_agent.execute(resume_text)
        
        # Step 4: Final Reporting agent handles synthesis and cognitive generation
        final_report: FinalReport = self.report_agent.synthesize(
            ats=ats_data,
            jd=jd_data,
            writing=writing_data,
            resume_text=resume_text,
            jd_text=jd_text
        )
        
        logger.info("Multi-agent analysis execution completed successfully.")
        return final_report