import Settings.constants as constants

import LLM.Ollama.Util_Ollama as Util_Ollama


def llm_chat_text_response(messages):
    if constants.AI_PROVIDER == constants.PROVIDER_OLLAMA and Util_Ollama.is_ollama_running():
        return Util_Ollama.get_ollama_chat_response(messages)
    return ""


def get_models():
    if constants.AI_PROVIDER == constants.PROVIDER_OLLAMA and Util_Ollama.is_ollama_running():
        return Util_Ollama.get_ollama_models()
    return []


def delete_model(model_name):
    if constants.AI_PROVIDER == constants.PROVIDER_OLLAMA and Util_Ollama.is_ollama_running():
        Util_Ollama.delete_ollama_model(model_name)
    return ""
