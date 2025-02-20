import re
import os

BAD_WORDS_FILE = "data/bad_words.txt"

def load_bad_words():
    """Загружает список запрещённых слов из файла."""
    if not os.path.exists(BAD_WORDS_FILE):
        return set()  # Если файла нет, просто возвращаем пустой список

    with open(BAD_WORDS_FILE, "r", encoding="utf-8") as f:
        words = [line.strip().lower() for line in f.readlines()]
    return set(words)  # Используем set() для быстрого поиска

BAD_WORDS = load_bad_words()  # Загружаем при старте

def is_safe_response(response: str) -> bool:
    """Проверяет, содержит ли ответ запрещённые слова."""
    lower_response = response.lower()
    for word in BAD_WORDS:
        if re.search(rf"\b{word}\b", lower_response):  # Ищем слово как отдельное слово
            print(f"[ФИЛЬТР] Обнаружено запрещённое слово: {word}")
            return False
    return True
