#!/usr/bin/env python3
"""
EmailAI - 邮件营销专员
智能邮件营销自动化系统
"""

import os
import json
import re
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmailType(Enum):
    """邮件类型"""
    WELCOME = "welcome"
    PROMOTIONAL = "promotional"
    NEWSLETTER = "newsletter"
    ABANDONED_CART = "abandoned_cart"
    RE_ENGAGEMENT = "re_engagement"
    TRANSACTIONAL = "transactional"
    SURVEY = "survey"


class EmailStatus(Enum):
    """邮件状态"""
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    SENT = "sent"
    DELIVERED = "delivered"
    OPENED = "opened"
    CLICKED = "clicked"
    BOUNCED = "bounced"
    UNSUBSCRIBED = "unsubscribed"


@dataclass
class Subscriber:
    """订阅者"""
    email: str
    name: str = ""
    tags: List[str] = None
    subscribed_at: datetime = None
    last_activity: datetime = None
    engagement_score: float = 0.0
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []
        if self.subscribed_at is None:
            self.subscribed_at = datetime.now()
    
    def to_dict(self) -> Dict:
        return {
            "email": self.email,
            "name": self.name,
            "tags": self.tags,
            "subscribed_at": self.subscribed_at.isoformat() if self.subscribed_at else None,
            "last_activity": self.last_activity.isoformat() if self.last_activity else None,
            "engagement_score": self.engagement_score
        }


@dataclass
class EmailCampaign:
    """邮件营销活动"""
    id: str
    name: str
    email_type: EmailType
    subject: str
    content: str
    sender_name: str
    sender_email: str
    recipients: List[str]
    scheduled_time: Optional[datetime]
    status: EmailStatus
    created_at: datetime
    sent_count: int = 0
    open_count: int = 0
    click_count: int = 0
    
    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "name": self.name,
            "email_type": self.email_type.value,
            "subject": self.subject,
            "content": self.content,
            "sender_name": self.sender_name,
            "sender_email": self.sender_email,
            "recipients": self.recipients,
            "scheduled_time": self.scheduled_time.isoformat() if self.scheduled_time else None,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "sent_count": self.sent_count,
            "open_count": self.open_count,
            "click_count": self.click_count
        }


@dataclass
class EmailMetrics:
    """邮件指标"""
    total_sent: int
    total_delivered: int
    total_opened: int
    total_clicked: int
    total_bounced: int
    total_unsubscribed: int
    
    @property
    def delivery_rate(self) -> float:
        return (self.total_delivered / self.total_sent * 100) if self.total_sent > 0 else 0
    
    @property
    def open_rate(self) -> float:
        return (self.total_opened / self.total_delivered * 100) if self.total_delivered > 0 else 0
    
    @property
    def click_rate(self) -> float:
        return (self.total_clicked / total_delivered * 100) if self.total_delivered > 0 else 0
    
    @property
    def bounce_rate(self) -> float:
        return (self.total_bounced / self.total_sent * 100) if self.total_sent > 0 else 0
    
    def to_dict(self) -> Dict:
        return {
            "total_sent": self.total_sent,
            "total_delivered": self.total_delivered,
            "total_opened": self.total_opened,
            "total_clicked": self.total_clicked,
            "total_bounced": self.total_bounced,
            "total_unsubscribed": self.total_unsubscribed,
            "delivery_rate": round(self.delivery_rate, 2),
            "open_rate": round(self.open_rate, 2),
            "click_rate": round(self.click_rate, 2),
            "bounce_rate": round(self.bounce_rate, 2)
        }


class SubjectLineOptimizer:
    """主题行优化器"""
    
    def __init__(self):
        self.power_words = {
            "urgency": ["限时", "马上", "立即", "最后", "紧急"],
            "curiosity": ["秘密", "揭秘", "真相", "你不知道的"],
            "benefit": ["免费", "优惠", "节省", "赚钱", "提升"],
            "social_proof": ["热门", "推荐", "大家都在用"],
            "personal": ["你", "你的", "专属", "定制"]
        }
        self.spam_words = ["免费", "赚钱", "点击这里", "限时", "立即行动"]
    
    def analyze_subject(self, subject: str) -> Dict:
        """分析主题行"""
        issues = []
        recommendations = []
        score = 100
        
        # 检查长度
        length = len(subject)
        if length < 20:
            issues.append(f"主题太短 ({length}字符)")
            score -= 15
        elif length > 60:
            issues.append(f"主题太长 ({length}字符)")
            score -= 10
        
        # 检查垃圾词
        spam_count = sum(1 for word in self.spam_words if word in subject)
        if spam_count > 0:
            issues.append(f"包含{spam_count}个垃圾邮件触发词")
            score -= spam_count * 10
        
        # 检查个性化
        if "{" not in subject and "你" not in subject and "您的" not in subject:
            recommendations.append("建议添加个性化元素，如收件人姓名")
        
        # 检查紧迫感
        has_urgency = any(word in subject for word in self.power_words["urgency"])
        if not has_urgency:
            recommendations.append("建议添加紧迫感词汇提高打开率")
        
        # 检查数字
        if not re.search(r'\d', subject):
            recommendations.append("建议添加数字增强吸引力")
        
        # 检查表情符号
        if not any(ord(c) > 127 for c in subject):
            recommendations.append("考虑添加表情符号提高视觉吸引力")
        
        return {
            "subject": subject,
            "length": length,
            "score": max(0, score),
            "issues": issues,
            "recommendations": recommendations,
            "optimized_versions": self._generate_variations(subject)
        }
    
    def _generate_variations(self, subject: str) -> List[str]:
        """生成主题行变体"""
        variations = []
        
        # 添加数字
        if not re.search(r'\d', subject):
            variations.append(f"3个{subject}")
        
        # 添加紧迫感
        variations.append(f"限时：{subject}")
        
        # 添加表情符号
        variations.append(f"🎁 {subject}")
        
        return variations[:3]
    
    def generate_subject(self, topic: str, email_type: EmailType) -> str:
        """生成主题行"""
        templates = {
            EmailType.WELCOME: [
                "欢迎加入{name}！你的专属福利已到账 🎁",
                "感谢订阅！这是你的欢迎礼物",
                "{name}，欢迎开启精彩旅程"
            ],
            EmailType.PROMOTIONAL: [
                "限时优惠：节省50%的最后机会",
                "专属折扣码：{code}",
                "🔥 热门产品限时特惠"
            ],
            EmailType.NEWSLETTER: [
                "本周精选：{topic}最新动态",
                "{name}，这是为你准备的内容",
                "行业洞察 #{issue_number}"
            ],
            EmailType.ABANDONED_CART: [
                "你的购物车还在等你 🛒",
                "忘记带走这些宝贝了吗？",
                "限时保留：购物车商品即将过期"
            ],
            EmailType.RE_ENGAGEMENT: [
                "我们想念你，{name}",
                "特别优惠：欢迎回来",
                "好久不见，有新东西想给你看"
            ]
        }
        
        email_templates = templates.get(email_type, templates[EmailType.NEWSLETTER])
        return random.choice(email_templates).format(topic=topic, name="", code="SAVE20")


class ContentPersonalizer:
    """内容个性化器"""
    
    def __init__(self):
        self.placeholders = {
            "{{first_name}}": "名字",
            "{{email}}": "邮箱",
            "{{company}}": "公司",
            "{{last_purchase}}": "上次购买",
            "{{signup_date}}": "注册日期"
        }
    
    def personalize_content(self, template: str, subscriber: Subscriber) -> str:
        """个性化内容"""
        content = template
        
        # 替换占位符
        content = content.replace("{{first_name}}", subscriber.name.split()[0] if subscriber.name else "朋友")
        content = content.replace("{{email}}", subscriber.email)
        content = content.replace("{{company}}", "")
        content = content.replace("{{signup_date}}", subscriber.subscribed_at.strftime("%Y年%m月%d日"))
        
        return content
    
    def add_dynamic_content(self, content: str, content_type: str, data: Dict) -> str:
        """添加动态内容"""
        if content_type == "product_recommendations":
            products = data.get("products", [])
            product_html = "\n".join([
                f"<div class='product'>{p['name']} - ${p['price']}</div>"
                for p in products[:3]
            ])
            return content.replace("{{product_recommendations}}", product_html)
        
        elif content_type == "recent_activity":
            activities = data.get("activities", [])
            activity_text = "\n".join([f"• {a}" for a in activities[:5]])
            return content.replace("{{recent_activity}}", activity_text)
        
        return content


class SegmentationEngine:
    """分段引擎"""
    
    def __init__(self):
        self.segments = {}
    
    def segment_by_engagement(self, subscribers: List[Subscriber]) -> Dict[str, List[Subscriber]]:
        """按参与度分段"""
        segments = {
            "highly_engaged": [],
            "moderately_engaged": [],
            "low_engaged": [],
            "inactive": []
        }
        
        for sub in subscribers:
            if sub.engagement_score >= 80:
                segments["highly_engaged"].append(sub)
            elif sub.engagement_score >= 50:
                segments["moderately_engaged"].append(sub)
            elif sub.engagement_score >= 20:
                segments["low_engaged"].append(sub)
            else:
                segments["inactive"].append(sub)
        
        return segments
    
    def segment_by_tags(self, subscribers: List[Subscriber], tags: List[str]) -> Dict[str, List[Subscriber]]:
        """按标签分段"""
        segments = {tag: [] for tag in tags}
        segments["untagged"] = []
        
        for sub in subscribers:
            matched = False
            for tag in sub.tags:
                if tag in segments:
                    segments[tag].append(sub)
                    matched = True
            if not matched:
                segments["untagged"].append(sub)
        
        return segments
    
    def segment_by_date(self, subscribers: List[Subscriber]) -> Dict[str, List[Subscriber]]:
        """按订阅日期分段"""
        segments = {
            "new": [],      # < 7 days
            "recent": [],   # 7-30 days
            "established": [], # 30-90 days
            "veteran": []   # > 90 days
        }
        
        now = datetime.now()
        
        for sub in subscribers:
            days = (now - sub.subscribed_at).days
            if days < 7:
                segments["new"].append(sub)
            elif days < 30:
                segments["recent"].append(sub)
            elif days < 90:
                segments["established"].append(sub)
            else:
                segments["veteran"].append(sub)
        
        return segments


class EmailAI:
    """邮件营销专员主类"""
    
    def __init__(self, config_path: str = "config.json"):
        self.config = self._load_config(config_path)
        self.subject_optimizer = SubjectLineOptimizer()
        self.content_personalizer = ContentPersonalizer()
        self.segmentation_engine = SegmentationEngine()
        self.subscribers: Dict[str, Subscriber] = {}
        self.campaigns: Dict[str, EmailCampaign] = {}
        self.metrics = EmailMetrics(0, 0, 0, 0, 0, 0)
        
        logger.info("EmailAI initialized successfully")
    
    def _load_config(self, config_path: str) -> Dict:
        """加载配置"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return self._default_config()
    
    def _default_config(self) -> Dict:
        """默认配置"""
        return {
            "sender_name": "AgentVerse",
            "sender_email": "noreply@agentverse.com",
            "default_template": "modern",
            "send_time_optimization": True,
            "ab_testing": True
        }
    
    def add_subscriber(self, email: str, name: str = "", tags: List[str] = None) -> Subscriber:
        """添加订阅者"""
        if tags is None:
            tags = []
        
        subscriber = Subscriber(email=email, name=name, tags=tags)
        self.subscribers[email] = subscriber
        
        logger.info(f"Subscriber added: {email}")
        return subscriber
    
    def remove_subscriber(self, email: str) -> bool:
        """移除订阅者"""
        if email in self.subscribers:
            del self.subscribers[email]
            logger.info(f"Subscriber removed: {email}")
            return True
        return False
    
    def create_campaign(self, name: str, email_type: EmailType, 
                       subject: str, content: str,
                       recipients: List[str] = None) -> EmailCampaign:
        """创建邮件活动"""
        campaign_id = f"campaign_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{random.randint(1000, 9999)}"
        
        if recipients is None:
            recipients = list(self.subscribers.keys())
        
        campaign = EmailCampaign(
            id=campaign_id,
            name=name,
            email_type=email_type,
            subject=subject,
            content=content,
            sender_name=self.config.get("sender_name", "AgentVerse"),
            sender_email=self.config.get("sender_email", "noreply@agentverse.com"),
            recipients=recipients,
            scheduled_time=None,
            status=EmailStatus.DRAFT,
            created_at=datetime.now()
        )
        
        self.campaigns[campaign_id] = campaign
        logger.info(f"Campaign created: {campaign_id}")
        
        return campaign
    
    def optimize_subject(self, subject: str) -> Dict:
        """优化主题行"""
        return self.subject_optimizer.analyze_subject(subject)
    
    def personalize_email(self, campaign_id: str, subscriber_email: str) -> str:
        """个性化邮件"""
        campaign = self.campaigns.get(campaign_id)
        subscriber = self.subscribers.get(subscriber_email)
        
        if not campaign or not subscriber:
            return ""
        
        return self.content_personalizer.personalize_content(
            campaign.content, subscriber
        )
    
    def segment_subscribers(self, segment_type: str = "engagement") -> Dict:
        """分段订阅者"""
        subscribers_list = list(self.subscribers.values())
        
        if segment_type == "engagement":
            return self.segmentation_engine.segment_by_engagement(subscribers_list)
        elif segment_type == "date":
            return self.segmentation_engine.segment_by_date(subscribers_list)
        else:
            return {"all": subscribers_list}
    
    def schedule_campaign(self, campaign_id: str, send_time: datetime) -> bool:
        """安排邮件活动"""
        campaign = self.campaigns.get(campaign_id)
        if not campaign:
            return False
        
        campaign.scheduled_time = send_time
        campaign.status = EmailStatus.SCHEDULED
        
        logger.info(f"Campaign scheduled: {campaign_id} at {send_time}")
        return True
    
    def get_campaign_metrics(self, campaign_id: str = None) -> Dict:
        """获取活动指标"""
        if campaign_id:
            campaign = self.campaigns.get(campaign_id)
            if campaign:
                return {
                    "campaign_id": campaign_id,
                    "sent": campaign.sent_count,
                    "opened": campaign.open_count,
                    "clicked": campaign.click_count,
                    "open_rate": round(campaign.open_count / campaign.sent_count * 100, 2) if campaign.sent_count > 0 else 0,
                    "click_rate": round(campaign.click_count / campaign.sent_count * 100, 2) if campaign.sent_count > 0 else 0
                }
            return {}
        
        return self.metrics.to_dict()
    
    def generate_report(self, period: str = "last_30_days") -> str:
        """生成报告"""
        metrics = self.metrics
        
        report = f"""
# 邮件营销报告

## 报告周期: {period}
生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## 📊 关键指标

| 指标 | 数值 | 行业基准 |
|------|------|----------|
| 发送量 | {metrics.total_sent:,} | - |
| 送达量 | {metrics.total_delivered:,} | - |
| 打开量 | {metrics.total_opened:,} | - |
| 点击量 | {metrics.total_clicked:,} | - |

## 📈 比率分析

- **送达率**: {metrics.delivery_rate:.1f}% (基准: 95%+)
- **打开率**: {metrics.open_rate:.1f}% (基准: 20-25%)
- **点击率**: {metrics.click_rate:.1f}% (基准: 2-5%)
- **退订率**: {metrics.total_unsubscribed / metrics.total_sent * 100:.2f}% (基准: <0.5%)

## 📋 活动列表

| 活动名称 | 类型 | 状态 | 发送量 | 打开率 |
|----------|------|------|--------|--------|
"""
        
        for campaign in list(self.campaigns.values())[-5:]:
            open_rate = f"{campaign.open_count / campaign.sent_count * 100:.1f}%" if campaign.sent_count > 0 else "N/A"
            report += f"| {campaign.name} | {campaign.email_type.value} | {campaign.status.value} | {campaign.sent_count} | {open_rate} |\n"
        
        report += """
## 💡 优化建议

1. **主题行优化**: A/B测试不同主题行
2. **发送时间**: 测试最佳发送时间
3. **内容个性化**: 提高个性化程度
4. **分段策略**: 精细化用户分段
5. **再激活**: 对不活跃用户进行再激活

---
*报告由 EmailAI 自动生成*
"""
        
        return report
    
    def export_data(self, filepath: str):
        """导出数据"""
        data = {
            "subscribers": [s.to_dict() for s in self.subscribers.values()],
            "campaigns": [c.to_dict() for c in self.campaigns.values()],
            "metrics": self.metrics.to_dict(),
            "config": self.config,
            "export_time": datetime.now().isoformat()
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Data exported to {filepath}")


# 使用示例
if __name__ == "__main__":
    email_ai = EmailAI()
    
    print("=" * 60)
    print("EmailAI - 邮件营销专员")
    print("=" * 60)
    
    # 添加订阅者
    print("\n📧 添加订阅者")
    print("-" * 60)
    
    subscribers_data = [
        ("user1@example.com", "张三", ["vip", "tech"]),
        ("user2@example.com", "李四", ["new"]),
        ("user3@example.com", "王五", ["vip", "marketing"]),
        ("user4@example.com", "赵六", []),
    ]
    
    for email, name, tags in subscribers_data:
        sub = email_ai.add_subscriber(email, name, tags)
        print(f"✅ {name} ({email}) - 标签: {', '.join(tags) if tags else '无'}")
    
    # 创建邮件活动
    print("\n📨 创建邮件活动")
    print("-" * 60)
    
    welcome_template = """
    <h1>欢迎{{first_name}}！</h1>
    <p>感谢订阅我们的邮件列表。</p>
    <p>作为欢迎礼物，我们为你准备了专属优惠码：<strong>WELCOME20</strong></p>
    <p>期待与你分享更多有价值的内容！</p>
    """
    
    campaign = email_ai.create_campaign(
        name="欢迎新用户",
        email_type=EmailType.WELCOME,
        subject="🎁 欢迎加入！你的专属福利已到账",
        content=welcome_template,
        recipients=list(email_ai.subscribers.keys())
    )
    
    print(f"✅ 活动创建: {campaign.name}")
    print(f"   ID: {campaign.id}")
    print(f"   收件人: {len(campaign.recipients)}人")
    
    # 优化主题行
    print("\n✨ 主题行优化")
    print("-" * 60)
    
    subject_analysis = email_ai.optimize_subject(campaign.subject)
    print(f"原始主题: {subject_analysis['subject']}")
    print(f"评分: {subject_analysis['score']}/100")
    
    if subject_analysis['issues']:
        print(f"\n⚠️ 问题:")
        for issue in subject_analysis['issues']:
            print(f"  • {issue}")
    
    if subject_analysis['recommendations']:
        print(f"\n💡 建议:")
        for rec in subject_analysis['recommendations']:
            print(f"  • {rec}")
    
    # 用户分段
    print("\n👥 用户分段分析")
    print("-" * 60)
    
    segments = email_ai.segment_subscribers("engagement")
    for segment_name, segment_subs in segments.items():
        print(f"{segment_name}: {len(segment_subs)}人")
    
    # 个性化示例
    print("\n🎯 个性化邮件示例")
    print("-" * 60)
    
    sample_email = "user1@example.com"
    personalized = email_ai.personalize_email(campaign.id, sample_email)
    print(f"收件人: {sample_email}")
    print(f"个性化内容预览:")
    print(personalized[:200] + "...")
    
    # 生成报告
    print("\n📊 生成营销报告")
    print("-" * 60)
    
    # 模拟一些数据
    email_ai.metrics.total_sent = 1000
    email_ai.metrics.total_delivered = 980
    email_ai.metrics.total_opened = 245
    email_ai.metrics.total_clicked = 52
    
    report = email_ai.generate_report()
    print(report[:800] + "...")
    
    print("\n" + "=" * 60)
    print("✅ 演示完成!")
    print("=" * 60)
