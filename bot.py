import telegram
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards import get_main_keyboard, get_language_keyboard, get_level_keyboard, get_type_keyboard, get_genre_keyboard, get_recommendation_keyboard, get_details_keyboard
from database import get_book_recommendation
from utils import format_book
from telegram.ext import ContextTypes

async def start(update, context: ContextTypes.DEFAULT_TYPE):
    message = await update.message.reply_text(
        '📚 *Привет!* Я бот для изучения литературы. Выбери действие: 👇\n'
        '👉 Язык: -, Уровень: -, Тип: -',
        reply_markup=get_main_keyboard(context), parse_mode='Markdown'
    )
    context.user_data['message_id'] = message.message_id

async def help_command(update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        '📖 *Как я могу помочь?* Я рекомендую книги на основе твоих предпочтений! 🎉\n'
        '1️⃣ Выбери язык, уровень и тип литературы.\n'
        '2️⃣ Если выбрана "Художественная", можешь выбрать жанр (или пропустить).\n'
        '3️⃣ Нажми "Рекомендовать книгу", чтобы получить подборку.\n'
        '4️⃣ Используй кнопки "Ещё" и "Предыдущая" для навигации.\n'
        '5️⃣ Нажми "Подробнее", чтобы узнать больше о книге!\n'
        'Если что-то непонятно, пиши /start и начнем заново! 😊',
        parse_mode='Markdown'
    )

async def about_project(update, context: ContextTypes.DEFAULT_TYPE):
    about_text = (
        '📚 *О проекте* ℹ️\n'
        'Я — бот для поиска литературы, который помогает находить книги для изучения языков! 🎉\n'
        'Моя цель — сделать процесс поиска книг удобным и быстрым. Ты можешь выбрать язык, уровень, тип книги (учебная или художественная) и жанр, а я найду подходящие варианты.\n\n'
        '📩 *Обратная связь*: Если у тебя есть идеи или предложения, пиши моему создателю! @littlefroggit\n\n'
        'Спасибо, что пользуешься мной! 😊'
    )
    await update.message.reply_text(about_text, parse_mode='Markdown')

async def button_handler(update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    message_id = context.user_data.get('message_id')
    chat_id = query.message.chat_id
    
    language = context.user_data.get('language', '-')
    level = context.user_data.get('level', '-')
    book_type = context.user_data.get('book_type', '-')
    genre = context.user_data.get('genre', '-')
    
    if query.data == 'select_language':
        await query.edit_message_text('🌐 *Выбери язык для чтения:*', reply_markup=get_language_keyboard(), parse_mode='Markdown')
    elif query.data == 'select_level':
        await query.edit_message_text('🎓 *Выбери свой уровень:*', reply_markup=get_level_keyboard(), parse_mode='Markdown')
    elif query.data == 'select_type':
        await query.edit_message_text('📚 *Какую книгу ты ищешь?*', reply_markup=get_type_keyboard(), parse_mode='Markdown')
    elif query.data == 'recommend':
        missing = []
        if not context.user_data.get('language'):
            missing.append("язык")
        if not context.user_data.get('level'): 
            missing.append("уровень")
        if not context.user_data.get('book_type'):
            missing.append("тип литературы")
        
        if missing:
            await query.edit_message_text(
                f'❌ *Ой, нужно выбрать {", ".join(missing)}!* 😊\n'
                f'👉 *Язык*: {language}, *Уровень*: {level}, *Тип*: {book_type}, *Жанр*: {genre if genre else '-'}',
                reply_markup=get_main_keyboard(context), parse_mode='Markdown'
            )
        else:
            await query.edit_message_text('⏳ *Ищу книги для тебя...*', reply_markup=None, parse_mode='Markdown')
            books = get_book_recommendation(language, level, book_type, genre)
            if not books:
                await query.edit_message_text(
                    '📖 *Книги не найдены для этой комбинации...* Попробуй другие параметры! 😊\n'
                    f'👉 *Язык*: {language}, *Уровень*: {level}, *Тип*: {book_type}, *Жанр*: {genre if genre else '-'}',
                    reply_markup=get_main_keyboard(context), parse_mode='Markdown'
                )
                return
            
            context.user_data['books'] = books
            context.user_data['book_index'] = 0
            
            first_book = format_book(books[0])
            
            keyboard = get_recommendation_keyboard(context)
            await query.edit_message_text(
                f'🎉 *Вот твоя подборка!* 📚\n'
                f'👉 *Язык*: {language}, *Уровень*: {level}, *Тип*: {book_type}, *Жанр*: {genre if genre else '-'}\n'
                f'📘 *Книга 1 из {len(books)}*: {first_book}',
                reply_markup=keyboard, parse_mode='Markdown'
            )
            
    elif query.data.startswith('language_'):
        language = query.data.replace('language_', '')
        context.user_data['language'] = language
        if 'books' in context.user_data:
            del context.user_data['books']
        if 'book_index' in context.user_data:
            del context.user_data['book_index']
        await query.edit_message_text(
            f'🌍 *Ты выбрал язык:* {language}\n' 
            f'👉 *Язык*: {language}, *Уровень*: {level}, *Тип*: {book_type}, *Жанр*: {genre if genre else '-'}',
            reply_markup=get_main_keyboard(context), parse_mode='Markdown'
        )
        
    elif query.data.startswith('level_'):
        level = query.data.replace('level_', '')
        context.user_data['level'] = level
        if 'books' in context.user_data:
            del context.user_data['books']
        if 'book_index' in context.user_data:
            del context.user_data['book_index']
        await query.edit_message_text(
            f'🎓 *Ты выбрал уровень:* {level}\n'
            f'👉 *Язык*: {language}, *Уровень*: {level}, *Тип*: {book_type}, *Жанр*: {genre if genre else '-'}',
            reply_markup=get_main_keyboard(context), parse_mode='Markdown'
        )
        
    elif query.data.startswith('type_'):
        book_type = query.data.replace('type_', '')
        context.user_data['book_type'] = book_type
        if 'books' in context.user_data:
            del context.user_data['books']
        if 'book_index' in context.user_data:
            del context.user_data['book_index']
        if book_type == "художественная":
            await query.edit_message_text(
                '*Выбери жанр (или пропусти):*',
                reply_markup=get_genre_keyboard(),
                parse_mode='Markdown'
            )
        else:
            await query.edit_message_text(
                f'📚 *Ты выбрал тип:* {book_type}\n'
                f'👉 *Язык*: {language}, *Уровень*: {level}, *Тип*: {book_type}, *Жанр*: {genre if genre else '-'}',
                reply_markup=get_main_keyboard(context), parse_mode='Markdown'
            )
    
    elif query.data.startswith('genre_'):
        genre = query.data.replace('genre_', '')
        context.user_data['genre'] = genre
        if 'books' in context.user_data:
            del context.user_data['books']
        if 'book_index' in context.user_data:
            del context.user_data['book_index']
        await query.edit_message_text(
            f'🎨 *Ты выбрал жанр:* {genre}\n'
            f'👉 *Язык*: {language}, *Уровень*: {level}, *Тип*: {book_type}, *Жанр*: {genre}',
            reply_markup=get_main_keyboard(context), parse_mode='Markdown'
        )
        
    elif query.data == 'skip_genre':
        context.user_data['genre'] = None
        if 'books' in context.user_data:
            del context.user_data['books']
        if 'book_index' in context.user_data:
            del context.user_data['book_index']
        await query.edit_message_text(
            f'⏭️ *Жанр пропущен.*\n'
            f'👉 *Язык*: {language}, *Уровень*: {level}, *Тип*: {book_type}, *Жанр*: {genre if genre else "-"}',
            reply_markup=get_main_keyboard(context), parse_mode='Markdown'
        )
        
    elif query.data == 'back':
        await query.edit_message_text(
            '📖 *Давай выберем книгу!* 😊\n'
            f'👉 *Язык*: {language}, *Уровень*: {level}, *Тип*: {book_type}, *Жанр*: {genre if genre else "-"}',
            reply_markup=get_main_keyboard(context), parse_mode='Markdown'
        )
        
    elif query.data == 'reset':
        context.user_data.clear()
        await query.edit_message_text(
            '🔄 *Все настройки сброшены!* Давай начнем заново! 😊\n'
            '👉 *Язык*: -, *Уровень*: -, *Тип*: -, *Жанр*: -',
            reply_markup=get_main_keyboard(context), parse_mode='Markdown'
        )
    
    elif query.data == 'help':
        help_text = (
            '📖 *Как я могу помочь?* Я рекомендую книги на основе твоих предпочтений! 🎉\n'
            '1️⃣ Выбери язык, уровень и тип литературы.\n'
            '2️⃣ Если выбрана "Художественная", можешь выбрать жанр (или пропустить).\n'
            '3️⃣ Нажми "Рекомендовать книгу", чтобы получить подборку.\n'
            '4️⃣ Используй кнопки "Ещё" и "Предыдущая" для навигации.\n'
            '5️⃣ Нажми "Подробнее", чтобы узнать больше о книге!\n'
            'Если что-то непонятно, пиши /start и начнем заново! 😊'
        )
        await query.edit_message_text(
            help_text,
            reply_markup=get_main_keyboard(context),
            parse_mode='Markdown'
        )
        
    elif query.data == 'about':
        about_text = (
            '📚 *О проекте* ℹ️\n'
            'Я — бот для поиска литературы, который помогает находить книги для изучения языков! 🎉\n'
            'Моя цель — сделать процесс поиска книг удобным и быстрым. Ты можешь выбрать язык, уровень, тип книги (учебная или художественная) и жанр, а я найду подходящие варианты.\n\n'
            '📩 *Обратная связь*: Если у тебя есть идеи или предложения, пиши моему создателю! @littlefroggit\n\n'
            'Спасибо, что пользуешься мной! 😊'
        )
        await query.edit_message_text(
            about_text,
            reply_markup=get_main_keyboard(context),
            parse_mode='Markdown'
        )
    
    elif query.data == 'details':
        books = context.user_data.get('books', [])
        index = context.user_data.get('book_index', 0)
        if not books or index < 0 or index >= len(books):
            await query.message.reply_text("😔 Не удалось загрузить информацию о книге. Попробуй снова!")
            return
        
        book = books[index]
        details, info_link = format_book(book, full_details=True)
        
        short_text = f'📘 *Книга {index + 1} из {len(books)}*: {format_book(book)}'
        context.user_data['short_text'] = short_text
        context.user_data['language'] = language
        context.user_data['level'] = level
        context.user_data['book_type'] = book_type
        
        await query.edit_message_text(
            details,
            reply_markup=get_details_keyboard(index, info_link),
            parse_mode='Markdown'
        )
        
    elif query.data.startswith('back_to_book_'):
        index = int(query.data.replace('back_to_book_', ''))
        context.user_data['book_index'] = index
        books = context.user_data.get('books', [])
        if not books or index < 0 or index >= len(books):
            await query.edit_message_text(
                "😔 Не удалось вернуться к книге. Попробуй снова!",
                reply_markup=get_recommendation_keyboard(context),
                parse_mode='Markdown'
            )
        
        short_text = context.user_data.get('short_text', '')
        language = context.user_data.get('language', '-')
        level = context.user_data.get('level', '-')
        book_type = context.user_data.get('book_type', '-')
        genre = context.user_data.get('genre', '-')
        
        full_text = (
            f'🎉 *Вот твоя подборка!* 📚\n'
            f'👉 *Язык*: {language}, *Уровень*: {level}, *Тип*: {book_type}, *Жанр*: {genre if genre else "Не выбран"}\n'
            f'{short_text}'
        )
        
        keyboard = get_recommendation_keyboard(context)
        await query.edit_message_text(
            full_text,
            reply_markup=keyboard,
            parse_mode='Markdown'
        )

    elif query.data in ['more', 'previous', 'back_to_start']:
        books = context.user_data.get('books', [])
        index = context.user_data.get('book_index', 0)
        max_index = len(books) - 1 if books else 0
        
        if query.data == 'more' and index < max_index:
            index += 1
            context.user_data['book_index'] = index
            book = format_book(books[index])
            keyboard = get_recommendation_keyboard(context)
            await query.edit_message_text(
                f'📘 *Книга {index + 1} из {len(books)}*: {book}',
                reply_markup=keyboard, parse_mode='Markdown'
            )
        elif query.data == 'previous' and index > 0:
            index -= 1
            context.user_data['book_index'] = index
            book = format_book(books[index])
            keyboard = get_recommendation_keyboard(context)
            await query.edit_message_text(
                f'📘 *Книга {index + 1} из {len(books)}*: {book}',
                reply_markup=keyboard, parse_mode='Markdown'
            )
        
        elif query.data == 'back_to_start':
            await query.edit_message_text(
                '📚 *Привет!* Я бот для поиска литературы. Давай подберем тебе книгу! 📖\n'
                f'👉 *Язык*: {language}, *Уровень*: {level}, *Тип*: {book_type}, *Жанр*: {genre if genre else "Не выбран"}',
                reply_markup=get_main_keyboard(context),
                parse_mode='Markdown'
            )
        
        elif query.data == 'more' and index >= max_index:
            await query.message.reply_text("📚 Это последняя книга в списке! Попробуй другие параметры! 😊")
        elif query.data == 'previous' and index <= 0:
            await query.message.reply_text("📚 Это первая книга в списке! 😊")

async def reset(update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        '🔄 *Все настройки сброшены!* Давай начнем заново! 😊\n'
        'Нажми /start, чтобы выбрать новые параметры! 📖',
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Начать 📖", callback_data='start')]]),
        parse_mode='Markdown'
    )

async def error_handler(update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Произошла ошибка: {context.error}")