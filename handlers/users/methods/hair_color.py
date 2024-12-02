def get_hair_code(text: str, language: str = 'ukr') -> int:
    HAIR_CODES = {
        "ukr": {
            1: "Блонд (світле волосся)",
            2: "Русявий (світло-коричневе волосся)",
            3: "Каштановий (середньо-коричневе волосся)",
            4: "Темно-каштановий (темно-коричневе волосся)",
            5: "Чорний (дуже темне волосся)",
            6: "Рудий (рудий або мідний відтінок)",
            7: "Інший колір волосся, якого немає в списку"
        },
        "eng": {
            1: "Blond (light hair)",
            2: "Light brown (light brown hair)",
            3: "Chestnut (medium brown hair)",
            4: "Dark chestnut (dark brown hair)",
            5: "Black (very dark hair)",
            6: "Red (red or copper tint)",
            7: "Other hair color not listed"
        }
    }

    # Перевірка чи підтримується мова
    if language not in HAIR_CODES:
        raise ValueError(f"Unsupported language: {language}")

    # Пошук відповідного коду волосся
    for code, description in HAIR_CODES[language].items():
        if text.lower() in description.lower():
            return code

    # Якщо відповідний код не знайдено
    return -1

def get_hair_description(code: int, language: str = 'ukr') -> str:
    HAIR_CODES = {
        "ukr": {
            1: "Блонд (світле волосся)",
            2: "Русявий (світло-коричневе волосся)",
            3: "Каштановий (середньо-коричневе волосся)",
            4: "Темно-каштановий (темно-коричневе волосся)",
            5: "Чорний (дуже темне волосся)",
            6: "Рудий (рудий або мідний відтінок)",
            7: "Інший колір волосся, якого немає в списку"
        },
        "eng": {
            1: "Blond (light hair)",
            2: "Light brown (light brown hair)",
            3: "Chestnut (medium brown hair)",
            4: "Dark chestnut (dark brown hair)",
            5: "Black (very dark hair)",
            6: "Red (red or copper tint)",
            7: "Other hair color not listed"
        }
    }

    # Перевірка чи підтримується мова
    if language not in HAIR_CODES:
        raise ValueError(f"Unsupported language: {language}")

    # Отримання опису волосся за кодом
    return HAIR_CODES[language].get(code, "Код не знайдено")