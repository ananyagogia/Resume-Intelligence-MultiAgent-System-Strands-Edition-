import re
from typing import List, Counter
from core.models import WritingQualityResult

VAGUE_PHRASES = {
    "responsible for", "assisted with", "helped design", "worked on", "participated in",
    "team player", "results-oriented", "detail-oriented", "passionate professional"
}

PASSIVE_INDICATORS = {
    "was developed by", "were engineered by", "was responsible for", "tasks were given",
    "was managed by", "had been chosen"
}

class WritingAnalyserEngine:
    """
    Deterministic structural linguistics parser analyzing language patterns.
    """
    
    @staticmethod
    def analyze(text: str) -> WritingQualityResult:
        lowered = text.lower()
        words = re.findall(r'\b\w+\b', lowered)
        
        # 1. Deduce duplicate keyword repetition clusters
        filtered_words = [w for w in words if len(w) > 4]
        counts = Counter(filtered_words)
        repetitive = [word for word, count in counts.items() if count >= 6]
        
        # 2. Vague syntax analysis
        vague_detected = [p for p in VAGUE_PHRASES if p in lowered]
        
        # 3. Passive parsing constraints
        passive_count = sum(lowered.count(p) for p in PASSIVE_INDICATORS)
        
        # 4. Extract bullet compositions
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        bullets = [l for l in lines if l.startswith(('•', '-', '*'))]
        
        weak_bullets = 0
        for b in bullets:
            b_low = b.lower()
            # Weak if bullet has no numbers/metrics and is short
            has_metric = bool(re.search(r'\d', b))
            if not has_metric and len(b.split()) < 12:
                weak_bullets += 1
                
        # 5. Deterministic structural calculation of Natural Composition Index
        # Formula starts at 100 base score, penalizing bad patterns
        deductions = (len(repetitive) * 4) + (len(vague_detected) * 5) + (passive_count * 6) + (weak_bullets * 5)
        heuristic_score = max(10.0, float(100 - deductions))
        
        explanation = (
            f"Linguistic health rating computed at {heuristic_score}/100 based entirely on clear metrics: "
            f"Flagged {weak_bullets} weak bullet structures missing metrics, caught {passive_count} occurrences of passive voice, "
            f"and isolated {len(vague_detected)} boilerplate expressions."
        )
        
        return WritingQualityResult(
            repetitive_words_detected=repetitive,
            weak_bullet_points_count=weak_bullets,
            passive_voice_instances=passive_count,
            vague_phrases_detected=vague_detected,
            ai_heuristic_score=heuristic_score,
            ai_heuristic_explanation=explanation
        )