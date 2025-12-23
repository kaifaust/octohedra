from fastapi import APIRouter, Query
from fastapi.responses import PlainTextResponse

from services.octoflake_service import generate_fractal

router = APIRouter()


@router.get("/generate", response_class=PlainTextResponse)
async def generate(
    iteration: int = Query(default=2, ge=1, le=5, description="Fractal iteration depth"),
    scale: int = Query(default=0, ge=0, le=3, description="Scale factor"),
    config: str = Query(default="rainbow_speed", description="Config preset name"),
):
    """Generate an Octoflake fractal and return as OBJ."""
    obj_content = generate_fractal(iteration=iteration, scale=scale, config_name=config)
    return PlainTextResponse(
        content=obj_content,
        media_type="model/obj",
        headers={"Content-Disposition": f"inline; filename=flake_{iteration}.obj"},
    )
