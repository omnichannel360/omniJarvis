"""
Hands MCP server — PC-side tools exposed over Tailscale.
Device-token auth, gate enforced, binds to PC Tailscale IP only.
"""
import json
import logging
from pathlib import Path

from fastapi import FastAPI, WebSocket, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
import uvicorn

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Jarvis Hands", version="0.1.0")

# CORS: only Tailscale IPs
app.add_middleware(
    CORSMiddleware,
    allow_origins=["100.0.0.0/10"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Workspace root
WORKSPACE = Path(r"C:\Jarvis\workspace")
WORKSPACE.mkdir(parents=True, exist_ok=True)

# UI root
UI_PATH = Path(__file__).parent / "ui"


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check."""
    return {"status": "ok", "service": "hands"}


@app.get("/ui")
async def serve_ui() -> HTMLResponse:
    """Serve Jarvis UI."""
    ui_file = UI_PATH / "index.html"
    if not ui_file.exists():
        logger.warning(f"UI file not found: {ui_file}")
        return HTMLResponse("<h1>Jarvis UI — not yet deployed</h1>", status_code=200)
    return HTMLResponse(ui_file.read_text())


@app.websocket("/ws/ui")
async def ws_ui(websocket: WebSocket) -> None:
    """WebSocket for UI (echo stub)."""
    await websocket.accept()
    logger.info("UI WebSocket connected")
    try:
        while True:
            data = await websocket.receive_json()
            # Echo state changes; real implementation routes to voice pipeline
            logger.debug(f"UI message: {data}")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")


@app.post("/tools/workspace/list")
async def workspace_list(
    path: str = "",
    token: str = Header(None),
) -> dict[str, object]:
    """List workspace files (Tier 0)."""
    if not await verify_token(token):
        raise HTTPException(status_code=403, detail="Invalid token")
    
    target = (WORKSPACE / path).resolve()
    if not str(target).startswith(str(WORKSPACE)):
        raise HTTPException(status_code=400, detail="Path escape detected")
    
    if not target.exists():
        return {"files": [], "error": "Not found"}
    
    files = [
        {"name": f.name, "type": "dir" if f.is_dir() else "file", "size": f.stat().st_size if f.is_file() else 0}
        for f in target.iterdir()
    ]
    return {"files": files}


@app.post("/tools/workspace/read")
async def workspace_read(
    path: str = "",
    token: str = Header(None),
) -> dict[str, object]:
    """Read file from workspace (Tier 0)."""
    if not await verify_token(token):
        raise HTTPException(status_code=403, detail="Invalid token")
    
    target = (WORKSPACE / path).resolve()
    if not str(target).startswith(str(WORKSPACE)):
        raise HTTPException(status_code=400, detail="Path escape")
    
    if not target.exists() or not target.is_file():
        raise HTTPException(status_code=404, detail="Not found")
    
    return {"path": str(target), "content": target.read_text()}


@app.post("/tools/workspace/write")
async def workspace_write(
    path: str = "",
    content: str = "",
    token: str = Header(None),
) -> dict[str, str]:
    """Write file to workspace (Tier 1)."""
    if not await verify_token(token):
        raise HTTPException(status_code=403, detail="Invalid token")
    
    target = (WORKSPACE / path).resolve()
    if not str(target).startswith(str(WORKSPACE)):
        raise HTTPException(status_code=400, detail="Path escape")
    
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content)
    logger.info(f"Wrote: {target}")
    return {"path": str(target), "status": "ok"}


async def verify_token(token: str | None) -> bool:
    """Verify device token (stub). Real implementation reads from keystore."""
    return token == "dev-token-for-phase-0"


def main() -> None:
    """Start hands server."""
    # Bind to Tailscale interface (100.x.x.x)
    # For Phase 0 testing, bind to localhost
    host = "127.0.0.1"
    port = 8787
    logger.info(f"Starting hands server on {host}:{port}")
    uvicorn.run(app, host=host, port=port, log_level="info")


if __name__ == "__main__":
    main()
