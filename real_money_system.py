#!/usr/bin/env python3
"""
AI Agent Money Machine - 百炼API集成版
6个Agent使用真实的百炼API工作
"""

import os
import sys
import json
import time
from datetime import datetime
from pathlib import Path

# 导入百炼配置
sys.path.insert(0, str(Path.home() / "ai-agent-money-machine"))
from bailian_config import AgentTeamWithBaiLian

class RealMoneyMakingSystem:
    """
    真实的AI Agent赚钱系统
    使用百炼API让Agent真正智能工作
    """
    
    def __init__(self):
        self.data_dir = Path.home() / "ai-agent-money-machine" / "revenue_data"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # 初始化Agent团队
        api_key = os.getenv("BAILIAN_API_KEY")
        self.team = AgentTeamWithBaiLian(api_key)
        
        # 检查API
        self.api_available = self.team.test_api() if api_key else False
        
        # Agent配置
        self.agents = {
            'content': {
                'name': 'ContentAI',
                'role': '内容创作专员',
                'task': '生成爆款内容',
                'price': 5,
                'model': 'qwen-plus'
            },
            'service': {
                'name': 'ServiceAI',
                'role': '客服专员',
                'task': '自动回复咨询',
                'price': 0.5,
                'model': 'qwen-turbo'
            },
            'research': {
                'name': 'ResearchAI',
                'role': '市场研究员',
                'task': '分析市场趋势',
                'price': 20,
                'model': 'qwen-max'
            },
            'trade': {
                'name': 'TradeAI',
                'role': '交易分析师',
                'task': '生成交易信号',
                'price': 10,
                'model': 'qwen-plus'
            },
            'seo': {
                'name': 'SEOAI',
                'role': 'SEO优化师',
                'task': '关键词优化',
                'price': 15,
                'model': 'qwen-plus'
            },
            'email': {
                'name': 'EmailAI',
                'role': '邮件营销专员',
                'task': '营销邮件',
                'price': 10,
                'model': 'qwen-plus'
            }
        }
        
        # 统计数据
        self.stats = {
            'tasks_today': 0,
            'revenue_today': 0,
            'revenue_total': 0,
            'start_time': datetime.now()
        }
        
        self.load_stats()
    
    def load_stats(self):
        """加载统计数据"""
        stats_file = self.data_dir / "stats.json"
        if stats_file.exists():
            with open(stats_file, 'r') as f:
                saved = json.load(f)
                self.stats.update(saved)
    
    def save_stats(self):
        """保存统计数据"""
        stats_file = self.data_dir / "stats.json"
        # 转换datetime为字符串
        stats_to_save = self.stats.copy()
        stats_to_save['start_time'] = self.stats['start_time'].isoformat()
        with open(stats_file, 'w') as f:
            json.dump(stats_to_save, f, indent=2)
    
    def run_content_task(self):
        """ContentAI任务"""
        print("\n📝 ContentAI 正在创作爆款内容...")
        
        topics = [
            "AI副业赚钱方法",
            "一人公司创业指南",
            "被动收入打造",
            "AI工具推荐",
            "自由职业攻略"
        ]
        
        topic = topics[self.stats['tasks_today'] % len(topics)]
        
        try:
            result = self.team.run_task('content', topic=topic, platform='wechat')
            
            if result and 'title' in result:
                print(f"   ✅ 完成!")
                print(f"   📌 标题: {result['title'][:50]}...")
                print(f"   📝 内容长度: {len(result.get('content', ''))} 字符")
                
                # 保存内容
                content_file = self.data_dir / f"content_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
                with open(content_file, 'w', encoding='utf-8') as f:
                    f.write(f"# {result['title']}\n\n")
                    f.write(result.get('content', ''))
                print(f"   💾 已保存: {content_file.name}")
                
                self.stats['tasks_today'] += 1
                self.stats['revenue_today'] += self.agents['content']['price']
                return True
        except Exception as e:
            print(f"   ❌ 错误: {str(e)[:50]}")
        
        return False
    
    def run_service_task(self):
        """ServiceAI任务"""
        print("\n💬 ServiceAI 正在处理客户咨询...")
        
        queries = [
            "这个产品怎么用？",
            "价格是多少？",
            "有退款政策吗？",
            "能定制吗？"
        ]
        
        query = queries[self.stats['tasks_today'] % len(queries)]
        
        try:
            result = self.team.run_task('service', message=query)
            
            if result:
                print(f"   ✅ 完成!")
                print(f"   💬 客户: {query}")
                print(f"   🤖 回复: {result[:60]}...")
                
                self.stats['tasks_today'] += 1
                self.stats['revenue_today'] += self.agents['service']['price']
                return True
        except Exception as e:
            print(f"   ❌ 错误: {str(e)[:50]}")
        
        return False
    
    def run_research_task(self):
        """ResearchAI任务"""
        print("\n🔍 ResearchAI 正在进行市场研究...")
        
        niches = [
            "AI工具市场",
            "副业经济",
            "SaaS创业",
            "内容营销"
        ]
        
        niche = niches[self.stats['tasks_today'] % len(niches)]
        
        try:
            result = self.team.run_task('research', niche=niche)
            
            if result:
                print(f"   ✅ 完成!")
                print(f"   📊 市场: {niche}")
                print(f"   📈 规模: {result.get('market_size', 'N/A')}")
                
                self.stats['tasks_today'] += 1
                self.stats['revenue_today'] += self.agents['research']['price']
                return True
        except Exception as e:
            print(f"   ❌ 错误: {str(e)[:50]}")
        
        return False
    
    def run_trade_task(self):
        """TradeAI任务"""
        print("\n📈 TradeAI 正在分析市场...")
        
        try:
            result = self.team.run_task('trade', symbol='BTC/USDT')
            
            if result:
                print(f"   ✅ 完成!")
                print(f"   📊 交易对: {result.get('symbol', 'N/A')}")
                print(f"   📝 分析: {result.get('analysis', 'N/A')[:60]}...")
                print(f"   ⚠️  {result.get('disclaimer', '')}")
                
                self.stats['tasks_today'] += 1
                self.stats['revenue_today'] += self.agents['trade']['price']
                return True
        except Exception as e:
            print(f"   ❌ 错误: {str(e)[:50]}")
        
        return False
    
    def run_seo_task(self):
        """SEOAI任务"""
        print("\n🎯 SEOAI 正在优化关键词...")
        
        topics = [
            "AI赚钱",
            "被动收入",
            "一人公司",
            "AI副业"
        ]
        
        topic = topics[self.stats['tasks_today'] % len(topics)]
        
        try:
            result = self.team.run_task('seo', topic=topic)
            
            if result:
                print(f"   ✅ 完成!")
                print(f"   🔑 主题: {topic}")
                print(f"   📋 关键词: {', '.join(result.get('primary_keywords', [])[:3])}")
                
                self.stats['tasks_today'] += 1
                self.stats['revenue_today'] += self.agents['seo']['price']
                return True
        except Exception as e:
            print(f"   ❌ 错误: {str(e)[:50]}")
        
        return False
    
    def run_email_task(self):
        """EmailAI任务"""
        print("\n📧 EmailAI 正在创建营销活动...")
        
        campaigns = [
            "新品发布",
            "限时优惠",
            "用户教育",
            "案例分享"
        ]
        
        campaign = campaigns[self.stats['tasks_today'] % len(campaigns)]
        
        try:
            result = self.team.run_task('email', campaign_type=campaign, audience='潜在客户')
            
            if result:
                print(f"   ✅ 完成!")
                print(f"   📧 活动: {campaign}")
                subjects = result.get('subject_lines', [])
                if subjects:
                    print(f"   📝 主题: {subjects[0][:50]}...")
                
                self.stats['tasks_today'] += 1
                self.stats['revenue_today'] += self.agents['email']['price']
                return True
        except Exception as e:
            print(f"   ❌ 错误: {str(e)[:50]}")
        
        return False
    
    def run_daily_schedule(self):
        """执行每日工作计划"""
        print(f"\n{'='*70}")
        print(f"🤖 AI Agent赚钱团队 - 百炼API版")
        print(f"📅 {datetime.now().strftime('%Y年%m月%d日 %H:%M')}")
        print(f"{'='*70}")
        
        if not self.api_available:
            print("⚠️  百炼API未配置，将以模拟模式运行")
            print("   配置命令: export BAILIAN_API_KEY=your_key")
        else:
            print("✅ 百炼API已连接，Agent正在智能工作")
        
        print(f"{'='*70}\n")
        
        # 上午：内容创作 + SEO
        print("🌅 上午工作时段（内容创作）")
        print("-" * 70)
        self.run_content_task()
        self.run_content_task()
        self.run_seo_task()
        
        # 下午：研究 + 交易
        print("\n🌞 下午工作时段（研究分析）")
        print("-" * 70)
        self.run_research_task()
        self.run_trade_task()
        
        # 晚上：邮件 + 客服
        print("\n🌙 晚上工作时段（营销推广）")
        print("-" * 70)
        self.run_email_task()
        self.run_service_task()
        
        self.save_stats()
        self.print_report()
    
    def print_report(self):
        """打印工作报告"""
        print(f"\n{'='*70}")
        print(f"📊 工作报告")
        print(f"{'='*70}")
        print(f"✅ 完成任务: {self.stats['tasks_today']} 个")
        print(f"💰 今日收入: ${self.stats['revenue_today']}")
        print(f"💰 累计收入: ${self.stats['revenue_total'] + self.stats['revenue_today']}")
        print(f"{'='*70}\n")
        
        # 收入预测
        if self.stats['tasks_today'] > 0:
            daily_avg = self.stats['revenue_today'] / self.stats['tasks_today']
            print(f"📈 收入预测:")
            print(f"   日均收入潜力: ${daily_avg * 10:.0f}")
            print(f"   预计月收入: ${daily_avg * 10 * 30:.0f}")
            print(f"   预计年收入: ${daily_avg * 10 * 30 * 12:.0f}")


# 主程序
if __name__ == '__main__':
    print("🚀 启动AI Agent赚钱系统（百炼API版）\n")
    
    system = RealMoneyMakingSystem()
    system.run_daily_schedule()
    
    print("\n" + "="*70)
    print("✅ 一轮工作完成！")
    print("="*70)
    print("\n选项:")
    print("  1. 继续运行更多任务")
    print("  2. 查看生成的内容文件")
    print("  3. 配置百炼API（如果还没配置）")
    print("  4. 退出")
    
    try:
        choice = input("\n选择 (1-4): ").strip()
        
        if choice == '1':
            system.run_daily_schedule()
        elif choice == '2':
            print(f"\n📁 内容文件位置: {system.data_dir}")
            files = list(system.data_dir.glob("content_*.md"))
            if files:
                print(f"   已生成 {len(files)} 个内容文件:")
                for f in files[-5:]:  # 显示最近5个
                    print(f"   - {f.name}")
        elif choice == '3':
            print("\n配置步骤:")
            print("  1. 访问 https://dashscope.aliyun.com/")
            print("  2. 创建API Key")
            print("  3. 运行: export BAILIAN_API_KEY=your_key")
            print("  4. 重新启动本系统")
    except:
        pass
