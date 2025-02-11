from src.api.v1.endpoints import router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
load_dotenv()


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("CLIENT_SIDE")],
    allow_methods=["*"],
    allow_headers=["*"]
    )

app.include_router(router)