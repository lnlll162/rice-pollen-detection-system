@echo off
chcp 65001
echo 花粉识别系统部署脚本
echo ============================

:: 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到Python，请先安装Python 3.8或更高版本
    echo 您可以从 https://www.python.org/downloads/ 下载安装
    pause
    exit /b
)

:: 创建虚拟环境
echo [步骤1] 创建虚拟环境...
python -m venv venv
if %errorlevel% neq 0 (
    echo [错误] 创建虚拟环境失败
    pause
    exit /b
)

:: 激活虚拟环境
echo [步骤2] 激活虚拟环境...
call venv\Scripts\activate.bat

:: 升级pip
echo [步骤3] 升级pip...
python -m pip install --upgrade pip

:: 安装依赖
echo [步骤4] 安装必要的包...
:: 首先安装Streamlit（它会安装正确版本的Pillow）
pip install streamlit==1.28.0

:: 然后安装其他包
pip install numpy==1.26.4
pip install PyYAML==6.0.1
pip install torch==2.6.0 torchvision==0.21.0 --index-url https://download.pytorch.org/whl/cu118
pip install opencv-python==4.11.0.86
pip install ultralytics==8.3.104
pip install plotly==5.18.0
pip install pandas==2.2.0

:: 检查模型文件
echo [步骤5] 检查模型文件...
if not exist "runs\train7\weights\best.pt" (
    echo [警告] 未找到模型文件，请确保模型文件位于正确位置：
    echo runs\train7\weights\best.pt
    pause
)

:: 运行应用
echo [步骤6] 启动应用...
streamlit run app_streamlit.py

:: 如果程序异常退出，暂停显示错误信息
if %errorlevel% neq 0 (
    echo [错误] 程序运行出错，请检查错误信息
    pause
)

:: 退出虚拟环境
deactivate 