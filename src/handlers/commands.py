from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from src.config import (
    WELCOME_MESSAGE, HELP_MESSAGE, FORMATS_MESSAGE, 
    SETTINGS_MESSAGE, IMAGES, DEFAULT_SETTINGS
)
from src.keyboards import get_main_keyboard, get_settings_keyboard

def get_user_settings(context: ContextTypes.DEFAULT_TYPE) -> dict:
    """Get user settings or create default ones."""
    if 'settings' not in context.user_data:
        context.user_data['settings'] = DEFAULT_SETTINGS.copy()
    return context.user_data['settings']

def format_settings(settings: dict) -> str:
    """Format settings for display."""
    quality_text = {90: "Высокое", 80: "Среднее", 60: "Низкое"}
    return (
        f"• Качество: {quality_text.get(settings['image_quality'], 'Среднее')}\n"
        f"• Формат по умолчанию: {settings['default_format']}\n"
        f"• Сохранение EXIF: {'Включено' if settings['maintain_exif'] else 'Выключено'}\n"
        f"• Оптимизация размера: {'Включена' if settings['optimize_size'] else 'Выключена'}"
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    keyboard = get_main_keyboard()
    await update.message.reply_text(
        text=f"{IMAGES['welcome']} {WELCOME_MESSAGE}",
        reply_markup=keyboard
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text(
        text=f"{IMAGES['help']} {HELP_MESSAGE}"
    )

async def formats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Show supported formats."""
    await update.message.reply_text(
        text=f"{IMAGES['formats']} {FORMATS_MESSAGE}"
    )

async def settings_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle settings command."""
    settings = get_user_settings(context)
    formatted_settings = format_settings(settings)
    keyboard = get_settings_keyboard()
    
    await update.message.reply_text(
        text=f"{IMAGES['settings']} {SETTINGS_MESSAGE.format(current_settings=formatted_settings)}",
        reply_markup=keyboard
    ) 