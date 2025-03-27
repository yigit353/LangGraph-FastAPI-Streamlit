import requests
import json
import sseclient


def test_generate():
    """Test the generate endpoint with SSE streaming."""
    url = "http://localhost:8000/generate"
    headers = {"Content-Type": "application/json"}
    data = {"topic": "dogs"}

    print(f"Sending request to {url} with data: {data}")

    # Use a stream request to get SSE events
    response = requests.post(url, json=data, headers=headers, stream=True)

    # Create SSE client
    client = sseclient.SSEClient(response)
    
    # Process events
    for event in client.events():
        data = json.loads(event.data)
        print("-" * 50)
        print(f"Type: {data.get('type', 'N/A')}")
        print(f"Content: {data.get('content', 'N/A')}")
        print(f"Thinking: {data.get('thinking', 'N/A')}")

if __name__ == "__main__":
    test_generate()
