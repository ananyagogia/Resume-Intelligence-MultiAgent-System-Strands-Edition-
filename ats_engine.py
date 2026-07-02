import re
from typing import List, Dict
from core.models import ATSAnalysisResult, ContactInfo, SectionPresence, FormattingSignals

COMMON_SKILLS_DB = {
    "python", "java", "javascript", "typescript", "c++", "c", "go", "rust", "sql", "nosql",
    "aws", "azure", "gcp", "docker", "kubernetes", "terraform", "ci/cd", "git", "github",
    "pytorch", "tensorflow", "scikit-learn", "llm", "rag", "langchain", "gan", "tkinter",
    "agile", "scrum", "system design", "html", "css", "gan-based"
}

ACTION_VERBS = {
    "built", "designed", "developed", "engineered", "implemented", "improved", "managed",
    "optimized", "spearheaded", "accelerated", "achieved", "coordinated", "executed"
}

class ATSEngine:
    """
    Deterministic scoring matrix matching real technical resume standards.
    Permanently removes the unnecessary 'Summary' constraint for engineering profiles.
    """
    
    @staticmethod
    def analyze(text: str) -> ATSAnalysisResult:
        lowered = text.lower()
        
        # 1. Contact Information Verification
        email_match = bool(re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text))
        phone_match = bool(re.search(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}|\+\d{2}\d{10}', text))
        linkedin_match = "linkedin.com/" in lowered
        github_match = "github.com/" in lowered
        
        contact = ContactInfo(
            has_email=email_match,
            has_phone=phone_match,
            has_linkedin=linkedin_match,
            has_github=github_match
        )
        
        # 2. Section Assertions (No summary penalty)
        sections = SectionPresence(
            summary=True, # Explicitly bypassing to avoid penalty
            experience=any(h in lowered for h in ["experience", "employment", "work history", "projects", "academic projects"]),
            education="education" in lowered,
            skills="skills" in lowered,
            projects=any(h in lowered for h in ["projects", "personal projects", "open source"])
        )
        
        # 3. Formatting & Signals
        bullet_points = text.count("•") + text.count("- ") + text.count("* ")
        has_bullets = bullet_points > 3
        est_pages = max(1, len(text) // 3000)
        formatting = FormattingSignals(has_bullet_points=has_bullets, estimated_page_count=est_pages)
        
        # 4. Syntactic Term Matchers
        detected_skills = [skill for skill in COMMON_SKILLS_DB if re.search(r'\b' + re.escape(skill) + r'\b', lowered)]
        words = re.findall(r'\b\w+\b', lowered)
        action_verbs_found = sum(1 for w in words if w in ACTION_VERBS)
        metrics_found = len(re.findall(r'\b\d+%\b|\$\d+|\b\d+\s*(?:million|users|percent|roi|reduction|growth|cgpa|ranking)\b', lowered))
        
        # 5. Corrected Score Allocation Map (Max 100)
        score_breakdown: Dict[str, float] = {}
        
        # Contact Mapping (Max 20)
        contact_score = (sum([email_match, phone_match, linkedin_match, github_match]) / 4.0) * 20.0
        score_breakdown["Contact Links Validation"] = round(contact_score, 2)
        
        # Structural Layout Sections (Max 20)
        valid_sections = sum([sections.experience, sections.education, sections.skills, sections.projects])
        section_score = (valid_sections / 4.0) * 20.0
        score_breakdown["Technical Sections Structural Presence"] = round(section_score, 2)
        
        # Verb & Impact Architecture (Max 30)
        verb_score = min(15.0, (action_verbs_found / 5.0) * 15.0)
        metric_score = min(15.0, (metrics_found / 2.0) * 15.0)
        score_breakdown["Action Verbs Validation"] = round(verb_score, 2)
        score_breakdown["Quantifiable Impacts & Performance Metrics"] = round(metric_score, 2)
        
        # Core Tech Stack Density (Max 20)
        skill_score = min(20.0, (len(detected_skills) / 6.0) * 20.0)
        score_breakdown["Core Tech Skill Density"] = round(skill_score, 2)
        
        # Layout (Max 10)
        layout_score = 10.0 if (has_bullets and est_pages <= 2) else 5.0
        score_breakdown["Layout Execution Standards"] = round(layout_score, 2)
        
        return ATSAnalysisResult(
            score=min(100.0, round(sum(score_breakdown.values()), 2)),
            contact_info=contact,
            sections=sections,
            formatting=formatting,
            detected_skills=detected_skills,
            action_verbs_count=action_verbs_found,
            quantified_metrics_count=metrics_found,
            score_breakdown=score_breakdown
        )