from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from openai import OpenAI

app = FastAPI()

API_KEY = "sk-d450ac646a11497398b5044fbf9377f8"

@app.get("/")
async def index():
    return "Hello, FastAPI!"

@app.get("/submit")
async def submit(request: Request):
    client = OpenAI(api_key=API_KEY, base_url="https://api.deepseek.com")
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": "Hello"},
        ],
        stream=True,
    )

    async def stream_response():
        for chunk in response:
            yield chunk.choices[0].delta.content or ""

    return StreamingResponse(stream_response(), media_type="text/plain")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)