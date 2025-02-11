from pydantic import BaseModel
from typing import Dict, Optional, Literal

class StartRequest(BaseModel):
    human_req: str

class ResumeRequest(BaseModel):
    thread_id: str

class GraphResponse(BaseModel):
    thread_id: str
