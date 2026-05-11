#!/usr/bin/env python3
"""
AI Agent Money Machine - Automated Delivery System
自动交付系统 - 支付成功后自动发送下载链接

Features:
- Monitor Stripe payments via webhook
- Send download links via email
- Track delivery status
- Handle retries and errors
"""

import os
import json
import hashlib
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class DeliverySystem:
    """自动交付系统"""
    
    def __init__(self, config_path: str = "delivery_config.json"):
        self.config = self._load_config(config_path)
        self.deliveries_db = {}
        self.load_deliveries()
    
    def _load_config(self, path: str) -> Dict:
        """加载配置"""
        default_config = {
            "smtp_server": "smtp.gmail.com",
            "smtp_port": 587,
            "smtp_username": "your-email@gmail.com",
            "smtp_password": "your-app-password",
            "from_email": "noreply@agentverse.ai",
            "from_name": "AgentVerse",
            "download_base_url": "https://github.com/elenashang888/ai-agent-money-machine/releases",
            "delivery_expiry_days": 7,
            "retry_attempts": 3,
            "retry_delay_minutes": 5
        }
        
        try:
            with open(path, 'r') as f:
                return {**default_config, **json.load(f)}
        except FileNotFoundError:
            return default_config
    
    def load_deliveries(self):
        """加载交付记录"""
        db_path = "deliveries_db.json"
        if os.path.exists(db_path):
            with open(db_path, 'r') as f:
                self.deliveries_db = json.load(f)
    
    def save_deliveries(self):
        """保存交付记录"""
        with open("deliveries_db.json", 'w') as f:
            json.dump(self.deliveries_db, f, indent=2)
    
    def generate_download_token(self, email: str, plan: str) -> str:
        """生成安全的下载令牌"""
        timestamp = str(int(time.time()))
        data = f"{email}:{plan}:{timestamp}:{self.config.get('secret_key', 'default_secret')}"
        token = hashlib.sha256(data.encode()).hexdigest()[:32]
        return token
    
    def get_download_url(self, email: str, plan: str) -> str:
        """获取下载链接"""
        token = self.generate_download_token(email, plan)
        
        # 根据套餐返回不同的下载链接
        download_urls = {
            "starter": f"{self.config['download_base_url']}/download/starter?token={token}",
            "professional": f"{self.config['download_base_url']}/download/pro?token={token}",
            "enterprise": f"{self.config['download_base_url']}/download/enterprise?token={token}"
        }
        
        return download_urls.get(plan, download_urls["starter"])
    
    def record_delivery(self, email: str, plan: str, payment_id: str) -> Dict:
        """记录交付信息"""
        delivery_id = f"DEL_{int(time.time())}_{email.split('@')[0]}"
        
        delivery = {
            "id": delivery_id,
            "email": email,
            "plan": plan,
            "payment_id": payment_id,
            "created_at": datetime.now().isoformat(),
            "expires_at": (datetime.now() + timedelta(days=self.config['delivery_expiry_days'])).isoformat(),
            "download_url": self.get_download_url(email, plan),
            "status": "pending",
            "attempts": 0,
            "last_attempt": None,
            "email_sent": False
        }
        
        self.deliveries_db[delivery_id] = delivery
        self.save_deliveries()
        
        return delivery
    
    def send_delivery_email(self, delivery: Dict) -> bool:
        """发送交付邮件"""
        try:
            # 创建邮件
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f"Your AI Agent Money Machine - {delivery['plan'].title()} Package"
            msg['From'] = f"{self.config['from_name']} <{self.config['from_email']}>"
            msg['To'] = delivery['email']
            
            # HTML邮件内容
            html_content = self._get_email_template(delivery)
            
            msg.attach(MIMEText(html_content, 'html'))
            
            # 发送邮件
            with smtplib.SMTP(self.config['smtp_server'], self.config['smtp_port']) as server:
                server.starttls()
                server.login(
                    self.config['smtp_username'],
                    self.config['smtp_password']
                )
                server.send_message(msg)
            
            # 更新状态
            delivery['email_sent'] = True
            delivery['status'] = 'delivered'
            delivery['last_attempt'] = datetime.now().isoformat()
            self.save_deliveries()
            
            print(f"✅ Delivery email sent to {delivery['email']}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to send email: {e}")
            delivery['attempts'] += 1
            delivery['last_attempt'] = datetime.now().isoformat()
            
            if delivery['attempts'] >= self.config['retry_attempts']:
                delivery['status'] = 'failed'
            
            self.save_deliveries()
            return False
    
    def _get_email_template(self, delivery: Dict) -> str:
        """获取邮件模板"""
        plan_features = {
            "starter": [
                "6 AI Agents included",
                "Basic templates",
                "Documentation",
                "Community access"
            ],
            "professional": [
                "All 6 AI Agents",
                "Advanced templates",
                "Source code access",
                "Video training",
                "Priority support",
                "Monthly updates"
            ],
            "enterprise": [
                "Everything in Pro",
                "Commercial license",
                "1-on-1 coaching",
                "Custom development",
                "White-label rights",
                "Lifetime updates"
            ]
        }
        
        features = plan_features.get(delivery['plan'], plan_features['starter'])
        features_html = ''.join([f'<li>{f}</li>' for f in features])
        
        return f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px; text-align: center; color: white; border-radius: 10px 10px 0 0; }}
        .content {{ background: #f9f9f9; padding: 40px; border-radius: 0 0 10px 10px; }}
        .button {{ display: inline-block; background: #667eea; color: white; padding: 15px 30px; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
        .features {{ background: white; padding: 20px; border-radius: 5px; margin: 20px 0; }}
        .footer {{ text-align: center; color: #999; margin-top: 30px; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎉 Welcome to AI Agent Money Machine!</h1>
            <p>Your {delivery['plan'].title()} package is ready</p>
        </div>
        
        <div class="content">
            <h2>Hi there,</h2>
            
            <p>Thank you for your purchase! Your download is ready.</p>
            
            <div style="text-align: center;">
                <a href="{delivery['download_url']}" class="button">Download Your Package</a>
            </div>
            
            <p style="color: #666; font-size: 14px;">Link expires: {delivery['expires_at'][:10]}</p>
            
            <div class="features">
                <h3>What's included in your {delivery['plan'].title()} package:</h3>
                <ul>
                    {features_html}
                </ul>
            </div>
            
            <h3>Getting Started:</h3>
            <ol>
                <li>Download the package using the button above</li>
                <li>Extract the files to your preferred location</li>
                <li>Follow the README.md for setup instructions</li>
                <li>Join our Discord community for support</li>
            </ol>
            
            <p>Need help? Reply to this email or contact us at support@agentverse.ai</p>
            
            <div class="footer">
                <p>Best regards,<br>The AgentVerse Team</p>
                <p style="margin-top: 20px;">
                    <a href="https://github.com/elenashang888/ai-agent-money-machine">GitHub</a> | 
                    <a href="#">Documentation</a> | 
                    <a href="#">Support</a>
                </p>
            </div>
        </div>
    </div>
</body>
</html>
"""
    
    def process_payment(self, payment_data: Dict) -> Dict:
        """处理支付完成事件"""
        email = payment_data.get('customer_email')
        plan = payment_data.get('metadata', {}).get('plan', 'starter')
        payment_id = payment_data.get('id')
        
        if not email:
            raise ValueError("Customer email not found")
        
        # 记录交付
        delivery = self.record_delivery(email, plan, payment_id)
        
        # 发送邮件
        success = self.send_delivery_email(delivery)
        
        if not success and delivery['attempts'] < self.config['retry_attempts']:
            # 安排重试
            print(f"⏳ Will retry in {self.config['retry_delay_minutes']} minutes")
        
        return delivery
    
    def retry_failed_deliveries(self):
        """重试失败的交付"""
        for delivery_id, delivery in self.deliveries_db.items():
            if delivery['status'] == 'pending' and delivery['attempts'] < self.config['retry_attempts']:
                # 检查是否需要重试
                if delivery['last_attempt']:
                    last_attempt = datetime.fromisoformat(delivery['last_attempt'])
                    if datetime.now() - last_attempt < timedelta(minutes=self.config['retry_delay_minutes']):
                        continue
                
                print(f"🔄 Retrying delivery: {delivery_id}")
                self.send_delivery_email(delivery)
    
    def get_delivery_status(self, delivery_id: str) -> Optional[Dict]:
        """获取交付状态"""
        return self.deliveries_db.get(delivery_id)
    
    def list_deliveries(self, status: Optional[str] = None) -> List[Dict]:
        """列出交付记录"""
        if status:
            return [d for d in self.deliveries_db.values() if d['status'] == status]
        return list(self.deliveries_db.values())


# Webhook处理示例
class StripeWebhookHandler:
    """Stripe Webhook处理器"""
    
    def __init__(self, delivery_system: DeliverySystem):
        self.delivery = delivery_system
    
    def handle_event(self, event_data: Dict) -> Dict:
        """处理Stripe事件"""
        event_type = event_data.get('type')
        
        if event_type == 'checkout.session.completed':
            session = event_data['data']['object']
            
            # 提取支付信息
            payment_data = {
                'id': session['id'],
                'customer_email': session['customer_details']['email'],
                'metadata': session.get('metadata', {}),
                'amount_total': session['amount_total'],
                'currency': session['currency']
            }
            
            # 处理交付
            delivery = self.delivery.process_payment(payment_data)
            
            return {
                'status': 'success',
                'delivery_id': delivery['id'],
                'message': 'Payment processed and delivery initiated'
            }
        
        elif event_type == 'invoice.payment_failed':
            # 处理支付失败
            return {
                'status': 'failed',
                'message': 'Payment failed, no delivery'
            }
        
        return {'status': 'ignored', 'message': f'Event type {event_type} not handled'}


# 使用示例
if __name__ == "__main__":
    # 初始化系统
    delivery = DeliverySystem()
    
    # 模拟支付完成
    test_payment = {
        'id': 'pi_test_123456',
        'customer_email': 'test@example.com',
        'metadata': {'plan': 'professional'},
        'amount_total': 29900,
        'currency': 'usd'
    }
    
    # 处理交付
    result = delivery.process_payment(test_payment)
    print(f"\nDelivery processed: {result['id']}")
    print(f"Status: {result['status']}")
    print(f"Download URL: {result['download_url']}")
