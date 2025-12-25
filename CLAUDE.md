# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with this repository.

## Project Overview

Octohedra is a fractal geometry generator that creates octahedral fractal structures for 3D printing and visualization. It consists of a Python backend (FastAPI) and a Next.js frontend with Three.js for 3D rendering.

**Live site:** https://octohedra.com

## Architecture

```
octohedra/
├── backend/           # Python FastAPI backend
│   ├── main.py        # FastAPI app entry point
│   ├── routers/       # API endpoints
│   ├── services/      # Business logic
│   └── octohedra/     # Fractal generator core library
│       ├── builders/  # Shape builders (RecipeBuilder, etc.)
│       ├── grid/      # Grid system for octahedral cells
│       └── tests/     # Unit tests
│
└── client/            # Next.js frontend
    ├── app/           # Next.js app router
    ├── components/    # React components (uses Radix UI + Tailwind)
    ├── hooks/         # Custom React hooks
    └── lib/           # API client and utilities
```

## Development Commands

### Backend (Python)

```bash
cd backend

# Install dependencies
poetry install

# Run development server
poetry run uvicorn main:app --reload --port 8001

# Run tests
poetry run pytest

# Run tests with coverage
poetry run pytest --cov

# Lint code
poetry run ruff check .

# Fix lint issues
poetry run ruff check . --fix
```

### Frontend (Next.js)

```bash
cd client

# Install dependencies
npm install

# Run development server (port 3001)
npm run dev

# Build for production
npm run build

# Run linter
npm run lint
```

## API Endpoints

| Endpoint                 | Method | Description                |
|--------------------------|--------|----------------------------|
| `/health`                | GET    | Health check               |
| `/api/v1/generate`       | POST   | Generate fractal mesh (OBJ)|
| `/api/v1/generate/stl`   | POST   | Generate fractal mesh (STL)|
| `/api/v1/presets`        | GET    | List available presets     |
| `/api/v1/presets/{name}` | GET    | Get preset recipe          |

## Key Technologies

- **Backend:** Python 3.11+, FastAPI, NumPy, Trimesh, numpy-stl
- **Frontend:** Next.js 16, React 19, React Three Fiber, Radix UI, Tailwind CSS
- **3D:** Three.js via @react-three/fiber and @react-three/drei

## Code Style

- **Python:** Ruff for linting (pycodestyle, pyflakes, isort, pyupgrade), line length 100
- **TypeScript:** ESLint with Next.js config
