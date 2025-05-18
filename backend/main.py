from fastapi import FastAPI
from pydantic import BaseModel
from .executor import run_code
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS settings for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict to your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CodeRequest(BaseModel):
    code: str
    input: str
@app.get("/")
async def root():
    # This handles GET requests to /
    return {"message": "Code runner backend is live"}
@app.post("/execute")
async def execute_code(req: CodeRequest):
    output = run_code(req.code, req.input)
    # Just return output, frontend formats it with separator
    return {"output": output.strip()}