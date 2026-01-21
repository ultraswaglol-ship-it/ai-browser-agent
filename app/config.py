import os
import sys
from dotenv import load_dotenv

load_dotenv()

def get_env_variable(name: str, default: str = None, required: bool = True) -> str:
    value = os.getenv(name, default)
    if required and not value:
        print(f" Ошибка конфигурации: Не найдена переменная окружения '{name}'")
        sys.exit(1)
    return value

OPENROUTER_API_KEY = get_env_variable("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = get_env_variable("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")

MODEL_NAME = get_env_variable("MODEL_NAME", "anthropic/claude-3.5-sonnet")

HEADLESS = get_env_variable("HEADLESS", "False").lower() == "true"
SLOW_MO = int(get_env_variable("SLOW_MO", "1000"))
VIEWPORT = {"width": 1280, "height": 800}

print(f" Конфигурация загружена. Используем модель: {MODEL_NAME}")