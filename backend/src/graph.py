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
    response = model.ainvoke(user_message)

    return {
        "messages": user_message,
        "assistant_response": response.content
    }
