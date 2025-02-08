from ollama import chat
from ollama import ChatResponse
import Settings.constants as constants
import psutil
import ollama
from . import RAG_Ollama

# CHAT


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
        return

# RAG


def query_rag(messages, current_msg):
    return RAG_Ollama.rag_generate_answer(messages, current_msg)


def process_rag(file_paths):
    return RAG_Ollama.rag_process_document(file_paths)


def clear_memory():
    RAG_Ollama.clear_memory()
