import platform
from typing import TypedDict
from langchain_deepseek import ChatDeepSeek
from langgraph.graph import START, StateGraph
import asyncio

joke_model = ChatDeepSeek(model="deepseek-reasoner", max_tokens=1000, tags=["joke"])
poem_model = ChatDeepSeek(model="deepseek-chat", max_tokens=1000, tags=["poem"])


class State(TypedDict):
    topic: str
    joke: str
    poem: str


async def call_model(state, config):
    topic = state["topic"]
    print("Writing joke...\n")
    joke_response = await joke_model.ainvoke(
        [{"role": "user", "content": f"Write a joke about {topic}"}],
        config,
    )
    print("\n\nWriting poem...")
    poem_response = await poem_model.ainvoke(
        [{"role": "user", "content": f"Write a short poem about {topic}"}],
        config,
    )
    return {"joke": joke_response.content, "poem": poem_response.content}


graph = StateGraph(State).add_node(call_model).add_edge(START, "call_model").compile()


async def main():
    thinking_started = False

    async for msg, metadata in graph.astream(
        {"topic": "cats"},
        stream_mode="messages",
    ):
        if "joke" in metadata.get("tags", []):
            if msg.content:
                if thinking_started:
                    print("\n</thinking>\n")
                    thinking_started = False
                print(msg.content, end="", flush=True)
            if "reasoning_content" in msg.additional_kwargs:
                if not thinking_started:
                    print("<thinking>")
                    thinking_started = True
                print(msg.additional_kwargs["reasoning_content"], end="", flush=True)
        if "poem" in metadata.get("tags", []):
            print(msg.content, end="", flush=True)


if __name__ == "__main__":
    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
