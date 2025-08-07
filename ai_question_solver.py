#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
وحدة الذكاء الاصطناعي لحل الأسئلة
"""

import openai
import logging
import os
import re
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

class AIQuestionSolver:
    def __init__(self):
        """تهيئة حلال الأسئلة بالذكاء الاصطناعي"""
        self.client = openai.OpenAI(
            api_key=os.getenv('OPENAI_API_KEY'),
            base_url=os.getenv('OPENAI_API_BASE')
        )
        
    def extract_question_and_options(self, page_text: str) -> Dict[str, any]:
        """استخراج السؤال والخيارات من نص الصفحة"""
        try:
            # تنظيف النص
            cleaned_text = re.sub(r'\s+', ' ', page_text).strip()
            
            # البحث عن أنماط الأسئلة الشائعة
            question_patterns = [
                r'ما هو.*?\?',
                r'من هو.*?\?',
                r'أي من.*?\?',
                r'كم.*?\?',
                r'متى.*?\?',
                r'أين.*?\?',
                r'لماذا.*?\?',
                r'كيف.*?\?',
                r'هل.*?\?',
                r'ماذا.*?\?'
            ]
            
            question = None
            for pattern in question_patterns:
                match = re.search(pattern, cleaned_text, re.IGNORECASE)
                if match:
                    question = match.group(0)
                    break
            
            # إذا لم نجد سؤال، نأخذ أول جملة تنتهي بعلامة استفهام
            if not question:
                question_match = re.search(r'[^.!]*\?', cleaned_text)
                if question_match:
                    question = question_match.group(0).strip()
            
            # استخراج الخيارات (البحث عن أزرار أو قوائم)
            options = []
            
            # البحث عن خيارات مرقمة أو مرتبة
            option_patterns = [
                r'[أ-ي]\)\s*([^)]+)',
                r'[1-9]\)\s*([^)]+)',
                r'[A-Z]\)\s*([^)]+)',
                r'•\s*([^•]+)',
                r'-\s*([^-]+)'
            ]
            
            for pattern in option_patterns:
                matches = re.findall(pattern, cleaned_text)
                if matches:
                    options.extend([opt.strip() for opt in matches])
                    break
            
            return {
                'question': question,
                'options': options,
                'raw_text': cleaned_text
            }
            
        except Exception as e:
            logger.error(f"خطأ في استخراج السؤال والخيارات: {e}")
            return {
                'question': None,
                'options': [],
                'raw_text': page_text
            }
    
    def solve_question(self, question: str, options: List[str]) -> Dict[str, any]:
        """حل السؤال باستخدام الذكاء الاصطناعي"""
        try:
            if not question or not options:
                return {
                    'success': False,
                    'answer_index': 0,
                    'confidence': 0.0,
                    'reasoning': 'لم يتم العثور على سؤال أو خيارات واضحة'
                }
            
            # إعداد الرسالة للذكاء الاصطناعي
            prompt = f"""
أنت خبير في الإجابة على الأسئلة العامة والثقافية. يرجى الإجابة على السؤال التالي:

السؤال: {question}

الخيارات:
"""
            
            for i, option in enumerate(options):
                prompt += f"{i+1}. {option}\n"
            
            prompt += """
يرجى تحديد الإجابة الصحيحة وتقديم تفسير مختصر. أجب بالتنسيق التالي:
الإجابة: [رقم الخيار]
التفسير: [تفسير مختصر]
الثقة: [نسبة من 0 إلى 1]
"""
            
            # استدعاء الذكاء الاصطناعي
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "أنت مساعد ذكي متخصص في الإجابة على الأسئلة العامة والثقافية باللغة العربية."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.1
            )
            
            ai_response = response.choices[0].message.content
            
            # استخراج الإجابة من رد الذكاء الاصطناعي
            answer_match = re.search(r'الإجابة:\s*(\d+)', ai_response)
            reasoning_match = re.search(r'التفسير:\s*([^\n]+)', ai_response)
            confidence_match = re.search(r'الثقة:\s*([\d.]+)', ai_response)
            
            answer_index = 0
            if answer_match:
                answer_index = max(0, int(answer_match.group(1)) - 1)
                answer_index = min(answer_index, len(options) - 1)
            
            confidence = 0.7
            if confidence_match:
                confidence = float(confidence_match.group(1))
            
            reasoning = "تم تحديد الإجابة بناءً على المعرفة العامة"
            if reasoning_match:
                reasoning = reasoning_match.group(1).strip()
            
            return {
                'success': True,
                'answer_index': answer_index,
                'confidence': confidence,
                'reasoning': reasoning,
                'ai_response': ai_response
            }
            
        except Exception as e:
            logger.error(f"خطأ في حل السؤال: {e}")
            return {
                'success': False,
                'answer_index': 0,
                'confidence': 0.0,
                'reasoning': f'خطأ تقني: {str(e)}'
            }
    
    def solve_question_from_page(self, page_text: str, button_texts: List[str] = None) -> Dict[str, any]:
        """حل السؤال من نص الصفحة مباشرة"""
        try:
            # استخراج السؤال والخيارات
            extracted = self.extract_question_and_options(page_text)
            
            # إذا لم نجد خيارات في النص، استخدم نصوص الأزرار
            if not extracted['options'] and button_texts:
                extracted['options'] = button_texts
            
            # حل السؤال
            if extracted['question'] and extracted['options']:
                result = self.solve_question(extracted['question'], extracted['options'])
                result['extracted_question'] = extracted['question']
                result['extracted_options'] = extracted['options']
                return result
            else:
                # إذا لم نجد سؤال واضح، نحاول التخمين الذكي
                return self.smart_guess(page_text, button_texts)
                
        except Exception as e:
            logger.error(f"خطأ في حل السؤال من الصفحة: {e}")
            return {
                'success': False,
                'answer_index': 0,
                'confidence': 0.0,
                'reasoning': f'خطأ في المعالجة: {str(e)}'
            }
    
    def smart_guess(self, page_text: str, button_texts: List[str] = None) -> Dict[str, any]:
        """تخمين ذكي عندما لا يمكن استخراج السؤال بوضوح"""
        try:
            if not button_texts:
                return {
                    'success': False,
                    'answer_index': 0,
                    'confidence': 0.0,
                    'reasoning': 'لا توجد خيارات متاحة للتخمين'
                }
            
            # استخدام الذكاء الاصطناعي للتخمين بناءً على السياق
            prompt = f"""
بناءً على النص التالي والخيارات المتاحة، ما هو الخيار الأكثر منطقية؟

النص: {page_text}

الخيارات:
"""
            
            for i, option in enumerate(button_texts):
                prompt += f"{i+1}. {option}\n"
            
            prompt += """
يرجى اختيار الخيار الأفضل وتقديم تفسير.
الإجابة: [رقم الخيار]
التفسير: [تفسير مختصر]
"""
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "أنت مساعد ذكي يساعد في اتخاذ قرارات منطقية بناءً على السياق."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.3
            )
            
            ai_response = response.choices[0].message.content
            
            # استخراج الإجابة
            answer_match = re.search(r'الإجابة:\s*(\d+)', ai_response)
            reasoning_match = re.search(r'التفسير:\s*([^\n]+)', ai_response)
            
            answer_index = 0
            if answer_match:
                answer_index = max(0, int(answer_match.group(1)) - 1)
                answer_index = min(answer_index, len(button_texts) - 1)
            
            reasoning = "تخمين ذكي بناءً على السياق"
            if reasoning_match:
                reasoning = reasoning_match.group(1).strip()
            
            return {
                'success': True,
                'answer_index': answer_index,
                'confidence': 0.5,  # ثقة متوسطة للتخمين
                'reasoning': reasoning,
                'ai_response': ai_response
            }
            
        except Exception as e:
            logger.error(f"خطأ في التخمين الذكي: {e}")
            return {
                'success': False,
                'answer_index': 0,
                'confidence': 0.0,
                'reasoning': f'خطأ في التخمين: {str(e)}'
            }

