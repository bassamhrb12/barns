#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
وحدة التشغيل التلقائي لموقع Barns EWC 2025
"""

import asyncio
import time
import logging
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from ai_question_solver import AIQuestionSolver

logger = logging.getLogger(__name__)

class BarnsAutomation:
    def __init__(self, screenshot_callback=None):
        self.driver = None
        self.wait = None
        self.base_url = "http://barnsewc25.com"
        self.screenshot_callback = screenshot_callback
        self.screenshots_dir = "/tmp/barns_screenshots"
        self.ai_solver = AIQuestionSolver()
        self.setup_screenshots_dir()
    
    def setup_screenshots_dir(self):
        """إنشاء مجلد لحفظ لقطات الشاشة"""
        if not os.path.exists(self.screenshots_dir):
            os.makedirs(self.screenshots_dir)
    
    async def take_screenshot(self, step_name):
        """التقاط لقطة شاشة وإرسالها للبوت"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{step_name}_{timestamp}.png"
            filepath = os.path.join(self.screenshots_dir, filename)
            
            # التقاط لقطة الشاشة
            self.driver.save_screenshot(filepath)
            logger.info(f"تم التقاط لقطة شاشة: {filename}")
            
            # إرسال لقطة الشاشة للبوت إذا كان هناك callback
            if self.screenshot_callback:
                await self.screenshot_callback(filepath, step_name)
            
            return filepath
            
        except Exception as e:
            logger.error(f"خطأ في التقاط لقطة الشاشة: {e}")
            return None
    
    def setup_driver(self):
        """إعداد متصفح Chrome"""
        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless")  # تشغيل بدون واجهة
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
            
            # تثبيت ChromeDriver تلقائياً
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.wait = WebDriverWait(self.driver, 10)
            
            logger.info("تم إعداد المتصفح بنجاح")
            return True
            
        except Exception as e:
            logger.error(f"خطأ في إعداد المتصفح: {e}")
            return False
    
    def close_driver(self):
        """إغلاق المتصفح"""
        if self.driver:
            self.driver.quit()
            logger.info("تم إغلاق المتصفح")
    
    async def run_automation(self, phone_number, password):
        """تشغيل العملية التلقائية الكاملة"""
        result = {
            'success': False,
            'error': None,
            'questions_solved': 0,
            'points_received': 0,
            'status': 'فشل'
        }
        
        try:
            # إعداد المتصفح
            if not self.setup_driver():
                result['error'] = "فشل في إعداد المتصفح"
                return result
            
            # تسجيل الدخول
            login_result = await self.login(phone_number, password)
            if not login_result['success']:
                result['error'] = login_result['error']
                return result
            
            # بدء اللعبة وحل الأسئلة
            game_result = await self.play_game()
            if game_result['success']:
                result['success'] = True
                result['questions_solved'] = game_result['questions_solved']
                result['points_received'] = game_result['points_received']
                result['status'] = 'مكتمل'
            else:
                result['error'] = game_result['error']
            
            return result
            
        except Exception as e:
            logger.error(f"خطأ في العملية التلقائية: {e}")
            result['error'] = f"خطأ تقني: {str(e)}"
            return result
        
        finally:
            self.close_driver()
    
    async def login(self, phone_number, password):
        """تسجيل الدخول إلى الموقع"""
        result = {'success': False, 'error': None}
        
        try:
            logger.info("بدء عملية تسجيل الدخول")
            
            # الذهاب إلى الموقع
            self.driver.get(self.base_url)
            await asyncio.sleep(2)
            await self.take_screenshot("01_website_loaded")
            
            # اختيار اللغة العربية
            try:
                arabic_btn = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'عربي')]"))
                )
                arabic_btn.click()
                await asyncio.sleep(2)
                await self.take_screenshot("02_arabic_selected")
                logger.info("تم اختيار اللغة العربية")
            except TimeoutException:
                logger.warning("لم يتم العثور على زر اللغة العربية")
            
            # إدخال رقم الجوال
            try:
                phone_input = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, "//input[@placeholder='05XXXXXXXX']"))
                )
                phone_input.clear()
                phone_input.send_keys(phone_number)
                logger.info(f"تم إدخال رقم الجوال: {phone_number}")
                await self.take_screenshot("03_phone_entered")
                
                # الضغط على التالي
                next_btn = self.driver.find_element(By.XPATH, "//input[@type='submit' or @type='button'][last()]")
                next_btn.click()
                await asyncio.sleep(2)
                await self.take_screenshot("04_phone_submitted")
                
            except (TimeoutException, NoSuchElementException) as e:
                result['error'] = "فشل في إدخال رقم الجوال"
                logger.error(f"خطأ في إدخال رقم الجوال: {e}")
                await self.take_screenshot("error_phone_input")
                return result
            
            # إدخال كلمة المرور
            try:
                password_input = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, "//input[@placeholder='كلمة المرور']"))
                )
                password_input.clear()
                password_input.send_keys(password)
                logger.info("تم إدخال كلمة المرور")
                await self.take_screenshot("05_password_entered")
                
                # الضغط على تسجيل الدخول
                login_btn = self.driver.find_element(By.XPATH, "//input[@type='submit' or @type='button'][last()]")
                login_btn.click()
                await asyncio.sleep(3)
                await self.take_screenshot("06_login_submitted")
                
            except (TimeoutException, NoSuchElementException) as e:
                result['error'] = "فشل في إدخال كلمة المرور"
                logger.error(f"خطأ في إدخال كلمة المرور: {e}")
                await self.take_screenshot("error_password_input")
                return result
            
            # التحقق من نجاح تسجيل الدخول
            try:
                start_game_btn = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'ابدأ اللعبة')]"))
                )
                result['success'] = True
                logger.info("تم تسجيل الدخول بنجاح")
                await self.take_screenshot("07_login_success")
                
            except TimeoutException:
                # التحقق من رسائل الخطأ
                try:
                    error_msg = self.driver.find_element(By.XPATH, "//*[contains(text(), 'خطأ') or contains(text(), 'غير صحيح')]")
                    result['error'] = "بيانات الدخول غير صحيحة"
                except NoSuchElementException:
                    result['error'] = "فشل في تسجيل الدخول - سبب غير معروف"
                
                logger.error(f"فشل تسجيل الدخول: {result['error']}")
                await self.take_screenshot("error_login_failed")
            
            return result
            
        except Exception as e:
            result['error'] = f"خطأ في تسجيل الدخول: {str(e)}"
            logger.error(f"خطأ في تسجيل الدخول: {e}")
            return result
    
    async def play_game(self):
        """بدء اللعبة وحل الأسئلة"""
        result = {
            'success': False,
            'error': None,
            'questions_solved': 0,
            'points_received': 0
        }
        
        try:
            logger.info("بدء اللعبة")
            
            # الضغط على "ابدأ اللعبة"
            try:
                start_btn = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'ابدأ اللعبة')]"))
                )
                start_btn.click()
                await asyncio.sleep(3)
                await self.take_screenshot("08_game_started")
                logger.info("تم بدء اللعبة")
                
            except TimeoutException:
                # التحقق من انتهاء المحاولات
                try:
                    end_msg = self.driver.find_element(By.XPATH, "//*[contains(text(), 'انتهت') or contains(text(), 'غدا')]")
                    result['error'] = "انتهت المحاولات لهذا اليوم"
                    logger.info("انتهت المحاولات لهذا اليوم")
                    await self.take_screenshot("error_attempts_finished")
                    return result
                except NoSuchElementException:
                    result['error'] = "فشل في بدء اللعبة"
                    await self.take_screenshot("error_game_start_failed")
                    return result
            
            # حل الأسئلة
            questions_count = 0
            max_questions = 5  # عدد الأسئلة المتوقع
            
            for question_num in range(1, max_questions + 1):
                try:
                    logger.info(f"حل السؤال رقم {question_num}")
                    
                    # انتظار ظهور السؤال
                    await asyncio.sleep(2)
                    await self.take_screenshot(f"09_question_{question_num}_loaded")
                    
                    # الحصول على نص الصفحة
                    page_text = self.driver.page_source
                    
                    # البحث عن خيارات الإجابة
                    answer_buttons = self.driver.find_elements(By.XPATH, "//button[contains(@class, 'answer') or contains(text(), 'قراند') or contains(text(), 'فورتنايت') or contains(text(), 'تيكن') or contains(text(), 'زيلدا')]")
                    
                    if not answer_buttons:
                        # البحث عن أي أزرار قد تكون إجابات
                        answer_buttons = self.driver.find_elements(By.XPATH, "//button[not(contains(text(), 'التالي')) and not(contains(text(), 'السابق'))]")
                    
                    if answer_buttons:
                        # استخراج نصوص الأزرار
                        button_texts = [btn.text.strip() for btn in answer_buttons if btn.text.strip()]
                        
                        # استخدام الذكاء الاصطناعي لحل السؤال
                        ai_result = self.ai_solver.solve_question_from_page(page_text, button_texts)
                        
                        if ai_result['success']:
                            # اختيار الإجابة المقترحة من الذكاء الاصطناعي
                            selected_index = ai_result['answer_index']
                            selected_index = min(selected_index, len(answer_buttons) - 1)
                            
                            logger.info(f"الذكاء الاصطناعي اختار الخيار {selected_index + 1}: {button_texts[selected_index] if selected_index < len(button_texts) else 'غير محدد'}")
                            logger.info(f"التفسير: {ai_result['reasoning']}")
                            logger.info(f"مستوى الثقة: {ai_result['confidence']:.2f}")
                            
                            answer_buttons[selected_index].click()
                        else:
                            # في حالة فشل الذكاء الاصطناعي، اختر الإجابة الأولى
                            logger.warning(f"فشل الذكاء الاصطناعي: {ai_result['reasoning']}")
                            answer_buttons[0].click()
                        
                        questions_count += 1
                        logger.info(f"تم الإجابة على السؤال {question_num}")
                        await asyncio.sleep(2)
                        await self.take_screenshot(f"10_question_{question_num}_answered")
                        
                        # البحث عن زر "السؤال التالي" أو "التالي"
                        try:
                            next_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'التالي') or contains(text(), 'السؤال التالي')]")
                            next_btn.click()
                            await asyncio.sleep(2)
                            await self.take_screenshot(f"11_next_question_{question_num}")
                        except NoSuchElementException:
                            # قد نكون في السؤال الأخير
                            await self.take_screenshot(f"12_final_question_{question_num}")
                            break
                    else:
                        logger.warning(f"لم يتم العثور على خيارات للسؤال {question_num}")
                        await self.take_screenshot(f"error_no_options_question_{question_num}")
                        break
                        
                except Exception as e:
                    logger.error(f"خطأ في السؤال {question_num}: {e}")
                    await self.take_screenshot(f"error_question_{question_num}")
                    break
            
            # محاولة استلام النقاط
            try:
                # البحث عن زر استلام النقاط
                claim_buttons = self.driver.find_elements(By.XPATH, "//button[contains(text(), 'استلام') or contains(text(), '500') or contains(text(), 'نقطة')]")
                
                if claim_buttons:
                    claim_buttons[0].click()
                    result['points_received'] = 500
                    logger.info("تم استلام النقاط")
                    await asyncio.sleep(2)
                    await self.take_screenshot("13_points_claimed")
                else:
                    await self.take_screenshot("14_no_points_button")
                
            except Exception as e:
                logger.warning(f"لم يتم استلام النقاط: {e}")
                await self.take_screenshot("error_points_claim")
            
            result['success'] = True
            result['questions_solved'] = questions_count
            logger.info(f"تم حل {questions_count} أسئلة")
            
            return result
            
        except Exception as e:
            result['error'] = f"خطأ في اللعبة: {str(e)}"
            logger.error(f"خطأ في اللعبة: {e}")
            return result

# دالة مساعدة للاختبار
async def test_automation():
    """اختبار الوحدة"""
    automation = BarnsAutomation()
    result = await automation.run_automation("0576183980", "ZZXXCCVVbbnnmm@1")
    print(f"النتيجة: {result}")

if __name__ == "__main__":
    asyncio.run(test_automation())

