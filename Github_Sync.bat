@echo off
SETLOCAL EnableDelayedExpansion

echo ========================================
echo   🚀 GitHub Auto Sync Started...
echo ========================================

:: 获取当前日期时间作为默认提交信息
set timestamp=%date% %time%
set commit_msg=Update: !timestamp!

:: 检查是否有传入参数作为提交信息
if not "%~1"=="" (
    set commit_msg=%~1
)

echo.
echo [1/3] Adding changes...
git add .

echo.
echo [2/3] Committing with message: "!commit_msg!"
git commit -m "!commit_msg!"

echo.
echo [3/3] Pushing to GitHub (main branch)...
git push origin main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo   ✨ Sync Successful!
    echo ========================================
) else (
    echo.
    echo ❌ Error occurred during sync. Check your internet or login status.
)

pause
