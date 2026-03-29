from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from aiml.pipeline import analyze_prompt

# In-memory statistics for the demo dashboard
stats = {
    "total_analyzed": 0,
    "total_blocked": 0,
    "total_allowed": 0,
    "total_suspicious": 0,
    "categories": {}
}

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


def validate_prompt(prompt: str) -> tuple:
    """Validate input prompt. Returns (is_valid: bool, error_message: str)."""
    if not prompt or not prompt.strip():
        return False, "Prompt cannot be empty"
    if len(prompt) > 10000:
        return False, "Prompt exceeds 10,000 character limit"
    return True, ""


@app.get("/")
async def health_check():
    return {"status": "ok", "service": "sentinel-ai"}


@app.post("/analyze")
async def analyze(request: PromptRequest):
    """
    Analyze a user prompt for jailbreak / adversarial intent.

    Returns a verdict with status (ALLOWED | BLOCKED | SUSPICIOUS),
    confidence, and reasoning.
    """
    is_valid, error = validate_prompt(request.prompt)
    if not is_valid:
        return {
            "status": "ALLOWED",
            "confidence": 0.0,
            "category": "validation_error",
            "reason": error
        }
    
    result = analyze_prompt(request.prompt)

    # Update demo stats
    stats["total_analyzed"] += 1
    status = result.get("status", "ALLOWED")
    
    if status == "BLOCKED":
        stats["total_blocked"] += 1
    elif status == "SUSPICIOUS":
        stats["total_suspicious"] += 1
    else:
        stats["total_allowed"] += 1
        
    category = result.get("category", "unknown")
    stats["categories"][category] = stats["categories"].get(category, 0) + 1

    return result

@app.get("/stats")
async def get_stats():
    """Returns analytics payload for the demo dashboard."""
    return stats
