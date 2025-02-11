from typing import Literal, Optional
from langgraph.graph import StateGraph, MessagesState, START, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.checkpoint.memory import MemorySaver
import os
from dotenv import load_dotenv
load_dotenv()

model = ChatOpenAI(
    openai_api_key=os.getenv("OPEN_AI_KEY"),
    openai_api_base=os.getenv("OPEN_AI_BASE"),
    model_name=os.getenv("OPEN_AI_MODEL_NAME")
)

# --- Graph State Definition ---
class DraftReviewState(MessagesState):
    human_req: str
    human_comment: Optional[str]
    status: Literal["approved", "feedback"]
    assistant_response: str

def assistant_draft(state: DraftReviewState)-> DraftReviewState:
    user_message = HumanMessage(content=state["human_req"])
    system_message = SystemMessage(content=(f"""
        You are an AI assistant revising your previous draft. 
        
        FEEDBACK FROM HUMAN: "{state["human_comment"]}"
        
        Carefully incorporate this feedback into your response. Address all comments, 
        corrections, or suggestions. Ensure your revised response fully integrates 
        the feedback, improves clarity, and resolves any issues raised.
        
        DO NOT repeat the feedback verbatim in your response.

    """))

    all_messages = [user_message] + [system_message]

    response = model.ainvoke(all_messages)

    return {
        "messages": all_messages,
        "assistant_response": response.content
    }


# --- Graph Construction ---
builder=StateGraph(DraftReviewState)

builder.add_node("assistant_draft", assistant_draft)
builder.add_edge(START, 'assistant_draft')
builder.add_edge('assistant_draft', END)

memory = MemorySaver()

graph = builder.compile(checkpointer=memory)

# __all__ = ["graph", "DraftReviewState"]