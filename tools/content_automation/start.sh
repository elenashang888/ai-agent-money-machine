#!/bin/bash
# 启动AI内容自动化系统

echo "🚀 启动AI内容自动化系统..."

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到Python3，请先安装"
    exit 1
fi

# 检查API Key
if [ -z "$BAILIAN_API_KEY" ]; then
    echo "⚠️ 警告：未设置BAILIAN_API_KEY环境变量"
    echo "请运行：export BAILIAN_API_KEY=your_api_key"
    echo "或编辑 .env 文件"
fi

# 创建虚拟环境（如果不存在）
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
echo "📥 安装依赖..."
pip install -q requests

# 创建输出目录
mkdir -p output
mkdir -p logs

# 启动系统
echo "✅ 系统启动完成！"
echo ""
echo "使用方法："
echo "  python3 content_generator.py"
echo ""
echo "或运行交互式版本："
echo "  python3 -c \"from content_generator import ContentPipeline; p = ContentPipeline(); p.create_content('AI赚钱', 'wechat')\""
echo ""

# 保持虚拟环境激活
exec bash
