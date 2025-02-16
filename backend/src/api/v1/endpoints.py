from fastapi import APIRouter, Request, Response
from uuid import uuid4
from models import StartRequest, ResumeRequest, GraphResponse
from sse_starlette import EventSourceResponse
from graph import graph
import json, logging
logger = logging.getLogger(__name__)

router = APIRouter()

run_config={}

@router.get('/graph/stream/create', response_model=GraphResponse)
def create_graph_streaming(request: StartRequest):
    thread_id = str(uuid4())

    run_config[thread_id]={
        "human_req": request.human_req
    }

    return GraphResponse(
        thread_id=thread_id
    )


@router.get('/graph/stream/{thread_id}')
async def stream_graph(request: Request, thread_id: str):
    if thread_id not in run_config:
        return f"Thread_id not found"
    
    run_data = run_config[thread_id]
    config = {"configurable": {"thread_id": thread_id}}

    input_state = run_data["human_req"]

    async def event_generator():
        init_data = json.dumps({"thread_id": thread_id})
        yield {"data": init_data}

        try:
            # pass
            for msg, metadata in graph.astream(input_state, config):
                if await request.is_disconnected():
                    logger.info("DEBUG : Client disconnected")
                if metadata.get('langgraph_node') in ['assistant_draft']:
                    token_data = json.dumps({"content": msg.content})
                    logger.info(f"DEBUG: Sending token event with data: {token_data[:30]}")
                    yield {"event": "token", "data": token_data}

        except Exception as e:
            logger.error()
            yield {"event": "error", "data": json.dumps({"error": str(e)})}
    
    return EventSourceResponse(event_generator())

            
