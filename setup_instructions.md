# تعليمات إعداد بوت Barns EWC 2025

## الخطوة 1: إنشاء بوت تيليجرام

### 1.1 فتح تيليجرام
- افتح تطبيق تيليجرام على هاتفك أو الكمبيوتر

### 1.2 البحث عن BotFather
- ابحث عن `@BotFather`
- اضغط على النتيجة الأولى (يجب أن يكون لديه علامة التحقق الزرقاء)

### 1.3 إنشاء البوت
1. اكتب `/start` لبدء المحادثة مع BotFather
2. اكتب `/newbot` لإنشاء بوت جديد
3. أدخل اسم البوت (مثال: Barns EWC Bot)
4. أدخل اسم المستخدم للبوت (يجب أن ينتهي بـ bot، مثال: barns_ewc_bot)
5. احفظ التوكن الذي ستحصل عليه (يبدو مثل: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

## الخطوة 2: تحميل وإعداد الكود

### 2.1 تحميل الملفات
- حمل جميع الملفات إلى مجلد على الكمبيوتر
- تأكد من وجود الملفات التالية:
  - `bot.py`
  - `barns_automation.py`
  - `config.py`
  - `requirements.txt`
  - `run_bot.sh`

### 2.2 تثبيت Python
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3 python3-pip

# Windows
# حمل Python من python.org
```

### 2.3 تثبيت المتطلبات
```bash
pip3 install -r requirements.txt
```

### 2.4 تثبيت Google Chrome
```bash
# Ubuntu/Debian
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list
sudo apt-get update
sudo apt-get install -y google-chrome-stable

# Windows
# حمل Chrome من google.com/chrome
```

## الخطوة 3: إعداد التوكن

### الطريقة الأولى: متغير البيئة
```bash
export BOT_TOKEN="YOUR_BOT_TOKEN_HERE"
```

### الطريقة الثانية: تعديل الكود
1. افتح ملف `bot.py`
2. ابحث عن السطر:
   ```python
   BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
   ```
3. استبدل `YOUR_BOT_TOKEN_HERE` بالتوكن الحقيقي

## الخطوة 4: تشغيل البوت

### الطريقة الأولى: استخدام السكريبت
```bash
./run_bot.sh
```

### الطريقة الثانية: تشغيل مباشر
```bash
python3 bot.py
```

## الخطوة 5: اختبار البوت

1. ابحث عن البوت في تيليجرام باستخدام اسم المستخدم
2. اكتب `/start`
3. اتبع التعليمات لإدخال رقم الجوال وكلمة المرور
4. انتظر النتائج

## استكشاف الأخطاء الشائعة

### خطأ: "ModuleNotFoundError"
```bash
pip3 install -r requirements.txt
```

### خطأ: "Chrome not found"
- تأكد من تثبيت Google Chrome
- في Linux: `sudo apt-get install google-chrome-stable`

### خطأ: "Invalid token"
- تأكد من صحة التوكن
- تأكد من عدم وجود مسافات إضافية

### خطأ: "Permission denied"
```bash
chmod +x run_bot.sh
```

## نصائح مهمة

1. **الأمان**: لا تشارك توكن البوت مع أحد
2. **الخصوصية**: لا تشارك بيانات الدخول
3. **الاستخدام**: استخدم البوت بمسؤولية
4. **التحديثات**: تحقق من التحديثات بانتظام

## الدعم

إذا واجهت أي مشاكل:
1. تأكد من اتباع جميع الخطوات
2. تحقق من رسائل الخطأ
3. راجع ملف `README.md`
4. تواصل مع المطور إذا لزم الأمر

