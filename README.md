# 🚀 Universal File Converter Bot

A versatile Telegram bot for converting files between different formats. A simple and convenient tool for quick conversion of documents, images, and videos.

![Python Version](https://img.shields.io/badge/Python-3.9+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

### 📄 Documents
- **DOCX → PDF** - Convert Word documents to PDF
- **DOCX → PPTX** - Transform documents into PowerPoint presentations
- **PDF → DOCX** - Convert PDF to editable Word format
- **TXT → DOCX/PDF** - Convert text files to other formats

### 🎥 Video
- Support for popular formats (MP4, AVI, MOV, MKV)
- Device metadata injection:
  - iPhone (iOS 17.4)
  - Android (Samsung Galaxy S24 Ultra)
  - CapCut (version 9.9.0)

### 🖼 Images
- Convert between JPEG, PNG, WebP formats
- Preserve image quality
- EXIF metadata support

## 🛠 Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/file-converter-bot.git
cd file-converter-bot
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install FFmpeg:
- **Windows**: 
  ```bash
  # Using Chocolatey
  choco install ffmpeg
  
  # Or download manually from https://ffmpeg.org/download.html
  # and add to PATH
  ```
- **Linux**:
  ```bash
  sudo apt update
  sudo apt install ffmpeg
  ```
- **macOS**:
  ```bash
  brew install ffmpeg
  ```

5. Create a `.env` file and add your bot token:
```env
TOKEN=your_telegram_bot_token
```

## 🚀 Quick Start

```bash
python main.py
```

## 💡 Usage

1. Start chat with bot: `/start`
2. Send a file for conversion
3. Choose desired format
4. Get your converted file!

### 📋 Commands
- `/start` - Start working with the bot
- `/help` - Show help information
- `/formats` - List supported formats
- `/settings` - Conversion settings

## 🔧 Technical Details

### Used Libraries
- `python-telegram-bot` - Main framework for Telegram bot
- `python-docx` - Working with DOCX documents
- `python-pptx` - Creating presentations
- `PyPDF2` - PDF file operations
- `ffmpeg-python` - Video conversion
- `Pillow` - Image processing

### System Requirements
- Python 3.9 or higher
- FFmpeg
- 512MB RAM minimum
- 1GB free disk space

## 🤝 Contributing

We welcome contributions to the project! Here's how:

1. Fork the repository
2. Create a branch for your changes
3. Make changes and create a pull request

## 📝 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 📞 Support

If you have questions or issues:
- Create an Issue in the repository
- Contact the developer via Telegram

## ⭐ Star History

If you find this project helpful, give it a star! It helps others discover this project.

## 🔍 Key Features

- 🔄 Easy file format conversion
- 📱 Device-specific metadata support
- 🎨 High-quality image processing
- 📊 PowerPoint presentation generation
- 🎥 Advanced video conversion
- 💾 Efficient file handling
- 🔒 Secure file processing
- 🚀 Fast conversion speed

## 🛡 Security

- All file processing is done locally
- No data is stored permanently
- Secure file handling
- Privacy-focused design

## 🌟 Why Choose This Bot?

- **Easy to Use**: Simple interface for quick file conversion
- **Versatile**: Supports multiple file formats
- **Reliable**: Stable and tested conversion process
- **Free**: Open source and free to use
- **Secure**: Local processing, no data storage
- **Fast**: Efficient conversion algorithms
- **Customizable**: Various conversion options
- **Well-Maintained**: Regular updates and support
