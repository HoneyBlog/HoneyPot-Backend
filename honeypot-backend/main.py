from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config.database import create_tables, test_connection

from routers.router import router  # Ensure correct import

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
