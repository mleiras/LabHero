from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.schemas import SimulateRequest, SimulateResponse
from app.simulator import simulate

app = FastAPI(title="LabHero Backend", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/simulate", response_model=SimulateResponse)
def post_simulate(req: SimulateRequest) -> SimulateResponse:
    return simulate(req)
