import os
import io
import logging
import tempfile
import subprocess
from datetime import datetime
from pathlib import Path
from telegram import Update
from telegram.ext import ContextTypes
from mutagen.mp4 import MP4, MP4Cover
from mutagen.id3 import ID3, TIT2, TPE1, TDRC
from src.keyboards import get_video_format_keyboard, get_metadata_keyboard
from src.config import IMAGES, METADATA_PRESETS, DEFAULT_SETTINGS

logger = logging.getLogger(__name__)

# Добавляем путь к FFmpeg
FFMPEG_BIN = r"C:\ffmpeg\bin"
FFMPEG_EXE = os.path.join(FFMPEG_BIN, "ffmpeg.exe")
FFPROBE_EXE = os.path.join(FFMPEG_BIN, "ffprobe.exe")

def run_ffmpeg(input_path, output_path, metadata=None):
    """Run FFmpeg command with the specified parameters."""
    command = [FFMPEG_EXE, '-i', input_path]
    
    if metadata:
        for key, value in metadata.items():
            command.extend(['-metadata', f'{key}={value}'])
    
    command.extend(['-y', output_path])
    
    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"FFmpeg error: {e.stderr}")
        raise RuntimeError(f"Ошибка при конвертации: {e.stderr}")

def probe_video(input_path):
    """Check if video file is valid using FFprobe."""
    try:
        result = subprocess.run(
            [FFPROBE_EXE, input_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.returncode == 0
    except Exception as e:
        logger.error(f"FFprobe error: {str(e)}")
        return False

SUPPORTED_VIDEO_FORMATS = ['MP4', 'AVI', 'MOV', 'MKV']
DEVICE_METADATA = {
    'iPhone': {
        'make': 'Apple',
        'model': 'iPhone 15 Pro Max',
        'software': 'iOS 17.4',
        'encoder': 'com.apple.videotoolbox.videoencoder',
        'creation_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'copyright': '© Apple Inc.',
        'device_id': 'iPhone15,2',
        'device_manufacturer': 'Apple',
        'device_model': 'iPhone 15 Pro Max',
        'os_version': 'iOS 17.4',
        'location': '0+0/',
        'date': datetime.now().strftime('%Y:%m:%d %H:%M:%S'),
        'description': 'Video recorded with iPhone 15 Pro Max',
        'artist': 'iPhone User',
        'album': 'iPhone Camera Roll'
    },
    'CapCut': {
        'software': 'CapCut 9.9.0',
        'artist': 'Edited with CapCut',
        'comment': 'Created with CapCut',
        'encoder': 'CapCut Video Editor',
        'creation_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'copyright': '© ByteDance Inc.',
        'composer': 'CapCut Editor',
        'handler_name': 'CapCut Media Handler',
        'album': 'CapCut Projects',
        'date': datetime.now().strftime('%Y:%m:%d %H:%M:%S'),
        'description': 'Video edited with CapCut 9.9.0',
        'keywords': 'capcut,video,edit,tiktok',
        'title': 'CapCut Video',
        'compatible_brands': 'isomiso2mp41',
        'major_brand': 'isom',
        'minor_version': '512'
    },
    'Android': {
        'make': 'Samsung',
        'model': 'Galaxy S24 Ultra',
        'software': 'Android 14',
        'encoder': 'com.samsung.videoeditor',
        'creation_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'copyright': '© Samsung Electronics',
        'device_id': 'SM-S928B',
        'device_manufacturer': 'Samsung',
        'device_model': 'Galaxy S24 Ultra',
        'os_version': 'Android 14 OneUI 6.1',
        'location': '0+0/',
        'date': datetime.now().strftime('%Y:%m:%d %H:%M:%S'),
        'description': 'Video recorded with Samsung Galaxy S24 Ultra',
        'artist': 'Samsung User',
        'album': 'Samsung Camera',
        'handler_name': 'Samsung Video Media Handler',
        'compatible_brands': 'isomiso2mp41',
        'major_brand': 'isom',
        'minor_version': '512'
    }
}

def get_user_settings(context: ContextTypes.DEFAULT_TYPE) -> dict:
    """Get user settings or create default ones."""
    if 'settings' not in context.user_data:
        context.user_data['settings'] = DEFAULT_SETTINGS.copy()
    return context.user_data['settings']

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle video messages."""
    try:
        logger.info("Starting video handling process")
        video = update.message.video or update.message.document
        if not video:
            await update.message.reply_text(
                text=f"{IMAGES['error']} Пожалуйста, отправьте видео файл."
            )
            return

        # Log video information
        logger.info(f"Received video - File ID: {video.file_id}, "
                   f"File name: {getattr(video, 'file_name', 'video')}, "
                   f"MIME type: {getattr(video, 'mime_type', 'video/mp4')}")

        # Download video
        logger.info("Downloading video file")
        video_file = await context.bot.get_file(video.file_id)
        video_bytes = await video_file.download_as_bytearray()
        
        logger.info(f"Video downloaded successfully, size: {len(video_bytes)} bytes")
        
        # Store video info in context
        context.user_data['current_video'] = {
            'bytes': video_bytes,
            'name': getattr(video, 'file_name', 'video'),
            'mime_type': getattr(video, 'mime_type', 'video/mp4')
        }
        
        # Ask user what they want to do
        keyboard = get_metadata_keyboard()
        await update.message.reply_text(
            text=f"{IMAGES['formats']}\nЧто вы хотите сделать с видео?\n\n"
                 "• Конвертировать в другой формат\n"
                 "• Добавить метаданные устройства (iPhone/Android)\n"
                 "• Добавить метаданные CapCut",
            reply_markup=keyboard
        )
        
    except Exception as e:
        logger.error(f"Error handling video: {str(e)}", exc_info=True)
        await update.message.reply_text(
            text=f"{IMAGES['error']} Произошла ошибка при обработке видео."
        )

async def convert_video(update: Update, context: ContextTypes.DEFAULT_TYPE, target_format: str, metadata_type: str = None) -> None:
    """Convert video to target format and optionally add metadata."""
    temp_dir = None
    try:
        logger.info(f"Starting video conversion to {target_format}")
        if 'current_video' not in context.user_data:
            await update.message.reply_text(
                text=f"{IMAGES['error']} Пожалуйста, сначала отправьте видео."
            )
            return
            
        video_info = context.user_data['current_video']
        video_bytes = video_info['bytes']
        original_name = Path(video_info['name']).stem
        
        logger.info(f"Creating temporary directory for video conversion")
        temp_dir = tempfile.mkdtemp()
        logger.info(f"Temporary directory created at: {temp_dir}")
        
        # Save original video
        source_path = os.path.join(temp_dir, f"source{Path(video_info['name']).suffix}")
        logger.info(f"Saving source video to: {source_path}")
        with open(source_path, 'wb') as f:
            f.write(video_bytes)
        
        if not os.path.exists(source_path):
            raise FileNotFoundError(f"Source file was not created at {source_path}")
            
        # Prepare output path
        target_path = os.path.join(temp_dir, f"output.{target_format.lower()}")
        logger.info(f"Target path will be: {target_path}")
        
        # Check if video is valid
        if not probe_video(source_path):
            raise RuntimeError("Невозможно обработать видео файл. Проверьте, что файл не поврежден.")
            
        # Convert video
        logger.info("Starting FFmpeg conversion")
        
        # Get metadata settings
        settings = get_user_settings(context)
        metadata_type = metadata_type or settings.get('video_metadata')
        
        # Prepare metadata
        metadata = {}
        if metadata_type and metadata_type in DEVICE_METADATA:
            metadata = DEVICE_METADATA[metadata_type].copy()
            # Обновляем временные метки текущим временем
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            metadata['creation_time'] = current_time
            metadata['date'] = current_time
        
        logger.info("Running FFmpeg conversion")
        run_ffmpeg(source_path, target_path, metadata)
        
        if not os.path.exists(target_path):
            raise FileNotFoundError(f"Converted file was not created at {target_path}")
        
        logger.info("Conversion completed successfully")
        
        # Additional metadata for MP4/MOV
        if target_format.upper() in ['MP4', 'MOV'] and metadata_type:
            try:
                logger.info("Adding additional metadata for MP4/MOV")
                video = MP4(target_path)
                
                # Маппинг стандартных метаданных в MP4 теги
                mp4_mapping = {
                    'make': '\xa9mak',
                    'model': '\xa9mod',
                    'software': '\xa9swr',
                    'artist': '\xa9ART',
                    'comment': '\xa9cmt',
                    'encoder': '\xa9enc',
                    'copyright': 'cprt',
                    'album': '\xa9alb',
                    'title': '\xa9nam',
                    'description': 'desc',
                    'composer': '\xa9wrt',
                    'date': '\xa9day',
                    'keywords': 'keyw',
                    'handler_name': 'hndl'
                }
                
                # Добавляем все доступные метаданные
                for key, mp4_key in mp4_mapping.items():
                    if key in metadata:
                        video[mp4_key] = metadata[key]
                
                # Добавляем специфичные для устройства метаданные
                if metadata_type == 'iPhone':
                    video['©too'] = 'Apple Camera'
                    video['©gen'] = 'Original'
                elif metadata_type == 'CapCut':
                    video['©too'] = 'CapCut 9.9.0'
                    video['©gen'] = 'CapCut Export'
                elif metadata_type == 'Android':
                    video['©too'] = 'Samsung Camera'
                    video['©gen'] = 'Original'
                
                video.save()
                logger.info("Additional metadata added successfully")
            except Exception as e:
                logger.error(f"Error adding MP4 metadata: {str(e)}", exc_info=True)
        
        # Read converted file
        logger.info("Reading converted file")
        with open(target_path, 'rb') as f:
            output_bytes = f.read()
        
        # Send converted file
        logger.info("Sending converted file")
        await update.message.reply_document(
            document=output_bytes,
            filename=f"{original_name}.{target_format.lower()}",
            caption=f"Вот ваше видео в формате {target_format.upper()}! ✨"
        )
        
        # Send success message with detailed metadata info
        metadata_info = f"\n📝 Добавлены метаданные: {metadata_type}" if metadata_type else ""
        settings_info = "\n⚙️ Настройки:"
        if metadata_type:
            if metadata_type == 'iPhone':
                settings_info += f"\n• Устройство: {metadata['make']} {metadata['model']}"
                settings_info += f"\n• Версия iOS: {metadata['os_version']}"
                settings_info += f"\n• Кодировщик: {metadata['encoder']}"
            elif metadata_type == 'CapCut':
                settings_info += f"\n• Программа: {metadata['software']}"
                settings_info += f"\n• Версия: 9.9.0"
                settings_info += f"\n• Кодировщик: {metadata['encoder']}"
            elif metadata_type == 'Android':
                settings_info += f"\n• Устройство: {metadata['make']} {metadata['model']}"
                settings_info += f"\n• Версия Android: {metadata['os_version']}"
                settings_info += f"\n• Кодировщик: {metadata['encoder']}"
        
        await update.message.reply_text(
            text=f"{IMAGES['success']} Конвертация завершена успешно!{metadata_info}{settings_info}"
        )
        
        # Clear stored video
        del context.user_data['current_video']
        
    except Exception as e:
        logger.error(f"Error converting video: {str(e)}", exc_info=True)
        error_message = str(e)
        if "FFmpeg" in error_message:
            error_message = "FFmpeg не найден или не может быть использован. Убедитесь, что FFmpeg установлен корректно."
        await update.message.reply_text(
            text=f"{IMAGES['error']} Произошла ошибка при конвертации видео. Подробности: {error_message}"
        )
    finally:
        # Cleanup temporary directory
        if temp_dir and os.path.exists(temp_dir):
            try:
                for file in os.listdir(temp_dir):
                    file_path = os.path.join(temp_dir, file)
                    if os.path.exists(file_path):
                        os.remove(file_path)
                os.rmdir(temp_dir)
                logger.info("Temporary directory cleaned up successfully")
            except Exception as e:
                logger.error(f"Error cleaning up temporary directory: {str(e)}", exc_info=True) 