#!/usr/bin/env python3
"""
百炼API配置模块
为6个AI Agent提供真实的AI能力
"""

import os
import json
import requests
from typing import List, Dict, Optional

class BaiLianAPI:
    """
    百炼API封装类
    支持通义千问系列模型
    """
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("BAILIAN_API_KEY")
        self.base_url = "https://dashscope.aliyuncs.com/api/v1"
        
        # 模型配置
        self.models = {
            'qwen-turbo': 'qwen-turbo',      # 快速响应，低成本
            'qwen-plus': 'qwen-plus',        # 平衡型
            'qwen-max': 'qwen-max',          # 最强能力
            'qwen-coder': 'qwen-coder'       # 代码专用
        }
        
    def chat(self, 
             messages: List[Dict], 
             model: str = "qwen-plus",
             temperature: float = 0.7,
             max_tokens: int = 4000) -> Optional[str]:
        """
        调用百炼API进行对话
        
        Args:
            messages: 消息列表 [{"role": "user", "content": "..."}]
            model: 模型名称
            temperature: 创造性程度 (0-1)
            max_tokens: 最大输出token数
            
        Returns:
            AI生成的文本，失败返回None
        """
        if not self.api_key:
            print("❌ 错误: 未设置BAILIAN_API_KEY")
            return None
        
        url = f"{self.base_url}/services/aigc/text-generation/generation"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": model,
            "input": {"messages": messages},
            "parameters": {
                "result_format": "message",
                "max_tokens": max_tokens,
                "temperature": temperature,
                "top_p": 0.9
            }
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            
            if response.status_code == 200:
                data = response.json()
                if "output" in data and "choices" in data["output"]:
                    return data["output"]["choices"][0]["message"]["content"]
                else:
                    print(f"⚠️ API响应格式异常: {data}")
                    return None
            elif response.status_code == 401:
                error = response.json()
                print(f"❌ API Key无效: {error.get('message', 'Unknown error')}")
                print("   请检查: https://dashscope.aliyun.com/ → API-KEY管理")
                return None
            else:
                print(f"❌ API错误: {response.status_code}")
                print(f"   响应: {response.text[:200]}")
                return None
                
        except requests.exceptions.Timeout:
            print("❌ API请求超时")
            return None
        except Exception as e:
            print(f"❌ API调用异常: {str(e)}")
            return None
    
    def test_connection(self) -> bool:
        """测试API连接是否正常"""
        print("🔄 测试百炼API连接...")
        result = self.chat(
            messages=[{"role": "user", "content": "你好"}],
            model="qwen-turbo",
            max_tokens=50
        )
        if result:
            print(f"✅ API连接成功！响应: {result[:30]}...")
            return True
        return False


class AgentWithBaiLian:
    """
    集成百炼API的Agent基类
    6个Agent都继承这个类
    """
    
    def __init__(self, api_key: str = None):
        self.api = BaiLianAPI(api_key)
        self.model = "qwen-plus"  # 默认模型
        
    def generate(self, prompt: str, system_prompt: str = None) -> str:
        """
        生成内容
        
        Args:
            prompt: 用户提示词
            system_prompt: 系统提示词（可选）
            
        Returns:
            生成的内容
        """
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        result = self.api.chat(messages, model=self.model)
        
        if result:
            return result
        else:
            # API失败时返回模拟内容
            return self._mock_generate(prompt)
    
    def _mock_generate(self, prompt: str) -> str:
        """API失败时的模拟生成"""
        return f"[模拟模式] 基于提示词: {prompt[:50]}...\n\n（请配置有效的BAILIAN_API_KEY以获取真实AI生成内容）"


# ============ 6个Agent的具体实现 ============

class ContentAgent(AgentWithBaiLian):
    """ContentAI - 内容创作Agent"""
    
    def __init__(self, api_key: str = None):
        super().__init__(api_key)
        self.model = "qwen-plus"
    
    def create_article(self, topic: str, platform: str = "wechat") -> Dict:
        """创建完整文章"""
        
        system_prompt = """你是一位专业的内容创作者，擅长创作爆款文章。
根据用户提供的主题和平台，生成高质量的内容。
输出格式必须是JSON，包含以下字段：
- title: 文章标题
- content: 完整文章内容（Markdown格式）
- summary: 内容摘要
- keywords: 关键词列表"""
        
        prompt = f"""请为主题"{topic}"创作一篇{platform}平台的爆款文章。

要求：
1. 标题要有吸引力，使用数字、悬念或痛点
2. 内容结构清晰，有小标题
3. 语言风格适合{platform}平台
4. 包含实用干货，不是泛泛而谈
5. 字数1500-2500字

请直接输出JSON格式。"""
        
        result = self.generate(prompt, system_prompt)
        
        try:
            # 尝试解析JSON
            if "```json" in result:
                json_str = result.split("```json")[1].split("```")[0].strip()
            elif "```" in result:
                json_str = result.split("```")[1].strip()
            else:
                json_str = result
            
            data = json.loads(json_str)
            return {
                'success': True,
                'title': data.get('title', topic),
                'content': data.get('content', result),
                'summary': data.get('summary', ''),
                'keywords': data.get('keywords', []),
                'platform': platform
            }
        except:
            # 解析失败，返回原始文本
            return {
                'success': True,
                'title': topic,
                'content': result,
                'summary': '',
                'keywords': [],
                'platform': platform
            }


class ServiceAgent(AgentWithBaiLian):
    """ServiceAI - 客服Agent"""
    
    def __init__(self, api_key: str = None):
        super().__init__(api_key)
        self.model = "qwen-turbo"  # 快速响应
    
    def reply(self, message: str, context: Dict = None) -> str:
        """回复客户消息"""
        
        system_prompt = """你是一位专业的客服代表，友好、耐心、专业。
回答客户问题时：
1. 先理解客户问题
2. 给出清晰、有帮助的回答
3. 必要时引导客户进行下一步
4. 保持礼貌和专业"""
        
        context_str = ""
        if context:
            context_str = f"\n上下文信息：{json.dumps(context, ensure_ascii=False)}"
        
        prompt = f"""客户消息：{message}{context_str}

请给出专业、友好的回复。"""
        
        return self.generate(prompt, system_prompt)


class ResearchAgent(AgentWithBaiLian):
    """ResearchAI - 市场研究Agent"""
    
    def __init__(self, api_key: str = None):
        super().__init__(api_key)
        self.model = "qwen-max"  # 最强模型用于研究
    
    def analyze_market(self, niche: str) -> Dict:
        """分析市场趋势"""
        
        system_prompt = """你是一位资深市场分析师，擅长行业趋势分析和竞品研究。
提供数据驱动的洞察，包括市场规模、增长趋势、竞争格局等。
输出JSON格式。"""
        
        prompt = f"""请分析"{niche}"市场的现状和趋势：

请提供：
1. 市场规模和增长预测
2. 主要竞争对手分析
3. 市场机会和风险
4. 进入策略建议
5. 关键成功因素

输出JSON格式，包含：
- market_size: 市场规模
- growth_rate: 增长率
- competitors: 竞争对手列表
- opportunities: 机会列表
- risks: 风险列表
- recommendations: 建议列表"""
        
        result = self.generate(prompt, system_prompt)
        
        try:
            if "```json" in result:
                json_str = result.split("```json")[1].split("```")[0].strip()
            elif "```" in result:
                json_str = result.split("```")[1].strip()
            else:
                json_str = result
            
            return json.loads(json_str)
        except:
            return {
                'market_size': '未知',
                'growth_rate': '未知',
                'competitors': [],
                'opportunities': ['市场正在增长'],
                'risks': ['竞争激烈'],
                'recommendations': [result[:200]]
            }


class TradeAgent(AgentWithBaiLian):
    """TradeAI - 交易分析Agent"""
    
    def __init__(self, api_key: str = None):
        super().__init__(api_key)
        self.model = "qwen-plus"
    
    def generate_signal(self, symbol: str = "BTC/USDT") -> Dict:
        """生成交易信号（模拟模式）"""
        
        system_prompt = """你是一位专业的交易分析师，提供技术分析和交易建议。
重要提示：这只是技术分析演示，不构成投资建议。
所有信号都在模拟模式下运行。"""
        
        prompt = f"""请分析{symbol}的技术面：

请提供：
1. 当前趋势判断（多/空/震荡）
2. 关键支撑位和阻力位
3. 建议的操作策略
4. 风险提示

注意：这是模拟演示，仅用于学习目的。"""
        
        result = self.generate(prompt, system_prompt)
        
        return {
            'symbol': symbol,
            'signal': '模拟信号',
            'analysis': result,
            'demo_mode': True,
            'disclaimer': '本信号仅供演示，不构成投资建议'
        }


class SEOAgent(AgentWithBaiLian):
    """SEOAI - SEO优化Agent"""
    
    def __init__(self, api_key: str = None):
        super().__init__(api_key)
        self.model = "qwen-plus"
    
    def analyze_keywords(self, topic: str) -> Dict:
        """分析关键词"""
        
        system_prompt = """你是一位SEO专家，擅长关键词研究和内容优化。
提供具体可执行的SEO建议。"""
        
        prompt = f"""请为"{topic}"进行关键词分析：

请提供：
1. 主要关键词（搜索量高）
2. 长尾关键词（竞争度低）
3. 关键词布局建议
4. 内容优化建议
5. 标题和描述建议

输出JSON格式。"""
        
        result = self.generate(prompt, system_prompt)
        
        try:
            if "```json" in result:
                json_str = result.split("```json")[1].split("```")[0].strip()
            elif "```" in result:
                json_str = result.split("```")[1].strip()
            else:
                json_str = result
            
            return json.loads(json_str)
        except:
            return {
                'primary_keywords': [topic],
                'long_tail_keywords': [],
                'suggestions': [result[:300]]
            }


class EmailAgent(AgentWithBaiLian):
    """EmailAI - 邮件营销Agent"""
    
    def __init__(self, api_key: str = None):
        super().__init__(api_key)
        self.model = "qwen-plus"
    
    def create_campaign(self, campaign_type: str, audience: str) -> Dict:
        """创建邮件营销活动"""
        
        system_prompt = """你是一位邮件营销专家，擅长撰写高转化率的营销邮件。
邮件要有吸引力、有说服力，同时保持专业。"""
        
        prompt = f"""请为"{campaign_type}"活动创建一封营销邮件：

目标受众：{audience}

请提供：
1. 邮件主题行（5个选项，按吸引力排序）
2. 邮件正文
3. 行动号召（CTA）
4. 发送时间建议

输出JSON格式。"""
        
        result = self.generate(prompt, system_prompt)
        
        try:
            if "```json" in result:
                json_str = result.split("```json")[1].split("```")[0].strip()
            elif "```" in result:
                json_str = result.split("```")[1].strip()
            else:
                json_str = result
            
            data = json.loads(json_str)
            return {
                'subject_lines': data.get('subject_lines', []),
                'body': data.get('body', result),
                'cta': data.get('cta', '立即行动'),
                'send_time': data.get('send_time', '工作日上午10点')
            }
        except:
            return {
                'subject_lines': ['新品上线', '限时优惠'],
                'body': result,
                'cta': '了解更多',
                'send_time': '工作日上午10点'
            }


# ============ Agent团队管理器 ============

class AgentTeamWithBaiLian:
    """
    集成百炼API的Agent团队
    """
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("BAILIAN_API_KEY")
        
        # 初始化6个Agent
        self.agents = {
            'content': ContentAgent(self.api_key),
            'service': ServiceAgent(self.api_key),
            'research': ResearchAgent(self.api_key),
            'trade': TradeAgent(self.api_key),
            'seo': SEOAgent(self.api_key),
            'email': EmailAgent(self.api_key)
        }
        
        print(f"✅ Agent团队已初始化（百炼API）")
        print(f"   - ContentAI: 内容创作")
        print(f"   - ServiceAI: 客户服务")
        print(f"   - ResearchAI: 市场研究")
        print(f"   - TradeAI: 交易分析")
        print(f"   - SEOAI: SEO优化")
        print(f"   - EmailAI: 邮件营销")
    
    def test_api(self) -> bool:
        """测试API是否可用"""
        return self.agents['content'].api.test_connection()
    
    def run_task(self, agent_type: str, **kwargs):
        """运行指定Agent的任务"""
        agent = self.agents.get(agent_type)
        if not agent:
            return {'error': f'未知Agent类型: {agent_type}'}
        
        if agent_type == 'content':
            return agent.create_article(kwargs.get('topic'), kwargs.get('platform', 'wechat'))
        elif agent_type == 'service':
            return agent.reply(kwargs.get('message'), kwargs.get('context'))
        elif agent_type == 'research':
            return agent.analyze_market(kwargs.get('niche'))
        elif agent_type == 'trade':
            return agent.generate_signal(kwargs.get('symbol', 'BTC/USDT'))
        elif agent_type == 'seo':
            return agent.analyze_keywords(kwargs.get('topic'))
        elif agent_type == 'email':
            return agent.create_campaign(kwargs.get('campaign_type'), kwargs.get('audience'))
        
        return {'error': '任务执行失败'}


# ============ 测试代码 ============

if __name__ == '__main__':
    print("🚀 百炼API Agent团队测试\n")
    
    # 从环境变量获取API Key
    api_key = os.getenv("BAILIAN_API_KEY")
    
    if not api_key:
        print("❌ 请设置环境变量 BAILIAN_API_KEY")
        print("   export BAILIAN_API_KEY=your_api_key_here")
        print("\n💡 获取API Key: https://dashscope.aliyun.com/")
        exit(1)
    
    # 初始化团队
    team = AgentTeamWithBaiLian(api_key)
    
    # 测试API连接
    if not team.test_api():
        print("\n⚠️ API测试失败，将以模拟模式运行")
    
    print("\n" + "="*60)
    print("测试各Agent功能...")
    print("="*60 + "\n")
    
    # 测试ContentAI
    print("📝 ContentAI 测试:")
    result = team.run_task('content', topic='AI副业赚钱', platform='wechat')
    print(f"标题: {result.get('title', 'N/A')[:50]}...")
    print(f"内容长度: {len(result.get('content', ''))} 字符\n")
    
    # 测试ServiceAI
    print("💬 ServiceAI 测试:")
    result = team.run_task('service', message='这个产品怎么用？')
    print(f"回复: {result[:100]}...\n")
    
    # 测试ResearchAI
    print("🔍 ResearchAI 测试:")
    result = team.run_task('research', niche='AI工具市场')
    print(f"市场规模: {result.get('market_size', 'N/A')}")
    print(f"建议: {result.get('recommendations', [])[:2]}\n")
    
    print("✅ 测试完成！")
