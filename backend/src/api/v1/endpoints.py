from fastapi import APIRouter, Request, Response
from uuid import uuid4
from models import StartRequest, ResumeRequest, GraphResponse
from sse_starlette import EventSourceResponse
import json

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

    input_state = None

    async def event_generator():
        init_data = json.dumps({"thread_id": thread_id})
        yield {"data": init_data}

        try:
            pass

        except Exception as e:
            print()
            yield {"event": "error", "data": json.dumps({"error": str(e)})}
            