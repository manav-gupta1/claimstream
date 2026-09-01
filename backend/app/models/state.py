from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class WorkflowStatus(str, Enum):
    INITIALIZED = "INITIALIZED"
    QUERY_ANALYZED = "QUERY_ANALYZED"
    EVIDENCE_RETRIEVED = "EVIDENCE_RETRIEVED"
    CLINICAL_ANALYZED = "CLINICAL_ANALYZED"
    RESPONSE_GENERATED = "RESPONSE_GENERATED"
    VERIFICATION_COMPLETED = "VERIFICATION_COMPLETED"
    PENDING_HUMAN_REVIEW = "PENDING_HUMAN_REVIEW"
    HUMAN_REVIEWED = "HUMAN_REVIEWED"
    VERIFIED = "VERIFIED"
    ESCALATED = "ESCALATED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class VerificationStatus(str, Enum):
    VERIFIED = "VERIFIED"
    NEEDS_REVIEW = "NEEDS_REVIEW"


class HumanDecisionType(str, Enum):
    APPROVE = "APPROVE"
    REQUEST_MODIFICATION = "REQUEST_MODIFICATION"
    ESCALATE = "ESCALATE"


class EvidenceItem(BaseModel):
    id: str = Field(..., description="Unique evidence ID")
    source: str = Field(..., description="EHR source resource, e.g., Condition, Procedure, Encounter")
    type: str = Field(..., description="Type of evidence, e.g., Clinical Note, Lab Result, Imaging Report")
    content: str = Field(..., description="Text content or clinical snippet")
    timestamp: str = Field(..., description="Date/time of clinical record")
    relevance: float = Field(..., ge=0.0, le=1.0, description="Relevance score to query")


class QueryAnalysis(BaseModel):
    query_intent: str = Field(..., description="Core intent of TPA query")
    requested_information: List[str] = Field(default_factory=list, description="Specific details requested by TPA")
    required_evidence_categories: List[str] = Field(
        default_factory=list, description="Categories of clinical data needed to respond"
    )
    urgency: Optional[str] = Field(default="STANDARD", description="Urgency level, e.g., HIGH, STANDARD")


class ClinicalAnalysis(BaseModel):
    timeline: List[Dict[str, str]] = Field(default_factory=list, description="Chronological clinical timeline")
    consistency: str = Field(..., description="Assessment of clinical record consistency")
    justification: str = Field(..., description="Clinical medical necessity rationale")
    missing_evidence: List[str] = Field(default_factory=list, description="Missing clinical documentation")
    conflicting_evidence: List[str] = Field(default_factory=list, description="Discrepancies found across records")


class GeneratedResponse(BaseModel):
    draft_response: str = Field(..., description="Formal response package synthesized for TPA")
    citations: List[str] = Field(default_factory=list, description="Explicit clinical evidence citations")
    suggested_attachments: List[str] = Field(default_factory=list, description="Suggested EHR documents to attach")


class VerificationResult(BaseModel):
    status: VerificationStatus = Field(..., description="VERIFIED or NEEDS_REVIEW")
    confidence_score: float = Field(..., ge=0.0, le=100.0, description="Confidence percentage 0-100")
    unsupported_claims: List[str] = Field(default_factory=list, description="Claims lacking direct evidence")
    issues: List[str] = Field(default_factory=list, description="List of verification flags or missing criteria")


class AgentTraceItem(BaseModel):
    agent_name: str = Field(..., description="Name of agent executing node")
    action: str = Field(..., description="Description of action performed")
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat(), description="Execution timestamp")
    output_summary: str = Field(..., description="Brief summary of agent output")
    details: Optional[Dict[str, Any]] = Field(default=None, description="Structured agent payload")


class HumanDecision(BaseModel):
    decision: HumanDecisionType = Field(..., description="APPROVE, REQUEST_MODIFICATION, or ESCALATE")
    reviewer_notes: Optional[str] = Field(None, description="Notes or modifications requested by reviewer")
    reviewer_id: Optional[str] = Field("dr_reviewer_1", description="Reviewer identifier")
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class ClaimStreamState(BaseModel):
    case_id: str = Field(..., description="Unique case identifier")
    query: str = Field(..., description="Original TPA / Insurance clarification query text")
    patient_id: str = Field(..., description="Patient identifier")
    patient_data: Dict[str, Any] = Field(default_factory=dict, description="Synthetic FHIR/EHR patient data")

    # Workflow Artifacts
    query_analysis: Optional[QueryAnalysis] = None
    retrieved_evidence: List[EvidenceItem] = Field(default_factory=list)
    clinical_analysis: Optional[ClinicalAnalysis] = None
    generated_response: Optional[GeneratedResponse] = None
    verification_result: Optional[VerificationResult] = None

    # Scores & Status
    confidence_score: float = Field(default=0.0, ge=0.0, le=100.0)
    workflow_status: WorkflowStatus = Field(default=WorkflowStatus.INITIALIZED)
    human_review_required: bool = Field(default=False)
    human_decision: Optional[HumanDecision] = None

    # Audit & Diagnostics
    agent_trace: List[AgentTraceItem] = Field(default_factory=list)
    errors: List[str] = Field(default_factory=list)
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
