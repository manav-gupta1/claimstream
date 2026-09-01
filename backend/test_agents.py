from app.agents import (
    clinical_agent_node,
    query_agent_node,
    response_agent_node,
    retrieval_agent_node,
    verification_agent_node,
)
from app.data import get_mock_case
from app.models import (
    ClaimStreamState,
    VerificationStatus,
    WorkflowStatus,
)


def run_agent_unit_test(case_id: str):
    print(f"\n==========================================")
    print(f"Running Agent Pipeline Unit Test: {case_id}")
    print(f"==========================================")

    # 1. Initialize State from Mock Data
    case_data = get_mock_case(case_id)
    assert case_data is not None, f"Case {case_id} not found"

    state = ClaimStreamState(
        case_id=case_data["case_id"],
        query=case_data["query"],
        patient_id=case_data["patient_id"],
        patient_data=case_data["patient_data"],
        workflow_status=WorkflowStatus.INITIALIZED,
    )

    # 2. Execute Query Agent
    print("[1/5] Executing Query Agent...")
    u1 = query_agent_node(state)
    state = state.model_copy(update=u1)
    assert state.query_analysis is not None, "query_analysis must be populated"
    print(f"  -> Intent: {state.query_analysis.query_intent}")
    print(f"  -> Requested Info: {state.query_analysis.requested_information}")
    print(f"  -> Required Categories: {state.query_analysis.required_evidence_categories}")

    # 3. Execute Retrieval Agent
    print("\n[2/5] Executing Retrieval Agent...")
    u2 = retrieval_agent_node(state)
    state = state.model_copy(update=u2)
    assert len(state.retrieved_evidence) > 0, "retrieved_evidence must not be empty"
    print(f"  -> Retrieved {len(state.retrieved_evidence)} evidence items:")
    for ev in state.retrieved_evidence:
        print(f"     * [{ev.id}] {ev.source} - {ev.type} (Relevance: {ev.relevance})")

    # 4. Execute Clinical Analysis Agent
    print("\n[3/5] Executing Clinical Analysis Agent...")
    u3 = clinical_agent_node(state)
    state = state.model_copy(update=u3)
    assert state.clinical_analysis is not None, "clinical_analysis must be populated"
    print(f"  -> Consistency: {state.clinical_analysis.consistency}")
    print(f"  -> Justification: {state.clinical_analysis.justification}")
    print(f"  -> Missing Evidence ({len(state.clinical_analysis.missing_evidence)}): {state.clinical_analysis.missing_evidence}")
    print(f"  -> Conflicting Evidence ({len(state.clinical_analysis.conflicting_evidence)}): {state.clinical_analysis.conflicting_evidence}")

    # 5. Execute Response Agent
    print("\n[4/5] Executing Response Agent...")
    u4 = response_agent_node(state)
    state = state.model_copy(update=u4)
    assert state.generated_response is not None, "generated_response must be populated"
    print(f"  -> Citations Count: {len(state.generated_response.citations)}")
    print(f"  -> Suggested Attachments: {state.generated_response.suggested_attachments}")
    print(f"  -> Response Snippet: {state.generated_response.draft_response[:120]}...")

    # 6. Execute Verification Agent
    print("\n[5/5] Executing Verification Agent...")
    u5 = verification_agent_node(state)
    state = state.model_copy(update=u5)
    assert state.verification_result is not None, "verification_result must be populated"
    print(f"  -> Confidence Score: {state.confidence_score:.1f}%")
    print(f"  -> Verification Status: {state.verification_result.status.value}")
    print(f"  -> Human Review Required: {state.human_review_required}")
    print(f"  -> Workflow Status: {state.workflow_status.value}")
    print(f"  -> Issues Detected: {state.verification_result.issues}")

    # 7. Check Agent Trace
    assert len(state.agent_trace) == 5, f"Expected 5 trace items, found {len(state.agent_trace)}"
    trace_names = [t.agent_name for t in state.agent_trace]
    print(f"\nTrace Nodes Recorded: {trace_names}")

    # 8. Case-Specific Assertions
    if case_id == "CASE_001":
        assert state.confidence_score >= 90.0, f"CASE_001 confidence must be >= 90, got {state.confidence_score}"
        assert state.verification_result.status == VerificationStatus.VERIFIED, "CASE_001 must be VERIFIED"
        assert state.human_review_required is False, "CASE_001 must not require human review"
        assert state.workflow_status == WorkflowStatus.VERIFIED, "CASE_001 workflow status must be VERIFIED"
        print(f"✓ CASE_001 PASSED ALL CLEAR CASE CRITERIA (Confidence: {state.confidence_score:.1f}%)")
    elif case_id == "CASE_002":
        assert state.confidence_score < 80.0, f"CASE_002 confidence must be < 80, got {state.confidence_score}"
        assert state.verification_result.status == VerificationStatus.NEEDS_REVIEW, "CASE_002 must be NEEDS_REVIEW"
        assert state.human_review_required is True, "CASE_002 must require human review"
        assert state.workflow_status == WorkflowStatus.PENDING_HUMAN_REVIEW, "CASE_002 workflow status must be PENDING_HUMAN_REVIEW"
        assert len(state.clinical_analysis.missing_evidence) > 0 or len(state.clinical_analysis.conflicting_evidence) > 0
        print(f"✓ CASE_002 PASSED ALL AMBIGUOUS CASE CRITERIA (Confidence: {state.confidence_score:.1f}%, HITL Required: True)")

    return state


def main():
    print("--- Starting ClaimStream Multi-Agent Unit Tests ---")
    s1 = run_agent_unit_test("CASE_001")
    s2 = run_agent_unit_test("CASE_002")
    print("\n==========================================")
    print("✓ ALL AGENT UNIT TESTS PASSED SUCCESSFULLY")
    print(f"  CASE_001 Score: {s1.confidence_score:.1f}% | Status: {s1.workflow_status.value}")
    print(f"  CASE_002 Score: {s2.confidence_score:.1f}% | Status: {s2.workflow_status.value}")
    print("==========================================")


if __name__ == "__main__":
    main()
