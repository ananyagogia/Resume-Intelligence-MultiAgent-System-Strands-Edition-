import json
import logging
from google import genai
from google.genai import types
from core.config import settings
from core.models import FinalReport, ImprovementSuggestion

logger = logging.getLogger("resume_intel.reporting_agent")

class FinalReportAgent:
    """
    Strands Synthesis Agent. Compiles all engine data telemetry metrics,
    uses Gemini to generate actionable improvements, and outputs the final structured report.
    """
    def __init__(self):
        self.name = "Orchestration_Reporter"
        self.role = "Principal Enterprise Document Synthesizer"
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        
    def _clean_json_text(self, text: str) -> str:
        # Markdown block parsing fix
        cleaned = text.strip()
        if cleaned.startswith("```"):
            cleaned = re.sub(r'^```(?:json)?\n', '', cleaned, flags=re.IGNORECASE)
            cleaned = re.sub(r'\n```$', '', cleaned)
        return cleaned.strip()

    def synthesize(self, ats: dict, jd: dict, writing: dict, resume_text: str, jd_text: str) -> FinalReport:
        logger.info(f"[{self.name}] assembling final evaluation schema structures and generating improvements.")
        
        # Simple, clear language generation rules added to prompt
        improvement_prompt = f"""
        You are an expert Career Advisor. Review the automated analysis metrics below and prepare clear, easy-to-understand, actionable suggestions that the user can implement to fix their resume and significantly increase their ATS/Job Match score.
        
        RESUME:
        \"\"\"{resume_text}\"\"\"
        
        ATS ENGINE RESULTS:
        {json.dumps(ats, indent=2)}
        
        JOB DESCRIPTION MATCH ENGINE RESULTS:
        {json.dumps(jd, indent=2)}
        
        WRITING QUALITY ENGINE RESULTS:
        {json.dumps(writing, indent=2)}
        
        TASK:
        Generate a JSON array of actionable suggestions matching the Pydantic model.
        
        CRITICAL RULES:
        1. Write in plain, everyday conversational language. Explain clearly WHAT is wrong and EXACTLY HOW the user can rewrite it to secure more points.
        2. Identify specific missing skills from the JD missing lists or low metric sections found in the results.
        3. Provide highly practical rewrite examples using standard metric impacts.
        
        Your output must look exactly like this schema format example:
        [
          {{
            "category": "Missing Core Technologies",
            "finding": "Your resume does not mention critical skills required by the job post.",
            "actionable_fix": "Add missing technologies like Kubernetes and Docker into your technical skills matrix section to pass automated keyword scanner filters.",
            "example": "Technical Core: Python, SQL, Docker, Kubernetes, AWS Node Deployment Management."
          }}
        ]
        
        Output ONLY the raw JSON array. Do not use markdown blocks or backticks.
        """
        
        import re
        improvements = []
        try:
            imp_response = self.client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=improvement_prompt,
                config=types.GenerateContentConfig(temperature=0.2)
            )
            clean_txt = self._clean_json_text(imp_response.text)
            items = json.loads(clean_txt)
            improvements = [ImprovementSuggestion(**item) for item in items]
        except Exception as e:
            logger.error(f"[{self.name}] Improvement parsing failed: {e}. Injecting user-friendly fallback entries.")
            improvements = [
                ImprovementSuggestion(
                    category="ATS Improvement",
                    finding="Your bullet points lack quantifiable business impact metrics and metrics data metrics.",
                    actionable_fix="Rewrite experience bullets to specify exact numbers, percentages, or savings achieved to prove the scale of your work.",
                    example="Before: Responsible for cloud deployment. After: Engineered fully automated CI/CD workflows reducing overall application deployment cycles by 35% on AWS."
                ),
                ImprovementSuggestion(
                    category="Job Match Optimization",
                    finding="Several targeted technical tools from the job description were not discovered on your current resume profile layout.",
                    actionable_fix="Review the 'Missing Technical Skillsets' list below and safely integrate those you have worked with directly into your core competency profile headings.",
                    example="Core Skills Section Update: Appended missing stack targets matching professional project scope guidelines."
                )
            ]

        report_prompt = f"""
        Review the technical assessment records generated by the multi-agent execution pipeline.
        
        ATS Metrics: {json.dumps(ats)}
        JD Match Metrics: {json.dumps(jd)}
        Writing Review Metrics: {json.dumps(writing)}
        
        Task:
        Compile an array of true, objective Strengths and Weaknesses based strictly on the data.
        - Every Weakness must specify actual missing attributes (e.g., missing specific technology found in the JD or explicit structural issues found by the ATS engine).
        - Do not generalize.
        
        Return an output matching this JSON schema blueprint:
        {{
           "strengths": ["string"],
           "weaknesses": ["string"]
        }}
        
        Output only raw clean JSON text. Do not wrap in markdown or backticks.
        """
        
        try:
            rep_response = self.client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=report_prompt,
                config=types.GenerateContentConfig(temperature=0.1)
            )
            clean_rep = self._clean_json_text(rep_response.text)
            payload = json.loads(clean_rep)
            strengths_list = payload.get("strengths", ["Profile structure satisfies necessary resume design sections criteria."])
            weaknesses_list = payload.get("weaknesses", ["Keyword match variance detected relative to core job specification parameters."])
        except Exception:
            strengths_list = ["Profile structure satisfies necessary resume design sections criteria."]
            weaknesses_list = ["Keyword match variance detected relative to core job specification parameters."]
            
        return FinalReport(
            ats_analysis=ats,
            jd_match=jd,
            writing_quality=writing,
            strengths=strengths_list,
            weaknesses=weaknesses_list,
            actionable_improvements=improvements
        )