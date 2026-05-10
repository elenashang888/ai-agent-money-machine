#!/usr/bin/env python3
"""
ContentAI - 内容创作助手
Monthly Potential: $500-3000
功能：自动生成小红书/公众号/知乎/推特内容
"""

import json
import random
from typing import Dict, List
from datetime import datetime

class ContentAI:
    """AI内容创作助手 - 多平台内容自动生成"""
    
    def __init__(self, config_path: str = "config.json"):
        self.config = self._load_config(config_path)
        self.metrics = {
            'posts_generated': 0,
            'time_saved_hours': 0,
            'platforms_used': []
        }
        
        # 内容模板库
        self.templates = {
            'xiaohongshu': {
                'style': 'emoji丰富，口语化，有网感',
                'structure': ['钩子开头', '痛点共鸣', '解决方案', '行动号召'],
                'hashtags': ['#干货分享', '#自我提升', '#搞钱', '#副业', '#AI工具']
            },
            'wechat': {
                'style': '专业深度，逻辑清晰',
                'structure': ['标题党', '引言', '正文分点', '总结升华'],
                'hashtags': []
            },
            'zhihu': {
                'style': '理性分析，数据支撑',
                'structure': ['问题重述', '背景分析', '核心观点', '案例论证', '总结'],
                'hashtags': []
            },
            'twitter': {
                'style': '简洁有力，观点鲜明',
                'structure': ['核心观点', '展开论述', 'call to action'],
                'hashtags': ['#AI', '#buildinpublic', '#indiehackers']
            }
        }
    
    def _load_config(self, path: str) -> Dict:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return self._default_config()
    
    def _default_config(self) -> Dict:
        return {
            'platforms': ['xiaohongshu', 'wechat', 'zhihu', 'twitter'],
            'topics': ['AI工具', '副业赚钱', '个人成长', '效率提升'],
            'output_dir': './content_output',
            'api_key': ''
        }
    
    def generate_post(self, topic: str, platform: str, tone: str = 'professional') -> Dict:
        """生成单篇内容"""
        template = self.templates.get(platform, self.templates['wechat'])
        
        # 生成内容（模拟AI生成）
        content = self._create_content(topic, platform, template, tone)
        
        self.metrics['posts_generated'] += 1
        self.metrics['time_saved_hours'] += 1.5  # 每篇节省1.5小时
        
        if platform not in self.metrics['platforms_used']:
            self.metrics['platforms_used'].append(platform)
        
        return {
            'platform': platform,
            'topic': topic,
            'title': content['title'],
            'body': content['body'],
            'hashtags': content['hashtags'],
            'estimated_engagement': self._estimate_engagement(platform),
            'created_at': datetime.now().isoformat()
        }
    
    def _create_content(self, topic: str, platform: str, template: Dict, tone: str) -> Dict:
        """创建内容核心逻辑"""
        
        # 标题生成
        title_templates = {
            'xiaohongshu': [
                f"🔥{topic}月入过万？我用这个方法做到了！",
                f"💡{topic}新手必看｜3步搞定",
                f"✨{topic}攻略｜亲测有效"
            ],
            'wechat': [
                f"深度解析：{topic}的底层逻辑",
                f"{topic}：从0到1的完整指南",
                f"为什么{topic}能改变你的生活"
            ],
            'zhihu': [
                f"{topic}真的有用吗？我用数据说话",
                f"如何系统学习{topic}？",
                f"{topic}避坑指南"
            ],
            'twitter': [
                f"Just discovered {topic} and it's game-changing 🚀",
                f"Thread: How I mastered {topic} in 30 days",
                f"Hot take: {topic} is underrated"
            ]
        }
        
        title = random.choice(title_templates.get(platform, title_templates['wechat']))
        
        # 正文生成
        body = self._generate_body(topic, platform, template)
        
        return {
            'title': title,
            'body': body,
            'hashtags': template.get('hashtags', [])
        }
    
    def _generate_body(self, topic: str, platform: str, template: Dict) -> str:
        """生成正文内容"""
        if platform == 'xiaohongshu':
            return f"""姐妹们！今天分享{topic}的干货👇

💔 你是不是也遇到这些问题？
• 不知道怎么开始
• 试了几次就放弃
• 看不到效果很焦虑

✅ 我的解决方法：
1️⃣ 先找准定位，别盲目跟风
2️⃣ 每天坚持30分钟，形成习惯
3️⃣ 记录数据，及时调整策略

💡 关键心得：
{topic}不是一蹴而就的，需要耐心和坚持！

🎁 福利：评论区扣1，送你入门资料包

{' '.join(template['hashtags'][:3])}"""
        
        elif platform == 'wechat':
            return f"""## {topic}：从入门到精通

在这个信息爆炸的时代，{topic}已经成为必备技能。

### 一、为什么要学习{topic}？

1. **提升效率**：自动化处理重复工作
2. **增加收入**：开拓副业机会
3. **保持竞争力**：适应未来趋势

### 二、如何开始学习？

第一步：明确目标
第二步：选择工具
第三步：实践练习

### 三、常见问题

Q: 需要编程基础吗？
A: 不需要，现在有大量无代码工具

Q: 多久能看到效果？
A: 通常1-3个月，取决于投入程度

### 结语

{topic}不是终点，而是新起点。开始行动吧！"""
        
        elif platform == 'twitter':
            return f"""1/ {topic} changed my life.

Here's what I learned in 6 months:

2/ Start small, think big.
Don't try to master everything at once.

3/ Consistency > Intensity
30 mins daily beats 5 hours once a week.

4/ Build in public
Share your journey. Get feedback. Grow faster.

5/ The best time to start was yesterday.
The second best time is now.

What are you building? 👇"""
        
        else:
            return f"{topic}是一个值得深入研究的领域。本文将从多个角度分析其价值和实践方法..."
    
    def _estimate_engagement(self, platform: str) -> Dict:
        """预估互动数据"""
        base_rates = {
            'xiaohongshu': {'likes': 500, 'saves': 200, 'comments': 50},
            'wechat': {'reads': 1000, 'likes': 100, 'shares': 30},
            'zhihu': {'views': 5000, 'upvotes': 200, 'comments': 80},
            'twitter': {'impressions': 10000, 'likes': 300, 'retweets': 50}
        }
        return base_rates.get(platform, base_rates['wechat'])
    
    def batch_generate(self, topics: List[str], platforms: List[str]) -> List[Dict]:
        """批量生成内容"""
        results = []
        for topic in topics:
            for platform in platforms:
                post = self.generate_post(topic, platform)
                results.append(post)
        return results
    
    def get_metrics(self) -> Dict:
        """获取收益指标"""
        posts = self.metrics['posts_generated']
        time_saved = self.metrics['time_saved_hours']
        
        # 按每小时$50计算价值
        value_generated = time_saved * 50
        
        # 月度预估（假设每天生成5篇）
        monthly_posts = 5 * 30
        monthly_value = monthly_posts * 1.5 * 50
        
        return {
            'total_posts': posts,
            'time_saved_hours': time_saved,
            'value_generated_usd': value_generated,
            'platforms_used': self.metrics['platforms_used'],
            'monthly_projection_usd': monthly_value,
            'monthly_posts_projection': monthly_posts
        }
    
    def content_calendar(self, days: int = 30) -> Dict:
        """生成内容日历"""
        calendar = {}
        topics = self.config.get('topics', ['AI工具', '副业赚钱'])
        platforms = self.config.get('platforms', ['xiaohongshu'])
        
        for day in range(1, days + 1):
            topic = topics[day % len(topics)]
            platform = platforms[day % len(platforms)]
            calendar[f'Day {day}'] = {
                'topic': topic,
                'platform': platform,
                'status': 'planned'
            }
        
        return calendar


# 演示模式
if __name__ == '__main__':
    agent = ContentAI()
    
    print("=" * 50)
    print("📝 ContentAI - 内容创作助手")
    print("=" * 50)
    
    # 生成示例内容
    print("\n🎯 生成小红书内容：")
    post = agent.generate_post("AI副业", "xiaohongshu")
    print(f"标题: {post['title']}")
    print(f"内容预览: {post['body'][:100]}...")
    
    print("\n🎯 生成Twitter内容：")
    post2 = agent.generate_post("AI副业", "twitter")
    print(f"内容:\n{post2['body']}")
    
    # 显示指标
    print("\n📊 收益预估：")
    metrics = agent.get_metrics()
    for key, value in metrics.items():
        print(f"  {key}: {value}")
