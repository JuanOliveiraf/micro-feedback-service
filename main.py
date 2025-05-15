from fastapi import FastAPI,Query
from typing import List
from feedback import gerar_feedbacks
from models import FeedbackSaida
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # ou use ["*"] durante o desenvolvimento
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/feedback/{mentored_id}", response_model=List[FeedbackSaida])
def retorna_feedback(mentored_id: int):
    return gerar_feedbacks(mentored_id)