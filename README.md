# art

Fractal geometry generators and other tech-art experiments.

## Quick Start

Run the full-stack app locally (fractal generator + 3D viewer):

```bash
# Terminal 1: Start the Python backend
cd backend
poetry install
poetry run uvicorn main:app --reload --port 8000

# Terminal 2: Start the Next.js frontend
cd client
npm install
npm run dev
```

Open http://localhost:3001 to view fractals in your browser.

## Project Structure

```text
art/
├── backend/                 # Python backend (FastAPI + Octoflake)
│   ├── main.py              # FastAPI app entry point
│   ├── routers/             # API endpoints
│   ├── services/            # Business logic
│   ├── Octoflake/           # Fractal generator core
│   │   └── analysis/
│   │       └── printing/    # Shape builders, grid, utils
│   ├── 3DType/              # 3D text experiments
│   └── Script Graveyard/    # Old/archived code
│
├── client/                  # Next.js frontend
│   ├── app/                 # Next.js app router
│   ├── components/          # React components (FractalViewer)
│   ├── hooks/               # Custom hooks
│   └── lib/                 # API client
│
├── Misc Models/             # One-off 3D models
├── Misc Printer Plates/     # Ready-to-print plates
├── Nocturne X/              # Art installation hardware
├── Pixelblaze Patterns/     # LED animation code
├── SCAD/                    # OpenSCAD experiments
└── Three Sided Dice/        # Sphericon shapes
```

## Backend

### Setup

Requires Python 3.11+ and [Poetry](https://python-poetry.org/docs/#installation).

```bash
cd backend
poetry install
```

### Running the API

```bash
poetry run uvicorn main:app --reload --port 8000
```

API docs available at http://localhost:8000/docs

### Generate fractals directly

```bash
poetry run python -m printing.builders.FlakeBuilder
```

Output files are saved to `backend/Octoflake/analysis/output/`.

### Development

```bash
# Run tests
poetry run pytest

# Run tests with coverage
poetry run pytest --cov

# Lint code
poetry run ruff check .
```

## Client

### Setup

Requires Node.js 18+.

```bash
cd client
npm install
```

### Running locally

```bash
npm run dev
```

### Build for production

```bash
npm run build
```

### Deploying to Vercel

1. Connect repo to Vercel
2. Set root directory to `client/`
3. Add environment variable: `NEXT_PUBLIC_API_URL=https://your-api-server.com`

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/api/v1/generate` | GET | Generate fractal mesh |

### Generate Fractal

```
GET /api/v1/generate?iteration=2&scale=0&config=rainbow_speed
```

Parameters:
- `iteration` (1-5): Fractal depth
- `scale` (0-3): Scale factor
- `config`: Preset name (`rainbow_speed`, `rainbow_gem`, `quantum_gem`, `quantum_speed`, `debug`)

Returns: OBJ mesh as text
