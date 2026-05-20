from pathlib import Path

from cobra.io import read_sbml_model
from mewpy.simulation import get_simulator

from app.schemas import SimulateRequest, SimulateResponse

_MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "e_coli_core.xml.gz"
_model = read_sbml_model(str(_MODEL_PATH))
_simul = get_simulator(_model)
_genes = _simul.find_genes()


def simulate(req: SimulateRequest) -> SimulateResponse:
    try:
        _simul.objective = req.objective

        constraints = {k: tuple(v) for k, v in req.env_conditions.items()}

        for gene_id in req.gene_knockouts:
            if gene_id not in _genes.index:
                continue
            for reaction_id in _genes.loc[gene_id, "reactions"]:
                constraints[reaction_id] = (0, 0)

        result = _simul.simulate(method=req.method, constraints=constraints)

        text = str(result)
        lines = text.splitlines()
        if len(lines) > 1 and lines[1].strip() == "Status: INFEASIBLE":
            return SimulateResponse(
                objective=req.objective,
                result="Status: INFEASIBLE",
                status="infeasible",
            )
        value = round(float(lines[0][11:]), 3)
        return SimulateResponse(
            objective=req.objective,
            result=value,
            status="ok",
        )

    except Exception as e:
        return SimulateResponse(
            objective=req.objective,
            result=str(e),
            status="error",
            message=str(e),
        )
