# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import ask, context, report
from utils.config import load_env

# Load environment variables
load_env()

# Initialize FastAPI app
app = FastAPI(
    title="Model Context Protocol Server",
    version="1.0.0"
)

# CORS (optional, useful for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(ask.router, prefix="/ask", tags=["Ask"])
app.include_router(context.router, prefix="/context", tags=["Context"])
app.include_router(report.router, prefix="/report", tags=["Report"])

# Lifecycle hooks
# @app.on_event("startup")
# async def startup_event():
#     await connect_db()

# @app.on_event("shutdown")
# async def shutdown_event():
#     await disconnect_db()

# Local development server (optional)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
