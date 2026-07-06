import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS configuration (optional, but good for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

@app.get('/api/test')
def test_backend():
    """A simple endpoint to check if the backend is running."""
    return {"message": "Backend is running!"}

@app.get('/api/test/{message}')
def echo_message(message: str):
    """An endpoint that echoes back a message."""
    return {"echo": message}

# Serve the frontend build
frontend_build_path = "frontend/build"
if os.path.isdir(frontend_build_path):
    app.mount("/static", StaticFiles(directory=os.path.join(frontend_build_path, "static")))

    @app.get('/{{*path}}')
    def serve_frontend(path: str = ''):
        """Serve the frontend index.html for any non-API route."""
        return FileResponse(os.path.join(frontend_build_path, "index.html"))
else:
    print(f"Warning: Frontend build directory '{frontend_build_path}' not found. Frontend will not be served.")

# If frontend is not built, we still need to return index.html for any request
# that isn't an API route. This is a fallback for when the frontend build doesn't exist.
# However, the StaticFiles mount above is preferred when it exists.
from fastapi.responses import FileResponse

@app.get('/{{*path}}')
def catch_all_api_or_frontend(path: str = ''):
    """Catch-all route for non-API paths. Tries to serve index.html if frontend exists."""
    if os.path.isdir(frontend_build_path):
        return FileResponse(os.path.join(frontend_build_path, "index.html"))
    else:
        return {"message": "Frontend build not found. Visit /api/ routes."}

