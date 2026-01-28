from fastapi import FastAPI
import uvicorn
from api.v1.api import router as api_router
from core.config import settings
app = FastAPI()
app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0" , port=8000, reload=True)