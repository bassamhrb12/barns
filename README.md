# بوت Barns EWC 2025 التيليجرام

بوت تيليجرام يقوم بتسجيل الدخول إلى موقع Barns EWC 2025 وحل الأسئلة واستلام النقاط تلقائياً.

## المميزات

- ✅ تسجيل الدخول التلقائي إلى الموقع
- ✅ حل الأسئلة تلقائياً
- ✅ استلام النقاط
- ✅ واجهة تيليجرام سهلة الاستخدام
- ✅ تقارير مفصلة عن النتائج

## المتطلبات

- Python 3.8+
- Google Chrome
- توكن بوت تيليجرام

## التثبيت

### 1. تحميل الملفات

```bash
git clone <repository-url>
cd barns_telegram_bot
```

### 2. تثبيت المتطلبات

```bash
pip3 install -r requirements.txt
```

### 3. تثبيت Google Chrome

```bash
# Ubuntu/Debian
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list
sudo apt-get update
sudo apt-get install -y google-chrome-stable
```

### 4. إنشاء بوت تيليجرام

1. ابحث عن `@BotFather` في تيليجرام
2. أرسل `/newbot`
3. اتبع التعليمات لإنشاء البوت
4. احفظ التوكن الذي ستحصل عليه

### 5. إعداد التوكن

```bash
export BOT_TOKEN="YOUR_BOT_TOKEN_HERE"
```

أو قم بتعديل ملف `bot.py` وضع التوكن مباشرة:

```python
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
```

## التشغيل

### تشغيل البوت

```bash
python3 bot.py
```

### اختبار الوحدة التلقائية

```bash
python3 test_automation.py
```

## كيفية الاستخدام

1. ابحث عن البوت في تيليجرام
2. اكتب `/start`
3. أدخل رقم الجوال (10 أرقام تبدأ بـ 05)
4. أدخل كلمة المرور
5. انتظر حتى اكتمال العملية

## الأوامر المتاحة

- `/start` - بدء جلسة جديدة
- `/help` - عرض المساعدة
- `/cancel` - إلغاء العملية الحالية

## هيكل المشروع

```
barns_telegram_bot/
├── bot.py                 # الملف الرئيسي للبوت
├── barns_automation.py    # وحدة التشغيل التلقائي
├── config.py             # ملف الإعدادات
├── test_automation.py    # اختبار الوحدة
├── requirements.txt      # المتطلبات
└── README.md            # دليل الاستخدام
```

## استكشاف الأخطاء

### خطأ في تسجيل الدخول
- تأكد من صحة رقم الجوال وكلمة المرور
- تأكد من أن الحساب لم يتم حظره

### خطأ في المتصفح
- تأكد من تثبيت Google Chrome
- تأكد من وجود اتصال بالإنترنت

### خطأ في البوت
- تأكد من صحة توكن البوت
- تأكد من أن البوت مفعل

## الأمان

- لا تشارك توكن البوت مع أحد
- لا تشارك بيانات الدخول
- استخدم البوت على مسؤوليتك الشخصية

## الدعم

للحصول على الدعم أو الإبلاغ عن مشاكل، يرجى التواصل مع المطور.

## الترخيص

هذا المشروع للاستخدام التعليمي فقط.

