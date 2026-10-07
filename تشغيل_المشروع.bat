@echo off
chcp 65001 >nul
title تشغيل مشروع التنقيب عن البيانات - Data Mining Project

echo.
echo ============================================================
echo    مرحباً بك في مشروع التنقيب عن بيانات مطاعم Yelp
echo ============================================================
echo.

cd /d "%~dp0"

echo [1/4] جارٍ التحقق من تثبيت Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ لم يتم العثور على Python!
    echo    قم بتنزيل Python من https://www.python.org/downloads/
    echo    وتأكد من تحديد "Add Python to PATH" أثناء التثبيت
    pause
    exit /b 1
)
echo ✅ Python موجود

echo.
echo [2/4] جارٍ تثبيت المكتبات المطلوبة (إن لزم الأمر)...
python -m pip install --quiet -r requirements.txt
if errorlevel 1 (
    echo ⚠️  تحذير: فشل تثبيت بعض المكتبات، سيتم المحاولة بالرغم من ذلك
)
echo ✅ تمت مراجعة المكتبات

echo.
echo [3/4] جارٍ التحقق من إعدادات المشروع...
python run_step.py verify
set EXITCODE=%ERRORLEVEL%

echo.
echo [4/4] جارٍ تشغيل Jupyter Notebook...
echo.
echo   سيتم فتح المتصفح تلقائياً خلال ثوانٍ...
echo   اختر الملف: Demo_Quick_Start.ipynb للتجربة السريعة
echo   أو اختر أي دفتر من مجلدات step1 إلى step5
echo.
pause

start "" python -m notebook --notebook-dir="%~dp0"
exit /b 0
