from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.presentation.api.v1.routes import router as api_v1_router
from src.infrastructure.config.settings import settings
from src.domain.utils.class_object import singleton
from src.infrastructure.database.db import Base, engine

# Create the database tables
Base.metadata.create_all(bind=engine)

@singleton
class AppCreator:
    def __init__(self):
        self.app = FastAPI(
            title=settings.PROJECT_NAME,
            version="1.0.0",
        )
        self.setup_cors()
        self.setup_routes()

    def setup_cors(self):
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # Restrict in production
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def setup_routes(self):
        self.app.include_router(api_v1_router, prefix=settings.ROUTE_PREFIX)

    def get_app(self):
        return self.app
    
app_creator = AppCreator()
app = app_creator.get_app()

@app.get("/")
def read_root():
    return {"message": "Welcome to the API"}