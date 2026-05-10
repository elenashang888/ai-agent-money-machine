#!/bin/bash
# AI Agent Money Machine - 启动脚本
# 一键启动所有Agent服务

echo "🚀 AI Agent Money Machine 启动器"
echo "=================================="
echo ""

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 未安装"
    exit 1
fi

echo "✅ Python3 已检测"

# 检查依赖
echo "📦 检查依赖..."
python3 -c "import flask" 2>/dev/null || pip3 install flask flask-cors -q

echo "✅ 依赖检查完成"
echo ""

# 启动API服务器
echo "🎯 启动统一API服务器..."
echo "   地址: http://localhost:5000"
echo "   文档: http://localhost:5000/"
echo ""

cd /opt/data/home/ai-agent-money-machine
python3 api_server.py &

SERVER_PID=$!
echo "✅ API服务器已启动 (PID: $SERVER_PID)"
echo ""

# 显示Agent信息
echo "📊 Agent 状态:"
echo "   • ContentAI   - 内容创作助手     ($500-3000/月)"
echo "   • ServiceAI   - 智能客服机器人   ($500-2000/月)"
echo "   • ResearchAI  - 产品研究分析师   ($1000-5000/月)"
echo "   • TradeAI     - 智能交易助手     (Variable)"
echo "   • SEOAI       - SEO优化专家      ($2000-10000/月)"
echo "   • EmailAI     - 邮件营销专员     ($1000-5000/月)"
echo ""
echo "💰 总收益潜力: $5500-25000/月"
echo ""

# 显示API端点
echo "🔗 API端点:"
echo "   GET  /              - API文档"
echo "   GET  /api/health    - 健康检查"
echo "   GET  /api/dashboard - 仪表盘"
echo ""
echo "   POST /api/content/generate  - 生成内容"
echo "   POST /api/service/chat      - 客服对话"
echo "   POST /api/research/trend    - 趋势分析"
echo "   POST /api/trade/signal      - 交易信号"
echo "   POST /api/seo/keywords      - 关键词研究"
echo "   POST /api/email/generate    - 生成邮件"
echo ""

echo "=================================="
echo "按 Ctrl+C 停止服务"
echo ""

# 等待中断
trap "echo ''; echo '🛑 正在停止服务...'; kill $SERVER_PID 2>/dev/null; echo '✅ 服务已停止'; exit 0" INT

wait $SERVER_PID
