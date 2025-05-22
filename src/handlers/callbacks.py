from telegram import Update
from telegram.ext import ContextTypes
from src.handlers.converters import convert_image
from src.handlers.document_converter import convert_document
from src.handlers.video_converter import convert_video
from src.keyboards import (
    get_main_keyboard, get_quality_keyboard, 
    get_format_default_keyboard, get_boolean_keyboard,
    get_settings_keyboard, get_format_keyboard,
    get_metadata_keyboard, get_video_format_keyboard
)
from src.handlers.commands import help_command, formats_command, settings_command
from src.config import IMAGES

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle text messages."""
    text = update.message.text

    if text == 'Конвертировать файл':
        await update.message.reply_text(
            text=f"{IMAGES['formats']}\nОтправьте мне файл в одном из поддерживаемых форматов:\n\n"
                 "📸 Изображения:\n"
                 "• JPG\n"
                 "• PNG\n"
                 "• WEBP\n\n"
                 "📄 Документы:\n"
                 "• PDF\n"
                 "• DOCX/DOC\n"
                 "• TXT\n\n"
                 "🎥 Видео:\n"
                 "• MP4\n"
                 "• AVI\n"
                 "• MOV\n"
                 "• MKV\n\n"
                 "Вы можете отправить файл как фотографию или как документ."
        )
    elif text == 'Помощь':
        await help_command(update, context)
    elif text == 'Форматы':
        await formats_command(update, context)
    elif text == 'Настройки':
        await settings_command(update, context)
    elif text == 'Качество изображения':
        keyboard = get_quality_keyboard()
        await update.message.reply_text(
            text=f"{IMAGES['settings']}\nВыберите качество изображения:\n\n"
                 "• Высокое - минимальное сжатие\n"
                 "• Среднее - оптимальное сжатие\n"
                 "• Низкое - максимальное сжатие",
            reply_markup=keyboard
        )
    elif text == 'Формат по умолчанию':
        keyboard = get_format_default_keyboard()
        await update.message.reply_text(
            text=f"{IMAGES['settings']}\nВыберите формат по умолчанию:\n\n"
                 "Этот формат будет использоваться, если вы не выберете другой.",
            reply_markup=keyboard
        )
    elif text == 'EXIF данные':
        keyboard = get_boolean_keyboard()
        await update.message.reply_text(
            text=f"{IMAGES['settings']}\nСохранять EXIF данные при конвертации?\n\n"
                 "EXIF данные содержат информацию о фотографии (камера, настройки и т.д.)",
            reply_markup=keyboard
        )
    elif text == 'Оптимизация':
        keyboard = get_boolean_keyboard()
        await update.message.reply_text(
            text=f"{IMAGES['settings']}\nВключить оптимизацию размера файла?\n\n"
                 "При включенной оптимизации файлы будут меньше, но конвертация займет больше времени.",
            reply_markup=keyboard
        )
    elif text == 'Конвертировать':
        keyboard = get_format_keyboard()
        await update.message.reply_text(
            text=f"{IMAGES['formats']}\nВыберите формат для конвертации:",
            reply_markup=keyboard
        )
    elif text == 'Изменить метаданные':
        keyboard = get_metadata_keyboard()
        await update.message.reply_text(
            text=f"{IMAGES['settings']}\nВыберите тип метаданных:\n\n"
                 "• iPhone - метаданные iPhone 15 Pro Max\n"
                 "• Android - метаданные Samsung S24 Ultra\n"
                 "• CapCut - метаданные редактора CapCut",
            reply_markup=keyboard
        )
    elif text == 'Отмена':
        if 'current_image' in context.user_data:
            del context.user_data['current_image']
        if 'current_document' in context.user_data:
            del context.user_data['current_document']
        if 'current_video' in context.user_data:
            del context.user_data['current_video']
        keyboard = get_main_keyboard()
        await update.message.reply_text(
            text=f"{IMAGES['error']} Операция отменена. Чем могу помочь?",
            reply_markup=keyboard
        )
    elif text == 'Назад':
        keyboard = get_main_keyboard()
        await update.message.reply_text(
            text=f"{IMAGES['welcome']} Главное меню:",
            reply_markup=keyboard
        )
    elif text in ['JPG', 'PNG', 'WEBP']:
        if context.user_data.get('setting_default_format'):
            context.user_data['settings']['default_format'] = text
            del context.user_data['setting_default_format']
            keyboard = get_settings_keyboard()
            await update.message.reply_text(
                text=f"{IMAGES['success']} Формат по умолчанию установлен: {text}",
                reply_markup=keyboard
            )
        else:
            metadata_type = context.user_data.get('metadata_type')
            await convert_image(update, context, text, metadata_type)
            if 'metadata_type' in context.user_data:
                del context.user_data['metadata_type']
    elif text in ['MP4', 'AVI', 'MOV', 'MKV']:
        metadata_type = context.user_data.get('metadata_type')
        await convert_video(update, context, text, metadata_type)
        if 'metadata_type' in context.user_data:
            del context.user_data['metadata_type']
    elif text in ['PDF', 'DOCX', 'TXT']:
        await convert_document(update, context, text)
    elif text in ['Высокое', 'Среднее', 'Низкое']:
        quality = {'Высокое': 90, 'Среднее': 80, 'Низкое': 60}
        context.user_data['settings']['image_quality'] = quality[text]
        keyboard = get_settings_keyboard()
        await update.message.reply_text(
            text=f"{IMAGES['success']} Качество изображения установлено на: {text}",
            reply_markup=keyboard
        )
    elif text in ['iPhone', 'Android', 'CapCut']:
        context.user_data['metadata_type'] = text
        if 'current_video' in context.user_data:
            keyboard = get_video_format_keyboard()
        else:
            keyboard = get_format_keyboard()
        await update.message.reply_text(
            text=f"{IMAGES['settings']} Выбраны метаданные: {text}\n"
                 "Теперь выберите формат для конвертации:",
            reply_markup=keyboard
        )
    elif text in ['Включить', 'Выключить']:
        value = text == 'Включить'
        if context.user_data.get('setting_exif'):
            context.user_data['settings']['maintain_exif'] = value
            del context.user_data['setting_exif']
            setting_name = 'EXIF данных'
        elif context.user_data.get('setting_optimize'):
            context.user_data['settings']['optimize_size'] = value
            del context.user_data['setting_optimize']
            setting_name = 'оптимизации'
        else:
            return
            
        keyboard = get_settings_keyboard()
        await update.message.reply_text(
            text=f"{IMAGES['success']} Настройка {setting_name} {text.lower()}на",
            reply_markup=keyboard
        ) 