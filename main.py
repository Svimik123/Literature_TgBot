import telegram
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from bot import start, help_command, reset, button_handler, about_project, error_handler

TOKEN = 'TokenIsHere'

def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('reset', reset))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_error_handler(error_handler)

    print('Бот запущен!')
    application.run_polling()

if __name__ == '__main__':
    main()