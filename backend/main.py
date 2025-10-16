from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.authentication import router as authentication_router
from backend.dashboard import router as dashboard_router
from backend.movies import router as movies_router


app = FastAPI()
app.include_router(authentication_router.router)
app.include_router(dashboard_router.router)
app.include_router(movies_router.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Your Next.js frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
async def read_root():
    return { "message": "Backed is up"}