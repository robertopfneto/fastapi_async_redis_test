from fastapi import FastAPI

from handlers.health import router as healt_router

app = FastAPI()
app.include_router(healt_router)