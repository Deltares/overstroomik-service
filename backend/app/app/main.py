from typing import Optional

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.models import Data, Response, WebService, Location

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


@app.post("/location", response_model=Response)
async def dataservice(location: Location):
    # location.resolve()
    # something with data
    return Response(location=location)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=settings.PORT)
