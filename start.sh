#!/bin/bash
# AI Agent Money Machine - 一键启动脚本
# 自动配置并启动6个Agent赚钱系统

echo "🚀 AI Agent Money Machine - 一键启动"
echo "=========================================="
echo ""

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 检查目录
cd ~/ai-agent-money-machine || exit 1

echo "📁 工作目录: $(pwd)"
echo ""

# 步骤1: 检查Python
echo "🔍 步骤1: 检查Python环境..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    echo -e "${GREEN}✅ Python已安装: $PYTHON_VERSION${NC}"
else
    echo -e "${RED}❌ Python3未安装${NC}"
    exit 1
fi

# 步骤2: 检查依赖
echo ""
echo "🔍 步骤2: 检查依赖..."
python3 -c "import requests" 2>/dev/null
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ requests库已安装${NC}"
else
    echo "📦 安装requests库..."
    pip3 install requests -q
    echo -e "${GREEN}✅ requests库安装完成${NC}"
fi

# 步骤3: 检查API Key
echo ""
echo "🔍 步骤3: 检查百炼API配置..."

if [ -f ".env" ]; then
    source .env
fi

if [ -n "$BAILIAN_API_KEY" ]; then
    echo -e "${GREEN}✅ 百炼API Key已配置${NC}"
    echo "   Key前缀: ${BAILIAN_API_KEY:0:10}..."
    API_CONFIGURED=true
else
    echo -e "${YELLOW}⚠️  百炼API Key未配置${NC}"
    echo "   系统将运行模拟模式"
    echo ""
    echo "   如需配置真实AI，请："
    echo "   1. 访问 https://dashscope.aliyun.com/"
    echo "   2. 获取API Key"
    echo "   3. 运行: echo 'BAILIAN_API_KEY=your_key' > .env"
    API_CONFIGURED=false
fi

# 步骤4: 检查Agent文件
echo ""
echo "🔍 步骤4: 检查Agent文件..."

AGENT_FILES=(
    "bailian_config.py"
    "real_money_system.py"
    "money_making_system.py"
    "api_server.py"
)

ALL_FILES_EXIST=true
for file in "${AGENT_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✅ $file${NC}"
    else
        echo -e "${RED}❌ $file 不存在${NC}"
        ALL_FILES_EXIST=false
    fi
done

if [ "$ALL_FILES_EXIST" = false ]; then
    echo -e "${RED}❌ 部分文件缺失，请重新克隆项目${NC}"
    exit 1
fi

# 步骤5: 启动选择
echo ""
echo "=========================================="
echo "🎯 选择启动模式"
echo "=========================================="
echo ""
echo "1) 🚀 快速体验 - 运行一轮演示"
echo "2) 🤖 真实AI模式 - 使用百炼API（需配置Key）"
echo "3) 🌐 启动API服务器 - 提供HTTP接口"
echo "4) 📊 生成营销材料 - 创建销售页面"
echo "5) ⚙️  配置百炼API"
echo "6) ❌ 退出"
echo ""

read -p "请选择 (1-6): " choice

case $choice in
    1)
        echo ""
        echo "🚀 启动快速体验模式..."
        echo "=========================================="
        python3 real_money_system.py
        ;;
    
    2)
        if [ "$API_CONFIGURED" = false ]; then
            echo ""
            echo -e "${RED}❌ 百炼API未配置${NC}"
            echo "请先选择选项5配置API"
            exit 1
        fi
        echo ""
        echo "🤖 启动真实AI模式..."
        echo "=========================================="
        python3 real_money_system.py
        ;;
    
    3)
        echo ""
        echo "🌐 启动API服务器..."
        echo "=========================================="
        echo "API地址: http://localhost:5000"
        echo "文档: http://localhost:5000/docs"
        echo ""
        echo "按 Ctrl+C 停止服务器"
        echo "=========================================="
        python3 api_server.py
        ;;
    
    4)
        echo ""
        echo "📊 生成营销材料..."
        echo "=========================================="
        python3 create_sales_page.py
        echo ""
        echo "生成的文件："
        ls -lh sales_page.html gumroad_description.md promo_tweets.txt 2>/dev/null
        ;;
    
    5)
        echo ""
        echo "⚙️  配置百炼API"
        echo "=========================================="
        echo ""
        echo "请访问: https://dashscope.aliyun.com/"
        echo "1. 登录阿里云账号"
        echo "2. 进入 API-KEY 管理"
        echo "3. 创建新的API Key"
        echo ""
        read -p "请输入API Key (sk-...): " api_key
        
        if [ -n "$api_key" ]; then
            echo "BAILIAN_API_KEY=$api_key" > .env
            echo -e "${GREEN}✅ API Key已保存到 .env${NC}"
            echo ""
            echo "现在可以运行真实AI模式了！"
        else
            echo -e "${RED}❌ API Key不能为空${NC}"
        fi
        ;;
    
    6)
        echo ""
        echo "👋 再见！"
        exit 0
        ;;
    
    *)
        echo -e "${RED}❌ 无效选择${NC}"
        exit 1
        ;;
esac

echo ""
echo "=========================================="
echo "✅ 操作完成！"
echo "=========================================="
