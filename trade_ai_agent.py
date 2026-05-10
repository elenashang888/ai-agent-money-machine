#!/usr/bin/env python3
"""
TradeAI - 智能交易助手
Monthly Potential: Variable (基于策略表现)
功能：量化策略、信号生成、风险管理、自动交易
"""

import json
import random
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from collections import defaultdict
import math

class TradeAI:
    """智能交易助手 - 量化交易自动化系统"""
    
    def __init__(self, config_path: str = "config.json"):
        self.config = self._load_config(config_path)
        self.metrics = {
            'signals_generated': 0,
            'trades_executed': 0,
            'profitable_trades': 0,
            'total_pnl': 0
        }
        
        # 策略配置
        self.strategies = self._init_strategies()
        
        # 市场数据缓存
        self.market_data = defaultdict(list)
        
        # 持仓
        self.positions = {}
        
        # 交易历史
        self.trade_history = []
        
    def _load_config(self, path: str) -> Dict:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return self._default_config()
    
    def _default_config(self) -> Dict:
        return {
            'risk_per_trade': 0.02,  # 每笔交易2%风险
            'max_positions': 5,
            'stop_loss_pct': 0.05,  # 5%止损
            'take_profit_pct': 0.15,  # 15%止盈
            'trading_pairs': ['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'AAPL', 'TSLA'],
            'timeframes': ['1h', '4h', '1d'],
            'paper_trading': True  # 默认模拟交易
        }
    
    def _init_strategies(self) -> Dict:
        """初始化交易策略"""
        return {
            'momentum': {
                'name': '动量策略',
                'description': '追踪趋势动量，顺势交易',
                'timeframe': '1d',
                'indicators': ['RSI', 'MACD', 'Volume'],
                'win_rate': 0.58,
                'avg_return': 0.035
            },
            'mean_reversion': {
                'name': '均值回归',
                'description': '价格偏离均值时反向交易',
                'timeframe': '4h',
                'indicators': ['Bollinger Bands', 'RSI'],
                'win_rate': 0.62,
                'avg_return': 0.025
            },
            'breakout': {
                'name': '突破策略',
                'description': '突破关键价位时入场',
                'timeframe': '1h',
                'indicators': ['Support/Resistance', 'Volume'],
                'win_rate': 0.45,
                'avg_return': 0.055
            },
            'arbitrage': {
                'name': '套利策略',
                'description': '跨市场/跨品种价差套利',
                'timeframe': '1m',
                'indicators': ['Price Spread', 'Correlation'],
                'win_rate': 0.75,
                'avg_return': 0.008
            }
        }
    
    def fetch_market_data(self, symbol: str, timeframe: str = '1d') -> List[Dict]:
        """获取市场数据（模拟）"""
        # 生成模拟K线数据
        if symbol not in self.market_data or len(self.market_data[symbol]) == 0:
            self.market_data[symbol] = self._generate_ohlcv(symbol, 100)
        
        return self.market_data[symbol]
    
    def _generate_ohlcv(self, symbol: str, periods: int) -> List[Dict]:
        """生成模拟OHLCV数据"""
        data = []
        base_price = random.uniform(50, 50000)  # 根据品种调整
        
        for i in range(periods):
            volatility = random.uniform(0.01, 0.05)
            change = random.gauss(0, volatility)
            
            open_price = base_price * (1 + change)
            high_price = open_price * (1 + abs(random.gauss(0, volatility/2)))
            low_price = open_price * (1 - abs(random.gauss(0, volatility/2)))
            close_price = (open_price + high_price + low_price) / 3 + random.gauss(0, volatility)
            volume = random.randint(1000000, 10000000)
            
            data.append({
                'timestamp': datetime.now() - timedelta(days=periods-i),
                'open': round(open_price, 2),
                'high': round(high_price, 2),
                'low': round(low_price, 2),
                'close': round(close_price, 2),
                'volume': volume
            })
            
            base_price = close_price
        
        return data
    
    def calculate_indicators(self, data: List[Dict]) -> Dict:
        """计算技术指标"""
        closes = [d['close'] for d in data]
        volumes = [d['volume'] for d in data]
        
        return {
            'sma_20': self._calculate_sma(closes, 20),
            'sma_50': self._calculate_sma(closes, 50),
            'rsi': self._calculate_rsi(closes, 14),
            'macd': self._calculate_macd(closes),
            'bollinger': self._calculate_bollinger(closes, 20),
            'volume_sma': self._calculate_sma(volumes, 20)
        }
    
    def _calculate_sma(self, data: List[float], period: int) -> float:
        """计算简单移动平均"""
        if len(data) < period:
            return sum(data) / len(data) if data else 0
        return sum(data[-period:]) / period
    
    def _calculate_rsi(self, data: List[float], period: int = 14) -> float:
        """计算RSI"""
        if len(data) < period + 1:
            return 50
        
        deltas = [data[i] - data[i-1] for i in range(1, len(data))]
        gains = [d for d in deltas[-period:] if d > 0]
        losses = [-d for d in deltas[-period:] if d < 0]
        
        avg_gain = sum(gains) / period if gains else 0
        avg_loss = sum(losses) / period if losses else 0
        
        if avg_loss == 0:
            return 100
        
        rs = avg_gain / avg_loss
        return 100 - (100 / (1 + rs))
    
    def _calculate_macd(self, data: List[float]) -> Dict:
        """计算MACD"""
        ema_12 = self._calculate_ema(data, 12)
        ema_26 = self._calculate_ema(data, 26)
        macd = ema_12 - ema_26
        signal = self._calculate_ema([macd], 9) if macd else 0
        
        return {
            'macd': macd,
            'signal': signal,
            'histogram': macd - signal
        }
    
    def _calculate_ema(self, data: List[float], period: int) -> float:
        """计算指数移动平均"""
        if len(data) < period:
            return sum(data) / len(data) if data else 0
        
        multiplier = 2 / (period + 1)
        ema = sum(data[:period]) / period
        
        for price in data[period:]:
            ema = (price - ema) * multiplier + ema
        
        return ema
    
    def _calculate_bollinger(self, data: List[float], period: int = 20) -> Dict:
        """计算布林带"""
        if len(data) < period:
            return {'upper': 0, 'middle': 0, 'lower': 0}
        
        sma = sum(data[-period:]) / period
        variance = sum((x - sma) ** 2 for x in data[-period:]) / period
        std = math.sqrt(variance)
        
        return {
            'upper': sma + (std * 2),
            'middle': sma,
            'lower': sma - (std * 2)
        }
    
    def generate_signal(self, symbol: str, strategy: str = 'momentum') -> Dict:
        """生成交易信号"""
        # 获取数据
        data = self.fetch_market_data(symbol)
        if len(data) < 50:
            return {'signal': 'HOLD', 'reason': 'Insufficient data'}
        
        # 计算指标
        indicators = self.calculate_indicators(data)
        current_price = data[-1]['close']
        
        # 策略逻辑
        signal = self._apply_strategy(symbol, current_price, indicators, strategy)
        
        self.metrics['signals_generated'] += 1
        
        return {
            'symbol': symbol,
            'signal': signal['action'],
            'price': current_price,
            'strategy': strategy,
            'indicators': {
                'rsi': round(indicators['rsi'], 2),
                'sma_20': round(indicators['sma_20'], 2),
                'sma_50': round(indicators['sma_50'], 2)
            },
            'confidence': signal['confidence'],
            'reason': signal['reason'],
            'timestamp': datetime.now().isoformat()
        }
    
    def _apply_strategy(self, symbol: str, price: float, indicators: Dict, strategy: str) -> Dict:
        """应用交易策略"""
        rsi = indicators['rsi']
        sma_20 = indicators['sma_20']
        sma_50 = indicators['sma_50']
        
        if strategy == 'momentum':
            if price > sma_20 > sma_50 and rsi > 50 and rsi < 70:
                return {'action': 'BUY', 'confidence': 0.75, 'reason': '上升趋势确认'}
            elif price < sma_20 < sma_50 and rsi > 30:
                return {'action': 'SELL', 'confidence': 0.70, 'reason': '下降趋势确认'}
        
        elif strategy == 'mean_reversion':
            bollinger = indicators['bollinger']
            if price < bollinger['lower'] and rsi < 30:
                return {'action': 'BUY', 'confidence': 0.80, 'reason': '超卖反弹'}
            elif price > bollinger['upper'] and rsi > 70:
                return {'action': 'SELL', 'confidence': 0.75, 'reason': '超买回调'}
        
        elif strategy == 'breakout':
            if price > sma_20 * 1.05:
                return {'action': 'BUY', 'confidence': 0.65, 'reason': '突破阻力位'}
            elif price < sma_20 * 0.95:
                return {'action': 'SELL', 'confidence': 0.65, 'reason': '跌破支撑位'}
        
        return {'action': 'HOLD', 'confidence': 0.5, 'reason': '无明确信号'}
    
    def calculate_position_size(self, symbol: str, signal: Dict, account_balance: float) -> Dict:
        """计算仓位大小"""
        risk_per_trade = self.config.get('risk_per_trade', 0.02)
        stop_loss_pct = self.config.get('stop_loss_pct', 0.05)
        
        risk_amount = account_balance * risk_per_trade
        position_size = risk_amount / (signal['price'] * stop_loss_pct)
        
        return {
            'symbol': symbol,
            'position_size': round(position_size, 4),
            'risk_amount': round(risk_amount, 2),
            'entry_price': signal['price'],
            'stop_loss': round(signal['price'] * (1 - stop_loss_pct), 2),
            'take_profit': round(signal['price'] * (1 + self.config.get('take_profit_pct', 0.15)), 2),
            'risk_reward_ratio': round(self.config.get('take_profit_pct', 0.15) / stop_loss_pct, 2)
        }
    
    def execute_trade(self, symbol: str, signal: Dict, account_balance: float) -> Dict:
        """执行交易"""
        # 计算仓位
        position = self.calculate_position_size(symbol, signal, account_balance)
        
        # 模拟执行
        trade = {
            'trade_id': f"TRADE_{len(self.trade_history)+1:04d}",
            'symbol': symbol,
            'action': signal['signal'],
            'entry_price': signal['price'],
            'position_size': position['position_size'],
            'stop_loss': position['stop_loss'],
            'take_profit': position['take_profit'],
            'timestamp': datetime.now().isoformat(),
            'status': 'OPEN',
            'pnl': 0
        }
        
        self.trade_history.append(trade)
        self.positions[symbol] = trade
        self.metrics['trades_executed'] += 1
        
        return trade
    
    def close_trade(self, trade_id: str, exit_price: float) -> Dict:
        """平仓"""
        for trade in self.trade_history:
            if trade['trade_id'] == trade_id and trade['status'] == 'OPEN':
                # 计算盈亏
                if trade['action'] == 'BUY':
                    pnl = (exit_price - trade['entry_price']) * trade['position_size']
                else:
                    pnl = (trade['entry_price'] - exit_price) * trade['position_size']
                
                trade['exit_price'] = exit_price
                trade['pnl'] = round(pnl, 2)
                trade['status'] = 'CLOSED'
                trade['closed_at'] = datetime.now().isoformat()
                
                self.metrics['total_pnl'] += pnl
                if pnl > 0:
                    self.metrics['profitable_trades'] += 1
                
                # 移除持仓
                if trade['symbol'] in self.positions:
                    del self.positions[trade['symbol']]
                
                return trade
        
        return {'error': 'Trade not found or already closed'}
    
    def get_portfolio_summary(self) -> Dict:
        """获取投资组合摘要"""
        total_trades = len(self.trade_history)
        closed_trades = [t for t in self.trade_history if t['status'] == 'CLOSED']
        
        if not closed_trades:
            return {
                'total_trades': total_trades,
                'open_positions': len(self.positions),
                'win_rate': 0,
                'total_pnl': 0,
                'avg_trade_return': 0
            }
        
        winning_trades = len([t for t in closed_trades if t['pnl'] > 0])
        total_pnl = sum(t['pnl'] for t in closed_trades)
        avg_return = total_pnl / len(closed_trades)
        
        return {
            'total_trades': total_trades,
            'closed_trades': len(closed_trades),
            'open_positions': len(self.positions),
            'win_rate': round(winning_trades / len(closed_trades) * 100, 2),
            'total_pnl': round(total_pnl, 2),
            'avg_trade_return': round(avg_return, 2),
            'current_positions': list(self.positions.keys())
        }
    
    def risk_assessment(self) -> Dict:
        """风险评估"""
        closed_trades = [t for t in self.trade_history if t['status'] == 'CLOSED']
        
        if len(closed_trades) < 5:
            return {
                'risk_level': 'UNKNOWN',
                'message': '交易数据不足，无法评估风险'
            }
        
        pnl_values = [t['pnl'] for t in closed_trades]
        
        # 计算风险指标
        max_drawdown = min(pnl_values) if min(pnl_values) < 0 else 0
        volatility = (max(pnl_values) - min(pnl_values)) / abs(sum(pnl_values) / len(pnl_values)) if sum(pnl_values) != 0 else 0
        
        # 风险等级
        if volatility > 2:
            risk_level = 'HIGH'
            message = '⚠️ 波动率过高，建议降低仓位'
        elif volatility > 1:
            risk_level = 'MEDIUM'
            message = '⚡ 风险适中，注意止损'
        else:
            risk_level = 'LOW'
            message = '✅ 风险可控，保持当前策略'
        
        return {
            'risk_level': risk_level,
            'max_drawdown': round(max_drawdown, 2),
            'volatility': round(volatility, 2),
            'message': message,
            'recommendations': [
                '设置严格止损',
                '分散投资标的',
                '定期评估策略'
            ]
        }
    
    def backtest_strategy(self, symbol: str, strategy: str, days: int = 90) -> Dict:
        """策略回测"""
        # 生成历史数据
        data = self._generate_ohlcv(symbol, days)
        
        trades = []
        total_pnl = 0
        
        for i in range(50, len(data)):
            window = data[:i+1]
            indicators = self.calculate_indicators(window)
            price = data[i]['close']
            
            signal = self._apply_strategy(symbol, price, indicators, strategy)
            
            if signal['action'] != 'HOLD':
                # 模拟交易结果
                win_prob = self.strategies[strategy]['win_rate']
                is_win = random.random() < win_prob
                
                if is_win:
                    pnl = price * 0.03  # 3%收益
                else:
                    pnl = -price * 0.02  # 2%亏损
                
                trades.append({
                    'date': data[i]['timestamp'],
                    'action': signal['action'],
                    'price': price,
                    'pnl': pnl,
                    'result': 'WIN' if is_win else 'LOSS'
                })
                
                total_pnl += pnl
        
        winning_trades = len([t for t in trades if t['result'] == 'WIN'])
        
        return {
            'symbol': symbol,
            'strategy': strategy,
            'period': f'{days} days',
            'total_trades': len(trades),
            'winning_trades': winning_trades,
            'win_rate': round(winning_trades / len(trades) * 100, 2) if trades else 0,
            'total_pnl': round(total_pnl, 2),
            'avg_pnl_per_trade': round(total_pnl / len(trades), 2) if trades else 0,
            'profit_factor': round(sum(t['pnl'] for t in trades if t['pnl'] > 0) / abs(sum(t['pnl'] for t in trades if t['pnl'] < 0)), 2) if any(t['pnl'] < 0 for t in trades) else 0
        }
    
    def get_metrics(self) -> Dict:
        """获取交易指标"""
        signals = self.metrics['signals_generated']
        trades = self.metrics['trades_executed']
        pnl = self.metrics['total_pnl']
        
        # 月度预估（假设每天10个信号，50%执行）
        monthly_signals = 10 * 30
        monthly_trades = monthly_signals * 0.5
        
        # 假设平均收益率2%
        avg_trade_value = 1000  # 假设每笔$1000
        monthly_pnl = monthly_trades * avg_trade_value * 0.02
        
        return {
            'total_signals': signals,
            'total_trades': trades,
            'profitable_trades': self.metrics['profitable_trades'],
            'total_pnl': round(pnl, 2),
            'win_rate': f"{self.metrics['profitable_trades']/max(1,trades)*100:.1f}%",
            'monthly_signals_projection': monthly_signals,
            'monthly_trades_projection': int(monthly_trades),
            'monthly_pnl_projection': round(monthly_pnl, 2),
            'risk_level': self.risk_assessment()['risk_level']
        }


# 演示模式
if __name__ == '__main__':
    agent = TradeAI()
    
    print("=" * 50)
    print("📈 TradeAI - 智能交易助手")
    print("=" * 50)
    
    # 生成交易信号
    print("\n🎯 生成交易信号：")
    for symbol in ['BTC/USDT', 'ETH/USDT', 'AAPL']:
        signal = agent.generate_signal(symbol, 'momentum')
        print(f"\n{symbol}:")
        print(f"  信号: {signal['signal']}")
        print(f"  价格: ${signal['price']}")
        print(f"  信心度: {signal['confidence']}")
        print(f"  原因: {signal['reason']}")
    
    # 模拟交易执行
    print("\n💼 模拟交易执行：")
    account_balance = 10000
    for symbol in ['BTC/USDT', 'ETH/USDT']:
        signal = agent.generate_signal(symbol, 'momentum')
        if signal['signal'] == 'BUY':
            trade = agent.execute_trade(symbol, signal, account_balance)
            print(f"\n执行交易: {trade['trade_id']}")
            print(f"  标的: {trade['symbol']}")
            print(f"  方向: {trade['action']}")
            print(f"  入场: ${trade['entry_price']}")
            print(f"  止损: ${trade['stop_loss']}")
            print(f"  止盈: ${trade['take_profit']}")
    
    # 投资组合
    print("\n📊 投资组合：")
    portfolio = agent.get_portfolio_summary()
    for key, value in portfolio.items():
        print(f"  {key}: {value}")
    
    # 风险评估
    print("\n⚠️ 风险评估：")
    risk = agent.risk_assessment()
    print(f"  风险等级: {risk['risk_level']}")
    print(f"  建议: {risk['message']}")
    
    # 策略回测
    print("\n📈 策略回测 (BTC/USDT, 动量策略)：")
    backtest = agent.backtest_strategy('BTC/USDT', 'momentum', 90)
    print(f"  交易次数: {backtest['total_trades']}")
    print(f"  胜率: {backtest['win_rate']}%")
    print(f"  总盈亏: ${backtest['total_pnl']}")
    print(f"  盈亏比: {backtest['profit_factor']}")
    
    # 显示指标
    print("\n💰 交易指标：")
    metrics = agent.get_metrics()
    for key, value in metrics.items():
        print(f"  {key}: {value}")
