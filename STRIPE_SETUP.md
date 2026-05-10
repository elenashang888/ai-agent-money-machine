# Stripe 支付配置

## 🏦 Stripe 账户设置

### 1. 注册Stripe账户

访问: https://stripe.com
- 点击 "Start now"
- 使用邮箱注册
- 完成身份验证

### 2. 创建产品

**产品名称**: AI Agent Money Machine - Professional
**产品描述**: 6个AI Agent组成的自动化系统，帮你月入$5500-25000

### 3. 定价方案

#### 方案1: 一次性付款
```json
{
  "name": "专业版",
  "description": "6个AI Agent完整系统",
  "price": 29900,  // $299.00
  "currency": "usd",
  "type": "one_time"
}
```

#### 方案2: 分期付款 (可选)
```json
{
  "name": "专业版 - 3期",
  "description": "6个AI Agent完整系统",
  "price": 29900,
  "currency": "usd",
  "type": "one_time",
  "payment_method_options": {
    "installments": {
      "enabled": true,
      "plans": [
        {"count": 3, "interval": "month"}
      ]
    }
  }
}
```

---

## 💳 支付页面代码

### HTML + Stripe.js

```html
<!DOCTYPE html>
<html>
<head>
    <title>购买 AI Agent Money Machine</title>
    <script src="https://js.stripe.com/v3/"></script>
    <style>
        body {
            font-family: -apple-system, sans-serif;
            max-width: 600px;
            margin: 50px auto;
            padding: 20px;
        }
        .product {
            background: #f8f9fa;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
        }
        .price {
            font-size: 2.5rem;
            color: #667eea;
            font-weight: bold;
        }
        .features {
            list-style: none;
            padding: 0;
        }
        .features li {
            padding: 10px 0;
            border-bottom: 1px solid #ddd;
        }
        .features li:before {
            content: "✓ ";
            color: #28a745;
            font-weight: bold;
        }
        #payment-form {
            margin-top: 30px;
        }
        #card-element {
            border: 1px solid #ddd;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        button {
            background: #667eea;
            color: white;
            border: none;
            padding: 15px 40px;
            font-size: 1.1rem;
            border-radius: 5px;
            cursor: pointer;
            width: 100%;
        }
        button:hover {
            background: #5a6fd6;
        }
        #error-message {
            color: #dc3545;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <div class="product">
        <h1>🚀 AI Agent Money Machine</h1>
        <p class="price">$299 <span style="font-size: 1rem; color: #666;">一次性付款</span></p>
        <ul class="features">
            <li>6个完整AI Agent源代码</li>
            <li>Flask API服务器</li>
            <li>一键启动脚本</li>
            <li>详细部署文档</li>
            <li>营销落地页模板</li>
            <li>GitHub Actions配置</li>
            <li>终身免费更新</li>
        </ul>
    </div>

    <form id="payment-form">
        <div id="card-element"></div>
        <div id="error-message"></div>
        <button type="submit">立即购买 - $299</button>
    </form>

    <script>
        const stripe = Stripe('pk_test_YOUR_PUBLISHABLE_KEY');
        const elements = stripe.elements();
        const card = elements.create('card');
        card.mount('#card-element');

        const form = document.getElementById('payment-form');
        const errorMessage = document.getElementById('error-message');

        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const {token, error} = await stripe.createToken(card);
            
            if (error) {
                errorMessage.textContent = error.message;
            } else {
                // 发送token到服务器
                const response = await fetch('/create-charge', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        token: token.id,
                        amount: 29900,
                        description: 'AI Agent Money Machine - Professional'
                    })
                });
                
                const result = await response.json();
                if (result.success) {
                    alert('支付成功！下载链接已发送到您的邮箱。');
                    window.location.href = '/success';
                } else {
                    errorMessage.textContent = '支付失败，请重试。';
                }
            }
        });
    </script>
</body>
</html>
```

---

## 🔧 Python后端 (Flask)

```python
from flask import Flask, request, jsonify
import stripe
import os

app = Flask(__name__)

# Stripe配置
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')

@app.route('/create-payment-intent', methods=['POST'])
def create_payment_intent():
    try:
        intent = stripe.PaymentIntent.create(
            amount=29900,  # $299.00
            currency='usd',
            automatic_payment_methods={'enabled': True},
            metadata={
                'product': 'AI Agent Money Machine',
                'version': 'Professional'
            }
        )
        return jsonify({'clientSecret': intent.client_secret})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/webhook', methods=['POST'])
def webhook():
    payload = request.get_data()
    sig_header = request.headers.get('Stripe-Signature')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, os.environ.get('STRIPE_WEBHOOK_SECRET')
        )
        
        if event['type'] == 'payment_intent.succeeded':
            payment_intent = event['data']['object']
            # 发送下载链接邮件
            send_download_email(payment_intent['receipt_email'])
            
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 400

def send_download_email(email):
    # 实现邮件发送逻辑
    pass

if __name__ == '__main__':
    app.run(port=5001)
```

---

## 🔐 环境变量

```bash
# .env 文件
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

---

## 🧪 测试支付

### 测试卡号
- **成功**: 4242 4242 4242 4242
- **失败**: 4000 0000 0000 0002
- **3D Secure**: 4000 0025 0000 3155

### 测试信息
- 过期日期: 12/25
- CVC: 123
- 邮编: 12345

---

## 📊 Stripe Dashboard

访问: https://dashboard.stripe.com

### 查看指标
- 收入
- 转化率
- 退款率
- 客户分布

### 导出数据
- 交易记录
- 客户列表
- 财务报表

---

## 🚀 上线检查清单

- [ ] Stripe账户验证完成
- [ ] 产品创建完成
- [ ] 价格设置正确
- [ ] 测试支付通过
- [ ] Webhook配置正确
- [ ] 邮件发送配置完成
- [ ] 退款政策明确
- [ ] 隐私政策页面
- [ ] 服务条款页面

---

## 💰 定价建议

| 版本 | Stripe价格ID | 金额 |
|------|-------------|------|
| 基础版 | price_basic | $99 |
| 专业版 | price_pro | $299 |
| 企业版 | price_enterprise | $999 |

---

**准备好开始收款了吗？** 💳
