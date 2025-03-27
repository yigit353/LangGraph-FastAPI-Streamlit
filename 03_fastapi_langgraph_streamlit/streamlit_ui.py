import streamlit as st
import requests
import json
import sseclient
import time

thinking_template = """
<div style="background-color: #e6f2ff; padding: 10px; border-radius: 5px; font-style: italic; color: #333; border-left: 4px solid #4b9afa;">
    {thinking_content}
</div>
"""


# Define a spinner class that can be controlled programmatically
class ControlledSpinner:
    def __init__(self, text="In progress..."):
        self.text = text
        self._spinner = None

    def _start(self):
        with st.spinner(self.text):
            yield

    def start(self):
        self._spinner = iter(self._start())
        next(self._spinner)  # Start the spinner

    def stop(self):
        if self._spinner:
            next(self._spinner, None)  # Stop the spinner


# Set page config
st.set_page_config(page_title="LangGraph Chat", page_icon="💬", layout="wide")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Main chat interface
st.title("Chat with LangGraph")

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type your message here..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response
    with st.chat_message("assistant"):
        # Joke section
        joke_thinking_container = st.empty()
        thinking_expander_container = st.empty()
        joke_container = st.empty()

        # Divider
        divider = st.empty()

        # Poem section
        poem_container = st.empty()

        # Variables to store thinking content
        thinking_content = ""
        thinking_started = False
        thinking_completed = False
        joke_completed = False
        think_time_start = 0

        joke_content = "### Joke\n"
        poem_content = "### Poem\n"

        # Initialize spinners
        joke_spinner = ControlledSpinner("Thinking about creating a joke...")
        poem_spinner = ControlledSpinner("Creating a poem...")

        # Connect to the FastAPI server
        url = "http://localhost:8000/generate"
        headers = {"Content-Type": "application/json"}
        data = {"topic": prompt}  # Use the user message as the topic

        try:
            # Use a stream request to get SSE events
            response = requests.post(url, json=data, headers=headers, stream=True)

            # Create SSE client
            client = sseclient.SSEClient(response)

            # Process events
            for event in client.events():
                data = json.loads(event.data)
                message_type = data.get("type", "N/A")
                content = data.get("content", "")
                is_thinking = data.get("thinking", False)

                if message_type == "joke":
                    if is_thinking:
                        if not thinking_started:
                            thinking_started = True
                            joke_spinner.start()  # Start spinner
                            think_time_start = time.time()
                        # Accumulate thinking content
                        thinking_content += content
                        joke_thinking_container.markdown(
                            thinking_template.format(thinking_content=thinking_content),
                            unsafe_allow_html=True,
                        )

                    else:
                        if not thinking_completed:
                            thinking_completed = True
                            # Stop the thinking spinner
                            joke_spinner.stop()

                            joke_thinking_container.empty()
                            thinking_time = time.time() - think_time_start
                            # Show thinking in an accordion
                            with thinking_expander_container.expander(
                                "It took {:.2f} seconds to think. See the thinking process.".format(
                                    thinking_time
                                )
                            ):
                                st.text(thinking_content)

                            # Start joke creation spinner
                            joke_spinner = ControlledSpinner("Creating a joke...")
                            joke_spinner.start()
                            joke_container.markdown(joke_content)

                        joke_content += content
                        joke_container.markdown(joke_content)

                elif message_type == "poem":
                    if not joke_completed:
                        joke_completed = True
                        # Stop joke spinner
                        joke_spinner.stop()

                        # Add divider
                        divider.markdown("---")

                        # Start poem spinner
                        poem_spinner.start()
                        poem_container.markdown(poem_content)

                    poem_content += content
                    poem_container.markdown(poem_content)

            # Stop any remaining spinners
            joke_spinner.stop()
            poem_spinner.stop()

            # Save the complete response to chat history
            full_response = joke_content + "\n\n---\n\n" + poem_content
            st.session_state.messages.append(
                {"role": "assistant", "content": full_response}
            )

        except Exception as e:
            st.error(f"Error connecting to server: {str(e)}")
