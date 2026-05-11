# TradeAI - 智能交易助手

基于AI的智能交易分析和决策系统，提供技术分析、风险管理和交易建议。

## 🎯 功能特性

- **技术分析**: SMA、EMA、RSI、MACD、布林带等经典指标
- **智能信号**: 基于多指标综合判断生成交易信号
- **风险管理**: 自动计算仓位、止损、止盈
- **组合监控**: 实时跟踪持仓和风险暴露
- **历史记录**: 保存所有交易建议和分析结果

## 🚀 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行示例

```bash
python trade_ai.py
```

### 基础使用

```python
from trade_ai import TradeAI

# 初始化
trade_ai = TradeAI()

# 更新价格数据
trade_ai.update_price_data("BTC", 45000)

# 生成交易建议
recommendation = trade_ai.generate_signal("BTC", 45000)

print(f"信号: {recommendation.signal}")
print(f"置信度: {recommendation.confidence}")
print(f"止损: {recommendation.stop_loss}")
print(f"止盈: {recommendation.take_profit}")
```

## 📊 支持的指标

| 指标 | 描述 | 用途 |
|------|------|------|
| SMA | 简单移动平均线 | 趋势判断 |
| EMA | 指数移动平均线 | 趋势跟踪 |
| RSI | 相对强弱指标 | 超买超卖 |
| MACD | 异同移动平均线 | 动量判断 |
| Bollinger Bands | 布林带 | 波动率分析 |

## 🛡️ 风险管理

- **仓位控制**: 最大单仓位不超过组合10%
- **止损设置**: 默认2%止损
- **风险收益比**: 默认1:2
- **风险等级**: Low/Medium/High/Extreme

## 📈 交易信号

- **STRONG_BUY**: 强烈买入
- **BUY**: 买入
- **HOLD**: 持有
- **SELL**: 卖出
- **STRONG_SELL**: 强烈卖出

## ⚙️ 配置说明

编辑 `config.json`:

```json
{
  "max_position_size": 0.1,      // 最大仓位比例
  "max_portfolio_risk": 0.02,    // 最大组合风险
  "min_confidence": 0.6,          // 最小置信度
  "risk_reward_ratio": 2.0,       // 风险收益比
  "symbols": ["BTC", "ETH"]       // 监控标的
}
```

## 📝 输出示例

```
============================================================
TradeAI - 智能交易助手
============================================================

📊 分析 BTC...

💡 交易建议:
   标的: BTC
   信号: BUY
   置信度: 75.0%
   入场价: $45234.56
   止损: $44329.87
   止盈: $47044.25
   风险等级: medium
   理由: Signal: BUY, Reasons: RSI超卖(28.5), MACD bullish

✅ 分析完成!
```

## ⚠️ 免责声明

本系统仅供学习和研究使用，不构成投资建议。投资有风险，入市需谨慎。

## 📄 许可证

MIT License
