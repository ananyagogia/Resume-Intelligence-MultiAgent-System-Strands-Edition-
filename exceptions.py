class ResumeIntelException(Exception):
    """Base exception for the Resume Intelligence System."""
    pass

class IngestionError(ResumeIntelException):
    """Raised when document ingestion or parsing fails."""
    pass

class AnalysisError(ResumeIntelException):
    """Raised when an engine analysis execution fails."""
    pass

class AgentWorkflowError(ResumeIntelException):
    """Raised when Strands agent routing or coordination breaks."""
    pass