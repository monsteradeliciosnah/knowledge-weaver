from __future__ import annotations

import os
import shutil
from typing import List

from fastapi import FastAPI, UploadFile
from pydantic import BaseModel

from .indexer import MultiModalIndexer

app = FastAPI(title="Knowledge Weaver API")
IDX = None


@app.on_event("startup")
async def startup():
    global IDX
    IDX = MultiModalIndexer()


@app.post("/ingest")
async def ingest(files: List[UploadFile]):
    os.makedirs("data", exist_ok=True)
    for f in files:
        dest = os.path.join("data", f.filename)
        with open(dest, "wb") as out:
            shutil.copyfileobj(f.file, out)
    IDX.build("data")
    return {"status": "ok"}


class Query(BaseModel):
    q: str
    k: int = 5


@app.post("/search")
async def search(q: Query):
    res = IDX.search(q.q, q.k)
    return {"results": res}
