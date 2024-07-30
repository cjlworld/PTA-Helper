from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from openai import OpenAI

from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "https://pintia.cn"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = "sk-d450ac646a11497398b5044fbf9377f8"

@app.get("/")
async def index():
    return "Hello, FastAPI!"

class ProblemDescription(BaseModel):
    description: str

@app.post("/submit")
async def submit(problem_description: ProblemDescription) -> StreamingResponse:
    description = problem_description.description
    client = OpenAI(api_key=API_KEY, base_url="https://api.deepseek.com")
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": f"请你根据以下题目生成解析 \n {description}"},
        ],
        stream=True,
    )

    def stream_response():
        for chunk in response:
            yield chunk.choices[0].delta.content or ""

    return StreamingResponse(stream_response(), media_type="text/plain")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)