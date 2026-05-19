# LabHero backend

FastAPI service that wraps MEWpy simulations for the LabHero web version.

## Quick start

```
docker compose up --build
```

Then:

- Health check: http://localhost:8000/health
- Interactive API docs: http://localhost:8000/docs
- Simulate endpoint: `POST http://localhost:8000/simulate`

Source code is bind-mounted into the container and uvicorn runs with `--reload`,
so edits under `app/` reload automatically.

## Status

Scaffold only. The `/simulate` endpoint accepts the right request shape and
returns a placeholder response. MEWpy integration is the next step — see the
TODO in `app/simulator.py`.
