from fastapi import FastAPI
from contextlib import asynccontextmanager
from user_service.db import create_db_and_tables
from user_service.routes.auth_route import router as auth_router
from user_service.routes.register_route import router as register_router
from user_service.routes.user_route import router as user_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating Database Tables")
    create_db_and_tables()  # Synchronously create tables before app starts
    yield  # Lifespan context, between startup and shutdown
    print("Shutdown process")


# Initialize FastAPI app with lifespan management
app = FastAPI(
    lifespan=lifespan,
    title="User Service API",
    version="0.0.1",
)

@app.get("/")
def read_root():
    return {"Hello": "User Service"}
# Include the authentication and registration routes
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(register_router, prefix="/user", tags=["user"])
app.include_router(user_router)
