#!/bin/bash

# سكريبت تشغيل بوت Barns EWC 2025

echo "🤖 بدء تشغيل بوت Barns EWC 2025..."

# التحقق من وجود Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 غير مثبت!"
    exit 1
fi

# التحقق من وجود Chrome
if ! command -v google-chrome &> /dev/null; then
    echo "❌ Google Chrome غير مثبت!"
    echo "يرجى تثبيت Chrome أولاً:"
    echo "sudo apt-get install -y google-chrome-stable"
    exit 1
fi

# التحقق من وجود التوكن
if [ -z "$BOT_TOKEN" ]; then
    echo "⚠️  تحذير: متغير BOT_TOKEN غير محدد!"
    echo "يرجى تعيين التوكن:"
    echo "export BOT_TOKEN='YOUR_BOT_TOKEN_HERE'"
    echo ""
    echo "أو تعديل ملف bot.py مباشرة"
fi

# تثبيت المتطلبات إذا لم تكن مثبتة
echo "📦 التحقق من المتطلبات..."
pip3 install -r requirements.txt --quiet

# تشغيل البوت
echo "🚀 تشغيل البوت..."
python3 bot.py

