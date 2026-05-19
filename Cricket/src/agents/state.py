from typing import TypedDict, Annotated, List
from langchain_core.messages import BaseMessage
import operator

class AgentState(TypedDict):
    """
    The state of our multi-agent workflow.
    """
    # The user's original query
    query: str
    
    # The message history (if keeping conversation state)
    messages: Annotated[List[BaseMessage], operator.add]
    
    # Data gathered by the Research Agent
    research_context: str
    
    # Data gathered by the Stats Agent
    stats_data: str
    
    # Draft created by the Writer Agent
    draft: str
    
    # Final verified output by the Fact Checker Agent
    final_output: str
    
    # Current active agent/node name for routing
    current_agent: str
