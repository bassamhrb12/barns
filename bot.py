#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
بوت تيليجرام للتفاعل مع موقع Barns EWC 2025
"""

import logging
import asyncio
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
from barns_automation import BarnsAutomation

# إعداد التسجيل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# حالات المحادثة
PHONE_NUMBER, PASSWORD, PROCESSING = range(3)

class BarnsTelegramBot:
    def __init__(self, token):
        self.token = token
        self.application = Application.builder().token(token).build()
        self.setup_handlers()
    
    def setup_handlers(self):
        """إعداد معالجات الأوامر والرسائل"""
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', self.start)],
            states={
                PHONE_NUMBER: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.get_phone_number)],
                PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.get_password)],
                PROCESSING: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.processing)]
            },
            fallbacks=[CommandHandler('cancel', self.cancel)]
        )
        
        self.application.add_handler(conv_handler)
        self.application.add_handler(CommandHandler('help', self.help_command))
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """بداية المحادثة"""
        user = update.effective_user
        await update.message.reply_html(
            f"مرحباً {user.mention_html()}!\n\n"
            "أنا بوت Barns EWC 2025 🎮\n"
            "سأساعدك في تسجيل الدخول وحل الأسئلة واستلام النقاط تلقائياً.\n\n"
            "يرجى إدخال رقم الجوال (مثال: 0576183980):"
        )
        return PHONE_NUMBER
    
    async def get_phone_number(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """الحصول على رقم الجوال"""
        phone_number = update.message.text.strip()
        
        # التحقق من صحة رقم الجوال
        if not phone_number.startswith('05') or len(phone_number) != 10:
            await update.message.reply_text(
                "❌ رقم الجوال غير صحيح!\n"
                "يرجى إدخال رقم جوال صحيح يبدأ بـ 05 ويتكون من 10 أرقام:"
            )
            return PHONE_NUMBER
        
        context.user_data['phone_number'] = phone_number
        await update.message.reply_text(
            f"✅ تم حفظ رقم الجوال: {phone_number}\n\n"
            "الآن يرجى إدخال كلمة المرور:"
        )
        return PASSWORD
    
    async def get_password(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """الحصول على كلمة المرور"""
        password = update.message.text.strip()
        context.user_data['password'] = password
        
        await update.message.reply_text(
            "✅ تم حفظ كلمة المرور!\n\n"
            "🔄 جاري تسجيل الدخول وحل الأسئلة...\n"
            "يرجى الانتظار..."
        )
        
        # بدء عملية التشغيل التلقائي
        await self.process_automation(update, context)
        return ConversationHandler.END
    
    async def process_automation(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """تشغيل عملية التشغيل التلقائي"""
        try:
            phone_number = context.user_data['phone_number']
            password = context.user_data['password']
            
            # دالة callback لإرسال لقطات الشاشة
            async def send_screenshot(filepath, step_name):
                try:
                    # ترجمة أسماء الخطوات للعربية
                    step_translations = {
                        "01_website_loaded": "🌐 تم تحميل الموقع",
                        "02_arabic_selected": "🇸🇦 تم اختيار اللغة العربية",
                        "03_phone_entered": "📱 تم إدخال رقم الجوال",
                        "04_phone_submitted": "✅ تم إرسال رقم الجوال",
                        "05_password_entered": "🔐 تم إدخال كلمة المرور",
                        "06_login_submitted": "🔑 تم إرسال بيانات الدخول",
                        "07_login_success": "✅ تم تسجيل الدخول بنجاح",
                        "08_game_started": "🎮 تم بدء اللعبة",
                        "error_phone_input": "❌ خطأ في إدخال رقم الجوال",
                        "error_password_input": "❌ خطأ في إدخال كلمة المرور",
                        "error_login_failed": "❌ فشل تسجيل الدخول",
                        "error_attempts_finished": "⏰ انتهت المحاولات لهذا اليوم",
                        "error_game_start_failed": "❌ فشل في بدء اللعبة",
                        "13_points_claimed": "🎉 تم استلام النقاط",
                        "14_no_points_button": "⚠️ لم يتم العثور على زر النقاط"
                    }
                    
                    # إضافة ترجمات للأسئلة
                    for i in range(1, 6):
                        step_translations[f"09_question_{i}_loaded"] = f"❓ السؤال رقم {i}"
                        step_translations[f"10_question_{i}_answered"] = f"✅ تم الإجابة على السؤال {i}"
                        step_translations[f"11_next_question_{i}"] = f"➡️ الانتقال للسؤال التالي"
                        step_translations[f"12_final_question_{i}"] = f"🏁 السؤال الأخير {i}"
                        step_translations[f"error_no_options_question_{i}"] = f"❌ لا توجد خيارات للسؤال {i}"
                        step_translations[f"error_question_{i}"] = f"❌ خطأ في السؤال {i}"
                    
                    caption = step_translations.get(step_name, step_name)
                    
                    with open(filepath, 'rb') as photo:
                        await update.message.reply_photo(
                            photo=photo,
                            caption=caption
                        )
                except Exception as e:
                    logger.error(f"خطأ في إرسال لقطة الشاشة: {e}")
            
            # إنشاء كائن التشغيل التلقائي مع callback
            automation = BarnsAutomation(screenshot_callback=send_screenshot)
            
            # تشغيل العملية
            result = await automation.run_automation(phone_number, password)
            
            if result['success']:
                await update.message.reply_text(
                    f"🎉 تم بنجاح!\n\n"
                    f"📊 النتائج:\n"
                    f"• تم تسجيل الدخول: ✅\n"
                    f"• عدد الأسئلة المحلولة: {result.get('questions_solved', 0)}\n"
                    f"• النقاط المستلمة: {result.get('points_received', 0)}\n"
                    f"• الحالة: {result.get('status', 'مكتمل')}\n\n"
                    "لبدء جلسة جديدة، اكتب /start"
                )
            else:
                await update.message.reply_text(
                    f"❌ حدث خطأ!\n\n"
                    f"السبب: {result.get('error', 'خطأ غير معروف')}\n\n"
                    "يرجى المحاولة مرة أخرى لاحقاً أو التحقق من بيانات الدخول.\n"
                    "لبدء جلسة جديدة، اكتب /start"
                )
        
        except Exception as e:
            logger.error(f"خطأ في التشغيل التلقائي: {e}")
            await update.message.reply_text(
                "❌ حدث خطأ تقني!\n\n"
                "يرجى المحاولة مرة أخرى لاحقاً.\n"
                "لبدء جلسة جديدة، اكتب /start"
            )
    
    async def processing(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """معالجة الرسائل أثناء المعالجة"""
        await update.message.reply_text(
            "⏳ العملية قيد التنفيذ...\n"
            "يرجى الانتظار حتى اكتمال العملية."
        )
        return PROCESSING
    
    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """إلغاء المحادثة"""
        await update.message.reply_text(
            "❌ تم إلغاء العملية.\n"
            "لبدء جلسة جديدة، اكتب /start",
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """عرض المساعدة"""
        help_text = """
🤖 بوت Barns EWC 2025

الأوامر المتاحة:
• /start - بدء جلسة جديدة
• /help - عرض هذه المساعدة
• /cancel - إلغاء العملية الحالية

كيفية الاستخدام:
1. اكتب /start
2. أدخل رقم الجوال (10 أرقام تبدأ بـ 05)
3. أدخل كلمة المرور
4. انتظر حتى اكتمال العملية

سيقوم البوت بـ:
✅ تسجيل الدخول إلى الموقع
✅ حل الأسئلة تلقائياً
✅ استلام النقاط
✅ إرسال تقرير بالنتائج
        """
        await update.message.reply_text(help_text)
    
    def run(self):
        """تشغيل البوت"""
        logger.info("بدء تشغيل البوت...")
        self.application.run_polling()

if __name__ == '__main__':
    # يجب استبدال هذا التوكن بتوكن البوت الحقيقي
    BOT_TOKEN = "937658289:AAFfXxQTtm8E9JuTKDLC7qh0sEV7qNE0Sko"
    
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("❌ يرجى إضافة توكن البوت في المتغير BOT_TOKEN")
        print("يمكنك الحصول على التوكن من @BotFather في تيليجرام")
    else:
        bot = BarnsTelegramBot(BOT_TOKEN)
        bot.run()

