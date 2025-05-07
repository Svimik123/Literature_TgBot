from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_main_keyboard(context):
    language = context.user_data.get('language', '-')
    level = context.user_data.get('level', '-')
    book_type = context.user_data.get('book_type', '-')
    genre = context.user_data.get('genre', '-')
    keyboard = [
        [InlineKeyboardButton("Выбрать язык 📖", callback_data='select_language')],
        [InlineKeyboardButton("Выбери уровень 🎓", callback_data='select_level')],
        [InlineKeyboardButton("Выбрать тип 📚", callback_data='select_type')],
        [],
        [InlineKeyboardButton("Рекомендовать книгу ✅", callback_data='recommend'),
         InlineKeyboardButton("Сброс 🔄", callback_data='reset')],
        [InlineKeyboardButton("Помощь ❓", callback_data='help'),
         InlineKeyboardButton("О проекте ℹ️", callback_data='about')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_language_keyboard():
    keyboard = [
        [InlineKeyboardButton("Английский 🇬🇧", callback_data='language_английский')],
        [InlineKeyboardButton("Французский 🇫🇷", callback_data='language_французский')],
        [InlineKeyboardButton("Назад ⬅️", callback_data='back')],
    ]
    return InlineKeyboardMarkup(keyboard)

def get_level_keyboard():
    keyboard = [
        [InlineKeyboardButton("A1-A2", callback_data='level_a1-a2')],
        [InlineKeyboardButton("B1-B2", callback_data='level_b1-b2')],
        [InlineKeyboardButton("C1-C2", callback_data='level_c1-c2')],
        [InlineKeyboardButton("Назад ⬅️", callback_data='back')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_type_keyboard():
    keyboard = [
        [InlineKeyboardButton("Учебная 📖", callback_data='type_учебная')],
        [InlineKeyboardButton("Художественная 📕", callback_data='type_художественная')],
        [InlineKeyboardButton("Назад ⬅️", callback_data='back')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_genre_keyboard():
    keyboard = [
        [InlineKeyboardButton("Роман 📖", callback_data='genre_роман')],
        [InlineKeyboardButton("Фантастика 🚀", callback_data='genre_фантастика')],
        [InlineKeyboardButton("Детектив 🔍", callback_data='genre_детектив')],
        [InlineKeyboardButton("Приключения 🗺️", callback_data='genre_приключения')],
        [InlineKeyboardButton("Драма 🎭", callback_data='genre_драма')],
        [InlineKeyboardButton("Классика 📜", callback_data='genre_классика')],
        [InlineKeyboardButton("Пропустить ⏭️", callback_data='skip_genre')]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_recommendation_keyboard(context):
    books = context.user_data.get('books', [])
    index = context.user_data.get('book_index', 0)
    max_index = len(books) - 1 if books else 0
    
    prev_button = InlineKeyboardButton("⬅️ Предыдущая", callback_data='previous')
    next_button = InlineKeyboardButton("Ещё ➡️", callback_data='more')
    back_button = InlineKeyboardButton("↩️ Назад", callback_data='back_to_start')
    details_button = InlineKeyboardButton("Подробнее", callback_data='details')
    
    keyboard = [
        [prev_button, next_button, back_button],
        [details_button]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_details_keyboard(index, info_link):
    keyboard = [
        [InlineKeyboardButton("Вернуться к книге", callback_data=f'back_to_book_{index}')]
    ]
    if info_link:
        keyboard.append([InlineKeyboardButton("🔗 Перейти к книге", url=info_link)])
    return InlineKeyboardMarkup(keyboard)