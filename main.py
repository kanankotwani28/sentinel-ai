from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from aiml.pipeline import analyze_prompt

app = FastAPI(
    title="Sentinel AI",
    description="AIML Security Layer — Protects LLMs from prompt injection and jailbreak attacks",
    version="1.0.0",
)

# Allow all origins, no CORS restrictions
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class PromptRequest(BaseModel):
    prompt: str


@app.get("/")
async def health_check():
    return {"status": "ok", "service": "sentinel-ai"}


@app.post("/analyze")
async def analyze(request: PromptRequest):
    """
    Analyze a user prompt for jailbreak / adversarial intent.

    Returns a verdict with status (ALLOWED | BLOCKED | SUSPICIOUS),
    confidence, risk_score, detected patterns, and reasoning.
    """
    result = analyze_prompt(request.prompt)
    return result
