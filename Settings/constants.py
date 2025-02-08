import json

PROVIDER_OLLAMA = "OLLAMA"
PROVIDER_VLLM = "VLLM"

DEFAULT_LLM_PROVIDER = PROVIDER_OLLAMA
DEFAULT_EMBED_PROVIDER = PROVIDER_OLLAMA

DEFAULT_LLM_MODEL = "llama3.2:latest"
DEFAULT_EMBED_MODEL = "nomic-embed-text:latest"

# RAG Prompt template
PROMPT_TEMPLATE = """
You are an expert research assistant. Use the provided context to answer the query. 
If unsure, state that you don't know. Be concise and factual.

Query: {user_query} 
Context: {document_context} 
Answer:
"""


def load_constants():
    try:
        with open('settings.json', 'r') as f:
            settings = json.load(f)
            constants = {
                'AI_PROVIDER': settings.get('AI_PROVIDER', DEFAULT_LLM_PROVIDER),
                'EMBED_PROVIDER': settings.get('EMBED_PROVIDER', DEFAULT_EMBED_PROVIDER),
                'TEXT_LLM_MODEL': settings.get('TEXT_LLM_MODEL', DEFAULT_LLM_MODEL),
                'EMBED_LLM_MODEL': settings.get('EMBED_LLM_MODEL', DEFAULT_EMBED_MODEL),
                'TEXT_LLM_GENERAL_PROMPT': settings.get('TEXT_LLM_GENERAL_PROMPT', "Please explain me on"),
                'FONT_SIZE': settings.get('FONT_SIZE', 22),
                'BUTTON_SIZE': settings.get('BUTTON_SIZE', 50),
                'WINDOW_HEIGHT': settings.get('WINDOW_HEIGHT', 500),
                'WINDOW_WIDTH': settings.get('WINDOW_WIDTH', 800),
            }
            return constants
    except FileNotFoundError:
        raise Exception("Settings file not found")


constants = load_constants()


AI_PROVIDER = constants['AI_PROVIDER']
EMBED_PROVIDER = constants['EMBED_PROVIDER']

TEXT_LLM_MODEL = constants['TEXT_LLM_MODEL']
EMBED_LLM_MODEL = constants['EMBED_LLM_MODEL']

TEXT_LLM_GENERAL_PROMPT = constants['TEXT_LLM_GENERAL_PROMPT']

FONT_SIZE = constants['FONT_SIZE']
BUTTON_SIZE = constants['BUTTON_SIZE']
WINDOW_HEIGHT = constants['WINDOW_HEIGHT']
WINDOW_WIDTH = constants['WINDOW_WIDTH']
