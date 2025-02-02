from ollama import chat
from ollama import ChatResponse
import constants


def llm_chat_text_response(messages):
    response: ChatResponse = chat(
        model=constants.TEXT_LLM_MODEL, messages=messages)
    return response['message']['content']
