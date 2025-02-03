from ollama import chat
from ollama import ChatResponse
import constants
import psutil


def is_ollama_running():
    for proc in psutil.process_iter(['name']):
        if 'ollama' in proc.info['name'].lower():
            return True
    return False


def llm_chat_text_response(messages):
    response: ChatResponse = chat(
        model=constants.TEXT_LLM_MODEL, messages=messages)
    return response['message']['content']
