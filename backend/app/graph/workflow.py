from datetime import datetime
from typing import Any, Dict, List, Union
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph

from app.models.state import AgentTraceItem, ClaimStreamState, WorkflowStatus

# Global singleton instance of compiled graph
_compiled_graph = None


def _get_trace(state: Union[ClaimStreamState, Dict[str, Any]]) -> List[AgentTraceItem]:
    """Helper to safely extract existing agent_trace list from Pydantic state or dict."""
    if isinstance(state, ClaimStreamState):
        return list(state.agent_trace)
    elif isinstance(state, dict):
        raw_trace = state.get("agent_trace", [])
        trace_items = []
        for item in raw_trace:
            if isinstance(item, AgentTraceItem):
                trace_items.append(item)
            elif isinstance(item, dict):
                trace_items.append(AgentTraceItem(**item))
        return trace_items
    return []


# ==========================================
# Placeholder Agent Nodes
# ==========================================

def query_agent_node(state: Union[ClaimStreamState, Dict[str, Any]]) -> Dict[str, Any]:
    """Placeholder node for Query Agent."""
    trace = _get_trace(state)
    trace.append(
        AgentTraceItem(
            agent_name="query_agent",
            action="Analyzed TPA clarification query intent and requirements",
            output_summary="Query intent parsed. Evidence categories identified.",
            timestamp=datetime.utcnow().isoformat(),
        )
    )
    return {
        "workflow_status": WorkflowStatus.QUERY_ANALYZED,
        "agent_trace": trace,
        "updated_at": datetime.utcnow().isoformat(),
    }


def retrieval_agent_node(state: Union[ClaimStreamState, Dict[str, Any]]) -> Dict[str, Any]:
    """Placeholder node for Retrieval Agent."""
    trace = _get_trace(state)
    trace.append(
        AgentTraceItem(
            agent_name="retrieval_agent",
            action="Scanned synthetic FHIR patient records",
            output_summary="Evidence items extracted from clinical records.",
            timestamp=datetime.utcnow().isoformat(),
        )
    )
    return {
        "workflow_status": WorkflowStatus.EVIDENCE_RETRIEVED,
        "agent_trace": trace,
        "updated_at": datetime.utcnow().isoformat(),
    }


def clinical_agent_node(state: Union[ClaimStreamState, Dict[str, Any]]) -> Dict[str, Any]:
    """Placeholder node for Clinical Analysis Agent."""
    trace = _get_trace(state)
    trace.append(
        AgentTraceItem(
            agent_name="clinical_agent",
            action="Analyzed clinical timeline, consistency, and medical necessity",
            output_summary="Clinical rationale and documentation review completed.",
            timestamp=datetime.utcnow().isoformat(),
        )
    )
    return {
        "workflow_status": WorkflowStatus.CLINICAL_ANALYZED,
        "agent_trace": trace,
        "updated_at": datetime.utcnow().isoformat(),
    }


def response_agent_node(state: Union[ClaimStreamState, Dict[str, Any]]) -> Dict[str, Any]:
    """Placeholder node for Response Synthesis Agent."""
    trace = _get_trace(state)
    trace.append(
        AgentTraceItem(
            agent_name="response_agent",
            action="Synthesized formal TPA response package",
            output_summary="Draft response generated with evidence citations.",
            timestamp=datetime.utcnow().isoformat(),
        )
    )
    return {
        "workflow_status": WorkflowStatus.RESPONSE_GENERATED,
        "agent_trace": trace,
        "updated_at": datetime.utcnow().isoformat(),
    }


def verification_agent_node(state: Union[ClaimStreamState, Dict[str, Any]]) -> Dict[str, Any]:
    """Placeholder node for Verification Agent."""
    trace = _get_trace(state)
    trace.append(
        AgentTraceItem(
            agent_name="verification_agent",
            action="Executed verification agent placeholder",
            output_summary="Verification processing completed (placeholder).",
            timestamp=datetime.utcnow().isoformat(),
        )
    )
    return {
        "workflow_status": WorkflowStatus.VERIFICATION_COMPLETED,
        "agent_trace": trace,
        "updated_at": datetime.utcnow().isoformat(),
    }


# ==========================================
# Graph Builder & Factory
# ==========================================

def build_claimstream_graph(checkpointer=None):
    """Build and compile the ClaimStream LangGraph workflow with checkpointer support."""
    if checkpointer is None:
        checkpointer = MemorySaver()

    workflow = StateGraph(ClaimStreamState)

    # Register 5 placeholder nodes
    workflow.add_node("query_agent", query_agent_node)
    workflow.add_node("retrieval_agent", retrieval_agent_node)
    workflow.add_node("clinical_agent", clinical_agent_node)
    workflow.add_node("response_agent", response_agent_node)
    workflow.add_node("verification_agent", verification_agent_node)

    # Define linear sequential workflow
    workflow.add_edge(START, "query_agent")
    workflow.add_edge("query_agent", "retrieval_agent")
    workflow.add_edge("retrieval_agent", "clinical_agent")
    workflow.add_edge("clinical_agent", "response_agent")
    workflow.add_edge("response_agent", "verification_agent")
    workflow.add_edge("verification_agent", END)

    compiled_graph = workflow.compile(checkpointer=checkpointer)
    return compiled_graph


def get_claimstream_graph():
    """Retrieve or initialize reusable compiled graph instance."""
    global _compiled_graph
    if _compiled_graph is None:
        _compiled_graph = build_claimstream_graph()
    return _compiled_graph
