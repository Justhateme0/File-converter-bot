import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram import Update

from src.config import TOKEN
from src.handlers.commands import start, help_command, formats_command, settings_command
from src.handlers.converters import handle_photo, handle_document
from src.handlers.document_converter import handle_document_conversion, handle_conversion_choice
from src.handlers.video_converter import handle_video
from src.handlers.callbacks import handle_text

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

def main() -> None:
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(TOKEN).build()

    # Command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("formats", formats_command))
    application.add_handler(CommandHandler("settings", settings_command))

    # Message handlers
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    
    # Video handler
    application.add_handler(MessageHandler(
        filters.VIDEO | filters.Document.VIDEO |
        filters.Document.Category("video/mp4") |
        filters.Document.Category("video/x-msvideo") |
        filters.Document.Category("video/quicktime") |
        filters.Document.Category("video/x-matroska"),
        handle_video
    ))
    
    # Document handlers with mime type filters
    application.add_handler(MessageHandler(
        filters.Document.IMAGE | 
        filters.Document.Category("image/jpeg") | 
        filters.Document.Category("image/png") | 
        filters.Document.Category("image/webp"),
        handle_document
    ))
    
    application.add_handler(MessageHandler(
        filters.Document.Category("application/pdf") |
        filters.Document.Category("application/msword") |
        filters.Document.Category("application/vnd.openxmlformats-officedocument.wordprocessingml.document") |
        filters.Document.Category("text/plain"),
        handle_document_conversion
    ))
    
    # Handler for conversion format choice
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND & filters.Regex(r'^[12]$'),
        handle_conversion_choice
    ))
    
    # Text handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    # Run the bot until the user presses Ctrl-C
    logger.info("Bot started")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main() 