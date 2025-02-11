from fastapi import APIRouter, Request, Response
from uuid import uuid4
from src.models import StartRequest, ResumeRequest, GraphResponse
from sse_starlette import EventSourceResponse
import json

router = APIRouter()

