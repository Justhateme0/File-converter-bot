import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot token
TOKEN = os.getenv("TELEGRAM_TOKEN")

# Supported formats
SUPPORTED_IMAGE_FORMATS = ['JPG', 'PNG', 'WEBP']
SUPPORTED_DOCUMENT_FORMATS = ['PDF', 'DOCX', 'DOC', 'TXT']
SUPPORTED_VIDEO_FORMATS = ['MP4', 'AVI', 'MOV', 'MKV']

# Default settings
DEFAULT_SETTINGS = {
    'image_quality': 90,
    'default_format': 'PNG',
    'maintain_exif': True,
    'optimize_size': True,
    'video_metadata': None  # Может быть 'iPhone', 'Android' или 'CapCut'
}

# Metadata presets
METADATA_PRESETS = {
    'iPhone': {
        'make': 'Apple',
        'model': 'iPhone 15 Pro Max',
        'software': 'iOS 17.4',
        'creation_time': '2024',
        'encoder': 'Apple H.264'
    },
    'Android': {
        'make': 'Samsung',
        'model': 'Galaxy S24 Ultra',
        'software': 'Android 14',
        'creation_time': '2024',
        'encoder': 'Samsung H.264'
    },
    'CapCut': {
        'software': 'CapCut 9.9.0',
        'artist': 'Edited with CapCut',
        'comment': 'Created with CapCut',
        'encoder': 'CapCut Encoder'
    }
}

# Images for messages (используем стабильные эмодзи вместо изображений)
IMAGES = {
    'welcome': '👋',     # Приветствие
    'help': '❓',        # Помощь
    'settings': '⚙️',    # Настройки
    'formats': '📁',     # Форматы
    'success': '✅',     # Успех
    'error': '❌'        # Ошибка
}

# Messages
WELCOME_MESSAGE = """
Привет! Я бот для конвертации файлов. 🤖

Доступные команды:
/start - показать это сообщение
/help - показать справку по использованию
/formats - показать поддерживаемые форматы
/settings - настройки конвертации

Поддерживаемые форматы:
📸 Изображения: JPG ↔ PNG ↔ WEBP
📄 Документы: PDF ↔ DOCX ↔ TXT
🎥 Видео: MP4 ↔ AVI ↔ MOV ↔ MKV

Дополнительные возможности:
• Изменение метаданных (iPhone, Android, CapCut)
• Настройка качества
• Оптимизация размера

Просто отправьте мне файл, и я помогу вам его конвертировать!
"""

HELP_MESSAGE = """
📚 Как пользоваться ботом:

1️⃣ Отправьте файл, который хотите конвертировать
2️⃣ Выберите формат, в который хотите конвертировать
3️⃣ При необходимости, выберите дополнительные опции:
   • Изменение метаданных (устройство, приложение)
   • Настройка качества
   • Оптимизация размера

⚙️ Настройки изображений:
• Качество изображения
• Формат по умолчанию
• Сохранение EXIF данных
• Оптимизация размера

📄 Поддержка документов:
• Конвертация PDF в DOCX и TXT
• Конвертация DOCX/DOC в PDF и TXT
• Конвертация TXT в PDF и DOCX

🎥 Поддержка видео:
• Конвертация между форматами
• Добавление метаданных:
  - iPhone (iOS 17.4)
  - Android (Galaxy S24 Ultra)
  - CapCut (редактор)
• Оптимизация качества

При возникновении проблем, пожалуйста, попробуйте снова или свяжитесь с администратором.
"""

FORMATS_MESSAGE = """
📋 Поддерживаемые форматы:

📸 Изображения:
• JPG ↔ PNG ↔ WEBP
• Сохранение качества при конвертации
• Поддержка прозрачности для PNG и WEBP
• Настраиваемое качество сжатия
• Изменение метаданных устройства

📄 Документы:
• PDF ↔ DOCX
• DOCX/DOC → PDF
• DOCX/DOC → TXT
• TXT → PDF/DOCX

🎥 Видео:
• MP4 ↔ AVI ↔ MOV ↔ MKV
• Сохранение качества
• Добавление метаданных:
  - iPhone (как с iPhone 15 Pro Max)
  - Android (как с Galaxy S24 Ultra)
  - CapCut (как после редактирования)
"""

SETTINGS_MESSAGE = """
⚙️ Настройки конвертации:

Текущие настройки:
{current_settings}

Выберите параметр для изменения:
""" 