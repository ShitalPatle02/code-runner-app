from fastapi import FastAPI
from pydantic import BaseModel
from executor import run_code
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

app = FastAPI()

# CORS settings for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict to your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/", StaticFiles(directory="../frontend/build", html=True), name="static")

@app.get("/")
def read_index():
    return FileResponse("../frontend/build/index.html")

class CodeRequest(BaseModel):
    code: str
    input: str

@app.post("/execute")
async def execute_code(req: CodeRequest):
    output = run_code(req.code, req.input)
    # Just return output, frontend formats it with separator
    return {"output": output.strip()}