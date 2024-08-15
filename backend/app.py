from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from openai import OpenAI
import dashscope
from http import HTTPStatus

from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "https://pintia.cn",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DEEPSEEK_API_KEY = "sk-d450ac646a11497398b5044fbf9377f8"
QWEN_API_KEY = "sk-609f4051ace14214ad7101fc0face7d1"
USE_MODEL = "QWEN"


class ProblemDescription(BaseModel):
    description: str


@app.post("/submit")
async def submit(problem_description: ProblemDescription) -> StreamingResponse:
    description = problem_description.description
    prompt = f"请你根据以下题目生成解析 \n {description}"
    
    if USE_MODEL == "DEEPSEEK":
        client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "You are a helpful assistant"},
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            stream=True,
        )

        def stream_response():
            for chunk in response:
                yield chunk.choices[0].delta.content or ""

        return StreamingResponse(stream_response(), media_type="text/plain")

    elif USE_MODEL == "QWEN":
        messages = [{"role": "user", "content": prompt}]
        responses = dashscope.Generation.call(
            "qwen-max",
            api_key=QWEN_API_KEY,
            messages=messages,
            result_format="message",  # set the result to be "message"  format.
            stream=True,  # set streaming output
            incremental_output=True,  # get streaming output incrementally
        )
        def stream_response():
            for response in responses:
                if response.status_code == HTTPStatus.OK:
                    yield response.output.choices[0]["message"]["content"]
                else:
                    yield (
                        "Request id: %s, Status code: %s, error code: %s, error message: %s"
                        % (
                            response.request_id,
                            response.status_code,
                            response.code,
                            response.message,
                        )
                    )
        return StreamingResponse(stream_response(), media_type="text/plain")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
