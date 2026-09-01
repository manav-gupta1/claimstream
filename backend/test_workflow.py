from app.data import get_mock_case
from app.graph import get_claimstream_graph
from app.models import (
    ClaimStreamState,
    VerificationStatus,
    WorkflowStatus,
)


def run_graph_case(case_id: str, thread_id: str) -> ClaimStreamState:
    print(f"\n==========================================")
    print(f"Executing LangGraph Workflow: {case_id}")
    print(f"==========================================")

    # 1. Load mock case
    case_data = get_mock_case(case_id)
    assert case_data is not None, f"Case {case_id} not found"

    # 2. Build initial state
    initial_state = ClaimStreamState(
        case_id=case_data["case_id"],
        query=case_data["query"],
        patient_id=case_data["patient_id"],
        patient_data=case_data["patient_data"],
        workflow_status=WorkflowStatus.INITIALIZED,
    )

    # 3. Retrieve graph & execute with checkpointer config
    graph = get_claimstream_graph()
    config = {"configurable": {"thread_id": thread_id}}

    final_output = graph.invoke(initial_state, config=config)

    if isinstance(final_output, dict):
        final_state = ClaimStreamState(**final_output)
    else:
        final_state = final_output

    # 4. Verify Trace
    print(f"Workflow Executed {len(final_state.agent_trace)} Nodes:")
    for idx, trace in enumerate(final_state.agent_trace, 1):
        print(f"  {idx}. [{trace.agent_name}] -> {trace.output_summary}")

    assert len(final_state.agent_trace) == 5, f"Expected 5 traces, got {len(final_state.agent_trace)}"

    # 5. Verify Checkpointer Persistence
    checkpoint_state = graph.get_state(config)
    assert checkpoint_state is not None, "Checkpointer state must exist"
    assert checkpoint_state.values.get("case_id") == case_id, "Checkpointer must persist case_id"

    # 6. Verify Artifacts
    assert final_state.query_analysis is not None, "query_analysis must be populated"
    assert len(final_state.retrieved_evidence) > 0, "retrieved_evidence must not be empty"
    assert final_state.clinical_analysis is not None, "clinical_analysis must be populated"
    assert final_state.generated_response is not None, "generated_response must be populated"
    assert final_state.verification_result is not None, "verification_result must be populated"

    # 7. Case-specific Outcome Assertions
    if case_id == "CASE_001":
        assert final_state.workflow_status == WorkflowStatus.VERIFIED, (
            f"CASE_001 expected VERIFIED, got {final_state.workflow_status}"
        )
        assert final_state.confidence_score >= 90.0, f"Expected >= 90, got {final_state.confidence_score}"
        assert final_state.human_review_required is False
        assert final_state.verification_result.status == VerificationStatus.VERIFIED
        print(f"\n✓ CASE_001 Output: Status={final_state.workflow_status.value}, Confidence={final_state.confidence_score:.1f}%")

    elif case_id == "CASE_002":
        assert final_state.workflow_status == WorkflowStatus.PENDING_HUMAN_REVIEW, (
            f"CASE_002 expected PENDING_HUMAN_REVIEW, got {final_state.workflow_status}"
        )
        assert final_state.confidence_score < 80.0, f"Expected < 80, got {final_state.confidence_score}"
        assert final_state.human_review_required is True
        assert final_state.verification_result.status == VerificationStatus.NEEDS_REVIEW
        print(f"\n✓ CASE_002 Output: Status={final_state.workflow_status.value}, Confidence={final_state.confidence_score:.1f}% (HITL Required)")

    return final_state


def main():
    print("--- Starting LangGraph Integrated Workflow Test ---")
    s1 = run_graph_case("CASE_001", "thread_case_001_v1")
    s2 = run_graph_case("CASE_002", "thread_case_002_v1")
    print("\n==========================================")
    print("✓ ALL LANGGRAPH WORKFLOW INTEGRATION TESTS PASSED")
    print(f"  CASE_001: {s1.workflow_status.value} (Confidence: {s1.confidence_score:.1f}%)")
    print(f"  CASE_002: {s2.workflow_status.value} (Confidence: {s2.confidence_score:.1f}%)")
    print("==========================================")


if __name__ == "__main__":
    main()
