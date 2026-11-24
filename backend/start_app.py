from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import run_main_flow

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Request(BaseModel):
    question: str


@app.post("/ask")
def ask(req: Request):
    try:
        answer = run_main_flow(req.question)
        return {"answer": answer}
    except Exception as e:
        print("ERROR:", e)
        return {"answer": "Something went wrong"}