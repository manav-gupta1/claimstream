from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph

from app.agents.nodes import (
    clinical_agent_node,
    query_agent_node,
    response_agent_node,
    retrieval_agent_node,
    verification_agent_node,
)
from app.models.state import ClaimStreamState

# Global singleton instance of compiled graph
_compiled_graph = None


def build_claimstream_graph(checkpointer=None):
    """Build and compile the ClaimStream LangGraph workflow with checkpointer support."""
    if checkpointer is None:
        checkpointer = MemorySaver()

    workflow = StateGraph(ClaimStreamState)

    # Register 5 specialized agent nodes
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
