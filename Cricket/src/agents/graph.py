from langgraph.graph import StateGraph, END
from src.agents.state import AgentState
from src.agents.nodes import research_agent, stats_agent, writer_agent, fact_checker_agent

def create_workflow():
    """Compiles the multi-agent LangGraph workflow."""
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("researcher", research_agent)
    workflow.add_node("statistician", stats_agent)
    workflow.add_node("writer", writer_agent)
    workflow.add_node("fact_checker", fact_checker_agent)
    
    # Define edges (The flow of the graph)
    workflow.set_entry_point("researcher")
    
    workflow.add_edge("researcher", "statistician")
    workflow.add_edge("statistician", "writer")
    workflow.add_edge("writer", "fact_checker")
    workflow.add_edge("fact_checker", END)
    
    # Compile
    app = workflow.compile()
    return app

def run_workflow(query: str):
    """Utility to run the workflow."""
    app = create_workflow()
    initial_state = {"query": query, "messages": []}
    
    # Run the graph
    result = app.invoke(initial_state)
    return result.get("final_output", "No output generated.")
