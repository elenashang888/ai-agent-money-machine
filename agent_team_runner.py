#!/usr/bin/env python3
"""
AI Agent Money Machine - 自动化赚钱团队运行器
让6个AI Agent 24/7为你工作赚钱
"""

import json
import urllib.request
import urllib.error
import time
import random
from datetime import datetime
import os

class AgentTeam:
    """AI Agent赚钱团队管理器"""
    
    def __init__(self, api_base="http://localhost:5000"):
        self.api_base = api_base
        self.agents = {
            'content': {'name': 'ContentAI', 'task': '内容创作', 'income_per_task': 5},
            'service': {'name': 'ServiceAI', 'task': '客户服务', 'income_per_task': 3},
            'research': {'name': 'ResearchAI', 'task': '市场研究', 'income_per_task': 8},
            'trade': {'name': 'TradeAI', 'task': '交易信号', 'income_per_task': 10},
            'seo': {'name': 'SEOAI', 'task': 'SEO优化', 'income_per_task': 6},
            'email': {'name': 'EmailAI', 'task': '邮件营销', 'income_per_task': 4}
        }
        self.stats = {
            'tasks_completed': 0,
            'total_income': 0,
            'start_time': datetime.now()
        }
        
    def call_api(self, endpoint, data=None):
        """调用API"""
        try:
            url = f"{self.api_base}{endpoint}"
            if data:
                req = urllib.request.Request(
                    url,
                    data=json.dumps(data).encode(),
                    headers={'Content-Type': 'application/json'},
                    method='POST'
                )
            else:
                req = urllib.request.Request(url, method='GET')
            
            with urllib.request.urlopen(req, timeout=30) as response:
                return json.loads(response.read().decode())
        except Exception as e:
            return {'error': str(e)}
    
    def content_agent_task(self):
        """ContentAI任务：生成一篇小红书爆款内容"""
        topics = [
            "AI副业赚钱", "一人公司创业", "被动收入方法",
            "AI工具推荐", "自由职业指南", "数字游民生活"
        ]
        data = {
            'platform': 'xiaohongshu',
            'topic': random.choice(topics),
            'style': '爆款',
            'language': 'zh'
        }
        result = self.call_api('/api/content/generate', data)
        return result
    
    def service_agent_task(self):
        """ServiceAI任务：处理客户咨询"""
        queries = [
            "这个AI工具怎么用？",
            " pricing是多少？",
            "能定制吗？",
            "有退款政策吗？"
        ]
        data = {
            'message': random.choice(queries),
            'context': {'product': 'AI Agent Money Machine'}
        }
        result = self.call_api('/api/service/chat', data)
        return result
    
    def research_agent_task(self):
        """ResearchAI任务：研究市场趋势"""
        niches = [
            "AI工具市场", "副业趋势", "SaaS创业",
            "内容营销", "自动化工具"
        ]
        data = {
            'niche': random.choice(niches),
            'depth': 'quick'
        }
        result = self.call_api('/api/research/trend', data)
        return result
    
    def trade_agent_task(self):
        """TradeAI任务：生成交易信号（模拟模式）"""
        data = {
            'symbol': 'BTC/USDT',
            'strategy': 'trend_following',
            'demo_mode': True
        }
        result = self.call_api('/api/trade/signal', data)
        return result
    
    def seo_agent_task(self):
        """SEOAI任务：分析关键词"""
        keywords = [
            "AI赚钱", "被动收入", "一人公司",
            "AI副业", "自动化赚钱"
        ]
        data = {
            'keywords': random.sample(keywords, 2),
            'competitors': 3
        }
        result = self.call_api('/api/seo/keywords', data)
        return result
    
    def email_agent_task(self):
        """EmailAI任务：生成营销邮件"""
        campaigns = [
            "新品发布", "限时优惠", "用户教育",
            "案例分享", "免费试用"
        ]
        data = {
            'campaign_type': random.choice(campaigns),
            'audience': '潜在买家',
            'tone': '专业且友好'
        }
        result = self.call_api('/api/email/generate', data)
        return result
    
    def run_all_agents(self):
        """运行所有Agent完成一轮任务"""
        print(f"\n{'='*60}")
        print(f"🚀 AI Agent赚钱团队开始工作 - {datetime.now().strftime('%H:%M:%S')}")
        print(f"{'='*60}\n")
        
        results = {}
        
        # ContentAI - 内容创作
        print("📝 ContentAI 正在生成爆款内容...")
        results['content'] = self.content_agent_task()
        if 'content' in results['content']:
            print(f"   ✅ 完成！生成了 {len(results['content']['content'])} 字符内容")
            self.stats['tasks_completed'] += 1
            self.stats['total_income'] += self.agents['content']['income_per_task']
        else:
            print(f"   ⚠️ 演示模式运行")
        
        # ServiceAI - 客服
        print("💬 ServiceAI 正在处理客户咨询...")
        results['service'] = self.service_agent_task()
        if 'response' in results['service']:
            print(f"   ✅ 完成！回复: {results['service']['response'][:50]}...")
            self.stats['tasks_completed'] += 1
            self.stats['total_income'] += self.agents['service']['income_per_task']
        else:
            print(f"   ⚠️ 演示模式运行")
        
        # ResearchAI - 市场研究
        print("🔍 ResearchAI 正在分析市场趋势...")
        results['research'] = self.research_agent_task()
        if 'trends' in results['research']:
            print(f"   ✅ 完成！发现 {len(results['research']['trends'])} 个趋势")
            self.stats['tasks_completed'] += 1
            self.stats['total_income'] += self.agents['research']['income_per_task']
        else:
            print(f"   ⚠️ 演示模式运行")
        
        # TradeAI - 交易信号
        print("📈 TradeAI 正在生成交易信号...")
        results['trade'] = self.trade_agent_task()
        if 'signal' in results['trade']:
            print(f"   ✅ 完成！信号: {results['trade']['signal']}")
            self.stats['tasks_completed'] += 1
            self.stats['total_income'] += self.agents['trade']['income_per_task']
        else:
            print(f"   ⚠️ 演示模式运行")
        
        # SEOAI - SEO优化
        print("🎯 SEOAI 正在分析关键词...")
        results['seo'] = self.seo_agent_task()
        if 'keywords' in results['seo']:
            print(f"   ✅ 完成！分析了 {len(results['seo']['keywords'])} 个关键词")
            self.stats['tasks_completed'] += 1
            self.stats['total_income'] += self.agents['seo']['income_per_task']
        else:
            print(f"   ⚠️ 演示模式运行")
        
        # EmailAI - 邮件营销
        print("📧 EmailAI 正在生成营销邮件...")
        results['email'] = self.email_agent_task()
        if 'subject' in results['email']:
            print(f"   ✅ 完成！主题: {results['email']['subject']}")
            self.stats['tasks_completed'] += 1
            self.stats['total_income'] += self.agents['email']['income_per_task']
        else:
            print(f"   ⚠️ 演示模式运行")
        
        self.print_stats()
        return results
    
    def print_stats(self):
        """打印统计信息"""
        runtime = datetime.now() - self.stats['start_time']
        print(f"\n{'='*60}")
        print(f"📊 团队工作统计")
        print(f"{'='*60}")
        print(f"⏱️  运行时间: {runtime}")
        print(f"✅ 完成任务: {self.stats['tasks_completed']} 个")
        print(f"💰 预估收入: ${self.stats['total_income']}")
        print(f"{'='*60}\n")
    
    def continuous_run(self, interval=300):
        """持续运行模式"""
        print("🤖 AI Agent赚钱团队启动！")
        print(f"⏰ 每 {interval} 秒执行一轮任务")
        print("按 Ctrl+C 停止\n")
        
        try:
            while True:
                self.run_all_agents()
                print(f"⏳ 等待下一轮... ({interval}秒后)\n")
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n\n👋 团队停止工作")
            self.print_stats()

# 主程序
if __name__ == '__main__':
    team = AgentTeam()
    
    # 先运行一轮测试
    team.run_all_agents()
    
    # 询问是否进入持续运行模式
    print("\n是否进入24/7自动运行模式？")
    print("输入 'yes' 开始持续运行，或直接按Enter退出")
    
    try:
        response = input("> ").strip().lower()
        if response in ['yes', 'y', '是']:
            team.continuous_run(interval=300)  # 每5分钟运行一轮
    except:
        pass
