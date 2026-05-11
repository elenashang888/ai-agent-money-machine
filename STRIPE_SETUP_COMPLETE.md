# Stripe Payment Integration for AI Agent Money Machine

## Overview
This guide configures Stripe payment processing for the AI Agent Money Machine product.

## Product Setup

### 1. Create Products in Stripe Dashboard

**Starter Plan - $99**
```json
{
  "name": "AI Agent Money Machine - Starter",
  "description": "6 AI Agents with basic templates and documentation",
  "price": 9900,  // $99.00 in cents
  "currency": "usd",
  "type": "one_time"
}
```

**Professional Plan - $299**
```json
{
  "name": "AI Agent Money Machine - Professional",
  "description": "Complete package with source code, training, and priority support",
  "price": 29900,  // $299.00 in cents
  "currency": "usd",
  "type": "one_time"
}

**Enterprise Plan - $999**
```json
{
  "name": "AI Agent Money Machine - Enterprise",
  "description": "Full commercial license with 1-on-1 coaching and custom development",
  "price": 99900,  // $999.00 in cents
  "currency": "usd",
  "type": "one_time"
}
```

### 2. Stripe Checkout Integration

**File: `stripe-checkout.js`**

```javascript
// Stripe Configuration
const STRIPE_PUBLIC_KEY = 'pk_live_YOUR_PUBLISHABLE_KEY'; // Replace with your key

// Product Price IDs (from Stripe Dashboard)
const PRICE_IDS = {
  starter: 'price_starter_xxxxx',      // Replace with actual Price ID
  professional: 'price_professional_xxxxx',  // Replace with actual Price ID
  enterprise: 'price_enterprise_xxxxx'   // Replace with actual Price ID
};

// Initialize Stripe
const stripe = Stripe(STRIPE_PUBLIC_KEY);

// Checkout Function
async function checkout(plan) {
  try {
    const response = await fetch('/create-checkout-session', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        priceId: PRICE_IDS[plan],
        successUrl: window.location.origin + '/success.html?session_id={CHECKOUT_SESSION_ID}',
        cancelUrl: window.location.origin + '/cancel.html',
      }),
    });

    const session = await response.json();
    
    // Redirect to Stripe Checkout
    const result = await stripe.redirectToCheckout({
      sessionId: session.id,
    });

    if (result.error) {
      alert(result.error.message);
    }
  } catch (error) {
    console.error('Error:', error);
    alert('Payment failed. Please try again.');
  }
}

// Attach to buttons
document.getElementById('buy-starter').addEventListener('click', () => checkout('starter'));
document.getElementById('buy-professional').addEventListener('click', () => checkout('professional'));
document.getElementById('buy-enterprise').addEventListener('click', () => checkout('enterprise'));
```

### 3. Backend Integration (Node.js/Express)

**File: `server.js`**

```javascript
const express = require('express');
const stripe = require('stripe')('sk_live_YOUR_SECRET_KEY'); // Replace with your key
const app = express();

app.use(express.static('public'));
app.use(express.json());

// Create Checkout Session
app.post('/create-checkout-session', async (req, res) => {
  const { priceId, successUrl, cancelUrl } = req.body;

  try {
    const session = await stripe.checkout.sessions.create({
      payment_method_types: ['card'],
      line_items: [
        {
          price: priceId,
          quantity: 1,
        },
      ],
      mode: 'payment',
      success_url: successUrl,
      cancel_url: cancelUrl,
      automatic_tax: { enabled: true },
      customer_creation: 'always',
    });

    res.json({ id: session.id });
  } catch (error) {
    console.error('Error creating session:', error);
    res.status(500).json({ error: error.message });
  }
});

// Webhook for payment confirmation
app.post('/webhook', express.raw({ type: 'application/json' }), async (req, res) => {
  const sig = req.headers['stripe-signature'];
  const endpointSecret = 'whsec_YOUR_WEBHOOK_SECRET'; // Replace with your webhook secret

  let event;

  try {
    event = stripe.webhooks.constructEvent(req.body, sig, endpointSecret);
  } catch (err) {
    console.log(`Webhook Error: ${err.message}`);
    return res.status(400).send(`Webhook Error: ${err.message}`);
  }

  // Handle successful payment
  if (event.type === 'checkout.session.completed') {
    const session = event.data.object;
    
    // Send download link via email
    await sendDownloadLink(session.customer_email, session.metadata.plan);
    
    // Log sale
    console.log(`Payment successful: ${session.id}`);
  }

  res.json({ received: true });
});

// Success page
app.get('/success.html', (req, res) => {
  res.send(`
    <!DOCTYPE html>
    <html>
    <head>
      <title>Payment Successful</title>
      <style>
        body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
        .success { color: #4CAF50; font-size: 24px; }
        .container { max-width: 600px; margin: 0 auto; }
      </style>
    </head>
    <body>
      <div class="container">
        <h1 class="success">✓ Payment Successful!</h1>
        <p>Thank you for your purchase. Check your email for download instructions.</p>
        <p>Your AI Agent Money Machine package will be delivered within 5 minutes.</p>
      </div>
    </body>
    </html>
  `);
});

app.listen(3000, () => console.log('Server running on port 3000'));
```

### 4. Simple HTML Integration

**Update sales page buttons:**

```html
<!-- In your pricing section, replace the onclick alerts with actual Stripe integration -->

<!-- Option 1: Direct Stripe Payment Links (Easiest) -->
<a href="https://buy.stripe.com/YOUR_STARTER_LINK" class="buy-button">Get Started</a>
<a href="https://buy.stripe.com/YOUR_PROFESSIONAL_LINK" class="buy-button">Get Professional</a>
<a href="https://buy.stripe.com/YOUR_ENTERPRISE_LINK" class="buy-button">Contact Sales</a>

<!-- Option 2: Stripe Checkout (More control) -->
<button id="buy-starter" class="buy-button">Get Started</button>
<button id="buy-professional" class="buy-button">Get Professional</button>
<button id="buy-enterprise" class="buy-button">Contact Sales</button>

<!-- Add Stripe.js -->
<script src="https://js.stripe.com/v3/"></script>
<script src="stripe-checkout.js"></script>
```

## Setup Instructions

### Step 1: Create Stripe Account
1. Go to https://stripe.com
2. Sign up for free account
3. Complete verification
4. Get API keys from Dashboard

### Step 2: Create Products
1. In Stripe Dashboard → Products
2. Add 3 products with prices
3. Note the Price IDs

### Step 3: Get Payment Links (Easiest Method)
1. For each product, click "Create payment link"
2. Copy the URL
3. Replace in HTML: `https://buy.stripe.com/YOUR_LINK`

### Step 4: Configure Webhook (Optional)
1. Stripe Dashboard → Developers → Webhooks
2. Add endpoint: `https://yourdomain.com/webhook`
3. Select events: `checkout.session.completed`
4. Copy webhook secret

### Step 5: Test
1. Use Stripe test mode
2. Test card: 4242 4242 4242 4242
3. Any future date, any CVC, any ZIP

## Tax Configuration

**Automatic Tax (Recommended)**
- Enable in Stripe Dashboard
- Automatically calculates sales tax
- Supports 40+ countries

**Manual Tax**
- Configure tax rates per region
- Apply to checkout session

## Email Delivery

**Option 1: Stripe Email (Built-in)**
- Enable in Checkout settings
- Sends receipt automatically

**Option 2: Custom Email (Recommended)**
Use services like:
- SendGrid
- Mailgun
- AWS SES

**Example email template:**
```
Subject: Your AI Agent Money Machine Download

Hi {{name}},

Thank you for your purchase!

Your download link: {{download_url}}
Access expires in: 7 days

Getting started:
1. Download the package
2. Follow the setup guide
3. Join our Discord community

Need help? Reply to this email.

Best,
AgentVerse Team
```

## Security Checklist

- [ ] Never commit API keys to Git
- [ ] Use environment variables
- [ ] Enable HTTPS only
- [ ] Validate webhook signatures
- [ ] Log all transactions
- [ ] Set up monitoring

## Next Steps

1. Replace all placeholder keys with real ones
2. Test in Stripe test mode
3. Switch to live mode
4. Monitor first sales
5. Set up automated delivery

---

**Estimated Setup Time:** 30 minutes
**Cost:** Stripe takes 2.9% + $0.30 per transaction
