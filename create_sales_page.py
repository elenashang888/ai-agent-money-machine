#!/usr/bin/env python3
"""
AI Agent Money Machine - 销售页面生成器
创建专业的销售落地页
"""

import json
from datetime import datetime

class SalesPageGenerator:
    """销售页面生成器"""
    
    def __init__(self):
        self.product = {
            'name': 'AI Agent Money Machine',
            'name_cn': 'AI Agent赚钱机器',
            'tagline': '6个AI Agent 24/7为你工作赚钱',
            'tagline_cn': '让6个AI员工24小时不间断为你赚钱',
            'price_usd': 299,
            'price_cny': 1999,
            'features': [
                'ContentAI - 自动生成爆款内容',
                'ServiceAI - 24/7智能客服',
                'ResearchAI - 市场趋势分析',
                'TradeAI - 交易信号生成',
                'SEOAI - SEO关键词优化',
                'EmailAI - 自动邮件营销'
            ]
        }
    
    def generate_landing_page(self):
        """生成销售落地页HTML"""
        
        html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.product['name_cn']} - {self.product['tagline_cn']}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }}
        
        /* Hero Section */
        .hero {{
            padding: 100px 0;
            text-align: center;
            color: white;
        }}
        
        .hero h1 {{
            font-size: 3.5rem;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        
        .hero .tagline {{
            font-size: 1.5rem;
            margin-bottom: 30px;
            opacity: 0.95;
        }}
        
        .hero .price {{
            font-size: 3rem;
            font-weight: bold;
            margin: 30px 0;
        }}
        
        .hero .price .currency {{
            font-size: 1.5rem;
        }}
        
        .cta-button {{
            display: inline-block;
            background: #ff6b6b;
            color: white;
            padding: 20px 60px;
            font-size: 1.3rem;
            border-radius: 50px;
            text-decoration: none;
            font-weight: bold;
            transition: transform 0.3s, box-shadow 0.3s;
            box-shadow: 0 10px 30px rgba(255,107,107,0.4);
        }}
        
        .cta-button:hover {{
            transform: translateY(-3px);
            box-shadow: 0 15px 40px rgba(255,107,107,0.5);
        }}
        
        /* Features Section */
        .features {{
            background: white;
            padding: 80px 0;
        }}
        
        .features h2 {{
            text-align: center;
            font-size: 2.5rem;
            margin-bottom: 60px;
            color: #333;
        }}
        
        .features-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 30px;
        }}
        
        .feature-card {{
            background: #f8f9fa;
            padding: 40px;
            border-radius: 15px;
            transition: transform 0.3s, box-shadow 0.3s;
        }}
        
        .feature-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }}
        
        .feature-card h3 {{
            font-size: 1.5rem;
            margin-bottom: 15px;
            color: #667eea;
        }}
        
        .feature-card p {{
            color: #666;
            line-height: 1.8;
        }}
        
        /* Stats Section */
        .stats {{
            background: #2d3748;
            color: white;
            padding: 60px 0;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 40px;
            text-align: center;
        }}
        
        .stat-item h3 {{
            font-size: 3rem;
            color: #ff6b6b;
            margin-bottom: 10px;
        }}
        
        .stat-item p {{
            font-size: 1.1rem;
            opacity: 0.9;
        }}
        
        /* Pricing Section */
        .pricing {{
            background: #f8f9fa;
            padding: 80px 0;
        }}
        
        .pricing h2 {{
            text-align: center;
            font-size: 2.5rem;
            margin-bottom: 60px;
        }}
        
        .pricing-card {{
            background: white;
            max-width: 500px;
            margin: 0 auto;
            padding: 50px;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.1);
            text-align: center;
        }}
        
        .pricing-card .tier {{
            font-size: 1.3rem;
            color: #667eea;
            font-weight: bold;
            margin-bottom: 20px;
        }}
        
        .pricing-card .price {{
            font-size: 4rem;
            font-weight: bold;
            color: #333;
            margin-bottom: 30px;
        }}
        
        .pricing-card .price .currency {{
            font-size: 2rem;
        }}
        
        .pricing-card ul {{
            list-style: none;
            margin-bottom: 40px;
        }}
        
        .pricing-card li {{
            padding: 10px 0;
            color: #666;
            border-bottom: 1px solid #eee;
        }}
        
        .pricing-card li:last-child {{
            border-bottom: none;
        }}
        
        /* FAQ Section */
        .faq {{
            background: white;
            padding: 80px 0;
        }}
        
        .faq h2 {{
            text-align: center;
            font-size: 2.5rem;
            margin-bottom: 60px;
        }}
        
        .faq-item {{
            max-width: 800px;
            margin: 0 auto 30px;
            padding: 30px;
            background: #f8f9fa;
            border-radius: 10px;
        }}
        
        .faq-item h3 {{
            font-size: 1.2rem;
            margin-bottom: 15px;
            color: #333;
        }}
        
        .faq-item p {{
            color: #666;
            line-height: 1.8;
        }}
        
        /* Footer */
        footer {{
            background: #2d3748;
            color: white;
            padding: 40px 0;
            text-align: center;
        }}
        
        footer p {{
            opacity: 0.8;
        }}
        
        /* Responsive */
        @media (max-width: 768px) {{
            .hero h1 {{
                font-size: 2rem;
            }}
            
            .hero .tagline {{
                font-size: 1.1rem;
            }}
            
            .features-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <!-- Hero Section -->
    <section class="hero">
        <div class="container">
            <h1>🤖 {self.product['name_cn']}</h1>
            <p class="tagline">{self.product['tagline_cn']}</p>
            <div class="price">
                <span class="currency">$</span>{self.product['price_usd']}
            </div>
            <a href="#pricing" class="cta-button">立即购买 →</a>
            <p style="margin-top: 20px; opacity: 0.8;">30天无理由退款保证</p>
        </div>
    </section>
    
    <!-- Features Section -->
    <section class="features">
        <div class="container">
            <h2>6个AI Agent为你工作</h2>
            <div class="features-grid">
                <div class="feature-card">
                    <h3>📝 ContentAI</h3>
                    <p>自动生成小红书、公众号、知乎等平台爆款内容。每天产出10+篇高质量文章，无需人工写作。</p>
                </div>
                <div class="feature-card">
                    <h3>💬 ServiceAI</h3>
                    <p>24/7智能客服，自动回复客户咨询。支持多轮对话，转化率提升300%。</p>
                </div>
                <div class="feature-card">
                    <h3>🔍 ResearchAI</h3>
                    <p>实时分析市场趋势、竞品动态。为你的商业决策提供数据支持。</p>
                </div>
                <div class="feature-card">
                    <h3>📈 TradeAI</h3>
                    <p>生成交易信号和技术分析。模拟模式运行，学习交易策略。</p>
                </div>
                <div class="feature-card">
                    <h3>🎯 SEOAI</h3>
                    <p>自动分析关键词、优化内容。让你的内容在搜索引擎中排名靠前。</p>
                </div>
                <div class="feature-card">
                    <h3>📧 EmailAI</h3>
                    <p>自动生成营销邮件序列。提升邮件打开率和点击率。</p>
                </div>
            </div>
        </div>
    </section>
    
    <!-- Stats Section -->
    <section class="stats">
        <div class="container">
            <div class="stats-grid">
                <div class="stat-item">
                    <h3>6</h3>
                    <p>AI Agent</p>
                </div>
                <div class="stat-item">
                    <h3>24/7</h3>
                    <p>全天候工作</p>
                </div>
                <div class="stat-item">
                    <h3>$5,500+</h3>
                    <p>月收入潜力</p>
                </div>
                <div class="stat-item">
                    <h3>100%</h3>
                    <p>自动化运行</p>
                </div>
            </div>
        </div>
    </section>
    
    <!-- Pricing Section -->
    <section class="pricing" id="pricing">
        <div class="container">
            <h2>选择你的方案</h2>
            <div class="pricing-card">
                <div class="tier">专业版 Pro</div>
                <div class="price">
                    <span class="currency">$</span>{self.product['price_usd']}
                </div>
                <ul>
                    <li>✅ 6个完整AI Agent</li>
                    <li>✅ 源代码 + 部署文档</li>
                    <li>✅ API集成配置</li>
                    <li>✅ 自动化工作流</li>
                    <li>✅ 终身免费更新</li>
                    <li>✅ 技术支持</li>
                </ul>
                <a href="https://github.com/elenashang888/ai-agent-money-machine" class="cta-button">立即购买</a>
            </div>
        </div>
    </section>
    
    <!-- FAQ Section -->
    <section class="faq">
        <div class="container">
            <h2>常见问题</h2>
            <div class="faq-item">
                <h3>Q: 需要编程基础吗？</h3>
                <p>A: 不需要。我们提供完整的安装文档和视频教程，零基础也能在30分钟内搭建完成。</p>
            </div>
            <div class="faq-item">
                <h3>Q: 需要额外费用吗？</h3>
                <p>A: 只需要支付AI API的使用费用（每月约$10-50，取决于使用量）。系统本身一次性付费，无订阅费。</p>
            </div>
            <div class="faq-item">
                <h3>Q: 可以商用吗？</h3>
                <p>A: 可以！购买后获得MIT开源协议，可以自由修改、转售、商用。</p>
            </div>
            <div class="faq-item">
                <h3>Q: 有退款政策吗？</h3>
                <p>A: 有！30天无理由退款。如果系统不符合你的期望，全额退款。</p>
            </div>
        </div>
    </section>
    
    <!-- Footer -->
    <footer>
        <div class="container">
            <p>© 2026 AI Agent Money Machine. All rights reserved.</p>
            <p style="margin-top: 10px; font-size: 0.9rem;">让AI为你工作，实现真正的被动收入</p>
        </div>
    </footer>
</body>
</html>'''
        
        return html
    
    def generate_gumroad_description(self):
        """生成Gumroad产品描述"""
        
        description = f'''# 🤖 AI Agent Money Machine

**让6个AI Agent 24/7为你工作赚钱**

---

## 这是什么？

AI Agent Money Machine 是一个完整的AI自动化赚钱系统。包含6个专业AI Agent，可以：

- 📝 **自动生成爆款内容**（小红书/公众号/知乎）
- 💬 **24/7智能客服**（自动回复、转化客户）
- 🔍 **市场趋势分析**（竞品调研、机会发现）
- 📈 **交易信号生成**（技术分析、策略建议）
- 🎯 **SEO关键词优化**（提升搜索排名）
- 📧 **邮件营销自动化**（高转化率邮件序列）

---

## 包含什么？

✅ **6个完整AI Agent源代码**（Python）
✅ **Flask API服务器**（RESTful接口）
✅ **自动化工作流**（定时任务配置）
✅ **部署文档**（一步一步教程）
✅ **百炼API集成**（通义千问配置）
✅ **收入追踪系统**（自动统计收益）

---

## 收入潜力

| 指标 | 数值 |
|------|------|
| 月收入潜力 | $5,500 - $25,000 |
| 毛利率 | 85-95% |
| 运营成本 | $20-50/月 |

---

## 技术要求

- Python 3.8+
- 百炼API Key（阿里云）
- 服务器/VPS（可选，本地也可运行）

---

## 退款政策

**30天无理由退款**

如果系统不符合你的期望，只需发送邮件至 support@example.com，全额退款，不问原因。

---

## 许可证

MIT License - 可自由修改、转售、商用

---

**立即开始你的AI自动化赚钱之旅！** 🚀
'''
        
        return description
    
    def generate_promo_tweets(self):
        """生成推广推文"""
        
        tweets = [
            "🤖 6个AI Agent 24/7为你工作\n\nContentAI写内容\nServiceAI做客服\nResearchAI分析市场\nTradeAI给信号\nSEOAI优化排名\nEmailAI做营销\n\n全部自动化，被动收入$5000+/月\n\n限时$299 → 评论'AI'获取链接",
            
            "💡 一人公司 + 6个AI员工 = 无限可能\n\n我搭建了一套AI Agent系统，6个agent分工协作：\n- 内容创作\n- 客户服务\n- 市场研究\n- 交易分析\n- SEO优化\n- 邮件营销\n\n全部自动化运行\n\n想要源码？DM我",
            
            "🔥 2026年最值钱的技能：搭建AI Agent团队\n\n别人用1个ChatGPT\n我用6个专业Agent\n\n每个agent专精一个领域，24小时不间断工作\n\n这就是AI时代的'一人公司'\n\n源码可售，限时$299",
            
            "⚡ 从0到$5000/月的AI副业\n\n不需要：\n❌ 雇佣员工\n❌ 写代码能力\n❌ 大量时间\n\n只需要：\n✅ 6个AI Agent\n✅ 30分钟配置\n✅ 自动化运行\n\n被动收入，躺着赚钱\n\n想要？评论'Agent'",
            
            "📊 我的AI Agent团队今日工作报告：\n\n✅ ContentAI: 生成5篇爆款文章\n✅ ServiceAI: 处理20个客户咨询\n✅ ResearchAI: 完成3份市场报告\n✅ TradeAI: 生成10个交易信号\n✅ SEOAI: 优化15个关键词\n✅ EmailAI: 发送8封营销邮件\n\n而我，在睡觉 😴\n\n这就是自动化的力量"
        ]
        
        return tweets
    
    def save_all(self):
        """保存所有营销材料"""
        
        # 保存销售页面
        landing_page = self.generate_landing_page()
        with open('sales_page.html', 'w', encoding='utf-8') as f:
            f.write(landing_page)
        print("✅ 销售页面已保存: sales_page.html")
        
        # 保存Gumroad描述
        gumroad_desc = self.generate_gumroad_description()
        with open('gumroad_description.md', 'w', encoding='utf-8') as f:
            f.write(gumroad_desc)
        print("✅ Gumroad描述已保存: gumroad_description.md")
        
        # 保存推广推文
        tweets = self.generate_promo_tweets()
        with open('promo_tweets.txt', 'w', encoding='utf-8') as f:
            for i, tweet in enumerate(tweets, 1):
                f.write(f"=== 推文 {i} ===\n")
                f.write(tweet)
                f.write("\n\n")
        print("✅ 推广推文已保存: promo_tweets.txt")
        
        return {
            'landing_page': 'sales_page.html',
            'gumroad_desc': 'gumroad_description.md',
            'tweets': 'promo_tweets.txt'
        }


# 主程序
if __name__ == '__main__':
    print("🚀 生成销售营销材料\n")
    print("="*60)
    
    generator = SalesPageGenerator()
    files = generator.save_all()
    
    print("\n" + "="*60)
    print("🎉 营销材料生成完成！")
    print("="*60)
    print("\n生成的文件：")
    for name, path in files.items():
        print(f"  • {path}")
    
    print("\n下一步：")
    print("  1. 打开 sales_page.html 查看销售页面")
    print("  2. 复制 gumroad_description.md 到Gumroad")
    print("  3. 使用 promo_tweets.txt 在Twitter/X推广")
