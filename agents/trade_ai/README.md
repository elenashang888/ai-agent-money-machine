# TradeAI - 智能交易助手

## 📋 概述

TradeAI是AgentVerse项目中的智能交易助手（Agent #4），专注于量化交易策略、自动盯盘和风险控制。本工具**仅供学习研究使用，不构成投资建议**。

⚠️ **重要警告**：
- 金融交易风险极高，可能导致全部本金损失
- 默认使用模拟交易模式（paper_trading: true）
- 请在充分了解风险后再考虑真实交易
- 过往表现不代表未来收益

## 🚀 功能特性

### 1. 量化策略系统
- **动量策略**：追踪趋势动量，顺势交易
- **均值回归**：价格偏离均值时反向交易
- **突破策略**：突破关键价位时入场
- **套利策略**：跨市场/跨品种价差套利

### 2. 技术指标计算
- RSI（相对强弱指标）
- MACD（指数平滑异同平均线）
- 布林带（Bollinger Bands）
- 简单/指数移动平均线（SMA/EMA）
- 成交量分析

### 3. 风险管理
- 每笔交易风险限额（默认2%）
- 自动止损/止盈设置
- 最大持仓数量限制
- 风险等级评估
- 投资组合监控

### 4. 自动盯盘
- 实时信号生成
- 模拟交易执行
- 持仓管理
- 盈亏跟踪

### 5. 策略回测
- 历史数据模拟
- 策略性能评估
- 胜率/盈亏比计算
- 最大回撤分析

## 📁 文件结构

```
agents/trade_ai/
├── trade_ai.py      # 主程序
├── config.json      # 配置文件
└── README.md        # 说明文档
```

## ⚙️ 配置说明

### config.json 参数

```json
{
  "risk_per_trade": 0.02,        // 每笔交易风险比例
  "max_positions": 5,            // 最大持仓数量
  "stop_loss_pct": 0.05,         // 止损百分比
  "take_profit_pct": 0.15,       // 止盈百分比
  "trading_pairs": [...],        // 交易标的列表
  "timeframes": [...],           // 时间周期
  "paper_trading": true,         // 模拟交易模式
  "strategies": {...},           // 策略配置
  "risk_management": {...},      // 风险管理参数
  "notifications": {...},        // 通知设置
  "backtest": {...}              // 回测参数
}
```

### 策略权重配置

- `momentum`: 动量策略（权重40%）
- `mean_reversion`: 均值回归（权重30%）
- `breakout`: 突破策略（权重20%）
- `arbitrage`: 套利策略（权重10%，默认禁用）

## 🎯 使用方法

### 基本使用

```python
from trade_ai import TradeAI

# 初始化
agent = TradeAI('config.json')

# 生成交易信号
signal = agent.generate_signal('BTC/USDT', 'momentum')
print(signal)

# 执行交易
trade = agent.execute_trade('BTC/USDT', signal, account_balance=10000)
print(trade)

# 查看投资组合
portfolio = agent.get_portfolio_summary()
print(portfolio)

# 风险评估
risk = agent.risk_assessment()
print(risk)
```

### 策略回测

```python
# 回测策略
backtest = agent.backtest_strategy('BTC/USDT', 'momentum', days=90)
print(f"胜率: {backtest['win_rate']}%")
print(f"总盈亏: ${backtest['total_pnl']}")
print(f"盈亏比: {backtest['profit_factor']}")
```

### 运行演示

```bash
python trade_ai.py
```

## 📊 技术指标说明

### RSI（相对强弱指标）
- 范围：0-100
- 超买区：>70
- 超卖区：<30
- 中性区：30-70

### MACD
- MACD线：12日EMA - 26日EMA
- 信号线：MACD的9日EMA
- 柱状图：MACD - 信号线

### 布林带
- 中轨：20日SMA
- 上轨：中轨 + 2倍标准差
- 下轨：中轨 - 2倍标准差

## ⚠️ 风险提示

1. **市场风险**：金融市场波动剧烈，任何策略都可能失效
2. **技术风险**：系统故障、网络延迟可能导致交易失败
3. **流动性风险**：部分品种可能出现流动性不足
4. **模型风险**：历史数据不代表未来表现

## 🔒 安全建议

1. **始终使用模拟交易模式**进行测试
2. **小额资金**开始实盘交易
3. **严格止损**，控制单笔亏损
4. **分散投资**，避免集中风险
5. **定期评估**策略表现

## 📈 性能指标

TradeAI提供以下性能指标：

- **信号生成数**：系统生成的交易信号总数
- **交易执行数**：实际执行的交易数量
- **胜率**：盈利交易占比
- **总盈亏**：累计盈亏金额
- **平均收益**：每笔交易平均收益
- **风险等级**：当前风险水平评估

## 🛠️ 扩展开发

### 添加新策略

```python
def _init_strategies(self) -> Dict:
    strategies = {
        # ... 现有策略 ...
        'my_strategy': {
            'name': '我的策略',
            'description': '策略描述',
            'timeframe': '1h',
            'indicators': ['RSI', 'MACD'],
            'win_rate': 0.60,
            'avg_return': 0.03
        }
    }
    return strategies
```

### 自定义指标

```python
def _calculate_custom_indicator(self, data: List[float]) -> float:
    # 实现自定义指标逻辑
    return result
```

## 📚 依赖项

- Python 3.7+
- 标准库：json, random, datetime, collections, math, typing

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进TradeAI。

## 📄 许可证

本项目仅供学习研究使用。

## 📞 联系方式

如有问题或建议，请通过GitHub Issue联系。

---

**免责声明**：TradeAI是一个教育性质的量化交易工具，作者不对任何使用本工具进行的交易结果负责。投资有风险，入市需谨慎。
