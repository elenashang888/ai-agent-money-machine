#!/usr/bin/env python3
"""
TradeAI - 智能交易助手
基于AI的智能交易分析和决策系统
"""

import os
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import asyncio

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TradeSignal(Enum):
    """交易信号"""
    BUY = "buy"
    SELL = "sell"
    HOLD = "hold"
    STRONG_BUY = "strong_buy"
    STRONG_SELL = "strong_sell"


class RiskLevel(Enum):
    """风险等级"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    EXTREME = "extreme"


@dataclass
class MarketData:
    """市场数据"""
    symbol: str
    price: float
    volume: float
    timestamp: datetime
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    
    def to_dict(self) -> Dict:
        return {
            "symbol": self.symbol,
            "price": self.price,
            "volume": self.volume,
            "timestamp": self.timestamp.isoformat(),
            "open_price": self.open_price,
            "high_price": self.high_price,
            "low_price": self.low_price,
            "close_price": self.close_price
        }


@dataclass
class TradeRecommendation:
    """交易建议"""
    symbol: str
    signal: TradeSignal
    confidence: float
    entry_price: float
    stop_loss: float
    take_profit: float
    risk_level: RiskLevel
    reasoning: str
    timestamp: datetime
    
    def to_dict(self) -> Dict:
        return {
            "symbol": self.symbol,
            "signal": self.signal.value,
            "confidence": self.confidence,
            "entry_price": self.entry_price,
            "stop_loss": self.stop_loss,
            "take_profit": self.take_profit,
            "risk_level": self.risk_level.value,
            "reasoning": self.reasoning,
            "timestamp": self.timestamp.isoformat()
        }


@dataclass
class PortfolioPosition:
    """持仓信息"""
    symbol: str
    quantity: float
    avg_cost: float
    current_price: float
    unrealized_pnl: float
    realized_pnl: float
    
    @property
    def market_value(self) -> float:
        return self.quantity * self.current_price
    
    @property
    def total_pnl(self) -> float:
        return self.unrealized_pnl + self.realized_pnl
    
    def to_dict(self) -> Dict:
        return {
            "symbol": self.symbol,
            "quantity": self.quantity,
            "avg_cost": self.avg_cost,
            "current_price": self.current_price,
            "unrealized_pnl": self.unrealized_pnl,
            "realized_pnl": self.realized_pnl,
            "market_value": self.market_value,
            "total_pnl": self.total_pnl
        }


class TechnicalAnalyzer:
    """技术分析器"""
    
    def __init__(self):
        self.indicators = {}
    
    def calculate_sma(self, prices: List[float], period: int) -> float:
        """计算简单移动平均线"""
        if len(prices) < period:
            return sum(prices) / len(prices)
        return sum(prices[-period:]) / period
    
    def calculate_ema(self, prices: List[float], period: int) -> float:
        """计算指数移动平均线"""
        if len(prices) < period:
            return self.calculate_sma(prices, len(prices))
        
        multiplier = 2 / (period + 1)
        ema = self.calculate_sma(prices[:period], period)
        
        for price in prices[period:]:
            ema = (price - ema) * multiplier + ema
        
        return ema
    
    def calculate_rsi(self, prices: List[float], period: int = 14) -> float:
        """计算RSI指标"""
        if len(prices) < period + 1:
            return 50.0
        
        gains = []
        losses = []
        
        for i in range(1, len(prices)):
            change = prices[i] - prices[i-1]
            if change > 0:
                gains.append(change)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(abs(change))
        
        if len(gains) < period:
            return 50.0
        
        avg_gain = sum(gains[-period:]) / period
        avg_loss = sum(losses[-period:]) / period
        
        if avg_loss == 0:
            return 100.0
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi
    
    def calculate_macd(self, prices: List[float]) -> Tuple[float, float, float]:
        """计算MACD指标"""
        ema_12 = self.calculate_ema(prices, 12)
        ema_26 = self.calculate_ema(prices, 26)
        
        macd_line = ema_12 - ema_26
        signal_line = self.calculate_ema([macd_line], 9)
        histogram = macd_line - signal_line
        
        return macd_line, signal_line, histogram
    
    def calculate_bollinger_bands(self, prices: List[float], period: int = 20) -> Tuple[float, float, float]:
        """计算布林带"""
        if len(prices) < period:
            middle = sum(prices) / len(prices)
            std = 0
        else:
            recent_prices = prices[-period:]
            middle = sum(recent_prices) / period
            variance = sum((p - middle) ** 2 for p in recent_prices) / period
            std = variance ** 0.5
        
        upper = middle + (2 * std)
        lower = middle - (2 * std)
        
        return upper, middle, lower
    
    def analyze_trend(self, prices: List[float]) -> Dict:
        """分析趋势"""
        if len(prices) < 20:
            return {"trend": "neutral", "strength": 0}
        
        sma_20 = self.calculate_sma(prices, 20)
        sma_50 = self.calculate_sma(prices, min(50, len(prices)))
        
        current_price = prices[-1]
        
        if current_price > sma_20 > sma_50:
            trend = "bullish"
            strength = min((current_price - sma_50) / sma_50 * 100, 100)
        elif current_price < sma_20 < sma_50:
            trend = "bearish"
            strength = min((sma_50 - current_price) / sma_50 * 100, 100)
        else:
            trend = "neutral"
            strength = 0
        
        return {"trend": trend, "strength": strength}


class RiskManager:
    """风险管理器"""
    
    def __init__(self, max_position_size: float = 0.1, max_portfolio_risk: float = 0.02):
        self.max_position_size = max_position_size  # 最大单仓位比例
        self.max_portfolio_risk = max_portfolio_risk  # 最大组合风险
        self.positions: Dict[str, PortfolioPosition] = {}
    
    def calculate_position_size(self, symbol: str, entry_price: float, 
                                stop_loss: float, portfolio_value: float) -> float:
        """计算仓位大小"""
        risk_per_trade = portfolio_value * self.max_portfolio_risk
        price_risk = abs(entry_price - stop_loss)
        
        if price_risk == 0:
            return 0
        
        position_size = risk_per_trade / price_risk
        max_position = portfolio_value * self.max_position_size / entry_price
        
        return min(position_size, max_position)
    
    def calculate_stop_loss(self, entry_price: float, risk_percent: float = 0.02) -> float:
        """计算止损价格"""
        return entry_price * (1 - risk_percent)
    
    def calculate_take_profit(self, entry_price: float, stop_loss: float, 
                             risk_reward_ratio: float = 2.0) -> float:
        """计算止盈价格"""
        risk = entry_price - stop_loss
        return entry_price + (risk * risk_reward_ratio)
    
    def assess_risk_level(self, volatility: float, position_size: float, 
                         portfolio_value: float) -> RiskLevel:
        """评估风险等级"""
        position_ratio = position_size / portfolio_value
        
        if volatility > 0.05 or position_ratio > 0.2:
            return RiskLevel.EXTREME
        elif volatility > 0.03 or position_ratio > 0.1:
            return RiskLevel.HIGH
        elif volatility > 0.02 or position_ratio > 0.05:
            return RiskLevel.MEDIUM
        else:
            return RiskLevel.LOW
    
    def check_portfolio_risk(self) -> Dict:
        """检查组合风险"""
        total_exposure = sum(pos.market_value for pos in self.positions.values())
        total_pnl = sum(pos.total_pnl for pos in self.positions.values())
        
        return {
            "total_exposure": total_exposure,
            "total_pnl": total_pnl,
            "position_count": len(self.positions),
            "risk_assessment": "normal" if total_exposure < 100000 else "high"
        }


class TradeAI:
    """智能交易助手主类"""
    
    def __init__(self, config_path: str = "config.json"):
        self.config = self._load_config(config_path)
        self.technical_analyzer = TechnicalAnalyzer()
        self.risk_manager = RiskManager(
            max_position_size=self.config.get("max_position_size", 0.1),
            max_portfolio_risk=self.config.get("max_portfolio_risk", 0.02)
        )
        self.price_history: Dict[str, List[float]] = {}
        self.recommendations: List[TradeRecommendation] = []
        
        logger.info("TradeAI initialized successfully")
    
    def _load_config(self, config_path: str) -> Dict:
        """加载配置"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"Config file not found: {config_path}, using defaults")
            return self._default_config()
    
    def _default_config(self) -> Dict:
        """默认配置"""
        return {
            "max_position_size": 0.1,
            "max_portfolio_risk": 0.02,
            "min_confidence": 0.6,
            "risk_reward_ratio": 2.0,
            "symbols": ["BTC", "ETH", "AAPL", "TSLA"]
        }
    
    def update_price_data(self, symbol: str, price: float):
        """更新价格数据"""
        if symbol not in self.price_history:
            self.price_history[symbol] = []
        
        self.price_history[symbol].append(price)
        
        # 保持最多1000个数据点
        if len(self.price_history[symbol]) > 1000:
            self.price_history[symbol] = self.price_history[symbol][-1000:]
    
    def analyze_market(self, symbol: str, current_price: float) -> Dict:
        """分析市场"""
        self.update_price_data(symbol, current_price)
        
        if symbol not in self.price_history or len(self.price_history[symbol]) < 20:
            return {"error": "Insufficient data"}
        
        prices = self.price_history[symbol]
        
        # 计算技术指标
        sma_20 = self.technical_analyzer.calculate_sma(prices, 20)
        sma_50 = self.technical_analyzer.calculate_sma(prices, min(50, len(prices)))
        rsi = self.technical_analyzer.calculate_rsi(prices)
        macd, signal, histogram = self.technical_analyzer.calculate_macd(prices)
        upper, middle, lower = self.technical_analyzer.calculate_bollinger_bands(prices)
        trend = self.technical_analyzer.analyze_trend(prices)
        
        # 计算波动率
        volatility = self._calculate_volatility(prices)
        
        return {
            "symbol": symbol,
            "current_price": current_price,
            "sma_20": sma_20,
            "sma_50": sma_50,
            "rsi": rsi,
            "macd": macd,
            "signal": signal,
            "histogram": histogram,
            "bollinger_upper": upper,
            "bollinger_middle": middle,
            "bollinger_lower": lower,
            "trend": trend,
            "volatility": volatility
        }
    
    def _calculate_volatility(self, prices: List[float]) -> float:
        """计算波动率"""
        if len(prices) < 2:
            return 0
        
        returns = []
        for i in range(1, len(prices)):
            daily_return = (prices[i] - prices[i-1]) / prices[i-1]
            returns.append(daily_return)
        
        if not returns:
            return 0
        
        mean_return = sum(returns) / len(returns)
        variance = sum((r - mean_return) ** 2 for r in returns) / len(returns)
        
        return variance ** 0.5
    
    def generate_signal(self, symbol: str, current_price: float, 
                      portfolio_value: float = 100000) -> TradeRecommendation:
        """生成交易信号"""
        analysis = self.analyze_market(symbol, current_price)
        
        if "error" in analysis:
            return TradeRecommendation(
                symbol=symbol,
                signal=TradeSignal.HOLD,
                confidence=0,
                entry_price=current_price,
                stop_loss=current_price * 0.95,
                take_profit=current_price * 1.05,
                risk_level=RiskLevel.HIGH,
                reasoning="Insufficient data for analysis",
                timestamp=datetime.now()
            )
        
        # 基于技术指标生成信号
        signal = self._determine_signal(analysis)
        confidence = self._calculate_confidence(analysis)
        
        # 计算止损止盈
        stop_loss = self.risk_manager.calculate_stop_loss(current_price)
        take_profit = self.risk_manager.calculate_take_profit(
            current_price, stop_loss, self.config.get("risk_reward_ratio", 2.0)
        )
        
        # 评估风险等级
        risk_level = self.risk_manager.assess_risk_level(
            analysis["volatility"], 
            portfolio_value * 0.1,  # 假设10%仓位
            portfolio_value
        )
        
        # 生成理由
        reasoning = self._generate_reasoning(analysis, signal)
        
        recommendation = TradeRecommendation(
            symbol=symbol,
            signal=signal,
            confidence=confidence,
            entry_price=current_price,
            stop_loss=stop_loss,
            take_profit=take_profit,
            risk_level=risk_level,
            reasoning=reasoning,
            timestamp=datetime.now()
        )
        
        self.recommendations.append(recommendation)
        
        return recommendation
    
    def _determine_signal(self, analysis: Dict) -> TradeSignal:
        """确定交易信号"""
        rsi = analysis.get("rsi", 50)
        macd = analysis.get("macd", 0)
        histogram = analysis.get("histogram", 0)
        trend = analysis.get("trend", {}).get("trend", "neutral")
        
        # 综合多个指标
        buy_signals = 0
        sell_signals = 0
        
        # RSI信号
        if rsi < 30:
            buy_signals += 2
        elif rsi > 70:
            sell_signals += 2
        elif rsi < 50:
            buy_signals += 1
        else:
            sell_signals += 1
        
        # MACD信号
        if macd > 0 and histogram > 0:
            buy_signals += 2
        elif macd < 0 and histogram < 0:
            sell_signals += 2
        
        # 趋势信号
        if trend == "bullish":
            buy_signals += 1
        elif trend == "bearish":
            sell_signals += 1
        
        # 综合判断
        if buy_signals >= 4:
            return TradeSignal.STRONG_BUY
        elif buy_signals >= 2:
            return TradeSignal.BUY
        elif sell_signals >= 4:
            return TradeSignal.STRONG_SELL
        elif sell_signals >= 2:
            return TradeSignal.SELL
        else:
            return TradeSignal.HOLD
    
    def _calculate_confidence(self, analysis: Dict) -> float:
        """计算置信度"""
        confidence = 0.5  # 基础置信度
        
        # 基于RSI的置信度
        rsi = analysis.get("rsi", 50)
        if rsi < 20 or rsi > 80:
            confidence += 0.2
        
        # 基于MACD的置信度
        histogram = analysis.get("histogram", 0)
        if abs(histogram) > 0.5:
            confidence += 0.15
        
        # 基于趋势的置信度
        trend_strength = analysis.get("trend", {}).get("strength", 0)
        confidence += min(trend_strength / 100, 0.15)
        
        return min(confidence, 1.0)
    
    def _generate_reasoning(self, analysis: Dict, signal: TradeSignal) -> str:
        """生成交易理由"""
        reasons = []
        
        rsi = analysis.get("rsi", 50)
        if rsi < 30:
            reasons.append(f"RSI超卖({rsi:.1f})")
        elif rsi > 70:
            reasons.append(f"RSI超买({rsi:.1f})")
        
        macd = analysis.get("macd", 0)
        if macd > 0:
            reasons.append("MACD bullish")
        elif macd < 0:
            reasons.append("MACD bearish")
        
        trend = analysis.get("trend", {}).get("trend", "neutral")
        if trend != "neutral":
            reasons.append(f"Trend: {trend}")
        
        if not reasons:
            reasons.append("No clear signals")
        
        return f"Signal: {signal.value.upper()}, Reasons: {', '.join(reasons)}"
    
    def get_portfolio_summary(self) -> Dict:
        """获取组合摘要"""
        return self.risk_manager.check_portfolio_risk()
    
    def get_recommendation_history(self, limit: int = 10) -> List[Dict]:
        """获取历史建议"""
        recent = self.recommendations[-limit:]
        return [rec.to_dict() for rec in recent]
    
    def export_data(self, filepath: str):
        """导出数据"""
        data = {
            "recommendations": [rec.to_dict() for rec in self.recommendations],
            "portfolio": self.get_portfolio_summary(),
            "config": self.config,
            "export_time": datetime.now().isoformat()
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Data exported to {filepath}")


# 使用示例
if __name__ == "__main__":
    # 初始化TradeAI
    trade_ai = TradeAI()
    
    # 模拟价格数据
    symbols = ["BTC", "ETH", "AAPL"]
    
    print("=" * 60)
    print("TradeAI - 智能交易助手")
    print("=" * 60)
    
    for symbol in symbols:
        print(f"\n📊 分析 {symbol}...")
        
        # 模拟历史价格数据
        import random
        base_price = {"BTC": 45000, "ETH": 3000, "AAPL": 180}[symbol]
        prices = [base_price + random.uniform(-1000, 1000) for _ in range(100)]
        
        for price in prices:
            trade_ai.update_price_data(symbol, price)
        
        current_price = prices[-1]
        
        # 生成交易建议
        recommendation = trade_ai.generate_signal(symbol, current_price)
        
        print(f"\n💡 交易建议:")
        print(f"   标的: {recommendation.symbol}")
        print(f"   信号: {recommendation.signal.value.upper()}")
        print(f"   置信度: {recommendation.confidence:.1%}")
        print(f"   入场价: ${recommendation.entry_price:.2f}")
        print(f"   止损: ${recommendation.stop_loss:.2f}")
        print(f"   止盈: ${recommendation.take_profit:.2f}")
        print(f"   风险等级: {recommendation.risk_level.value}")
        print(f"   理由: {recommendation.reasoning}")
    
    print("\n" + "=" * 60)
    print("✅ 分析完成!")
    print("=" * 60)
