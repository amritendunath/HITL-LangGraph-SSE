from api.v1.endpoints import router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import uvicorn
load_dotenv()


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("CLIENT_SIDE")],
    allow_methods=["*"],
    allow_headers=["*"]
    )

app.include_router(router)

if __name__ =="__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5001, reload=True)