# main.py
from dotenv import load_dotenv

load_dotenv()

import jevlang  # noqa: F401  (installs the .jev import hook)
import triage
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Jev Ticket Router")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TicketRequest(BaseModel):
    text: str


class RouteResponse(BaseModel):
    team: str
    confidence: float
    urgency: float
    is_angry: bool
    auto_routed: bool
    reason: str | None = None


AUTO_ROUTE_THRESHOLD = 0.6


@app.get("/")
async def root():
    return {
        "service": "Jev Ticket Router",
        "docs": "/docs",
        "route_endpoint": "POST /route",
    }


@app.post("/route", response_model=RouteResponse)
async def route_ticket(request: TicketRequest):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Ticket text cannot be empty.")

    try:
        analysis = triage.analyze_ticket(request.text)

        # Choice → str subclass
        department = str(analysis.department)
        confidence = analysis.department.confidence

        # Score → float subclass
        urgency = float(analysis.urgency)

        # Noul → float subclass
        is_angry = float(analysis.is_angry) >= 0.5

        if confidence >= AUTO_ROUTE_THRESHOLD:
            team = department
            auto_routed = True
            reason = None
        else:
            team = "human"
            auto_routed = False
            reason = (
                f"Low confidence ({confidence:.2f}) on department "
                "classification. Sent to human review."
            )

        return RouteResponse(
            team=team,
            confidence=confidence,
            urgency=urgency,
            is_angry=is_angry,
            auto_routed=auto_routed,
            reason=reason,
        )

    except (ValueError, RuntimeError, KeyError) as e:
        raise HTTPException(
            status_code=500, detail=f"Decision engine error: {e!s}"
        ) from e


@app.get("/health")
async def health_check():
    return {"status": "ok"}