# AutoStream AI Agent

A LangGraph-based conversational agent built with Python, using Google Gemini 1.5 Flash for intelligent sales and lead capture.

## Setup Instructions

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Agent**:
   ```bash
   python agent.py
   ```

## Architecture

The system utilizes LangGraph's `create_react_agent` to manage an iterative reasoning loop (Reasoning + Acting). By defining tools seperti `retrieve_autostream_info` and `mock_lead_capture`, the LLM can dynamically decide when to fetch external data or trigger a business logic event based on user intent. 

The inclusion of `MemorySaver` provides a persistent `Checkpointer` that allows the agent to maintain conversational state across multiple turns. This is critical for the lead capture flow, where the agent must remember previously collected details (like Name or Email) while asking for the remaining information (Platform). The `thread_id` mechanism ensures that separate user sessions are isolated while retaining their respective histories, enabling a coherent and deterministic multi-turn dialogue.

## WhatsApp Deployment

To deploy this agent to WhatsApp, you would implement a FastAPI (or Flask) webhook to receive incoming Meta API events. The core mapping involves using the sender's `phone_number` as the LangGraph `thread_id`. When a message arrives:
1. The webhook extracts the message text and sender's phone number.
2. It invokes the LangGraph `app.invoke()` or `app.stream()` method, passing the `phone_number` in the configuration's `thread_id`.
3. The resulting assistant response is captured and routed back to the Meta Cloud API via a POST request to the `/messages` endpoint.
4. Memory is automatically persisted by LangGraph between requests, ensuring the "stateful" nature of the conversation is preserved even in an asynchronous messaging environment.
