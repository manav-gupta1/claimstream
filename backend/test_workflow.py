from app.data import get_mock_case
from app.graph import get_claimstream_graph
from app.models import ClaimStreamState, WorkflowStatus


def run_case_test(case_id: str, thread_id: str):
    print(f"\n==========================================")
    print(f"Testing Placeholder Workflow for: {case_id}")
    print(f"==========================================")

    # 1. Load Case
    mock_case = get_mock_case(case_id)
    assert mock_case is not None, f"{case_id} should exist in mock_data"

    # 2. Convert to ClaimStreamState
    initial_state = ClaimStreamState(
        case_id=mock_case["case_id"],
        query=mock_case["query"],
        patient_id=mock_case["patient_id"],
        patient_data=mock_case["patient_data"],
        workflow_status=WorkflowStatus.INITIALIZED,
    )

    print(f"Initialized State for {initial_state.case_id} (Patient: {initial_state.patient_id})")

    # 3. Retrieve compiled graph
    graph = get_claimstream_graph()

    # 4. Execute graph with thread_id config
    config = {"configurable": {"thread_id": thread_id}}

    print("Executing placeholder graph traversal...")
    final_output = graph.invoke(initial_state, config=config)

    # Convert dictionary or state to ClaimStreamState
    if isinstance(final_output, dict):
        final_state = ClaimStreamState(**final_output)
    else:
        final_state = final_output

    # 5. Verify all 5 node traces
    expected_agents = [
        "query_agent",
        "retrieval_agent",
        "clinical_agent",
        "response_agent",
        "verification_agent",
    ]

    trace_agent_names = [item.agent_name for item in final_state.agent_trace]
    print(f"Agent Trace Captured ({len(trace_agent_names)} nodes):")
    for idx, trace in enumerate(final_state.agent_trace, 1):
        print(f"  {idx}. [{trace.agent_name}] -> {trace.output_summary}")

    assert len(final_state.agent_trace) == 5, f"Expected 5 traces, found {len(final_state.agent_trace)}"
    for expected in expected_agents:
        assert expected in trace_agent_names, f"Expected agent '{expected}' in trace, but found {trace_agent_names}"

    # 6. Verify Checkpointer Persistence
    checkpoint_state = graph.get_state(config)
    assert checkpoint_state is not None, "Checkpointer state should not be None"
    assert checkpoint_state.values.get("case_id") == case_id, f"Checkpointer should persist case_id {case_id}"

    # 7. Verify neutral placeholder completion status
    assert final_state.workflow_status == WorkflowStatus.VERIFICATION_COMPLETED, (
        f"Expected status VERIFICATION_COMPLETED, got {final_state.workflow_status}"
    )

    print(f"✓ {case_id} Workflow Status: {final_state.workflow_status.value}")
    print(f"✓ {case_id} Checkpointer thread '{thread_id}' verified.")


def test_all_cases():
    print("--- Starting ClaimStream Step 2 Workflow Verification ---")
    run_case_test("CASE_001", "thread_case_001_placeholder")
    run_case_test("CASE_002", "thread_case_002_placeholder")
    print("\n==========================================")
    print("✓ ALL PLACEHOLDER WORKFLOW TESTS PASSED FOR CASE_001 & CASE_002")
    print("==========================================")


if __name__ == "__main__":
    test_all_cases()
