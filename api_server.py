#!/usr/bin/env python3
"""
AI Agent Money Machine - 统一API服务器
6个AI Agent的统一接口
"""

import sys
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

# 导入各个Agent
sys.path.insert(0, '/opt/data/home/ai-agent-money-machine')

from content_ai_agent import ContentAI
from service_ai_agent import ServiceAI
from research_ai_agent import ResearchAI
from trade_ai_agent import TradeAI
from seo_ai_agent import SEOAI
from email_ai_agent import EmailAI

app = Flask(__name__)
CORS(app)

# 初始化所有Agent
agents = {
    'content': ContentAI(),
    'service': ServiceAI(),
    'research': ResearchAI(),
    'trade': TradeAI(),
    'seo': SEOAI(),
    'email': EmailAI()
}

# ========== ContentAI 路由 ==========
@app.route('/api/content/generate', methods=['POST'])
def content_generate():
    """生成内容"""
    data = request.json
    topic = data.get('topic', 'AI工具')
    platform = data.get('platform', 'xiaohongshu')
    
    result = agents['content'].generate_post(topic, platform)
    metrics = agents['content'].get_metrics()
    
    return jsonify({
        'success': True,
        'data': result,
        'metrics': metrics,
        'estimated_value': f"${metrics['monthly_projection_usd']}/month"
    })

@app.route('/api/content/metrics', methods=['GET'])
def content_metrics():
    """获取ContentAI指标"""
    return jsonify({
        'success': True,
        'metrics': agents['content'].get_metrics()
    })

# ========== ServiceAI 路由 ==========
@app.route('/api/service/chat', methods=['POST'])
def service_chat():
    """客服对话"""
    data = request.json
    message = data.get('message', '')
    user_id = data.get('user_id', 'anonymous')
    
    result = agents['service'].generate_response(message, user_id)
    metrics = agents['service'].get_metrics()
    
    return jsonify({
        'success': True,
        'data': result,
        'metrics': metrics,
        'estimated_value': f"${metrics['monthly_projection_usd']}/month"
    })

@app.route('/api/service/metrics', methods=['GET'])
def service_metrics():
    """获取ServiceAI指标"""
    return jsonify({
        'success': True,
        'metrics': agents['service'].get_metrics()
    })

# ========== ResearchAI 路由 ==========
@app.route('/api/research/trend', methods=['POST'])
def research_trend():
    """趋势分析"""
    data = request.json
    keyword = data.get('keyword', 'AI工具')
    
    result = agents['research'].analyze_trend(keyword)
    metrics = agents['research'].get_metrics()
    
    return jsonify({
        'success': True,
        'data': result,
        'metrics': metrics,
        'estimated_value': f"${metrics['monthly_projection_usd']}/month"
    })

@app.route('/api/research/products', methods=['POST'])
def research_products():
    """产品研究"""
    data = request.json
    category = data.get('category', 'saas')
    
    result = agents['research'].product_research(category)
    
    return jsonify({
        'success': True,
        'data': result
    })

@app.route('/api/research/metrics', methods=['GET'])
def research_metrics():
    """获取ResearchAI指标"""
    return jsonify({
        'success': True,
        'metrics': agents['research'].get_metrics()
    })

# ========== TradeAI 路由 ==========
@app.route('/api/trade/signal', methods=['POST'])
def trade_signal():
    """交易信号"""
    data = request.json
    symbol = data.get('symbol', 'BTC/USDT')
    strategy = data.get('strategy', 'momentum')
    
    result = agents['trade'].generate_signal(symbol, strategy)
    metrics = agents['trade'].get_metrics()
    
    return jsonify({
        'success': True,
        'data': result,
        'metrics': metrics,
        'estimated_value': f"${metrics['monthly_pnl_projection']}/month (模拟)"
    })

@app.route('/api/trade/portfolio', methods=['GET'])
def trade_portfolio():
    """投资组合"""
    return jsonify({
        'success': True,
        'data': agents['trade'].get_portfolio_summary()
    })

@app.route('/api/trade/metrics', methods=['GET'])
def trade_metrics():
    """获取TradeAI指标"""
    return jsonify({
        'success': True,
        'metrics': agents['trade'].get_metrics()
    })

# ========== SEOAI 路由 ==========
@app.route('/api/seo/keywords', methods=['POST'])
def seo_keywords():
    """关键词研究"""
    data = request.json
    keyword = data.get('keyword', 'AI工具')
    
    result = agents['seo'].keyword_research(keyword)
    metrics = agents['seo'].get_metrics()
    
    return jsonify({
        'success': True,
        'data': result,
        'metrics': metrics,
        'estimated_value': f"${metrics['monthly_projection_usd']}/month"
    })

@app.route('/api/seo/optimize', methods=['POST'])
def seo_optimize():
    """内容优化"""
    data = request.json
    content = data.get('content', '')
    target = data.get('target_keyword', 'AI工具')
    
    result = agents['seo'].optimize_content(content, target)
    
    return jsonify({
        'success': True,
        'data': result
    })

@app.route('/api/seo/metrics', methods=['GET'])
def seo_metrics():
    """获取SEOAI指标"""
    return jsonify({
        'success': True,
        'metrics': agents['seo'].get_metrics()
    })

# ========== EmailAI 路由 ==========
@app.route('/api/email/generate', methods=['POST'])
def email_generate():
    """生成邮件"""
    data = request.json
    template_type = data.get('template_type', 'welcome')
    variables = data.get('variables', {})
    
    result = agents['email'].generate_email(template_type, variables)
    metrics = agents['email'].get_metrics()
    
    return jsonify({
        'success': True,
        'data': result,
        'metrics': metrics,
        'estimated_value': f"${metrics['monthly_projection_usd']}/month"
    })

@app.route('/api/email/sequence', methods=['POST'])
def email_sequence():
    """创建邮件序列"""
    result = agents['email'].create_welcome_sequence()
    
    return jsonify({
        'success': True,
        'data': result
    })

@app.route('/api/email/abtest', methods=['POST'])
def email_abtest():
    """A/B测试"""
    data = request.json
    email_type = data.get('email_type', 'promotional')
    variant_a = data.get('variant_a', {'subject': 'Variant A'})
    variant_b = data.get('variant_b', {'subject': 'Variant B'})
    
    result = agents['email'].ab_test(email_type, variant_a, variant_b)
    
    return jsonify({
        'success': True,
        'data': result
    })

@app.route('/api/email/metrics', methods=['GET'])
def email_metrics():
    """获取EmailAI指标"""
    return jsonify({
        'success': True,
        'metrics': agents['email'].get_metrics()
    })

# ========== 全局路由 ==========
@app.route('/api/health', methods=['GET'])
def health():
    """健康检查"""
    return jsonify({
        'status': 'ok',
        'service': 'AI Agent Money Machine',
        'agents': list(agents.keys()),
        'version': '1.0.0'
    })

@app.route('/api/dashboard', methods=['GET'])
def dashboard():
    """仪表盘 - 所有Agent指标"""
    all_metrics = {
        'content': agents['content'].get_metrics(),
        'service': agents['service'].get_metrics(),
        'research': agents['research'].get_metrics(),
        'trade': agents['trade'].get_metrics(),
        'seo': agents['seo'].get_metrics(),
        'email': agents['email'].get_metrics()
    }
    
    # 计算总价值
    total_monthly = sum(m.get('monthly_projection_usd', 0) for m in all_metrics.values())
    
    return jsonify({
        'success': True,
        'agents': all_metrics,
        'total_monthly_projection': f"${total_monthly}",
        'agent_count': len(agents)
    })

@app.route('/', methods=['GET'])
def index():
    """API首页"""
    return jsonify({
        'name': 'AI Agent Money Machine API',
        'version': '1.0.0',
        'agents': {
            'content': '/api/content/* - 内容创作助手',
            'service': '/api/service/* - 智能客服机器人',
            'research': '/api/research/* - 产品研究分析师',
            'trade': '/api/trade/* - 智能交易助手',
            'seo': '/api/seo/* - SEO优化专家',
            'email': '/api/email/* - 邮件营销专员'
        },
        'endpoints': {
            'health': '/api/health',
            'dashboard': '/api/dashboard'
        }
    })

if __name__ == '__main__':
    print("🚀 AI Agent Money Machine API 启动中...")
    print("=" * 50)
    print("可用Agent:")
    for agent_name in agents.keys():
        print(f"  - {agent_name}")
    print("=" * 50)
    print("API地址: http://localhost:5000")
    print("文档: http://localhost:5000/")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=5000, debug=True)
