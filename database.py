import json

def get_book_recommendation(language, level, book_type, genre=None):
    # Читаем локальную базу данных
    try:
        with open("books_database.json", "r", encoding="utf-8") as f:
            books = json.load(f)
    except FileNotFoundError:
        print("Файл books_database.json не найден")
        return []
    except json.JSONDecodeError as e:
        print(f"Ошибка при чтении JSON: {e}")
        return []

    # Фильтруем книги по параметрам
    language_codes = {
        "английский": "en",
        "французский": "fr"
    }
    lang_code = language_codes.get(language.lower(), "en")
    
    # Разбиваем уровень на диапазон (например, "a1-a2" -> ["a1", "a2"])
    level_range = level.lower().split("-")
    
    filtered_books = [
        {
            "volumeInfo": {
                "title": book["title"],
                "authors": [book["author"]],
                "description": book.get("description", ""),
                "language": book["language"],
                "publishedDate": book.get("published_date", "Не указана"),
                "pageCount": book.get("page_count", "Не указано"),
                "infoLink": book.get("link", "")
            }
        }
        for book in books
        if (book["language"] == lang_code) and
           (book["level"].lower() in level_range) and
           (book["type"] == book_type) and
           (not genre or book.get("genre", "").lower() == genre.lower())
    ]
    
    print(f"Найдено книг: {len(filtered_books)}")
    return filtered_books