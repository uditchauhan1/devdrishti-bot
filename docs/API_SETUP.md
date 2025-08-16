# 🔑 API Setup Guide

Complete guide to set up all required APIs and services for DevDrishti Bot.

## 📋 Required APIs

1. **Telegram Bot API** - Core messaging platform
2. **Google Gemini API** - AI content generation  
3. **Razorpay API** - Payment processing
4. **Google Sheets API** - Analytics (optional)

---

## 🤖 1. Telegram Bot API Setup

### Step 1: Create Bot with BotFather
1. Open Telegram and search for `@BotFather`
2. Send `/start` to begin
3. Send `/newbot` to create a new bot
4. Choose a **name** for your bot (e.g., "DevDrishti Astrologer")
5. Choose a **username** ending in 'bot' (e.g., "devdrishti_bot")

### Step 2: Get Bot Token
```
✅ Congratulations! You created a new bot.
Token: 1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefgh
Username: @devdrishti_bot
```

### Step 3: Configure Bot Settings
```bash
# Send these commands to @BotFather:
/setdescription - Set bot description
/setabouttext - Set about text  
/setuserpic - Upload bot profile picture
/setcommands - Set bot commands menu
```

### Bot Commands Setup
```
start - Begin your cosmic journey
help - Show available commands  
daily - Get free daily insight
personal - Purchase detailed reading
```

### Environment Variables
```bash
BOT_TOKEN=1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefgh
BOT_USERNAME=devdrishti_bot  # Without @
```

---

## 🧠 2. Google Gemini API Setup

### Step 1: Get API Key
1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Choose **"Create API key in new project"** or select existing project
5. Copy the generated API key

### Step 2: API Key Security
```bash
# ✅ DO: Keep your API key secure
GEMINI_API_KEY=AIzaSyABCDEFGHIJKLMNOPQRSTUVWXYZ1234567

# ❌ DON'T: Share or commit to public repos
```

### Step 3: Test API Access
```python
import requests

headers = {"Content-Type": "application/json"}
data = {
    "contents": [{"parts": [{"text": "Hello, test message"}]}]
}

response = requests.post(
    f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-latest:generateContent?key={api_key}",
    headers=headers,
    json=data
)

print(response.json())
```

### API Quotas & Limits
- **Free Tier**: 15 requests per minute
- **Rate Limit**: 1,500 requests per day
- **Context Length**: 1M tokens input, 8K tokens output
- **Cost**: $0.075 per 1K input tokens, $0.30 per 1K output tokens

### Environment Variables
```bash
GEMINI_API_KEY=AIzaSyABCDEFGHIJKLMNOPQRSTUVWXYZ1234567
```

---

## 💳 3. Razorpay API Setup

### Step 1: Create Razorpay Account
1. Go to [Razorpay Dashboard](https://dashboard.razorpay.com/signup)
2. Sign up with business email
3. Complete **KYC verification** (required for live payments)
4. Add bank account details
5. Submit required documents

### Step 2: Get API Keys

#### Test Environment (Development)
```bash
# Available immediately after signup
RAZORPAY_KEY_ID=rzp_test_1234567890ABCDEF
RAZORPAY_KEY_SECRET=1234567890ABCDEFGHIJKLMNOPQRSTUV
```

#### Live Environment (Production)  
```bash
# Available after KYC approval (2-3 business days)
RAZORPAY_KEY_ID=rzp_live_1234567890ABCDEF  
RAZORPAY_KEY_SECRET=1234567890ABCDEFGHIJKLMNOPQRSTUV
```

### Step 3: Configure Webhooks (Optional)
1. Go to **Settings** → **Webhooks**
2. Add webhook URL: `https://yourbot.railway.app/webhooks/razorpay`
3. Select events: `payment.captured`, `payment.failed`
4. Add webhook secret for security

### Step 4: Test Payment Flow
```python
import razorpay

client = razorpay.Client(auth=(key_id, key_secret))

# Create order
order = client.order.create({
    'amount': 19900,  # ₹199 in paise
    'currency': 'INR',
    'receipt': 'order_123',
    'payment_capture': 1
})

print(f"Order ID: {order['id']}")
```

### Razorpay Fees
- **UPI/Cards**: 2% + GST
- **Net Banking**: 2% + GST  
- **Wallets**: 2% + GST
- **Settlement**: T+1 working days
- **International**: 3% + GST

### Environment Variables
```bash
# Use test keys for development
RAZORPAY_KEY_ID=rzp_test_1234567890ABCDEF
RAZORPAY_KEY_SECRET=1234567890ABCDEFGHIJKLMNOPQRSTUV

# Use live keys for production  
RAZORPAY_KEY_ID=rzp_live_1234567890ABCDEF
RAZORPAY_KEY_SECRET=1234567890ABCDEFGHIJKLMNOPQRSTUV
```

---

## 📊 4. Google Sheets API Setup (Optional)

### Step 1: Create Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create new project: "DevDrishti Analytics"
3. Enable **Google Sheets API**
4. Enable **Google Drive API**

### Step 2: Create Service Account
1. Go to **IAM & Admin** → **Service Accounts**
2. Click **"Create Service Account"**
3. Name: "devdrishti-analytics"
4. Grant role: **Editor**
5. Create and download **JSON key file**

### Step 3: Share Google Sheet
1. Create new Google Sheet: "DevDrishti Analytics"
2. Share with service account email (from JSON file)
3. Grant **Editor** permissions
4. Copy sheet ID from URL

### Step 4: Configure Analytics
```python
import gspread
from google.oauth2.service_account import Credentials

# Authenticate with service account
credentials = Credentials.from_service_account_file(
    'service-account.json',
    scopes=['https://www.googleapis.com/auth/spreadsheets']
)

gc = gspread.authorize(credentials)
sheet = gc.open_by_key('your_sheet_id').sheet1

# Log sale data
sheet.append_row([
    datetime.now().isoformat(),
    user_id,
    price,
    'Sale completed'
])
```

### Environment Variables
```bash
GOOGLE_CREDS_FILE=service-account.json
SHEETS_ID=1abc-123-def456789_XYZabcdefg
```

---

## 🔒 Security Best Practices

### API Key Management
```bash
# ✅ Environment Variables (Railway)
BOT_TOKEN=your_secret_token
GEMINI_API_KEY=your_secret_key

# ❌ Hardcoded in Source Code  
BOT_TOKEN = "1234567890:ABC..."  # Never do this!
```

### Rate Limiting
```python
# Implement rate limiting to prevent abuse
import time
from collections import defaultdict

user_requests = defaultdict(list)
RATE_LIMIT = 5  # requests per minute

def check_rate_limit(user_id):
    now = time.time()
    user_requests[user_id] = [
        req_time for req_time in user_requests[user_id]
        if now - req_time < 60  # Last minute
    ]
    
    if len(user_requests[user_id]) >= RATE_LIMIT:
        return False
        
    user_requests[user_id].append(now)
    return True
```

### Error Handling
```python
# Always handle API failures gracefully
try:
    response = await gemini_api.generate_content(prompt)
except Exception as e:
    logger.error(f"Gemini API error: {e}")
    await bot.send_message(
        user_id, 
        "🙏 Service temporarily unavailable. Please try again."
    )
```

---

## 📈 Usage Monitoring

### API Usage Tracking
```python
import logging

# Set up comprehensive logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Log API usage
logger.info(f"Gemini API call for user {user_id}")
logger.info(f"Razorpay order created: {order_id}")
logger.info(f"Payment successful: {payment_id}")
```

### Cost Optimization
1. **Cache responses** where possible
2. **Batch API calls** to reduce requests  
3. **Monitor quotas** to avoid overages
4. **Use appropriate models** (smaller = cheaper)
5. **Implement retry logic** with exponential backoff

---

## 🎯 Testing Checklist

### Telegram Bot
- [ ] Bot responds to `/start`
- [ ] Commands work correctly
- [ ] Error messages are user-friendly
- [ ] Rate limiting prevents spam

### Gemini API
- [ ] Generates relevant astrology content
- [ ] Handles API errors gracefully
- [ ] Stays within rate limits
- [ ] Content quality is consistent

### Razorpay API  
- [ ] Test payments work in sandbox
- [ ] Live payments work in production
- [ ] Payment failures are handled
- [ ] Webhook events are processed

### Google Sheets (if enabled)
- [ ] Sales data is logged correctly
- [ ] Sheet permissions are correct
- [ ] Authentication works
- [ ] Error handling for sheet failures

---

## 🆘 Troubleshooting

### Common Issues

#### "Invalid Bot Token"
```bash
# Check token format: should be numbers:letters
# Example: 1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefgh
```

#### "Gemini API Quota Exceeded"
```bash
# Check quotas at: https://aistudio.google.com/app/apikey
# Implement retry with exponential backoff
# Consider upgrading to paid tier
```

#### "Razorpay Authentication Failed"
```bash
# Verify key_id and key_secret are correct
# Check if using test vs live keys appropriately  
# Ensure account is activated
```

#### "Google Sheets Permission Denied"
```bash
# Check service account has edit permissions
# Verify sheet is shared with service account email
# Confirm API is enabled in Google Cloud Console
```

---

**🎯 All APIs configured? You're ready to deploy!**

Continue to [Railway Deployment Guide](../deployment/RAILWAY_GUIDE.md) → 