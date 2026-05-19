from app.schemas import SimulateRequest, SimulateResponse


def simulate(req: SimulateRequest) -> SimulateResponse:
    # Step 2 will replace this body with the real MEWpy call:
    #
    #   from cobra.io import read_sbml_model
    #   from mewpy.simulation import get_simulator
    #   simul = get_simulator(_MODEL)              # loaded once at startup
    #   simul.objective = req.objective
    #   for gene_id in req.gene_knockouts:
    #       for r in simul.find_genes().loc[gene_id].reactions:
    #           req.env_conditions[r] = (0, 0)
    #   result = simul.simulate(method=req.method, constraints=req.env_conditions)
    #
    # then parse `result` the way run_simul does today.

    return SimulateResponse(
        objective=req.objective,
        result=0.873,
        status="ok",
        message="stub response; MEWpy integration pending",
    )
