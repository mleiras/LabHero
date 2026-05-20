from typing import Literal
from pydantic import BaseModel, Field


class SimulateRequest(BaseModel):
    method: Literal["FBA", "pFBA", "ROOM", "lMOMA"] = "FBA"
    objective: str = Field(
        ...,
        description="Reaction id used as the objective, e.g. BIOMASS_Ecoli_core_w_GAM",
    )
    gene_knockouts: list[str] = Field(
        default_factory=list,
        description="List of gene ids to knock out before simulating.",
    )
    env_conditions: dict[str, tuple[float, float]] = Field(
        default_factory=dict,
        description="Exchange-reaction bounds: reaction_id -> (lower_bound, upper_bound).",
    )


class SimulateResponse(BaseModel):
    objective: str
    result: float | str
    status: Literal["ok", "infeasible", "error"]
    message: str | None = None
