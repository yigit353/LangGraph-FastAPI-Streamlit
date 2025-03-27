import json
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

# Import the graph from the graph.py file
from graph import graph

# FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)


def sse_format(payload):
    return f"data: {json.dumps(payload)}\n\n"


@app.post("/generate")
async def generate_content(request: Request):
    data = await request.json()
    topic = data.get("topic", "cats")
    print(f"Received request for topic: {topic}")

    async def stream_generator():
        thinking_started = False

        async for msg, metadata in graph.astream(
            {"topic": topic},
            stream_mode="messages",
        ):
            node = metadata["langgraph_node"]
            if node == "generate_joke":
                if msg.content:
                    if thinking_started:
                        print("\n</thinking>\n")
                        thinking_started = False
                    print(msg.content, end="", flush=True)
                    yield sse_format(
                        {"content": msg.content, "type": "joke", "thinking": False}
                    )
                if "reasoning_content" in msg.additional_kwargs:
                    if not thinking_started:
                        print("<thinking>")
                        thinking_started = True
                    print(
                        msg.additional_kwargs["reasoning_content"], end="", flush=True
                    )
                    yield sse_format(
                        {
                            "content": msg.additional_kwargs["reasoning_content"],
                            "type": "joke",
                            "thinking": True,
                        }
                    )
            if node == "generate_poem":
                print(msg.content, end="", flush=True)
                yield sse_format(
                    {"content": msg.content, "type": "poem", "thinking": False}
                )

    return StreamingResponse(stream_generator(), media_type="text/event-stream")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
