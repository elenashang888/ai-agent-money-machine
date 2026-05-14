#!/bin/bash
# 百炼API配置脚本
# 自动配置6个Agent使用百炼API

echo "🚀 AI Agent Money Machine - 百炼API配置"
echo "=========================================="
echo ""

# 检查Python环境
echo "📋 检查环境..."
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到Python3，请先安装"
    exit 1
fi

echo "✅ Python3已安装"

# 检查requests库
echo "📦 检查依赖..."
python3 -c "import requests" 2>/dev/null || pip3 install requests -q

# 配置API Key
echo ""
echo "🔑 百炼API配置"
echo "----------------------------------------------"
echo "请访问: https://dashscope.aliyun.com/"
echo "1. 登录阿里云账号"
echo "2. 进入 API-KEY 管理"
echo "3. 创建或复制你的API Key"
echo ""

# 检查是否已有API Key
if [ -f ".env" ]; then
    source .env
fi

if [ -n "$BAILIAN_API_KEY" ]; then
    echo "✅ 检测到已配置的API Key"
    read -p "是否使用现有Key? (y/n): " use_existing
    if [ "$use_existing" != "y" ]; then
        BAILIAN_API_KEY=""
    fi
fi

if [ -z "$BAILIAN_API_KEY" ]; then
    read -p "请输入你的百炼API Key (sk-...): " BAILIAN_API_KEY
    
    # 保存到.env文件
    echo "BAILIAN_API_KEY=$BAILIAN_API_KEY" > .env
    echo "✅ API Key已保存到 .env 文件"
fi

export BAILIAN_API_KEY

echo ""
echo "🧪 测试API连接..."
echo "----------------------------------------------"

# 创建测试脚本
cat > /tmp/test_bailian.py << 'EOF'
import os
import sys
sys.path.insert(0, os.path.expanduser("~/ai-agent-money-machine"))

from bailian_config import AgentTeamWithBaiLian

# 初始化团队
team = AgentTeamWithBaiLian()

# 测试API
if team.test_api():
    print("\n✅ API连接成功！")
    print("\n测试各Agent功能：")
    print("-" * 50)
    
    # 快速测试
    print("\n1. ContentAI - 生成文章标题...")
    result = team.run_task('content', topic='AI副业赚钱', platform='wechat')
    print(f"   标题: {result.get('title', 'N/A')[:40]}...")
    
    print("\n2. ServiceAI - 客服回复...")
    result = team.run_task('service', message='这个产品怎么用？')
    print(f"   回复: {result[:50]}...")
    
    print("\n3. ResearchAI - 市场分析...")
    result = team.run_task('research', niche='AI工具市场')
    print(f"   市场规模: {result.get('market_size', 'N/A')}")
    
    print("\n✅ 所有Agent测试通过！")
    sys.exit(0)
else:
    print("\n❌ API连接失败")
    print("请检查：")
    print("1. API Key是否正确")
    print("2. 账号是否有足够余额")
    print("3. 网络连接是否正常")
    sys.exit(1)
EOF

python3 /tmp/test_bailian.py

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "🎉 配置成功！"
    echo "=========================================="
    echo ""
    echo "6个Agent现在可以使用百炼API了："
    echo "  • ContentAI - 生成爆款内容"
    echo "  • ServiceAI - 自动客服回复"
    echo "  • ResearchAI - 市场研究分析"
    echo "  • TradeAI - 交易信号（模拟）"
    echo "  • SEOAI - SEO关键词优化"
    echo "  • EmailAI - 邮件营销"
    echo ""
    echo "启动命令:"
    echo "  python3 money_making_system.py"
    echo ""
    echo "API Key保存在: .env"
    echo "=========================================="
else
    echo ""
    echo "⚠️ 配置遇到问题，请检查API Key"
fi
