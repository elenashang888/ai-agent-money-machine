#!/usr/bin/env python3
"""
ServiceAI - 智能客服机器人
7×24小时自动回复，处理售前售后
"""

import os
import json
import asyncio
import re
from datetime import datetime
from typing import List, Dict, Optional, Callable
from dataclasses import dataclass, asdict
from enum import Enum

class MessageType(Enum):
    """消息类型"""
    TEXT = "text"
    IMAGE = "image"
    VOICE = "voice"
    FILE = "file"

class IntentType(Enum):
    """意图类型"""
    GREETING = "greeting"           # 问候
    PRODUCT_INQUIRY = "product"     # 产品咨询
    PRICE_INQUIRY = "price"         # 价格咨询
    ORDER_STATUS = "order"          # 订单查询
    REFUND = "refund"               # 退款
    COMPLAINT = "complaint"         # 投诉
    TECH_SUPPORT = "tech"           # 技术支持
    GENERAL = "general"             # 一般问题
    UNKNOWN = "unknown"             # 未知

@dataclass
class Message:
    """消息数据类"""
    id: str
    user_id: str
    content: str
    msg_type: MessageType
    timestamp: datetime
    platform: str  # wechat, douyin, taobao, etc.
    
@dataclass
class Response:
    """回复数据类"""
    message: str
    actions: List[Dict]
    intent: IntentType
    confidence: float
    
class ServiceAI:
    """
    ServiceAI - 智能客服机器人
    
    功能：
    1. 7×24小时自动回复
    2. 多轮对话处理
    3. 意图识别
    4. 情感分析
    5. 工单自动创建
    6. 数据统计分析
    """
    
    def __init__(self, business_config: Optional[Dict] = None):
        """初始化ServiceAI"""
        self.business_config = business_config or self._default_config()
        self.knowledge_base = self._load_knowledge_base()
        self.conversation_history = {}
        self.intent_handlers = self._register_handlers()
        self.stats = {
            "total_messages": 0,
            "auto_replied": 0,
            "human_transferred": 0,
            "satisfaction": 0.0
        }
        
    def _default_config(self) -> Dict:
        """默认配置"""
        return {
            "business_name": "AgentVerse",
            "business_type": "AI工具",
            "products": [
                {"name": "ContentAI", "price": 99, "desc": "内容创作助手"},
                {"name": "ServiceAI", "price": 199, "desc": "智能客服机器人"},
                {"name": "TradeAI", "price": 299, "desc": "智能交易助手"}
            ],
            "faq": {
                "怎么购买": "点击菜单【购买产品】或回复【购买】",
                "多少钱": "我们有三个套餐：基础版99元，专业版199元，企业版299元",
                "有优惠吗": "新用户首单8折，回复【优惠】领取",
                "怎么退款": "7天无理由退款，联系客服处理",
                "技术支持": "技术问题请加QQ群：123456789"
            },
            "working_hours": "9:00-18:00",
            "human_handoff_threshold": 0.6,  # 置信度低于此值转人工
            "max_auto_reply": 5  # 单会话最大自动回复数
        }
    
    def _load_knowledge_base(self) -> Dict:
        """加载知识库"""
        return {
            "products": self.business_config.get("products", []),
            "faq": self.business_config.get("faq", {}),
            "policies": {
                "refund": "7天无理由退款",
                "warranty": "一年质保",
                "shipping": "24小时内发货"
            }
        }
    
    def _register_handlers(self) -> Dict[IntentType, Callable]:
        """注册意图处理器"""
        return {
            IntentType.GREETING: self._handle_greeting,
            IntentType.PRODUCT_INQUIRY: self._handle_product,
            IntentType.PRICE_INQUIRY: self._handle_price,
            IntentType.ORDER_STATUS: self._handle_order,
            IntentType.REFUND: self._handle_refund,
            IntentType.COMPLAINT: self._handle_complaint,
            IntentType.TECH_SUPPORT: self._handle_tech,
            IntentType.GENERAL: self._handle_general,
            IntentType.UNKNOWN: self._handle_unknown
        }
    
    async def process_message(self, message: Message) -> Response:
        """
        处理用户消息
        
        Args:
            message: 用户消息
            
        Returns:
            回复对象
        """
        self.stats["total_messages"] += 1
        
        # 1. 意图识别
        intent, confidence = self._classify_intent(message.content)
        
        # 2. 情感分析
        sentiment = self._analyze_sentiment(message.content)
        
        # 3. 保存对话历史
        self._save_history(message)
        
        # 4. 检查是否需要转人工
        if self._should_transfer_to_human(message, intent, confidence, sentiment):
            self.stats["human_transferred"] += 1
            return Response(
                message="正在为您转接人工客服，请稍候...",
                actions=[{"type": "transfer", "to": "human"}],
                intent=intent,
                confidence=confidence
            )
        
        # 5. 调用对应处理器
        handler = self.intent_handlers.get(intent, self._handle_unknown)
        response = await handler(message, sentiment)
        
        self.stats["auto_replied"] += 1
        
        return response
    
    def _classify_intent(self, content: str) -> tuple:
        """
        意图分类（基于规则+关键词）
        
        Returns:
            (意图类型, 置信度)
        """
        content = content.lower()
        
        # 问候意图
        greeting_patterns = ["你好", "您好", "hi", "hello", "在吗", "有人吗"]
        if any(p in content for p in greeting_patterns):
            return IntentType.GREETING, 0.95
        
        # 价格意图
        price_patterns = ["多少钱", "价格", "优惠", "折扣", "便宜", "贵"]
        if any(p in content for p in price_patterns):
            return IntentType.PRICE_INQUIRY, 0.9
        
        # 产品意图
        product_patterns = ["产品", "功能", "有什么", "介绍", "推荐"]
        if any(p in content for p in product_patterns):
            return IntentType.PRODUCT_INQUIRY, 0.85
        
        # 订单意图
        order_patterns = ["订单", "物流", "发货", "快递", "到哪了"]
        if any(p in content for p in order_patterns):
            return IntentType.ORDER_STATUS, 0.9
        
        # 退款意图
        refund_patterns = ["退款", "退货", "退钱", "不满意", "不要了"]
        if any(p in content for p in refund_patterns):
            return IntentType.REFUND, 0.95
        
        # 投诉意图
        complaint_patterns = ["投诉", "差评", "举报", "骗子", "坑人", "垃圾"]
        if any(p in content for p in complaint_patterns):
            return IntentType.COMPLAINT, 0.95
        
        # 技术支持
        tech_patterns = ["bug", "错误", "不行", "失败", "怎么用", "不会用", "技术"]
        if any(p in content for p in tech_patterns):
            return IntentType.TECH_SUPPORT, 0.85
        
        # FAQ匹配
        for question in self.knowledge_base["faq"].keys():
            if question in content or self._similarity(question, content) > 0.8:
                return IntentType.GENERAL, 0.9
        
        return IntentType.UNKNOWN, 0.5
    
    def _analyze_sentiment(self, content: str) -> Dict:
        """
        情感分析（简化版）
        
        Returns:
            情感分析结果
        """
        positive_words = ["好", "棒", "喜欢", "满意", "感谢", "谢谢", "不错", "推荐"]
        negative_words = ["差", "烂", "垃圾", "坑", "骗", "失望", "生气", "投诉", "退"]
        
        positive_count = sum(1 for w in positive_words if w in content)
        negative_count = sum(1 for w in negative_words if w in content)
        
        if negative_count > positive_count:
            return {"sentiment": "negative", "score": -0.5}
        elif positive_count > negative_count:
            return {"sentiment": "positive", "score": 0.5}
        else:
            return {"sentiment": "neutral", "score": 0}
    
    def _should_transfer_to_human(
        self,
        message: Message,
        intent: IntentType,
        confidence: float,
        sentiment: Dict
    ) -> bool:
        """判断是否需要转人工"""
        # 置信度太低
        if confidence < self.business_config["human_handoff_threshold"]:
            return True
        
        # 负面情绪严重
        if sentiment["sentiment"] == "negative" and sentiment["score"] < -0.8:
            return True
        
        # 投诉类
        if intent == IntentType.COMPLAINT:
            return True
        
        # 单会话回复次数过多
        user_history = self.conversation_history.get(message.user_id, [])
        auto_reply_count = sum(1 for h in user_history if h.get("is_auto_reply"))
        if auto_reply_count >= self.business_config["max_auto_reply"]:
            return True
        
        return False
    
    async def _handle_greeting(self, message: Message, sentiment: Dict) -> Response:
        """处理问候"""
        hour = datetime.now().hour
        if 6 <= hour < 12:
            greeting = "早上好"
        elif 12 <= hour < 18:
            greeting = "下午好"
        else:
            greeting = "晚上好"
        
        return Response(
            message=f"{greeting}！我是{self.business_config['business_name']}的智能客服，有什么可以帮您的吗？\n\n您可以问：\n• 产品介绍\n• 价格咨询\n• 技术支持\n• 订单查询",
            actions=[{"type": "show_menu", "options": ["产品介绍", "价格咨询", "技术支持"]}],
            intent=IntentType.GREETING,
            confidence=0.95
        )
    
    async def _handle_product(self, message: Message, sentiment: Dict) -> Response:
        """处理产品咨询"""
        products = self.knowledge_base["products"]
        
        product_list = "\n".join([
            f"• {p['name']}：{p['desc']}，{p['price']}元"
            for p in products
        ])
        
        return Response(
            message=f"我们的产品：\n\n{product_list}\n\n回复【购买+产品名】即可下单，比如【购买ContentAI】",
            actions=[{"type": "show_products", "products": products}],
            intent=IntentType.PRODUCT_INQUIRY,
            confidence=0.9
        )
    
    async def _handle_price(self, message: Message, sentiment: Dict) -> Response:
        """处理价格咨询"""
        products = self.knowledge_base["products"]
        
        price_info = "\n".join([
            f"• {p['name']}：{p['price']}元"
            for p in products
        ])
        
        return Response(
            message=f"我们的价格：\n\n{price_info}\n\n🎁 新用户首单8折优惠！\n回复【优惠】领取折扣码",
            actions=[{"type": "show_prices", "products": products}],
            intent=IntentType.PRICE_INQUIRY,
            confidence=0.9
        )
    
    async def _handle_order(self, message: Message, sentiment: Dict) -> Response:
        """处理订单查询"""
        return Response(
            message="请提供您的订单号，我帮您查询物流信息。\n\n格式：订单号+查询，比如【123456789查询】",
            actions=[{"type": "request_order_id"}],
            intent=IntentType.ORDER_STATUS,
            confidence=0.9
        )
    
    async def _handle_refund(self, message: Message, sentiment: Dict) -> Response:
        """处理退款"""
        return Response(
            message="我们支持7天无理由退款。\n\n请提供：\n1. 订单号\n2. 退款原因\n\n我会立即为您处理，款项将在3个工作日内原路退回。",
            actions=[{"type": "start_refund", "policy": "7天无理由"}],
            intent=IntentType.REFUND,
            confidence=0.95
        )
    
    async def _handle_complaint(self, message: Message, sentiment: Dict) -> Response:
        """处理投诉"""
        return Response(
            message="非常抱歉给您带来不好的体验！😔\n\n我会立即为您转接人工客服处理，请稍候...\n\n您也可以直接拨打客服电话：400-123-4567",
            actions=[{"type": "transfer", "to": "human", "priority": "high"}],
            intent=IntentType.COMPLAINT,
            confidence=0.95
        )
    
    async def _handle_tech(self, message: Message, sentiment: Dict) -> Response:
        """处理技术支持"""
        return Response(
            message="技术支持请加入我们的技术交流群：\n\n📱 QQ群：123456789\n💬 微信群：回复【加群】获取二维码\n\n常见问题文档：https://docs.agentverse.ai",
            actions=[{"type": "show_support", "channels": ["qq", "wechat"]}],
            intent=IntentType.TECH_SUPPORT,
            confidence=0.85
        )
    
    async def _handle_general(self, message: Message, sentiment: Dict) -> Response:
        """处理一般问题（FAQ）"""
        # 匹配FAQ
        for question, answer in self.knowledge_base["faq"].items():
            if question in message.content or self._similarity(question, message.content) > 0.8:
                return Response(
                    message=answer,
                    actions=[{"type": "faq_matched", "question": question}],
                    intent=IntentType.GENERAL,
                    confidence=0.9
                )
        
        # 没有匹配到FAQ
        return await self._handle_unknown(message, sentiment)
    
    async def _handle_unknown(self, message: Message, sentiment: Dict) -> Response:
        """处理未知问题"""
        return Response(
            message="抱歉，我可能没理解您的问题。\n\n您可以尝试：\n• 换种方式描述\n• 查看常见问题【回复FAQ】\n• 联系人工客服【回复人工】",
            actions=[{"type": "suggest_options", "options": ["FAQ", "人工"]}],
            intent=IntentType.UNKNOWN,
            confidence=0.5
        )
    
    def _save_history(self, message: Message):
        """保存对话历史"""
        if message.user_id not in self.conversation_history:
            self.conversation_history[message.user_id] = []
        
        self.conversation_history[message.user_id].append({
            "content": message.content,
            "timestamp": message.timestamp.isoformat(),
            "platform": message.platform
        })
        
        # 只保留最近20条
        self.conversation_history[message.user_id] = \
            self.conversation_history[message.user_id][-20:]
    
    def _similarity(self, s1: str, s2: str) -> float:
        """计算字符串相似度（简化版）"""
        # 这里可以使用更复杂的算法，如余弦相似度
        set1 = set(s1)
        set2 = set(s2)
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        return intersection / union if union > 0 else 0
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return {
            **self.stats,
            "resolution_rate": self.stats["auto_replied"] / max(self.stats["total_messages"], 1),
            "human_transfer_rate": self.stats["human_transferred"] / max(self.stats["total_messages"], 1)
        }
    
    def export_knowledge_base(self, filepath: str):
        """导出知识库"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.knowledge_base, f, ensure_ascii=False, indent=2)
    
    def import_knowledge_base(self, filepath: str):
        """导入知识库"""
        with open(filepath, 'r', encoding='utf-8') as f:
            self.knowledge_base = json.load(f)


# 使用示例
async def main():
    """主函数示例"""
    
    # 初始化ServiceAI
    service_ai = ServiceAI()
    
    print("🤖 ServiceAI 智能客服机器人已启动\n")
    
    # 模拟用户消息
    test_messages = [
        Message(id="1", user_id="user_001", content="你好", msg_type=MessageType.TEXT, timestamp=datetime.now(), platform="wechat"),
        Message(id="2", user_id="user_001", content="你们有什么产品？", msg_type=MessageType.TEXT, timestamp=datetime.now(), platform="wechat"),
        Message(id="3", user_id="user_001", content="多少钱？", msg_type=MessageType.TEXT, timestamp=datetime.now(), platform="wechat"),
        Message(id="4", user_id="user_002", content="我要退款", msg_type=MessageType.TEXT, timestamp=datetime.now(), platform="wechat"),
        Message(id="5", user_id="user_003", content="垃圾产品，投诉！", msg_type=MessageType.TEXT, timestamp=datetime.now(), platform="wechat"),
    ]
    
    for msg in test_messages:
        print(f"👤 用户: {msg.content}")
        response = await service_ai.process_message(msg)
        print(f"🤖 客服: {response.message}")
        print(f"📊 意图: {response.intent.value}, 置信度: {response.confidence:.2f}")
        print("-" * 50)
    
    # 打印统计
    stats = service_ai.get_stats()
    print("\n📈 客服统计:")
    print(f"  总消息数: {stats['total_messages']}")
    print(f"  自动回复: {stats['auto_replied']}")
    print(f"  转人工: {stats['human_transferred']}")
    print(f"  解决率: {stats['resolution_rate']:.1%}")


if __name__ == "__main__":
    # 运行示例
    asyncio.run(main())
