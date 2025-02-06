from ollama import chat
from ollama import ChatResponse
import constants
import psutil
import ollama


def get_ollama_chat_response(messages):
    response: ChatResponse = chat(
        model=constants.TEXT_LLM_MODEL, messages=messages)
    return response['message']['content']


def is_ollama_running():
    for proc in psutil.process_iter(['name']):
        if 'ollama' in proc.info['name'].lower():
            return True
    return False


def get_ollama_models():
    try:
        response = ollama.list()
        model_names = [model.model for model in response.models]
        return model_names
    except Exception as e:
        print(f"Error fetching models: {e}")
        return []


def delete_ollama_model(selected_model):
    try:
        ollama.delete(selected_model)
    except Exception as e:
        print(f"{e}")
