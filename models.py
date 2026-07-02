from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class ContactInfo(BaseModel):
    has_email: bool
    has_phone: bool
    has_linkedin: bool
    has_github: bool

class SectionPresence(BaseModel):
    summary: bool
    experience: bool
    education: bool
    skills: bool
    projects: bool

class FormattingSignals(BaseModel):
    has_bullet_points: bool
    estimated_page_count: int

class ATSAnalysisResult(BaseModel):
    score: float = Field(..., description="Deterministic score from 0 to 100")
    contact_info: ContactInfo
    sections: SectionPresence
    formatting: FormattingSignals
    detected_skills: List[str]
    action_verbs_count: int
    quantified_metrics_count: int
    score_breakdown: Dict[str, float]

class JDMatchResult(BaseModel):
    match_percentage: float
    matching_skills: List[str]
    missing_skills: List[str]
    experience_gap_detected: bool
    experience_gap_reason: str
    education_gap_detected: bool
    education_gap_reason: str
    calculation_breakdown: Dict[str, str]

class WritingQualityResult(BaseModel):
    repetitive_words_detected: List[str]
    weak_bullet_points_count: int
    passive_voice_instances: int
    vague_phrases_detected: List[str]
    ai_heuristic_score: float = Field(..., description="Heuristic scale 0-100, where 100 is highly natural")
    ai_heuristic_explanation: str

class ImprovementSuggestion(BaseModel):
    category: str  # e.g., "ATS", "JD Match", "Writing Quality"
    finding: str
    actionable_fix: str
    example: Optional[str] = None

class FinalReport(BaseModel):
    ats_analysis: ATSAnalysisResult
    jd_match: JDMatchResult
    writing_quality: WritingQualityResult
    strengths: List[str]
    weaknesses: List[str]
    actionable_improvements: List[ImprovementSuggestion]