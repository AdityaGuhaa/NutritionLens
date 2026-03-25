from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.analyze import router as analyze_router

# Create FastAPI app
app = FastAPI(
    title="NutriLens API",
    description="AI-powered food label analyzer",
    version="1.0.0"
)

# Enable CORS (important for frontend later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change later for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(analyze_router, prefix="/api")

# Health check route
@app.get("/")
def root():
    return {"message": "NutriLens API is running 🚀"}