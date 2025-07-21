from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database import init_database
from routes import levels, lessons, exercises, users

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database on startup
    await init_database()
    yield

app = FastAPI(
    title="Nahw Exercises API", 
    description="API for Arabic Grammar Learning",
    lifespan=lifespan
)

# Enable CORS for React Native
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(levels.router)
app.include_router(lessons.router)
app.include_router(exercises.router)
app.include_router(users.router)

@app.get("/")
async def read_root():
    return {"message": "Welcome to Nahw Exercises API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
