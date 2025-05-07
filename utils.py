def format_book(book, full_details=False):
    volume_info = book.get("volumeInfo", {})
    title = volume_info.get("title", "Название не найдено")
    authors = ", ".join(volume_info.get("authors", ["Автор неизвестен"]))
    
    if not full_details:
        return f"{title} by {authors}"
    else:
        description = volume_info.get("description", "Описание отсутствует.")
        page_count = volume_info.get("pageCount", "Не указано")
        published_date = volume_info.get("publishedDate", "Не указана")
        info_link = volume_info.get("infoLink", None)
        
        details = (
            f"📖 *{title}* by {authors}\n"
            f"📅 *Дата публикации*: {published_date}\n"
            f"📏 *Количество страниц*: {page_count}\n\n"
            f"📜 *Описание*: {description[:500]}{'...' if len(description) > 500 else ''}"
        )
        return details, info_link