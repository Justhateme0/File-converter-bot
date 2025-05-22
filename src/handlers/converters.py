import io
import logging
import piexif
from PIL import Image
from telegram import Update
from telegram.ext import ContextTypes
from src.keyboards import get_format_keyboard, get_metadata_keyboard
from src.config import IMAGES, DEFAULT_SETTINGS

logger = logging.getLogger(__name__)

DEVICE_METADATA = {
    'iPhone': {
        'make': 'Apple',
        'model': 'iPhone 15 Pro Max',
        'software': 'iOS 17.4'
    },
    'Android': {
        'make': 'Samsung',
        'model': 'Galaxy S24 Ultra',
        'software': 'Android 14'
    }
}

def get_user_settings(context: ContextTypes.DEFAULT_TYPE) -> dict:
    """Get user settings or create default ones."""
    if 'settings' not in context.user_data:
        context.user_data['settings'] = DEFAULT_SETTINGS.copy()
    return context.user_data['settings']

def create_exif_dict(metadata_type: str) -> bytes:
    """Create EXIF dictionary with device metadata."""
    if metadata_type not in DEVICE_METADATA:
        return None
        
    exif_dict = piexif.load(piexif.dump({}))  # Create empty EXIF dict
    device = DEVICE_METADATA[metadata_type]
    
    # Add device information
    exif_dict['0th'][piexif.ImageIFD.Make] = device['make'].encode('utf-8')
    exif_dict['0th'][piexif.ImageIFD.Model] = device['model'].encode('utf-8')
    exif_dict['0th'][piexif.ImageIFD.Software] = device['software'].encode('utf-8')
    
    return piexif.dump(exif_dict)

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle photo messages."""
    try:
        # Get the photo with the highest resolution
        photo = update.message.photo[-1]
        
        # Download the photo
        photo_file = await context.bot.get_file(photo.file_id)
        photo_bytes = await photo_file.download_as_bytearray()
        
        # Store the photo data in context
        context.user_data['current_image'] = photo_bytes
        
        # Ask user what they want to do
        keyboard = get_metadata_keyboard()
        await update.message.reply_text(
            text=f"{IMAGES['formats']}\nЧто вы хотите сделать с изображением?\n\n"
                 "• Конвертировать в другой формат\n"
                 "• Изменить метаданные\n"
                 "• Изменить качество",
            reply_markup=keyboard
        )
        
    except Exception as e:
        logger.error(f"Error handling photo: {str(e)}")
        await update.message.reply_text(
            text=f"{IMAGES['error']} Извините, произошла ошибка при обработке изображения. Пожалуйста, попробуйте снова."
        )

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle document messages."""
    try:
        document = update.message.document
        mime_type = document.mime_type
        
        if mime_type in ['image/jpeg', 'image/png', 'image/webp']:
            # Download the document
            doc_file = await context.bot.get_file(document.file_id)
            doc_bytes = await doc_file.download_as_bytearray()
            
            # Store the document data in context
            context.user_data['current_image'] = doc_bytes
            
            # Ask user what they want to do
            keyboard = get_metadata_keyboard()
            await update.message.reply_text(
                text=f"{IMAGES['formats']}\nЧто вы хотите сделать с изображением?\n\n"
                     "• Конвертировать в другой формат\n"
                     "• Изменить метаданные\n"
                     "• Изменить качество",
                reply_markup=keyboard
            )
        else:
            await update.message.reply_text(
                text=f"{IMAGES['error']} Извините, пока я могу конвертировать только изображения форматов JPG, PNG и WEBP."
            )
            
    except Exception as e:
        logger.error(f"Error handling document: {str(e)}")
        await update.message.reply_text(
            text=f"{IMAGES['error']} Извините, произошла ошибка при обработке файла. Пожалуйста, попробуйте снова."
        )

async def convert_image(update: Update, context: ContextTypes.DEFAULT_TYPE, target_format: str, metadata_type: str = None) -> None:
    """Convert image to target format and optionally add metadata."""
    try:
        if 'current_image' not in context.user_data:
            await update.message.reply_text(
                text=f"{IMAGES['error']} Пожалуйста, сначала отправьте изображение для конвертации."
            )
            return
            
        # Get image data and settings
        image_bytes = context.user_data['current_image']
        settings = get_user_settings(context)
        
        # Open image
        img = Image.open(io.BytesIO(image_bytes))
        
        # Convert and save
        output = io.BytesIO()
        
        # Convert format name to proper format
        format_mapping = {
            'JPG': 'JPEG',
            'PNG': 'PNG',
            'WEBP': 'WEBP'
        }
        
        save_format = format_mapping.get(target_format.upper())
        if not save_format:
            raise ValueError(f"Неподдерживаемый формат: {target_format}")
        
        # Save with appropriate settings for each format
        save_kwargs = {}
        
        if save_format == 'JPEG':
            # Remove alpha channel if present
            if img.mode in ('RGBA', 'LA'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1])
                img = background
            save_kwargs.update({
                'quality': settings['image_quality'],
                'optimize': settings['optimize_size']
            })
            
            # Add metadata if requested
            if metadata_type:
                exif_bytes = create_exif_dict(metadata_type)
                if exif_bytes:
                    save_kwargs['exif'] = exif_bytes
                
        elif save_format == 'PNG':
            save_kwargs.update({
                'optimize': settings['optimize_size']
            })
            
        elif save_format == 'WEBP':
            save_kwargs.update({
                'quality': settings['image_quality'],
                'method': 6 if settings['optimize_size'] else 4
            })
            
        # Save the image
        img.save(output, format=save_format, **save_kwargs)
        output.seek(0)
        
        # Send the converted file
        await update.message.reply_document(
            document=output,
            filename=f"converted_image.{target_format.lower()}",
            caption=f"Вот ваше изображение в формате {target_format.upper()}! ✨"
        )
        
        # Send success message with settings used
        quality_text = {90: "высокое", 80: "среднее", 60: "низкое"}
        settings_text = (
            f"{IMAGES['success']} 📊 Использованные настройки:\n"
            f"• Качество: {quality_text.get(settings['image_quality'], 'среднее')}\n"
            f"• Оптимизация: {'включена' if settings['optimize_size'] else 'выключена'}\n"
            f"• Метаданные: {metadata_type if metadata_type else 'без изменений'}"
        )
        
        await update.message.reply_text(text=settings_text)
        
        # Clear the stored image
        del context.user_data['current_image']
        
    except Exception as e:
        logger.error(f"Error converting image: {str(e)}")
        await update.message.reply_text(
            text=f"{IMAGES['error']} Извините, произошла ошибка при конвертации. Пожалуйста, попробуйте снова."
        ) 