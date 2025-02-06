import json

PROVIDER_OLLAMA = "OLLAMA"

DEFAULT_PROVIDER_OLLAMA = "OLLAMA"


def load_constants():
    try:
        with open('settings.json', 'r') as f:
            settings = json.load(f)
            constants = {
                'TEXT_LLM_MODEL': settings.get('TEXT_LLM_MODEL', "llama3.2:latest"),
                'TEXT_LLM_GENERAL_PROMPT': settings.get('TEXT_LLM_GENERAL_PROMPT', "Please explain me on"),
                'AI_PROVIDER': settings.get('AI_PROVIDER', DEFAULT_PROVIDER_OLLAMA),
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

TEXT_LLM_MODEL = constants['TEXT_LLM_MODEL']
TEXT_LLM_GENERAL_PROMPT = constants['TEXT_LLM_GENERAL_PROMPT']

FONT_SIZE = constants['FONT_SIZE']
BUTTON_SIZE = constants['BUTTON_SIZE']
WINDOW_HEIGHT = constants['WINDOW_HEIGHT']
WINDOW_WIDTH = constants['WINDOW_WIDTH']
