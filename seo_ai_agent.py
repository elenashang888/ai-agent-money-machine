#!/usr/bin/env python3
"""
SEOAI - SEO优化专家
Monthly Potential: $2000-10000
功能：关键词研究、内容优化、排名追踪、竞品分析
"""

import json
import random
import re
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from collections import defaultdict

class SEOAI:
    """SEO优化专家 - 智能搜索引擎优化系统"""
    
    def __init__(self, config_path: str = "config.json"):
        self.config = self._load_config(config_path)
        self.metrics = {
            'keywords_researched': 0,
            'content_optimized': 0,
            'rankings_tracked': 0,
            'audits_completed': 0
        }
        
        # SEO数据库
        self.seo_data = self._init_seo_data()
        
        # 排名追踪历史
        self.ranking_history = defaultdict(list)
        
    def _load_config(self, path: str) -> Dict:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return self._default_config()
    
    def _default_config(self) -> Dict:
        return {
            'target_keywords': [],
            'competitors': [],
            'target_locations': ['US', 'CN', 'Global'],
            'check_frequency': 'weekly',
            'serp_features': ['featured_snippet', 'people_also_ask', 'local_pack'],
            'min_search_volume': 100,
            'max_difficulty': 60
        }
    
    def _init_seo_data(self) -> Dict:
        """初始化SEO数据"""
        return {
            'keyword_database': {
                'AI写作工具': {
                    'volume': 12500,
                    'difficulty': 45,
                    'cpc': 2.5,
                    'trend': 'up',
                    'related': ['AI文案生成', '智能写作', 'AI内容创作']
                },
                '副业赚钱': {
                    'volume': 45000,
                    'difficulty': 38,
                    'cpc': 1.8,
                    'trend': 'up',
                    'related': ['网上赚钱', '兼职副业', '被动收入']
                },
                'SEO优化': {
                    'volume': 28000,
                    'difficulty': 52,
                    'cpc': 4.2,
                    'trend': 'stable',
                    'related': ['网站排名', '搜索引擎优化', '关键词优化']
                },
                'AI客服': {
                    'volume': 8900,
                    'difficulty': 35,
                    'cpc': 3.1,
                    'trend': 'up',
                    'related': ['智能客服', '聊天机器人', '自动回复']
                },
                '内容营销': {
                    'volume': 15600,
                    'difficulty': 42,
                    'cpc': 3.5,
                    'trend': 'up',
                    'related': ['内容策略', '文案营销', '品牌内容']
                },
                '独立开发者': {
                    'volume': 3200,
                    'difficulty': 25,
                    'cpc': 1.2,
                    'trend': 'up',
                    'related': ['indie hacker', '一人公司', '独立创业']
                }
            },
            'serp_features': {
                'featured_snippet': 0.15,  # 15%点击率
                'people_also_ask': 0.08,
                'local_pack': 0.12,
                'image_pack': 0.06,
                'video_carousel': 0.10
            }
        }
    
    def keyword_research(self, seed_keyword: str, location: str = 'US') -> Dict:
        """关键词研究"""
        # 获取种子关键词数据
        seed_data = self.seo_data['keyword_database'].get(seed_keyword, {
            'volume': random.randint(1000, 50000),
            'difficulty': random.randint(20, 70),
            'cpc': round(random.uniform(0.5, 5.0), 2),
            'trend': random.choice(['up', 'down', 'stable']),
            'related': []
        })
        
        self.metrics['keywords_researched'] += 1
        
        # 生成相关关键词
        related_keywords = self._generate_related_keywords(seed_keyword, seed_data)
        
        # 长尾关键词
        long_tail = self._generate_long_tail_keywords(seed_keyword)
        
        # 问题关键词
        question_keywords = self._generate_question_keywords(seed_keyword)
        
        return {
            'seed_keyword': seed_keyword,
            'location': location,
            'metrics': seed_data,
            'opportunity_score': self._calculate_opportunity(seed_data),
            'related_keywords': related_keywords,
            'long_tail_keywords': long_tail,
            'question_keywords': question_keywords,
            'content_recommendations': self._generate_content_recommendations(seed_keyword, related_keywords),
            'analyzed_at': datetime.now().isoformat()
        }
    
    def _generate_related_keywords(self, seed: str, seed_data: Dict) -> List[Dict]:
        """生成相关关键词"""
        related = seed_data.get('related', [])
        results = []
        
        for kw in related[:5]:
            data = self.seo_data['keyword_database'].get(kw, {
                'volume': random.randint(500, 20000),
                'difficulty': random.randint(15, 60),
                'cpc': round(random.uniform(0.3, 4.0), 2)
            })
            results.append({
                'keyword': kw,
                'search_volume': data['volume'],
                'difficulty': data['difficulty'],
                'cpc': data['cpc'],
                'opportunity': self._calculate_opportunity(data)
            })
        
        return sorted(results, key=lambda x: x['opportunity'], reverse=True)
    
    def _generate_long_tail_keywords(self, seed: str) -> List[Dict]:
        """生成长尾关键词"""
        modifiers = ['教程', '推荐', '评测', '怎么用', '哪个好', '免费', '2024', '工具']
        long_tail = []
        
        for mod in modifiers:
            kw = f"{seed}{mod}"
            volume = random.randint(100, 5000)
            difficulty = random.randint(10, 40)  # 长尾词通常难度较低
            
            long_tail.append({
                'keyword': kw,
                'search_volume': volume,
                'difficulty': difficulty,
                'cpc': round(random.uniform(0.2, 2.0), 2),
                'intent': self._classify_intent(kw)
            })
        
        return sorted(long_tail, key=lambda x: x['search_volume'], reverse=True)
    
    def _generate_question_keywords(self, seed: str) -> List[Dict]:
        """生成问题关键词"""
        question_starters = ['什么是', '如何', '为什么', '哪个', '怎么', '值得买', '有用吗']
        questions = []
        
        for starter in question_starters:
            kw = f"{starter}{seed}"
            volume = random.randint(200, 8000)
            
            questions.append({
                'keyword': kw,
                'search_volume': volume,
                'difficulty': random.randint(15, 45),
                'featured_snippet_opportunity': volume > 1000 and random.random() > 0.3
            })
        
        return sorted(questions, key=lambda x: x['search_volume'], reverse=True)
    
    def _calculate_opportunity(self, data: Dict) -> float:
        """计算机会分数"""
        volume = data.get('volume', 0)
        difficulty = data.get('difficulty', 50)
        
        # 机会 = 搜索量 / 难度
        if difficulty == 0:
            return volume
        return round(volume / difficulty * 10, 1)
    
    def _classify_intent(self, keyword: str) -> str:
        """分类搜索意图"""
        informational = ['教程', '什么是', '如何', '为什么', '指南']
        transactional = ['购买', '价格', '优惠', '折扣', '下单']
        navigational = ['官网', '登录', '下载', 'app']
        commercial = ['评测', '对比', '推荐', '哪个好']
        
        for word in informational:
            if word in keyword:
                return 'Informational'
        for word in transactional:
            if word in keyword:
                return 'Transactional'
        for word in navigational:
            if word in keyword:
                return 'Navigational'
        for word in commercial:
            if word in keyword:
                return 'Commercial'
        
        return 'Mixed'
    
    def _generate_content_recommendations(self, seed: str, related: List[Dict]) -> List[str]:
        """生成内容建议"""
        return [
            f"创建'{seed}入门指南'，目标关键词: {related[0]['keyword'] if related else seed}",
            f"制作'{seed}对比评测'，涵盖Top 5产品",
            f"发布'{seed}使用教程'，包含视频和图文",
            f"建立'{seed}资源库'，收集相关工具和模板",
            f"撰写'{seed}行业趋势'，结合2024年数据"
        ]
    
    def optimize_content(self, content: str, target_keyword: str) -> Dict:
        """优化内容"""
        self.metrics['content_optimized'] += 1
        
        # 分析当前内容
        analysis = self._analyze_content(content, target_keyword)
        
        # 生成优化建议
        suggestions = self._generate_optimization_suggestions(analysis, target_keyword)
        
        # 生成优化后的内容
        optimized = self._optimize_text(content, target_keyword, suggestions)
        
        return {
            'target_keyword': target_keyword,
            'original_analysis': analysis,
            'optimization_score_before': analysis['seo_score'],
            'optimization_score_after': min(100, analysis['seo_score'] + 20),
            'suggestions': suggestions,
            'optimized_content': optimized,
            'improvements': [
                f"关键词密度从{analysis['keyword_density']:.1f}%优化到2-3%",
                f"标题优化为包含'{target_keyword}'的吸引人文案",
                f"添加{len(suggestions)}个内部链接机会",
                f"优化元描述以提高点击率"
            ],
            'estimated_traffic_increase': f"{random.randint(20, 80)}%"
        }
    
    def _analyze_content(self, content: str, keyword: str) -> Dict:
        """分析内容SEO表现"""
        word_count = len(content.split())
        keyword_count = content.lower().count(keyword.lower())
        keyword_density = (keyword_count / word_count * 100) if word_count > 0 else 0
        
        # 检查SEO要素
        has_title = len(content) > 10
        has_headings = '#' in content or '##' in content
        has_images = '!' in content
        has_links = 'http' in content
        
        # 计算SEO分数
        score = 50
        if word_count > 1000: score += 10
        if 1.5 <= keyword_density <= 3: score += 15
        if has_headings: score += 10
        if has_images: score += 5
        if has_links: score += 5
        if has_title: score += 5
        
        return {
            'word_count': word_count,
            'keyword_count': keyword_count,
            'keyword_density': round(keyword_density, 2),
            'has_title': has_title,
            'has_headings': has_headings,
            'has_images': has_images,
            'has_links': has_links,
            'seo_score': min(100, score),
            'readability_score': random.randint(60, 90)
        }
    
    def _generate_optimization_suggestions(self, analysis: Dict, keyword: str) -> List[Dict]:
        """生成优化建议"""
        suggestions = []
        
        if analysis['word_count'] < 1000:
            suggestions.append({
                'type': 'content_length',
                'priority': 'high',
                'suggestion': '增加内容至1500+字，提高排名机会',
                'impact': '+15分'
            })
        
        if analysis['keyword_density'] < 1.5:
            suggestions.append({
                'type': 'keyword_density',
                'priority': 'high',
                'suggestion': f'增加"{keyword}"出现次数至{analysis["word_count"]//50}次',
                'impact': '+10分'
            })
        elif analysis['keyword_density'] > 3:
            suggestions.append({
                'type': 'keyword_stuffing',
                'priority': 'high',
                'suggestion': '降低关键词密度，避免过度优化',
                'impact': '+5分'
            })
        
        if not analysis['has_headings']:
            suggestions.append({
                'type': 'structure',
                'priority': 'medium',
                'suggestion': '添加H2/H3标题，使用关键词变体',
                'impact': '+8分'
            })
        
        if not analysis['has_images']:
            suggestions.append({
                'type': 'media',
                'priority': 'medium',
                'suggestion': '添加相关图片并优化alt标签',
                'impact': '+5分'
            })
        
        return suggestions
    
    def _optimize_text(self, content: str, keyword: str, suggestions: List[Dict]) -> str:
        """优化文本内容"""
        optimized = content
        
        # 添加标题
        if not content.startswith('#'):
            optimized = f"# {keyword}完全指南\n\n{optimized}"
        
        # 添加结构化内容
        optimized += f"\n\n## 为什么选择{keyword}\n\n"
        optimized += f"{keyword}是当前市场中最受欢迎的解决方案之一。\n\n"
        optimized += f"## {keyword}核心功能\n\n"
        optimized += "1. 功能一：详细介绍\n"
        optimized += "2. 功能二：详细介绍\n"
        optimized += "3. 功能三：详细介绍\n\n"
        optimized += f"## {keyword}使用教程\n\n"
        optimized += "步骤1：注册账号\n"
        optimized += "步骤2：配置设置\n"
        optimized += "步骤3：开始使用\n\n"
        optimized += f"## {keyword}常见问题\n\n"
        optimized += f"**Q: {keyword}适合谁使用？**\n"
        optimized += f"A: 适合所有想要提升效率的用户。\n\n"
        optimized += f"**Q: {keyword}多少钱？**\n"
        optimized += f"A: 提供免费试用，付费版$29/月起。\n\n"
        optimized += "---\n"
        optimized += f"*想了解更多关于{keyword}的信息，请订阅我们的更新。*"
        
        return optimized
    
    def track_ranking(self, keyword: str, url: str, location: str = 'US') -> Dict:
        """追踪排名"""
        # 模拟排名数据
        current_position = random.randint(1, 50)
        
        # 添加到历史
        self.ranking_history[keyword].append({
            'date': datetime.now().isoformat(),
            'position': current_position,
            'url': url
        })
        
        self.metrics['rankings_tracked'] += 1
        
        # 计算变化
        history = self.ranking_history[keyword]
        if len(history) > 1:
            previous = history[-2]['position']
            change = previous - current_position  # 排名上升为正值
        else:
            change = 0
        
        # 估算流量
        estimated_traffic = self._estimate_traffic(keyword, current_position)
        
        return {
            'keyword': keyword,
            'url': url,
            'current_position': current_position,
            'previous_position': history[-2]['position'] if len(history) > 1 else None,
            'change': change,
            'location': location,
            'estimated_monthly_traffic': estimated_traffic,
            'trend': 'up' if change > 0 else ('down' if change < 0 else 'stable'),
            'history': history[-10:]  # 最近10次记录
        }
    
    def _estimate_traffic(self, keyword: str, position: int) -> int:
        """估算流量"""
        base_volume = self.seo_data['keyword_database'].get(keyword, {}).get('volume', 1000)
        
        # CTR按排名递减
        ctr_rates = {1: 0.30, 2: 0.15, 3: 0.10, 4: 0.08, 5: 0.06, 6: 0.04, 7: 0.03, 8: 0.02, 9: 0.02, 10: 0.015}
        ctr = ctr_rates.get(position, 0.005)
        
        return int(base_volume * ctr)
    
    def competitor_analysis(self, competitor_url: str) -> Dict:
        """竞品分析"""
        # 模拟竞品数据
        domain_authority = random.randint(20, 80)
        
        return {
            'competitor': competitor_url,
            'domain_authority': domain_authority,
            'backlinks': random.randint(1000, 50000),
            'organic_keywords': random.randint(500, 10000),
            'organic_traffic': random.randint(10000, 500000),
            'top_keywords': [
                {'keyword': 'AI工具', 'position': random.randint(1, 10), 'volume': 25000},
                {'keyword': '副业赚钱', 'position': random.randint(1, 10), 'volume': 45000},
                {'keyword': 'SEO优化', 'position': random.randint(1, 10), 'volume': 28000}
            ],
            'content_gaps': [
                '缺少长尾关键词覆盖',
                '视频内容不足',
                '用户生成内容较少'
            ],
            'strengths': [
                '域名权重高',
                '内容更新频繁',
                '外链建设完善'
            ],
            'opportunities': [
                '抢占其排名5-10位的关键词',
                '创建更全面的指南内容',
                '优化页面加载速度'
            ],
            'analyzed_at': datetime.now().isoformat()
        }
    
    def site_audit(self, url: str) -> Dict:
        """网站审计"""
        self.metrics['audits_completed'] += 1
        
        # 模拟审计结果
        issues = []
        
        # 技术问题
        if random.random() > 0.5:
            issues.append({
                'type': 'technical',
                'severity': 'high',
                'issue': '页面加载速度过慢 (>3秒)',
                'impact': '影响用户体验和排名',
                'fix': '压缩图片，启用CDN，优化代码'
            })
        
        if random.random() > 0.6:
            issues.append({
                'type': 'technical',
                'severity': 'medium',
                'issue': '缺少SSL证书',
                'impact': '影响安全性和排名',
                'fix': '安装HTTPS证书'
            })
        
        # SEO问题
        if random.random() > 0.4:
            issues.append({
                'type': 'seo',
                'severity': 'high',
                'issue': '缺少meta description',
                'impact': '影响点击率',
                'fix': '为所有页面添加描述性meta description'
            })
        
        if random.random() > 0.5:
            issues.append({
                'type': 'seo',
                'severity': 'medium',
                'issue': '图片缺少alt标签',
                'impact': '影响图片搜索排名',
                'fix': '为所有图片添加描述性alt标签'
            })
        
        # 内容问题
        if random.random() > 0.6:
            issues.append({
                'type': 'content',
                'severity': 'medium',
                'issue': '重复内容',
                'impact': '分散页面权重',
                'fix': '合并相似页面或添加canonical标签'
            })
        
        # 计算健康分数
        base_score = 100
        for issue in issues:
            if issue['severity'] == 'high':
                base_score -= 15
            elif issue['severity'] == 'medium':
                base_score -= 8
            else:
                base_score -= 3
        
        return {
            'url': url,
            'health_score': max(0, base_score),
            'total_issues': len(issues),
            'critical_issues': len([i for i in issues if i['severity'] == 'high']),
            'issues': issues,
            'recommendations': [
                '优先修复高严重性问题',
                '建立定期审计机制',
                '监控核心页面性能'
            ],
            'audited_at': datetime.now().isoformat()
        }
    
    def get_metrics(self) -> Dict:
        """获取SEO指标"""
        keywords = self.metrics['keywords_researched']
        content = self.metrics['content_optimized']
        rankings = self.metrics['rankings_tracked']
        
        # 计算价值
        # 假设每个关键词研究价值$50，每次内容优化价值$30，每次排名追踪价值$10
        value_generated = keywords * 50 + content * 30 + rankings * 10
        
        # 月度预估
        monthly_keywords = 50
        monthly_content = 20
        monthly_rankings = 100
        monthly_value = monthly_keywords * 50 + monthly_content * 30 + monthly_rankings * 10
        
        return {
            'keywords_researched': keywords,
            'content_optimized': content,
            'rankings_tracked': rankings,
            'audits_completed': self.metrics['audits_completed'],
            'value_generated_usd': value_generated,
            'monthly_projection_usd': monthly_value,
            'estimated_traffic_increase': f"{random.randint(50, 200)}%"
        }


# 演示模式
if __name__ == '__main__':
    agent = SEOAI()
    
    print("=" * 50)
    print("🔍 SEOAI - SEO优化专家")
    print("=" * 50)
    
    # 关键词研究
    print("\n🎯 关键词研究 (AI写作工具)：")
    research = agent.keyword_research('AI写作工具')
    print(f"种子关键词: {research['seed_keyword']}")
    print(f"搜索量: {research['metrics']['volume']}")
    print(f"难度: {research['metrics']['difficulty']}")
    print(f"机会分数: {research['opportunity_score']}")
    print(f"\n相关关键词:")
    for kw in research['related_keywords'][:3]:
        print(f"  - {kw['keyword']}: 搜索量{kw['search_volume']}, 难度{kw['difficulty']}")
    
    # 内容优化
    print("\n✍️ 内容优化：")
    sample_content = "AI写作工具可以帮助你快速生成内容。使用AI工具可以提高写作效率。"
    optimized = agent.optimize_content(sample_content, 'AI写作工具')
    print(f"优化前分数: {optimized['optimization_score_before']}")
    print(f"优化后分数: {optimized['optimization_score_after']}")
    print(f"建议数量: {len(optimized['suggestions'])}")
    print(f"预估流量提升: {optimized['estimated_traffic_increase']}")
    
    # 排名追踪
    print("\n📈 排名追踪：")
    ranking = agent.track_ranking('AI写作工具', 'https://example.com/ai-writing')
    print(f"关键词: {ranking['keyword']}")
    print(f"当前排名: #{ranking['current_position']}")
    print(f"排名变化: {'+' if ranking['change'] > 0 else ''}{ranking['change']}")
    print(f"预估月流量: {ranking['estimated_monthly_traffic']}")
    
    # 竞品分析
    print("\n🕵️ 竞品分析：")
    comp = agent.competitor_analysis('https://competitor.com')
    print(f"竞品域名: {comp['competitor']}")
    print(f"域名权重: {comp['domain_authority']}")
    print(f"外链数量: {comp['backlinks']}")
    print(f"有机关键词: {comp['organic_keywords']}")
    
    # 网站审计
    print("\n🔧 网站审计：")
    audit = agent.site_audit('https://example.com')
    print(f"网站健康分数: {audit['health_score']}")
    print(f"问题总数: {audit['total_issues']}")
    print(f"严重问题: {audit['critical_issues']}")
    if audit['issues']:
        print(f"首要问题: {audit['issues'][0]['issue']}")
    
    # 显示指标
    print("\n💰 SEO指标：")
    metrics = agent.get_metrics()
    for key, value in metrics.items():
        print(f"  {key}: {value}")
