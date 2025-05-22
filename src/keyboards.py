from telegram import ReplyKeyboardMarkup

def get_main_keyboard() -> ReplyKeyboardMarkup:
    """Get main menu keyboard."""
    keyboard = [
        ['Конвертировать файл'],
        ['Форматы', 'Настройки'],
        ['Помощь']
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_format_keyboard() -> ReplyKeyboardMarkup:
    """Get format selection keyboard."""
    keyboard = [
        ['JPG', 'PNG', 'WEBP'],
        ['Отмена']
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_settings_keyboard() -> ReplyKeyboardMarkup:
    """Get settings keyboard."""
    keyboard = [
        ['Качество изображения'],
        ['Формат по умолчанию'],
        ['EXIF данные', 'Оптимизация'],
        ['Метаданные видео'],
        ['Назад']
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_quality_keyboard() -> ReplyKeyboardMarkup:
    """Get quality selection keyboard."""
    keyboard = [
        ['Высокое', 'Среднее', 'Низкое'],
        ['Назад']
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_format_default_keyboard() -> ReplyKeyboardMarkup:
    """Get default format selection keyboard."""
    keyboard = [
        ['JPG', 'PNG', 'WEBP'],
        ['Назад']
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_boolean_keyboard() -> ReplyKeyboardMarkup:
    """Get yes/no keyboard."""
    keyboard = [
        ['Включить', 'Выключить'],
        ['Назад']
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_doc_format_keyboard(current_format: str) -> ReplyKeyboardMarkup:
    """Get document format selection keyboard."""
    formats = ['PDF', 'DOCX', 'TXT']
    formats.remove(current_format)
    keyboard = [formats, ['Отмена']]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_video_format_keyboard() -> ReplyKeyboardMarkup:
    """Get video format selection keyboard."""
    keyboard = [
        ['MP4', 'AVI', 'MOV'],
        ['Конвертировать без метаданных'],
        ['Отмена']
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_metadata_keyboard() -> ReplyKeyboardMarkup:
    """Get metadata options keyboard."""
    keyboard = [
        ['iPhone', 'Android'],
        ['CapCut'],
        ['Конвертировать без метаданных'],
        ['Отмена']
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_video_metadata_keyboard() -> ReplyKeyboardMarkup:
    """Get video metadata settings keyboard."""
    keyboard = [
        ['iPhone', 'Android'],
        ['CapCut'],
        ['Убрать метаданные'],
        ['Назад']
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True) 