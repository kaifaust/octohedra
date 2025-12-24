# Octohedra

A fractal geometry generator that creates beautiful octahedral fractal structures for 3D printing and visualization.

**Live Demo:** [octohedra.com](https://octohedra.com)

## Features

- Interactive 3D viewer with auto-rotation
- Multiple preset fractal shapes (flake, tower, evil tower, flower)
- Custom recipe builder for creating unique fractals
- STL export for 3D printing with multiple quality presets
- Real-time fractal generation

## Quick Start

Run the full-stack app locally:

```bash
# Terminal 1: Start the Python backend
cd backend
poetry install
poetry run uvicorn main:app --reload --port 8001

# Terminal 2: Start the Next.js frontend
cd client
npm install
npm run dev
```

Open <http://localhost:3001> to view fractals in your browser.

## Project Structure

```text
octohedra/
├── backend/              # Python backend (FastAPI)
│   ├── main.py           # FastAPI app entry point
│   ├── routers/          # API endpoints
│   ├── services/         # Business logic
│   └── octohedra/        # Fractal generator core
│       ├── builders/     # Shape builders (RecipeBuilder, etc.)
│       ├── grid/         # Grid system for octahedral cells
│       ├── utils/        # Config and utilities
│       └── tests/        # Unit tests
│
└── client/               # Next.js frontend
    ├── app/              # Next.js app router
    ├── components/       # React components
    ├── hooks/            # Custom hooks
    └── lib/              # API client
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
poetry run uvicorn main:app --reload --port 8001
```

API docs available at http://localhost:8001/docs

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

## API Endpoints

| Endpoint                  | Method | Description                  |
| ------------------------- | ------ | ---------------------------- |
| `/health`                 | GET    | Health check                 |
| `/api/v1/generate`        | POST   | Generate fractal mesh (OBJ)  |
| `/api/v1/generate/stl`    | POST   | Generate fractal mesh (STL)  |
| `/api/v1/presets`         | GET    | List available presets       |
| `/api/v1/presets/{name}`  | GET    | Get preset recipe            |

### Generate Fractal

```bash
curl -X POST http://localhost:8001/api/v1/generate \
  -H "Content-Type: application/json" \
  -d '{"layers": [{"depth": 3}]}'
```

## License

MIT
