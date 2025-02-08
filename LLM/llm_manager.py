import Settings.constants as constants

import LLM.Ollama.Util_Ollama as Util_Ollama


def llm_response(file_paths, messages, current_msg):
    response = ''
    if constants.AI_PROVIDER == constants.PROVIDER_OLLAMA and Util_Ollama.is_ollama_running():
        if len(file_paths) > 0:
            response = Util_Ollama.query_rag(messages, current_msg)
        else:
            response = Util_Ollama.get_ollama_chat_response(messages)
    return response


def get_models():
    if constants.AI_PROVIDER == constants.PROVIDER_OLLAMA and Util_Ollama.is_ollama_running():
        return Util_Ollama.get_ollama_models()
    return []


def delete_model(model_name):
    if constants.AI_PROVIDER == constants.PROVIDER_OLLAMA and Util_Ollama.is_ollama_running():
        Util_Ollama.delete_ollama_model(model_name)


def process_rag_files(file_paths):
    if len(file_paths) > 0:
        if constants.AI_PROVIDER == constants.PROVIDER_OLLAMA and Util_Ollama.is_ollama_running():
            return Util_Ollama.process_rag(file_paths)
    return False


def clear_rag():
    if constants.AI_PROVIDER == constants.PROVIDER_OLLAMA and Util_Ollama.is_ollama_running():
        Util_Ollama.clear_memory()
