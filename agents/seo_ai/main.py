#!/usr/bin/env python3
"""
SEOAI - SEO Optimization Expert Agent
SEO优化专家智能体

功能模块:
1. 关键词研究 (Keyword Research)
2. 内容优化 (Content Optimization)
3. 外链建设 (Link Building)
4. SEO分析与报告 (SEO Analysis & Reporting)
"""

import json
import re
import asyncio
import aiohttp
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from datetime import datetime
from collections import Counter
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class KeywordData:
    """关键词数据结构"""
    keyword: str
    search_volume: int
    difficulty: float  # 0-100
    cpc: float  # Cost Per Click
    competition: str  # Low, Medium, High
    trend: str  # Rising, Stable, Falling
    related_keywords: List[str]
    long_tail_variants: List[str]
    intent: str  # Informational, Navigational, Transactional, Commercial


@dataclass
class ContentOptimization:
    """内容优化建议"""
    title_suggestions: List[str]
    meta_description: str
    heading_structure: List[Dict]
    keyword_density: Dict[str, float]
    readability_score: float
    content_gaps: List[str]
    internal_linking_suggestions: List[Dict]
    image_alt_texts: List[str]
    schema_markup_suggestions: List[str]


@dataclass
class BacklinkOpportunity:
    """外链机会"""
    target_url: str
    domain_authority: int
    relevance_score: float
    link_type: str  # Guest Post, Directory, Resource Page, etc.
    contact_email: Optional[str]
    outreach_template: str
    priority: str  # High, Medium, Low


@dataclass
class SEOReport:
    """SEO分析报告"""
    url: str
    overall_score: int
    technical_seo: Dict[str, Any]
    on_page_seo: Dict[str, Any]
    off_page_seo: Dict[str, Any]
    recommendations: List[str]
    competitor_analysis: Dict[str, Any]
    generated_at: datetime


class SEOAI:
    """
    SEO优化专家智能体
    
    主要职责:
    - 进行深度关键词研究
    - 提供内容优化建议
    - 发现外链建设机会
    - 生成全面的SEO分析报告
    """
    
    def __init__(self, config_path: str = "config.json"):
        """初始化SEOAI"""
        self.config = self._load_config(config_path)
        self.api_keys = self.config.get("api_keys", {})
        self.settings = self.config.get("settings", {})
        self.session: Optional[aiohttp.ClientSession] = None
        
    def _load_config(self, path: str) -> Dict:
        """加载配置文件"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"Config file not found: {path}, using defaults")
            return self._default_config()
    
    def _default_config(self) -> Dict:
        """默认配置"""
        return {
            "api_keys": {},
            "settings": {
                "max_keywords": 100,
                "min_search_volume": 100,
                "target_difficulty": 50,
                "content_min_length": 1500,
                "readability_target": 60
            }
        }
    
    async def __aenter__(self):
        """异步上下文管理器入口"""
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """异步上下文管理器出口"""
        if self.session:
            await self.session.close()
    
    # ==================== 关键词研究模块 ====================
    
    async def research_keywords(
        self, 
        seed_keywords: List[str],
        location: str = "US",
        language: str = "en"
    ) -> List[KeywordData]:
        """
        关键词研究主函数
        
        Args:
            seed_keywords: 种子关键词列表
            location: 目标地区
            language: 目标语言
            
        Returns:
            List[KeywordData]: 关键词数据列表
        """
        logger.info(f"Starting keyword research for: {seed_keywords}")
        
        all_keywords = []
        
        for seed in seed_keywords:
            # 生成关键词变体
            variants = await self._generate_keyword_variants(seed)
            
            # 获取搜索数据
            for variant in variants:
                keyword_data = await self._analyze_keyword(variant, location, language)
                if keyword_data.search_volume >= self.settings.get("min_search_volume", 100):
                    all_keywords.append(keyword_data)
        
        # 去重并按搜索量排序
        unique_keywords = self._deduplicate_keywords(all_keywords)
        unique_keywords.sort(key=lambda x: x.search_volume, reverse=True)
        
        return unique_keywords[:self.settings.get("max_keywords", 100)]
    
    async def _generate_keyword_variants(self, seed: str) -> List[str]:
        """生成关键词变体"""
        variants = [seed]
        
        # 问题型变体
        question_prefixes = [
            "what is", "how to", "why", "best", "top", "vs", "versus",
            "什么是", "如何", "为什么", "最好的", "顶级"
        ]
        for prefix in question_prefixes:
            variants.append(f"{prefix} {seed}")
        
        # 长尾变体
        long_tail_suffixes = [
            "for beginners", "tutorial", "guide", "tips", "tools",
            "初学者", "教程", "指南", "技巧", "工具"
        ]
        for suffix in long_tail_suffixes:
            variants.append(f"{seed} {suffix}")
        
        # 商业意图变体
        commercial_modifiers = [
            "buy", "price", "review", "discount", "cheap",
            "购买", "价格", "评测", "折扣", "便宜"
        ]
        for modifier in commercial_modifiers:
            variants.append(f"{modifier} {seed}")
        
        return variants
    
    async def _analyze_keyword(
        self, 
        keyword: str, 
        location: str, 
        language: str
    ) -> KeywordData:
        """分析单个关键词"""
        # 模拟API调用（实际应接入Google Keyword Planner, SEMrush等）
        search_volume = self._estimate_search_volume(keyword)
        difficulty = self._calculate_difficulty(keyword)
        cpc = self._estimate_cpc(keyword)
        competition = self._assess_competition(difficulty)
        trend = self._analyze_trend(keyword)
        related = await self._find_related_keywords(keyword)
        long_tail = await self._generate_long_tail(keyword)
        intent = self._determine_intent(keyword)
        
        return KeywordData(
            keyword=keyword,
            search_volume=search_volume,
            difficulty=difficulty,
            cpc=cpc,
            competition=competition,
            trend=trend,
            related_keywords=related,
            long_tail_variants=long_tail,
            intent=intent
        )
    
    def _estimate_search_volume(self, keyword: str) -> int:
        """估算搜索量"""
        # 基于关键词长度的启发式估算
        base_volume = max(1000, 50000 - len(keyword) * 1000)
        # 添加随机因子
        import random
        return int(base_volume * random.uniform(0.5, 1.5))
    
    def _calculate_difficulty(self, keyword: str) -> float:
        """计算关键词难度"""
        # 基于竞争程度的启发式计算
        difficulty = min(100, len(keyword) * 3 + 20)
        import random
        return round(difficulty * random.uniform(0.8, 1.2), 1)
    
    def _estimate_cpc(self, keyword: str) -> float:
        """估算CPC"""
        # 商业关键词通常CPC更高
        commercial_terms = ['buy', 'price', 'discount', '购买', '价格', '折扣']
        base_cpc = 2.5 if any(term in keyword.lower() for term in commercial_terms) else 1.0
        import random
        return round(base_cpc * random.uniform(0.5, 2.0), 2)
    
    def _assess_competition(self, difficulty: float) -> str:
        """评估竞争程度"""
        if difficulty < 30:
            return "Low"
        elif difficulty < 60:
            return "Medium"
        return "High"
    
    def _analyze_trend(self, keyword: str) -> str:
        """分析趋势"""
        import random
        trends = ["Rising", "Stable", "Falling"]
        weights = [0.4, 0.5, 0.1]
        return random.choices(trends, weights=weights)[0]
    
    async def _find_related_keywords(self, keyword: str) -> List[str]:
        """查找相关关键词"""
        words = keyword.split()
        related = []
        
        # 生成语义相关词
        for word in words:
            if len(word) > 3:
                related.extend([
                    f"{word} guide",
                    f"{word} tutorial",
                    f"{word} tips"
                ])
        
        return related[:10]
    
    async def _generate_long_tail(self, keyword: str) -> List[str]:
        """生成长尾关键词"""
        modifiers = [
            "for beginners", "step by step", "in 2024", "complete guide",
            "初学者", "一步一步", "2024年", "完整指南"
        ]
        return [f"{keyword} {mod}" for mod in modifiers[:5]]
    
    def _determine_intent(self, keyword: str) -> str:
        """确定搜索意图"""
        keyword_lower = keyword.lower()
        
        informational = ['what', 'how', 'why', 'guide', 'tutorial', '什么是', '如何', '为什么']
        transactional = ['buy', 'price', 'discount', 'purchase', '购买', '价格', '折扣']
        navigational = ['login', 'sign up', 'website', 'official', '登录', '注册', '官网']
        
        if any(term in keyword_lower for term in transactional):
            return "Transactional"
        elif any(term in keyword_lower for term in navigational):
            return "Navigational"
        elif any(term in keyword_lower for term in informational):
            return "Informational"
        return "Commercial"
    
    def _deduplicate_keywords(self, keywords: List[KeywordData]) -> List[KeywordData]:
        """去重关键词"""
        seen = set()
        unique = []
        for kw in keywords:
            if kw.keyword not in seen:
                seen.add(kw.keyword)
                unique.append(kw)
        return unique
    
    # ==================== 内容优化模块 ====================
    
    async def optimize_content(
        self,
        content: str,
        target_keywords: List[str],
        content_type: str = "blog_post"
    ) -> ContentOptimization:
        """
        内容优化主函数
        
        Args:
            content: 原始内容
            target_keywords: 目标关键词
            content_type: 内容类型
            
        Returns:
            ContentOptimization: 优化建议
        """
        logger.info(f"Optimizing content for keywords: {target_keywords}")
        
        # 分析内容
        word_count = len(content.split())
        keyword_density = self._calculate_keyword_density(content, target_keywords)
        readability = self._calculate_readability(content)
        
        # 生成优化建议
        title_suggestions = await self._generate_title_suggestions(
            target_keywords, content_type
        )
        meta_desc = await self._generate_meta_description(content, target_keywords)
        headings = self._suggest_heading_structure(content, target_keywords)
        gaps = self._identify_content_gaps(content, target_keywords)
        internal_links = self._suggest_internal_linking(content, target_keywords)
        alt_texts = self._generate_image_alt_texts(content, target_keywords)
        schema = self._suggest_schema_markup(content_type)
        
        return ContentOptimization(
            title_suggestions=title_suggestions,
            meta_description=meta_desc,
            heading_structure=headings,
            keyword_density=keyword_density,
            readability_score=readability,
            content_gaps=gaps,
            internal_linking_suggestions=internal_links,
            image_alt_texts=alt_texts,
            schema_markup_suggestions=schema
        )
    
    def _calculate_keyword_density(self, content: str, keywords: List[str]) -> Dict[str, float]:
        """计算关键词密度"""
        words = content.lower().split()
        total_words = len(words)
        density = {}
        
        for keyword in keywords:
            keyword_lower = keyword.lower()
            count = sum(1 for word in words if keyword_lower in word)
            density[keyword] = round((count / total_words) * 100, 2) if total_words > 0 else 0
        
        return density
    
    def _calculate_readability(self, content: str) -> float:
        """计算可读性分数（Flesch Reading Ease简化版）"""
        sentences = len(re.split(r'[.!?]+', content))
        words = len(content.split())
        syllables = sum(self._count_syllables(word) for word in content.split())
        
        if sentences == 0 or words == 0:
            return 0
        
        # 简化公式
        score = 206.835 - 1.015 * (words / sentences) - 84.6 * (syllables / words)
        return round(max(0, min(100, score)), 1)
    
    def _count_syllables(self, word: str) -> int:
        """计算音节数"""
        word = word.lower()
        vowels = "aeiouy"
        count = 0
        prev_was_vowel = False
        
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not prev_was_vowel:
                count += 1
            prev_was_vowel = is_vowel
        
        if word.endswith('e'):
            count -= 1
        
        return max(1, count)
    
    async def _generate_title_suggestions(
        self, 
        keywords: List[str], 
        content_type: str
    ) -> List[str]:
        """生成标题建议"""
        templates = {
            "blog_post": [
                "The Ultimate Guide to {keyword} in 2024",
                "How to Master {keyword}: A Complete Tutorial",
                "10 Proven Strategies for {keyword} Success",
                "{keyword}: Everything You Need to Know",
                "Why {keyword} Matters More Than Ever"
            ],
            "product_page": [
                "Best {keyword} - Top Rated Products 2024",
                "Premium {keyword} Solutions | Shop Now",
                "Affordable {keyword} | High Quality Guaranteed"
            ],
            "landing_page": [
                "Transform Your Business with {keyword}",
                "Get Started with {keyword} Today",
                "The #1 {keyword} Platform for Professionals"
            ]
        }
        
        suggestions = []
        primary_keyword = keywords[0] if keywords else "Your Topic"
        
        for template in templates.get(content_type, templates["blog_post"]):
            suggestions.append(template.format(keyword=primary_keyword.title()))
        
        return suggestions[:5]
    
    async def _generate_meta_description(
        self, 
        content: str, 
        keywords: List[str]
    ) -> str:
        """生成Meta描述"""
        # 提取内容前150个字符作为基础
        summary = content[:150].strip()
        if len(summary) < 50:
            summary = f"Learn everything about {keywords[0] if keywords else 'this topic'}. "
        
        # 添加CTA
        cta = " Discover expert tips and strategies today!"
        
        description = summary + cta
        return description[:160]  # 限制在160字符以内
    
    def _suggest_heading_structure(
        self, 
        content: str, 
        keywords: List[str]
    ) -> List[Dict]:
        """建议标题结构"""
        structure = [
            {"level": "H1", "text": f"Complete Guide to {keywords[0].title() if keywords else 'Your Topic'}"},
            {"level": "H2", "text": "What is " + (keywords[0].title() if keywords else "This Topic") + "?"},
            {"level": "H2", "text": "Why " + (keywords[0].title() if keywords else "This") + " Matters"},
            {"level": "H2", "text": "Key Benefits and Features"},
            {"level": "H3", "text": "Benefit 1: Increased Efficiency"},
            {"level": "H3", "text": "Benefit 2: Cost Savings"},
            {"level": "H2", "text": "How to Get Started"},
            {"level": "H2", "text": "Best Practices and Tips"},
            {"level": "H2", "text": "Common Mistakes to Avoid"},
            {"level": "H2", "text": "Conclusion"}
        ]
        return structure
    
    def _identify_content_gaps(self, content: str, keywords: List[str]) -> List[str]:
        """识别内容缺口"""
        gaps = []
        content_lower = content.lower()
        
        # 检查是否包含关键主题
        essential_topics = [
            "introduction", "benefits", "examples", 
            "how to", "tips", "conclusion"
        ]
        
        for topic in essential_topics:
            if topic not in content_lower:
                gaps.append(f"Missing {topic} section")
        
        # 检查关键词覆盖
        for keyword in keywords:
            if keyword.lower() not in content_lower:
                gaps.append(f"Primary keyword '{keyword}' not found in content")
        
        return gaps
    
    def _suggest_internal_linking(
        self, 
        content: str, 
        keywords: List[str]
    ) -> List[Dict]:
        """建议内链策略"""
        suggestions = []
        
        for i, keyword in enumerate(keywords[:3]):
            suggestions.append({
                "anchor_text": keyword,
                "target_page": f"/related-topic-{i+1}",
                "context": f"Learn more about {keyword}",
                "priority": "High" if i == 0 else "Medium"
            })
        
        return suggestions
    
    def _generate_image_alt_texts(self, content: str, keywords: List[str]) -> List[str]:
        """生成图片Alt文本"""
        primary_keyword = keywords[0] if keywords else "featured image"
        
        return [
            f"Illustration of {primary_keyword} concept",
            f"Diagram showing {primary_keyword} process",
            f"Infographic about {primary_keyword} benefits",
            f"Screenshot of {primary_keyword} example",
            f"Chart comparing {primary_keyword} options"
        ]
    
    def _suggest_schema_markup(self, content_type: str) -> List[str]:
        """建议Schema标记"""
        schemas = {
            "blog_post": [
                "Article schema",
                "BreadcrumbList schema",
                "Organization schema"
            ],
            "product_page": [
                "Product schema",
                "Offer schema",
                "Review schema"
            ],
            "landing_page": [
                "WebPage schema",
                "FAQPage schema",
                "HowTo schema"
            ]
        }
        
        return schemas.get(content_type, schemas["blog_post"])
    
    # ==================== 外链建设模块 ====================
    
    async def find_backlink_opportunities(
        self,
        niche: str,
        competitors: List[str],
        target_metrics: Optional[Dict] = None
    ) -> List[BacklinkOpportunity]:
        """
        发现外链建设机会
        
        Args:
            niche: 行业/利基市场
            competitors: 竞争对手域名列表
            target_metrics: 目标指标
            
        Returns:
            List[BacklinkOpportunity]: 外链机会列表
        """
        logger.info(f"Finding backlink opportunities in niche: {niche}")
        
        opportunities = []
        
        # 分析竞争对手外链
        for competitor in competitors:
            competitor_links = await self._analyze_competitor_backlinks(competitor)
            opportunities.extend(competitor_links)
        
        # 发现行业资源
        resource_opportunities = await self._find_resource_page_opportunities(niche)
        opportunities.extend(resource_opportunities)
        
        # 发现客座博客机会
        guest_post_opps = await self._find_guest_post_opportunities(niche)
        opportunities.extend(guest_post_opps)
        
        # 过滤和排序
        filtered = self._filter_opportunities(opportunities, target_metrics)
        filtered.sort(key=lambda x: (x.domain_authority, x.relevance_score), reverse=True)
        
        return filtered[:50]
    
    async def _analyze_competitor_backlinks(
        self, 
        competitor: str
    ) -> List[BacklinkOpportunity]:
        """分析竞争对手外链"""
        opportunities = []
        
        # 模拟外链数据
        import random
        for i in range(10):
            da = random.randint(20, 80)
            opportunities.append(BacklinkOpportunity(
                target_url=f"https://example{i}.com/resource-page",
                domain_authority=da,
                relevance_score=round(random.uniform(0.6, 0.95), 2),
                link_type="Resource Page",
                contact_email=f"editor@example{i}.com",
                outreach_template=self._generate_outreach_template("Resource Page"),
                priority="High" if da > 50 else "Medium"
            ))
        
        return opportunities
    
    async def _find_resource_page_opportunities(self, niche: str) -> List[BacklinkOpportunity]:
        """发现资源页面机会"""
        opportunities = []
        
        # 模拟资源页面
        import random
        resource_sites = [
            f"https://{niche.lower().replace(' ', '')}resources.com",
            f"https://best{niche.lower().replace(' ', '')}tools.com",
            f"https://{niche.lower().replace(' ', '')}hub.io"
        ]
        
        for site in resource_sites:
            opportunities.append(BacklinkOpportunity(
                target_url=f"{site}/resources",
                domain_authority=random.randint(30, 70),
                relevance_score=round(random.uniform(0.8, 0.98), 2),
                link_type="Resource Page",
                contact_email=f"admin@{site.replace('https://', '')}",
                outreach_template=self._generate_outreach_template("Resource Page"),
                priority="High"
            ))
        
        return opportunities
    
    async def _find_guest_post_opportunities(self, niche: str) -> List[BacklinkOpportunity]:
        """发现客座博客机会"""
        opportunities = []
        
        import random
        for i in range(5):
            da = random.randint(25, 65)
            opportunities.append(BacklinkOpportunity(
                target_url=f"https://blog{i}.com/write-for-us",
                domain_authority=da,
                relevance_score=round(random.uniform(0.7, 0.9), 2),
                link_type="Guest Post",
                contact_email=f"editor@blog{i}.com",
                outreach_template=self._generate_outreach_template("Guest Post"),
                priority="Medium" if da < 40 else "High"
            ))
        
        return opportunities
    
    def _generate_outreach_template(self, link_type: str) -> str:
        """生成外链拓展模板"""
        templates = {
            "Guest Post": """Subject: Guest Post Contribution - {niche} Expert

Hi [Name],

I hope this email finds you well. I'm [Your Name], a {niche} specialist with expertise in [specific topics].

I've been following your blog and really appreciate the quality content you publish. I'd love to contribute a guest post on [proposed topic] that would provide value to your readers.

Here are a few topic ideas:
1. [Topic 1]
2. [Topic 2]
3. [Topic 3]

Would any of these interest you? I'm happy to adjust based on your editorial calendar.

Best regards,
[Your Name]""",
            
            "Resource Page": """Subject: Resource Suggestion for [Page Name]

Hi [Name],

I came across your excellent resource page [URL] while researching {niche}. It's incredibly comprehensive!

I noticed you might be missing a resource on [specific topic]. I recently published a detailed guide that covers [brief description].

Here's the link: [Your URL]

I believe it would be a valuable addition to your page and help your visitors [specific benefit].

Thanks for maintaining such a helpful resource!

Best,
[Your Name]""",
            
            "Broken Link": """Subject: Quick heads up about a broken link

Hi [Name],

I was browsing your article [Article Title] and found it very informative. However, I noticed one of the links appears to be broken:

[Broken Link URL]

I actually have a similar resource that could replace it: [Your URL]

It covers [brief description] and is regularly updated.

Just wanted to help improve the reader experience!

Best regards,
[Your Name]"""
        }
        
        return templates.get(link_type, templates["Guest Post"])
    
    def _filter_opportunities(
        self, 
        opportunities: List[BacklinkOpportunity],
        target_metrics: Optional[Dict]
    ) -> List[BacklinkOpportunity]:
        """过滤外链机会"""
        if not target_metrics:
            return opportunities
        
        min_da = target_metrics.get("min_domain_authority", 20)
        min_relevance = target_metrics.get("min_relevance", 0.5)
        
        filtered = [
            opp for opp in opportunities
            if opp.domain_authority >= min_da 
            and opp.relevance_score >= min_relevance
        ]
        
        return filtered
    
    # ==================== SEO分析模块 ====================
    
    async def generate_seo_report(self, url: str) -> SEOReport:
        """
        生成完整SEO分析报告
        
        Args:
            url: 目标网址
            
        Returns:
            SEOReport: SEO分析报告
        """
        logger.info(f"Generating SEO report for: {url}")
        
        # 技术SEO分析
        technical = await self._analyze_technical_seo(url)
        
        # 页面SEO分析
        on_page = await self._analyze_on_page_seo(url)
        
        # 站外SEO分析
        off_page = await self._analyze_off_page_seo(url)
        
        # 竞争对手分析
        competitors = await self._analyze_competitors(url)
        
        # 生成建议
        recommendations = self._generate_recommendations(technical, on_page, off_page)
        
        # 计算总分
        overall_score = self._calculate_overall_score(technical, on_page, off_page)
        
        return SEOReport(
            url=url,
            overall_score=overall_score,
            technical_seo=technical,
            on_page_seo=on_page,
            off_page_seo=off_page,
            recommendations=recommendations,
            competitor_analysis=competitors,
            generated_at=datetime.now()
        )
    
    async def _analyze_technical_seo(self, url: str) -> Dict[str, Any]:
        """分析技术SEO"""
        return {
            "mobile_friendly": True,
            "page_speed": {
                "desktop": 85,
                "mobile": 78
            },
            "ssl_certificate": True,
            "xml_sitemap": True,
            "robots_txt": True,
            "canonical_urls": True,
            "structured_data": {
                "present": True,
                "types": ["Organization", "WebPage"]
            },
            "core_web_vitals": {
                "lcp": 2.1,  # Largest Contentful Paint
                "fid": 15,   # First Input Delay
                "cls": 0.05  # Cumulative Layout Shift
            }
        }
    
    async def _analyze_on_page_seo(self, url: str) -> Dict[str, Any]:
        """分析页面SEO"""
        return {
            "title_tag": {
                "present": True,
                "length": 58,
                "optimized": True
            },
            "meta_description": {
                "present": True,
                "length": 155,
                "optimized": True
            },
            "heading_structure": {
                "h1_count": 1,
                "h2_count": 5,
                "h3_count": 8,
                "optimized": True
            },
            "content_quality": {
                "word_count": 2150,
                "readability_score": 68,
                "keyword_density": 1.8,
                "uniqueness": 98
            },
            "image_optimization": {
                "alt_text_coverage": 85,
                "compressed": True
            },
            "internal_links": 12,
            "external_links": 5
        }
    
    async def _analyze_off_page_seo(self, url: str) -> Dict[str, Any]:
        """分析站外SEO"""
        return {
            "backlinks": {
                "total": 145,
                "referring_domains": 52,
                "dofollow": 120,
                "nofollow": 25
            },
            "domain_authority": 45,
            "page_authority": 38,
            "social_signals": {
                "shares": 850,
                "likes": 1200,
                "comments": 95
            },
            "brand_mentions": 23
        }
    
    async def _analyze_competitors(self, url: str) -> Dict[str, Any]:
        """分析竞争对手"""
        return {
            "top_competitors": [
                {
                    "domain": "competitor1.com",
                    "domain_authority": 58,
                    "backlinks": 320,
                    "top_keywords": 45
                },
                {
                    "domain": "competitor2.com",
                    "domain_authority": 52,
                    "backlinks": 280,
                    "top_keywords": 38
                },
                {
                    "domain": "competitor3.com",
                    "domain_authority": 48,
                    "backlinks": 195,
                    "top_keywords": 32
                }
            ],
            "keyword_gaps": [
                "advanced seo techniques",
                "seo automation tools",
                "local seo strategies"
            ],
            "content_opportunities": [
                "In-depth guides",
                "Video content",
                "Case studies"
            ]
        }
    
    def _generate_recommendations(
        self,
        technical: Dict,
        on_page: Dict,
        off_page: Dict
    ) -> List[str]:
        """生成SEO建议"""
        recommendations = []
        
        # 技术SEO建议
        if technical["page_speed"]["mobile"] < 80:
            recommendations.append(
                "Improve mobile page speed (currently " + 
                str(technical["page_speed"]["mobile"]) + 
                "/100). Consider image optimization and lazy loading."
            )
        
        # 页面SEO建议
        content = on_page["content_quality"]
        if content["word_count"] < 1500:
            recommendations.append(
                f"Expand content to at least 1500 words (currently {content['word_count']})"
            )
        
        if content["keyword_density"] < 1.0:
            recommendations.append(
                "Increase keyword density to 1-2% for better relevance"
            )
        
        if on_page["image_optimization"]["alt_text_coverage"] < 100:
            recommendations.append(
                f"Add alt text to remaining images ({100 - on_page['image_optimization']['alt_text_coverage']}% missing)"
            )
        
        # 站外SEO建议
        backlinks = off_page["backlinks"]
        if backlinks["referring_domains"] < 100:
            recommendations.append(
                f"Build more high-quality backlinks (currently {backlinks['referring_domains']} referring domains)"
            )
        
        recommendations.extend([
            "Implement FAQ schema markup for rich snippets",
            "Create more long-form content targeting featured snippets",
            "Optimize for Core Web Vitals to improve rankings",
            "Build topical authority through content clusters"
        ])
        
        return recommendations
    
    def _calculate_overall_score(
        self,
        technical: Dict,
        on_page: Dict,
        off_page: Dict
    ) -> int:
        """计算总体SEO分数"""
        scores = []
        
        # 技术SEO分数 (30%)
        tech_score = (
            technical["page_speed"]["desktop"] * 0.15 +
            technical["page_speed"]["mobile"] * 0.15
        )
        scores.append(tech_score)
        
        # 页面SEO分数 (40%)
        content = on_page["content_quality"]
        page_score = (
            min(content["readability_score"], 100) * 0.1 +
            min(content["uniqueness"], 100) * 0.1 +
            (100 if on_page["title_tag"]["optimized"] else 50) * 0.1 +
            (100 if on_page["meta_description"]["optimized"] else 50) * 0.1
        )
        scores.append(page_score)
        
        # 站外SEO分数 (30%)
        off_score = min(off_page["domain_authority"] * 1.5, 100) * 0.3
        scores.append(off_score)
        
        return int(sum(scores))
    
    # ==================== 工具方法 ====================
    
    def export_keywords_to_csv(self, keywords: List[KeywordData], filename: str):
        """导出关键词到CSV"""
        import csv
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'Keyword', 'Search Volume', 'Difficulty', 'CPC', 
                'Competition', 'Trend', 'Intent'
            ])
            
            for kw in keywords:
                writer.writerow([
                    kw.keyword, kw.search_volume, kw.difficulty, 
                    kw.cpc, kw.competition, kw.trend, kw.intent
                ])
        
        logger.info(f"Exported {len(keywords)} keywords to {filename}")
    
    def export_report_to_json(self, report: SEOReport, filename: str):
        """导出报告到JSON"""
        report_dict = {
            "url": report.url,
            "overall_score": report.overall_score,
            "technical_seo": report.technical_seo,
            "on_page_seo": report.on_page_seo,
            "off_page_seo": report.off_page_seo,
            "recommendations": report.recommendations,
            "competitor_analysis": report.competitor_analysis,
            "generated_at": report.generated_at.isoformat()
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report_dict, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Exported SEO report to {filename}")


# ==================== 主函数和CLI接口 ====================

async def main():
    """主函数 - 演示SEOAI功能"""
    print("=" * 60)
    print("SEOAI - SEO Optimization Expert Agent")
    print("=" * 60)
    
    async with SEOAI() as seo_ai:
        # 1. 关键词研究演示
        print("\n📊 关键词研究 (Keyword Research)")
        print("-" * 40)
        
        seed_keywords = ["AI marketing", "digital marketing automation"]
        keywords = await seo_ai.research_keywords(seed_keywords)
        
        print(f"\n找到 {len(keywords)} 个相关关键词:\n")
        for i, kw in enumerate(keywords[:5], 1):
            print(f"{i}. {kw.keyword}")
            print(f"   搜索量: {kw.search_volume:,} | 难度: {kw.difficulty} | 意图: {kw.intent}")
            print(f"   相关词: {', '.join(kw.related_keywords[:3])}")
            print()
        
        # 2. 内容优化演示
        print("\n📝 内容优化 (Content Optimization)")
        print("-" * 40)
        
        sample_content = """
        AI marketing is transforming how businesses reach customers. 
        With machine learning and automation, marketers can now personalize 
        content at scale and optimize campaigns in real-time.
        """
        
        optimization = await seo_ai.optimize_content(
            sample_content,
            ["AI marketing", "marketing automation"]
        )
        
        print("\n标题建议:")
        for i, title in enumerate(optimization.title_suggestions[:3], 1):
            print(f"  {i}. {title}")
        
        print(f"\nMeta描述: {optimization.meta_description}")
        print(f"可读性分数: {optimization.readability_score}/100")
        print(f"\n关键词密度:")
        for kw, density in optimization.keyword_density.items():
            print(f"  {kw}: {density}%")
        
        # 3. 外链建设演示
        print("\n🔗 外链建设 (Link Building)")
        print("-" * 40)
        
        opportunities = await seo_ai.find_backlink_opportunities(
            niche="digital marketing",
            competitors=["competitor1.com", "competitor2.com"]
        )
        
        print(f"\n发现 {len(opportunities)} 个外链机会:\n")
        for i, opp in enumerate(opportunities[:3], 1):
            print(f"{i}. {opp.target_url}")
            print(f"   DA: {opp.domain_authority} | 相关度: {opp.relevance_score}")
            print(f"   类型: {opp.link_type} | 优先级: {opp.priority}")
            print()
        
        # 4. SEO报告演示
        print("\n📈 SEO分析报告")
        print("-" * 40)
        
        report = await seo_ai.generate_seo_report("https://example.com")
        
        print(f"\n网站: {report.url}")
        print(f"总体SEO分数: {report.overall_score}/100")
        print(f"\n技术SEO状态:")
        print(f"  - 移动端速度: {report.technical_seo['page_speed']['mobile']}/100")
        print(f"  - SSL证书: {'✓' if report.technical_seo['ssl_certificate'] else '✗'}")
        print(f"\n页面SEO状态:")
        print(f"  - 字数: {report.on_page_seo['content_quality']['word_count']}")
        print(f"  - 可读性: {report.on_page_seo['content_quality']['readability_score']}/100")
        print(f"\n前3项优化建议:")
        for i, rec in enumerate(report.recommendations[:3], 1):
            print(f"  {i}. {rec}")
        
        print("\n" + "=" * 60)
        print("演示完成!")
        print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
