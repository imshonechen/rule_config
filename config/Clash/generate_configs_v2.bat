@echo off
chcp 65001
setlocal enabledelayedexpansion

:: 设置脚本路径（确保脚本和 .bat 在同一目录下）
set script_name=generate_configs_v2.py

:: 检查 Python 是否可用
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 没有检测到 Python，请先安装 Python 并配置环境变量。
    pause
    exit /b
)

:: 执行 Python 脚本
echo 正在执行 Python 脚本...
python "%~dp0%script_name%"

echo.
echo 执行完毕，按任意键关闭窗口。
pause
