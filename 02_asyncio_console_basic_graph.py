import platform
from typing import TypedDict
from langchain_deepseek import ChatDeepSeek
from langgraph.graph import StateGraph
import asyncio

joke_model = ChatDeepSeek(model="deepseek-reasoner", max_tokens=1000)
poem_model = ChatDeepSeek(model="deepseek-chat", max_tokens=1000)


class State(TypedDict):
    topic: str
    joke: str
    poem: str


async def generate_joke(state, config):
    topic = state["topic"]
    print("Writing joke...\n")
    joke_response = await joke_model.ainvoke(
        [{"role": "user", "content": f"Write a joke about {topic}"}],
        config,
    )
    print()
    return {"joke": joke_response.content}


async def generate_poem(state, config):
    topic = state["topic"]
    print("\nWriting poem...\n")
    poem_response = await poem_model.ainvoke(
        [{"role": "user", "content": f"Write a short poem about {topic}"}],
        config,
    )
    print()
    return {"poem": poem_response.content}


def create_graph():
    workflow = StateGraph(State)

    # Add nodes
    workflow.add_node("generate_joke", generate_joke)
    workflow.add_node("generate_poem", generate_poem)

    # Set the entry point
    workflow.set_entry_point("generate_joke")

    # Add edges
    workflow.add_edge("generate_joke", "generate_poem")

    # Set the final node
    workflow.set_finish_point("generate_poem")

    return workflow.compile()


graph = create_graph()


async def main():
    thinking_started = False

    async for msg, metadata in graph.astream(
        {"topic": "cats"},
        stream_mode="messages",
    ):
        node = metadata["langgraph_node"]
        if node == "generate_joke":
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
        if node == "generate_poem":
            print(msg.content, end="", flush=True)


if __name__ == "__main__":
    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
