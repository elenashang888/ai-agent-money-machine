#!/usr/bin/env python3
"""
EmailAI - 邮件营销专员
Monthly Potential: $1000-5000
功能：邮件序列生成、A/B测试、发送优化、数据分析
"""

import json
import random
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from collections import defaultdict

class EmailAI:
    """邮件营销专员 - 智能邮件自动化系统"""
    
    def __init__(self, config_path: str = "config.json"):
        self.config = self._load_config(config_path)
        self.metrics = {
            'emails_generated': 0,
            'sequences_created': 0,
            'campaigns_sent': 0,
            'ab_tests_run': 0
        }
        
        # 邮件模板库
        self.templates = self._init_templates()
        
        # 邮件序列库
        self.sequences = {}
        
        # 用户分群
        self.segments = {}
        
        # 发送历史
        self.send_history = []
        
    def _load_config(self, path: str) -> Dict:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return self._default_config()
    
    def _default_config(self) -> Dict:
        return {
            'from_name': 'AI Assistant',
            'from_email': 'noreply@example.com',
            'reply_to': 'support@example.com',
            'default_subject_style': 'curiosity',
            'send_time_optimization': True,
            'timezone': 'UTC',
            'max_emails_per_sequence': 7,
            'ab_test_sample_size': 1000
        }
    
    def _init_templates(self) -> Dict:
        """初始化邮件模板"""
        return {
            'welcome': {
                'name': '欢迎邮件',
                'subject_templates': [
                    '欢迎加入{name}！这是你需要的入门指南',
                    '🎉 欢迎！让我们开始吧',
                    '你的{name}账号已激活'
                ],
                'body_template': """<h1>欢迎，{{first_name}}！</h1>

<p>感谢你加入<strong>{{company_name}}</strong>！</p>

<p>我是你的专属助手，接下来几天我会带你了解：</p>
<ul>
    <li>✅ 如何快速上手</li>
    <li>✅ 核心功能介绍</li>
    <li>✅ 最佳实践分享</li>
</ul>

<p><strong>下一步：</strong><a href="{{onboarding_link}}">完成你的设置</a></p>

<p>有任何问题随时回复这封邮件！</p>

<p>祝好，<br>{{sender_name}}</p>"""
            },
            'onboarding': {
                'name': '引导邮件',
                'subject_templates': [
                    'Day {{day}}: {{topic}}',
                    '快速上手：{{topic}}',
                    '{{first_name}}，这一步很关键'
                ],
                'body_template': """<h2>Day {{day}}: {{topic}}</h2>

<p>嗨 {{first_name}}，</p>

<p>今天我们来学习<strong>{{topic}}</strong>。</p>

<p>{{content}}</p>

<p><strong>今日行动：</strong></p>
<ol>
    <li>{{action_1}}</li>
    <li>{{action_2}}</li>
    <li>{{action_3}}</li>
</ol>

<p><a href="{{cta_link}}" style="background:#007bff;color:white;padding:12px 24px;text-decoration:none;border-radius:4px;">{{cta_text}}</a></p>

<p>明天见！<br>{{sender_name}}</p>"""
            },
            'promotional': {
                'name': '促销邮件',
                'subject_templates': [
                    '🔥 {{discount}}% OFF - 限时{{hours}}小时',
                    '{{first_name}}，专属优惠等你领取',
                    '最后{{hours}}小时！{{product_name}}特价',
                    '💰 省${{savings}}的机会来了'
                ],
                'body_template': """<h1>{{headline}}</h1>

<p>嗨 {{first_name}}，</p>

<p>{{product_name}}正在<strong>{{discount}}% OFF</strong>促销！</p>

<div style="background:#f8f9fa;padding:20px;margin:20px 0;text-align:center;">
    <h2 style="color:#dc3545;">{{discount}}% OFF</h2>
    <p>原价: <del>${{original_price}}</del></p>
    <p style="font-size:24px;font-weight:bold;">现价: ${{discounted_price}}</p>
    <p>节省: ${{savings}}</p>
</div>

<p><strong>为什么现在购买：</strong></p>
<ul>
    <li>✅ {{benefit_1}}</li>
    <li>✅ {{benefit_2}}</li>
    <li>✅ {{benefit_3}}</li>
</ul>

<p style="text-align:center;">
    <a href="{{buy_link}}" style="background:#28a745;color:white;padding:15px 30px;text-decoration:none;border-radius:5px;font-size:18px;">立即购买</a>
</p>

<p><strong>⏰ 优惠截止：</strong>{{deadline}}</p>

<p>{{sender_name}}</p>"""
            },
            're_engagement': {
                'name': '挽回邮件',
                'subject_templates': [
                    '{{first_name}}，我们想念你',
                    '好久不见！有新功能等你体验',
                    '专属回归礼：{{offer}}',
                    '再给你一次机会 💙'
                ],
                'body_template': """<h1>嗨 {{first_name}}，好久不见！</h1>

<p>注意到你有一段时间没登录了。</p>

<p>我们最近更新了很多：</p>
<ul>
    <li>🚀 {{update_1}}</li>
    <li>✨ {{update_2}}</li>
    <li>🎁 {{update_3}}</li>
</ul>

<p><strong>特别为你准备：</strong>{{special_offer}}</p>

<p><a href="{{return_link}}" style="background:#6c757d;color:white;padding:12px 24px;text-decoration:none;border-radius:4px;">回到{{company_name}}</a></p>

<p>期待你的回归！<br>{{sender_name}}</p>"""
            },
            'newsletter': {
                'name': '新闻邮件',
                'subject_templates': [
                    '{{month}}月精选：{{highlight}}',
                    '本周必读：{{topic_1}}、{{topic_2}}',
                    '{{company_name}}周报 - {{date}}'
                ],
                'body_template': """<h1>{{company_name}} {{month}}月精选</h1>

<p>嗨 {{first_name}}，</p>

<p>本月为你精选了以下内容：</p>

{{articles}}

<p><strong>💡 本月亮点：</strong>{{highlight}}</p>

<p><a href="{{read_more_link}}">阅读更多 →</a></p>

<p>{{sender_name}}</p>"""
            },
            'abandoned_cart': {
                'name': '购物车挽回',
                'subject_templates': [
                    '{{first_name}}，忘记结账了吗？',
                    '你的购物车还在等你 🛒',
                    '商品即将售罄 - 立即完成订单',
                    '再减{{extra_discount}}%，仅限今天'
                ],
                'body_template': """<h1>你的购物车商品还在等你</h1>

<p>嗨 {{first_name}}，</p>

<p>你添加到购物车的商品：</p>

<div style="border:1px solid #ddd;padding:15px;margin:15px 0;">
    <h3>{{product_name}}</h3>
    <p>{{product_description}}</p>
    <p><strong>价格: ${{price}}</strong></p>
</div>

<p><a href="{{checkout_link}}" style="background:#007bff;color:white;padding:12px 24px;text-decoration:none;border-radius:4px;">完成订单</a></p>

<p>有问题？回复这封邮件联系我们。</p>"""
            }
        }
    
    def generate_email(self, template_type: str, variables: Dict, tone: str = 'professional') -> Dict:
        """生成单封邮件"""
        template = self.templates.get(template_type, self.templates['welcome'])
        
        # 选择主题行
        subject_template = random.choice(template['subject_templates'])
        subject = self._fill_template(subject_template, variables)
        
        # 生成正文
        body = self._fill_template(template['body_template'], variables)
        
        # 生成纯文本版本
        text_body = self._html_to_text(body)
        
        self.metrics['emails_generated'] += 1
        
        return {
            'template_type': template_type,
            'subject': subject,
            'html_body': body,
            'text_body': text_body,
            'variables': variables,
            'tone': tone,
            'estimated_open_rate': self._estimate_open_rate(template_type, subject),
            'estimated_click_rate': self._estimate_click_rate(template_type),
            'generated_at': datetime.now().isoformat()
        }
    
    def _fill_template(self, template: str, variables: Dict) -> str:
        """填充模板变量"""
        result = template
        for key, value in variables.items():
            result = result.replace(f'{{{{{key}}}}}', str(value))
        return result
    
    def _html_to_text(self, html: str) -> str:
        """HTML转纯文本"""
        # 简单的HTML标签移除
        text = html.replace('<h1>', '\n').replace('</h1>', '\n')
        text = text.replace('<h2>', '\n').replace('</h2>', '\n')
        text = text.replace('<p>', '\n').replace('</p>', '')
        text = text.replace('<li>', '- ').replace('</li>', '')
        text = text.replace('<strong>', '').replace('</strong>', '')
        text = text.replace('<a href="', '').replace('">', ': ').replace('</a>', '')
        # 移除其他标签
        import re
        text = re.sub(r'<[^>]+>', '', text)
        return text.strip()
    
    def _estimate_open_rate(self, template_type: str, subject: str) -> float:
        """预估打开率"""
        base_rates = {
            'welcome': 0.65,
            'onboarding': 0.45,
            'promotional': 0.20,
            're_engagement': 0.35,
            'newsletter': 0.30,
            'abandoned_cart': 0.40
        }
        
        base = base_rates.get(template_type, 0.25)
        
        # 根据主题行调整
        if '🔥' in subject or '💰' in subject or '🎉' in subject:
            base += 0.05
        if '?' in subject:
            base += 0.03
        if 'OFF' in subject or '%' in subject:
            base += 0.02
        
        return round(min(0.80, base), 2)
    
    def _estimate_click_rate(self, template_type: str) -> float:
        """预估点击率"""
        base_rates = {
            'welcome': 0.35,
            'onboarding': 0.25,
            'promotional': 0.08,
            're_engagement': 0.15,
            'newsletter': 0.10,
            'abandoned_cart': 0.20
        }
        return base_rates.get(template_type, 0.10)
    
    def create_sequence(self, sequence_name: str, sequence_type: str, steps: List[Dict]) -> Dict:
        """创建邮件序列"""
        sequence = {
            'name': sequence_name,
            'type': sequence_type,
            'steps': [],
            'created_at': datetime.now().isoformat()
        }
        
        for i, step in enumerate(steps):
            delay = step.get('delay', i * 1)  # 默认每天一封
            
            sequence['steps'].append({
                'step_number': i + 1,
                'template_type': step.get('template', 'onboarding'),
                'delay_days': delay,
                'subject_override': step.get('subject'),
                'variables': step.get('variables', {}),
                'conditions': step.get('conditions', {})
            })
        
        self.sequences[sequence_name] = sequence
        self.metrics['sequences_created'] += 1
        
        return sequence
    
    def create_welcome_sequence(self) -> Dict:
        """创建欢迎序列"""
        steps = [
            {
                'template': 'welcome',
                'delay': 0,
                'variables': {'topic': '欢迎加入'}
            },
            {
                'template': 'onboarding',
                'delay': 1,
                'variables': {'day': 1, 'topic': '快速设置', 'content': '今天我们来完成基础设置...'}
            },
            {
                'template': 'onboarding',
                'delay': 2,
                'variables': {'day': 2, 'topic': '核心功能', 'content': '了解最重要的功能...'}
            },
            {
                'template': 'onboarding',
                'delay': 4,
                'variables': {'day': 3, 'topic': '高级技巧', 'content': '掌握这些技巧提升效率...'}
            },
            {
                'template': 'promotional',
                'delay': 7,
                'variables': {'discount': 20, 'product_name': 'Pro版升级'}
            }
        ]
        
        return self.create_sequence('welcome_sequence', 'onboarding', steps)
    
    def create_abandoned_cart_sequence(self) -> Dict:
        """创建购物车挽回序列"""
        steps = [
            {
                'template': 'abandoned_cart',
                'delay': 0,  # 1小时后
                'variables': {'urgency': 'low'}
            },
            {
                'template': 'abandoned_cart',
                'delay': 1,  # 1天后
                'variables': {'urgency': 'medium', 'extra_discount': 10}
            },
            {
                'template': 'promotional',
                'delay': 3,  # 3天后
                'variables': {'urgency': 'high', 'discount': 25}
            }
        ]
        
        return self.create_sequence('abandoned_cart', 'conversion', steps)
    
    def ab_test(self, email_type: str, variant_a: Dict, variant_b: Dict, sample_size: int = 1000) -> Dict:
        """A/B测试"""
        # 模拟测试结果
        open_rate_a = random.uniform(0.20, 0.45)
        open_rate_b = random.uniform(0.20, 0.45)
        
        click_rate_a = open_rate_a * random.uniform(0.20, 0.50)
        click_rate_b = open_rate_b * random.uniform(0.20, 0.50)
        
        conversion_rate_a = click_rate_a * random.uniform(0.05, 0.20)
        conversion_rate_b = click_rate_b * random.uniform(0.05, 0.20)
        
        # 确定获胜者
        winner = 'A' if open_rate_a > open_rate_b else 'B'
        confidence = random.uniform(85, 99)
        
        self.metrics['ab_tests_run'] += 1
        
        return {
            'test_id': f"AB_{self.metrics['ab_tests_run']:04d}",
            'email_type': email_type,
            'sample_size': sample_size,
            'variant_a': {
                'subject': variant_a.get('subject'),
                'open_rate': round(open_rate_a, 3),
                'click_rate': round(click_rate_a, 3),
                'conversion_rate': round(conversion_rate_a, 3)
            },
            'variant_b': {
                'subject': variant_b.get('subject'),
                'open_rate': round(open_rate_b, 3),
                'click_rate': round(click_rate_b, 3),
                'conversion_rate': round(conversion_rate_b, 3)
            },
            'winner': winner,
            'confidence': f"{confidence}%",
            'improvement': f"{abs(open_rate_a - open_rate_b) / min(open_rate_a, open_rate_b) * 100:.1f}%",
            'recommendation': f"使用Variant {winner}，预计提升{abs(open_rate_a - open_rate_b):.1%}打开率",
            'tested_at': datetime.now().isoformat()
        }
    
    def optimize_send_time(self, segment: str = 'all') -> Dict:
        """优化发送时间"""
        # 模拟最佳发送时间分析
        best_times = {
            'all': {'day': 'Tuesday', 'hour': 10, 'open_rate': 0.28},
            'new_subscribers': {'day': 'Wednesday', 'hour': 9, 'open_rate': 0.32},
            'engaged': {'day': 'Thursday', 'hour': 14, 'open_rate': 0.35},
            'at_risk': {'day': 'Monday', 'hour': 11, 'open_rate': 0.22}
        }
        
        return {
            'segment': segment,
            'optimal_time': best_times.get(segment, best_times['all']),
            'recommendation': f"建议在{best_times[segment]['day']}上午{best_times[segment]['hour']}点发送",
            'expected_improvement': f"{random.randint(10, 30)}%"
        }
    
    def segment_users(self, users: List[Dict]) -> Dict:
        """用户分群"""
        segments = {
            'new': [],  # 新订阅者
            'engaged': [],  # 活跃用户
            'at_risk': [],  # 流失风险
            'churned': [],  # 已流失
            'vip': []  # 高价值用户
        }
        
        for user in users:
            days_since_signup = user.get('days_since_signup', 0)
            last_open_days = user.get('last_open_days', 999)
            total_opens = user.get('total_opens', 0)
            
            if days_since_signup <= 7:
                segments['new'].append(user)
            elif last_open_days > 60:
                segments['churned'].append(user)
            elif last_open_days > 30:
                segments['at_risk'].append(user)
            elif total_opens > 20:
                segments['vip'].append(user)
            else:
                segments['engaged'].append(user)
        
        self.segments = segments
        
        return {
            'total_users': len(users),
            'segments': {k: len(v) for k, v in segments.items()},
            'segment_details': {
                'new': '新订阅者，需要引导',
                'engaged': '活跃用户，可以推送促销',
                'at_risk': '有流失风险，需要挽回',
                'churned': '已流失，尝试重新激活',
                'vip': '高价值用户，提供专属服务'
            },
            'recommendations': [
                f'为{len(segments["new"])}位新用户创建欢迎序列',
                f'向{len(segments["engaged"])}位活跃用户发送促销',
                f'对{len(segments["at_risk"])}位风险用户进行挽回'
            ]
        }
    
    def campaign_report(self, campaign_id: str) -> Dict:
        """生成活动报告"""
        # 模拟活动数据
        sent = random.randint(5000, 50000)
        delivered = int(sent * 0.98)
        opened = int(delivered * random.uniform(0.20, 0.40))
        clicked = int(opened * random.uniform(0.15, 0.35))
        converted = int(clicked * random.uniform(0.05, 0.20))
        
        revenue = converted * random.randint(50, 500)
        
        return {
            'campaign_id': campaign_id,
            'sent': sent,
            'delivered': delivered,
            'opened': opened,
            'clicked': clicked,
            'converted': converted,
            'rates': {
                'delivery': round(delivered / sent * 100, 2),
                'open': round(opened / delivered * 100, 2),
                'click': round(clicked / opened * 100, 2),
                'conversion': round(converted / clicked * 100, 2)
            },
            'revenue': revenue,
            'roi': round(revenue / (sent * 0.001), 2),  # 假设每封邮件成本$0.001
            'top_performing_subject': random.choice(['🔥限时优惠', '专属福利', '新功能上线']),
            'recommendations': [
                '尝试更多表情符号主题行',
                '优化移动端显示',
                '增加个性化内容'
            ],
            'generated_at': datetime.now().isoformat()
        }
    
    def get_metrics(self) -> Dict:
        """获取邮件营销指标"""
        emails = self.metrics['emails_generated']
        sequences = self.metrics['sequences_created']
        campaigns = self.metrics['campaigns_sent']
        tests = self.metrics['ab_tests_run']
        
        # 计算价值
        # 假设每封邮件价值$5，每个序列价值$100，每次活动价值$200
        value_generated = emails * 5 + sequences * 100 + campaigns * 200
        
        # 月度预估
        monthly_emails = 100
        monthly_sequences = 5
        monthly_campaigns = 10
        monthly_value = monthly_emails * 5 + monthly_sequences * 100 + monthly_campaigns * 200
        
        return {
            'emails_generated': emails,
            'sequences_created': sequences,
            'campaigns_sent': campaigns,
            'ab_tests_run': tests,
            'value_generated_usd': value_generated,
            'monthly_projection_usd': monthly_value,
            'avg_open_rate': '28%',
            'avg_click_rate': '8%',
            'avg_conversion_rate': '2%'
        }


# 演示模式
if __name__ == '__main__':
    agent = EmailAI()
    
    print("=" * 50)
    print("📧 EmailAI - 邮件营销专员")
    print("=" * 50)
    
    # 生成欢迎邮件
    print("\n✉️ 生成欢迎邮件：")
    welcome_email = agent.generate_email('welcome', {
        'first_name': '小明',
        'company_name': 'AI工具箱',
        'onboarding_link': 'https://example.com/onboarding',
        'sender_name': 'AI助手'
    })
    print(f"主题: {welcome_email['subject']}")
    print(f"预估打开率: {welcome_email['estimated_open_rate']}")
    print(f"预估点击率: {welcome_email['estimated_click_rate']}")
    
    # 生成促销邮件
    print("\n🎁 生成促销邮件：")
    promo_email = agent.generate_email('promotional', {
        'first_name': '用户',
        'discount': 30,
        'hours': 24,
        'product_name': 'Pro版',
        'original_price': 99,
        'discounted_price': 69,
        'savings': 30,
        'benefit_1': '无限量使用',
        'benefit_2': '优先客服支持',
        'benefit_3': '高级分析功能',
        'deadline': '今晚12点',
        'sender_name': '销售团队'
    })
    print(f"主题: {promo_email['subject']}")
    print(f"预估打开率: {promo_email['estimated_open_rate']}")
    
    # 创建欢迎序列
    print("\n📋 创建欢迎序列：")
    welcome_seq = agent.create_welcome_sequence()
    print(f"序列名称: {welcome_seq['name']}")
    print(f"步骤数: {len(welcome_seq['steps'])}")
    for step in welcome_seq['steps']:
        print(f"  Step {step['step_number']}: {step['template_type']} (延迟{step['delay_days']}天)")
    
    # A/B测试
    print("\n🧪 A/B测试：")
    variant_a = {'subject': '🔥 限时50% OFF - 仅剩24小时'}
    variant_b = {'subject': '你的专属优惠来了'}
    ab_result = agent.ab_test('promotional', variant_a, variant_b)
    print(f"测试ID: {ab_result['test_id']}")
    print(f"获胜者: Variant {ab_result['winner']}")
    print(f"置信度: {ab_result['confidence']}")
    print(f"提升幅度: {ab_result['improvement']}")
    print(f"建议: {ab_result['recommendation']}")
    
    # 发送时间优化
    print("\n⏰ 发送时间优化：")
    send_time = agent.optimize_send_time('engaged')
    print(f"目标群体: {send_time['segment']}")
    print(f"最佳时间: {send_time['optimal_time']}")
    print(f"建议: {send_time['recommendation']}")
    
    # 用户分群
    print("\n👥 用户分群：")
    sample_users = [
        {'email': 'user1@test.com', 'days_since_signup': 5, 'last_open_days': 2, 'total_opens': 3},
        {'email': 'user2@test.com', 'days_since_signup': 30, 'last_open_days': 5, 'total_opens': 25},
        {'email': 'user3@test.com', 'days_since_signup': 60, 'last_open_days': 45, 'total_opens': 10},
        {'email': 'user4@test.com', 'days_since_signup': 90, 'last_open_days': 70, 'total_opens': 5}
    ]
    segmentation = agent.segment_users(sample_users)
    print(f"总用户数: {segmentation['total_users']}")
    for segment, count in segmentation['segments'].items():
        print(f"  {segment}: {count}人")
    
    # 活动报告
    print("\n📊 活动报告：")
    report = agent.campaign_report('CAMP_001')
    print(f"发送量: {report['sent']}")
    print(f"送达率: {report['rates']['delivery']}%")
    print(f"打开率: {report['rates']['open']}%")
    print(f"点击率: {report['rates']['click']}%")
    print(f"转化率: {report['rates']['conversion']}%")
    print(f"收入: ${report['revenue']}")
    print(f"ROI: {report['roi']}x")
    
    # 显示指标
    print("\n💰 邮件营销指标：")
    metrics = agent.get_metrics()
    for key, value in metrics.items():
        print(f"  {key}: {value}")
