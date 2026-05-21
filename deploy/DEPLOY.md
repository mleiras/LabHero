# LabHero Deployment Guide

This directory ships the game as a self-contained Docker stack: one container for the FastAPI/MEWpy backend, one for an nginx that serves the pygame-via-pygbag web bundle and reverse-proxies `/api/*` to the backend.

You do not need Python, pygbag, or any of the game's runtime dependencies on the host — only Docker. You do not need to edit any game code.

## Architecture

```
            ┌──────────────────────────────┐
 browser ──▶│  nginx (labhero-frontend)    │
            │   ├─ /        static bundle  │
            │   └─ /api/*   ──┐            │
            └─────────────────┼────────────┘
                              ▼
            ┌──────────────────────────────┐
            │  FastAPI (labhero-backend)   │
            │   POST /simulate (MEWpy)     │
            └──────────────────────────────┘
```

Both containers live on a private Docker network. Only the frontend's port 80 is exposed to the host. The backend is not reachable from outside the network.

## Prerequisites

- **Docker Engine 20.10+** and **Docker Compose v2** (`docker compose`, not `docker-compose`).
- ~2 GB free disk for the images. ~1 GB RAM at runtime (MEWpy + cobra hold ~300-500 MB resident).
- Outbound network access during build (for pip and the pygbag CDN).

To check:

```bash
docker --version
docker compose version
```

## Quick start

From the LabHero repo root:

```bash
cd deploy
docker compose build
docker compose up -d
```

First build takes 3-6 minutes (downloads ~600 MB of pip wheels for the backend, plus the pygbag bundle). Subsequent builds reuse layers and finish in under a minute.

Open http://YOUR-SERVER/ in a browser. The first page load takes 30-60 s as the browser bootstraps pyodide and installs the game's Python dependencies; this is one-time per browser (cached afterwards by the service worker).

To check the stack is healthy:

```bash
docker compose ps
curl http://localhost/api/health   # should return {"status":"ok"}
```

## Behind HTTPS

The included nginx listens on plain HTTP, port 80. For a public deployment you almost certainly want HTTPS — browsers block mixed content, and modern features like the wasm cache require a secure context.

**Recommended:** put a TLS-terminating reverse proxy in front. Common choices:

- **Cloudflare** — set the origin to your VM and Cloudflare handles certs, redirects, and edge caching. Zero config on this side.
- **Caddy** — `caddy run --config Caddyfile` with `your.domain { reverse_proxy localhost:80 }`.
- **nginx host-level** — add a second nginx in front with `proxy_pass http://127.0.0.1:80/` and certbot for Let's Encrypt.

Whatever you pick, the only requirement is that `WebSocket` is not needed (this stack uses plain HTTP request/response).

## Stopping and restarting

```bash
docker compose down          # stop + remove containers, keep images
docker compose down -v       # also remove volumes (no persistent data in this stack)
docker compose up -d         # start again
docker compose restart       # restart in place
docker compose logs -f       # tail logs
```

## Updating to a new game version

```bash
git pull
cd deploy
docker compose build --no-cache    # force rebuild so latest game code is bundled
docker compose up -d
```

After a deploy, **players will keep loading the cached bundle from their browser's service worker until it expires.** To make rollout immediate they need to clear site data (DevTools → Application → Storage → Clear site data) or open in an incognito window. The included nginx config sets `Cache-Control: no-cache` on `index.html` to nudge browsers toward checking for updates on each visit.

## Configuration

This stack runs with sensible defaults out of the box. You probably do not need to edit anything. If you do, the surfaces are:

- **`deploy/docker-compose.yml`** — service definitions, port mapping. Change `"80:80"` if you need to bind to a different host port.
- **`deploy/nginx.conf`** — proxy timeouts, MIME types, cache headers.
- **`deploy/Dockerfile.frontend`** — pinned pygbag version (0.9.3).
- **`backend/Dockerfile`** — pinned Python (3.10-slim) and the libexpat1 system dependency MEWpy/libsbml needs.

If you change `nginx.conf` you can hot-reload without rebuilding the image:

```bash
docker compose exec frontend nginx -s reload
```

## Troubleshooting

### Build fails on the pygbag step

The pygbag bundler downloads platform metadata from `pygame-web.github.io/cdn/` during the build. If the build host has no outbound HTTPS to that CDN, the build will fail. Either run the build on a host with outbound access, or build the image on a workstation and push it to a private registry the deploy server can pull from.

### Browser shows pyodide errors on first load

Open DevTools → Console. Errors that mention `XMLHttpRequest`, `simulate`, or `404` usually mean the frontend cannot reach the backend. Check:

```bash
docker compose logs backend       # should show "Application startup complete"
docker compose exec frontend wget -qO- http://backend:8000/health
```

The second command should return `{"status":"ok"}`. If it does not, the docker network is broken; `docker compose down && docker compose up -d` usually fixes it.

### Audio works but stutters when menus open

Expected on slower devices. The simulation menu builds 137 gene toggles plus ~40 reaction toggles, which on wasm takes 1-2 s. The build is broken into chunks that yield to the audio mixer between batches, but on a low-end CPU the gaps can still be audible. Not a bug.

### Quit Game does nothing

Expected on web. The game replaces "Quit Game" with "Back to Title" in the M menu when running in a browser, because browsers don't let JavaScript close their own tab.

## Known issues to revisit before going public

Three Dependabot CVEs were dismissed for the desktop game (h11 critical Chunked-Encoding, idna, Pillow) because they are not reachable in a Pygame desktop binary. They **become reachable** the moment the backend starts parsing real HTTP behind a public TLS terminator.

- **h11 < 0.13** is forced by MEWpy 0.1.36's transitive pin on `httpx==0.23.0`. The included nginx in this stack handles HTTP parsing itself before traffic reaches uvicorn, which is sufficient mitigation for the chunked-encoding bug. If you bypass nginx and expose uvicorn directly, the CVE is in play.
- **idna** is in the same dependency tree and has a low-severity CVE.
- **Pillow** is not currently in the runtime dependency closure but a future game update that adds image processing would introduce it.

If your security team needs a clean scan, the path is to upgrade MEWpy to a version that does not pin httpx 0.23.0, or to vendor the FBA call directly against cobrapy (the backend's `app/simulator.py` already does most of this — only the `mewpy.simulation.get_simulator` indirection would need replacing).

## Resource sizing for the UMinho VM

| Resource | Minimum | Comfortable |
|---|---|---|
| CPU | 1 vCPU | 2 vCPU |
| RAM | 1 GB | 2 GB |
| Disk | 4 GB | 10 GB |
| Network | outbound HTTPS during build only | same |

The runtime cost is dominated by uvicorn + cobra/MEWpy holding the `e_coli_core` model in memory. Concurrent FBA requests are CPU-bound but fast (<1 s each for the included model); a single vCPU handles a small classroom of simultaneous players comfortably.
