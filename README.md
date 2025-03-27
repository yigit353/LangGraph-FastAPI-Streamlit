# LangGraph with FastAPI and Streamlit

This repository demonstrates how to build LLM applications using LangGraph, FastAPI, and Streamlit. It focuses on streaming both token outputs and reasoning state from LangGraph through FastAPI to any frontend client, with Streamlit as the example implementation.

## Project Overview

This project provides three progressive examples:

1. **Basic AsyncIO Console Unit Graph**: A simple graph with a single node that handles both joke and poem generation.
2. **AsyncIO Console Basic Graph**: A more complex graph with separate nodes for generating jokes and poems.
3. **FastAPI + LangGraph + Streamlit**: A complete web application that streams LangGraph outputs to a Streamlit UI through FastAPI.

## Key Features

- Stream both tokens and thinking/reasoning state from LLMs
- Connect LangGraph to any frontend through FastAPI
- Demonstrate real-time UI updates with Streamlit
- Show both final content and reasoning process in the UI

## Setup Instructions

### 1. Environment Setup

1. Clone this repository:
   ```
   git clone https://github.com/yigit353/LangGraph-FastAPI-Streamlit.git
   cd LangGraph-FastAPI-Streamlit
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install required packages:
   ```
   pip install -r requirements.txt
   ```

4. Copy example.env to .env:
   ```
   cp example.env .env
   ```

5. Get a DeepSeek API key:
   - Visit [DeepSeek Platform](https://platform.deepseek.com/)
   - Create an account and generate an API key
   - Add your API key to the .env file:
     ```
     DEEPSEEK_API_KEY=your_api_key_here
     ```

### 2. Running the Examples

#### Example 1: Basic AsyncIO Console Unit Graph
```
python 01_asyncio_console_unit_graph.py
```
This example demonstrates a simple graph with a single node that handles both joke and poem generation.

#### Example 2: AsyncIO Console Basic Graph
```
python 02_asyncio_console_basic_graph.py
```
This example shows a more complex graph with separate nodes for generating jokes and poems.

#### Example 3: FastAPI + LangGraph + Streamlit

1. Start the FastAPI server:
```
cd 03_fastapi_langgraph_streamlit
python server.py
```

2. In a new terminal, start the Streamlit UI:
```
cd 03_fastapi_langgraph_streamlit
streamlit run streamlit_ui.py
```

3. Navigate to http://localhost:8501 in your browser to use the application.

4. (Optional) Test the API independently:
```
cd 03_fastapi_langgraph_streamlit
python test_client.py
```

## Why This Project is Unique and Useful

This project addresses several key challenges in building AI applications:

1. **Token Streaming**: Most LLM applications need to stream tokens to provide responsive UIs. This project demonstrates how to stream both final outputs and intermediate reasoning.

2. **Separation of Concerns**: By separating the LLM logic (LangGraph), API layer (FastAPI), and UI (Streamlit), the architecture is modular and maintainable.

3. **Frontend Agnostic**: While this example uses Streamlit, the FastAPI backend can connect to any frontend (React, Vue, etc.) through server-sent events (SSE).

4. **Reasoning Transparency**: The UI shows both the final output and the LLM's reasoning process, making the system more transparent and trustworthy.

5. **Progressive Learning Path**: The three examples progress from simple to complex, making it easier to understand each component.

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.