#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار وحدة التشغيل التلقائي
"""

import asyncio
import sys
from barns_automation import BarnsAutomation

async def test_automation():
    """اختبار الوحدة التلقائية"""
    print("🔄 بدء اختبار وحدة التشغيل التلقائي...")
    
    # بيانات الاختبار
    phone_number = "0576183980"
    password = "ZZXXCCVVbbnnmm@1"
    
    print(f"📱 رقم الجوال: {phone_number}")
    print(f"🔐 كلمة المرور: {password}")
    print()
    
    # إنشاء كائن التشغيل التلقائي
    automation = BarnsAutomation()
    
    try:
        # تشغيل العملية
        result = await automation.run_automation(phone_number, password)
        
        print("📊 النتائج:")
        print(f"• النجاح: {'✅' if result['success'] else '❌'}")
        print(f"• عدد الأسئلة المحلولة: {result.get('questions_solved', 0)}")
        print(f"• النقاط المستلمة: {result.get('points_received', 0)}")
        print(f"• الحالة: {result.get('status', 'غير محدد')}")
        
        if not result['success']:
            print(f"• الخطأ: {result.get('error', 'غير محدد')}")
        
        return result['success']
        
    except Exception as e:
        print(f"❌ خطأ في الاختبار: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_automation())
    sys.exit(0 if success else 1)

