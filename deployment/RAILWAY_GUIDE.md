# 🚀 Railway.app Deployment Guide

Complete guide to deploy DevDrishti Bot on Railway.app with professional setup.

## 🎯 Why Railway.app?

- ✅ **Free Tier**: $5 monthly credit (sufficient for testing)
- ✅ **Auto-scaling**: Handles traffic spikes automatically
- ✅ **Zero Config**: Detects Python automatically
- ✅ **Environment Variables**: Secure secret management
- ✅ **Instant Deploys**: Git push = auto deploy
- ✅ **Custom Domains**: Professional URLs
- ✅ **Persistent Storage**: For future database needs

## 🚀 Quick Deploy (2 Minutes)

### Step 1: Fork Repository
1. **Fork this repo** to your GitHub account
2. **Clone locally** (optional for customization)

### Step 2: Deploy to Railway
1. Go to [Railway.app](https://railway.app)
2. **Sign up** with GitHub account
3. Click **"New Project"**
4. Select **"Deploy from GitHub repo"**
5. Choose your **forked repository**
6. Railway auto-detects Python and starts building

### Step 3: Configure Environment Variables
In Railway dashboard, go to **Variables** tab and add:

```bash
# Required Variables
BOT_TOKEN=1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefgh
BOT_USERNAME=YourBotUsername
GEMINI_API_KEY=AIzaSyABCDEFGHIJKLMNOPQRSTUVWXYZ1234567
RAZORPAY_KEY_ID=rzp_live_1234567890ABCDEF
RAZORPAY_KEY_SECRET=1234567890ABCDEFGHIJKLMNOPQRSTUV

# Optional Variables (for enhanced features)
RATE_LIMIT_SECONDS=5
MAX_REQUESTS_PER_HOUR=60
```

### Step 4: Deploy & Test
1. Click **"Deploy"** 
2. Check **"Deployments"** tab for build logs
3. Once deployed, test your bot on Telegram
4. Check **"Logs"** for any issues

## 🔧 Detailed Configuration

### Environment Variables Setup

#### 1. Telegram Bot Token
```bash
# Get from @BotFather on Telegram
BOT_TOKEN=1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefgh
BOT_USERNAME=YourBotUsername  # Without @
```

#### 2. Google Gemini API
```bash
# Get from https://aistudio.google.com/app/apikey
GEMINI_API_KEY=AIzaSyABCDEFGHIJKLMNOPQRSTUVWXYZ1234567
```

#### 3. Razorpay Payment Gateway
```bash
# Test Environment (for development)
RAZORPAY_KEY_ID=rzp_test_1234567890ABCDEF
RAZORPAY_KEY_SECRET=1234567890ABCDEFGHIJKLMNOPQRSTUV

# Live Environment (for production)
RAZORPAY_KEY_ID=rzp_live_1234567890ABCDEF
RAZORPAY_KEY_SECRET=1234567890ABCDEFGHIJKLMNOPQRSTUV
```

#### 4. Optional Analytics (Google Sheets)
```bash
# Only if you want sales tracking in Google Sheets
GOOGLE_CREDS_FILE=service-account.json
SHEETS_ID=1abc-123-def456789_XYZabcdefg
```

### Railway Configuration Files

#### `railway.json` (Auto-detected)
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python main.py",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  },
  "environments": {
    "production": {
      "variables": {
        "PYTHONUNBUFFERED": "1",
        "PYTHON_VERSION": "3.11"
      }
    }
  }
}
```

## 📊 Monitoring & Logs

### Real-time Monitoring
1. **Deployments**: Track build status
2. **Logs**: View bot activity in real-time
3. **Metrics**: CPU, Memory, Network usage
4. **Usage**: Monthly spend tracking

### Log Analysis
```bash
# Common log patterns to watch for:
✅ "Bot polling started successfully"
✅ "User 12345 completed payment"
❌ "Error in daily reading for 67890"
❌ "Razorpay API error: Invalid key"
```

### Performance Optimization
```bash
# Railway automatically handles:
- CPU scaling (0.5-8 vCPUs)
- Memory scaling (512MB-32GB)
- Network optimization
- Geographic distribution
```

## 💰 Cost Management

### Free Tier Limits
- **$5 monthly credit** (enough for 500-1000 users)
- **No time limits** (runs 24/7)
- **Automatic sleep** after 30 min inactivity
- **Instant wake-up** on new requests

### Scaling Costs
| Users/Day | Monthly Cost | Revenue | Profit |
|-----------|-------------|---------|---------|
| 0-50 | $0 (Free) | ₹7,500 | ₹7,500 |
| 50-200 | $5-10 | ₹30,000 | ₹29,200 |
| 200-500 | $10-20 | ₹75,000 | ₹73,500 |
| 500+ | $20-50 | ₹150,000+ | ₹147,000+ |

### Cost Optimization Tips
1. **Use test keys** during development
2. **Monitor logs** for unnecessary API calls
3. **Enable rate limiting** to prevent abuse
4. **Use webhooks** instead of polling (future upgrade)

## 🔒 Security Best Practices

### Environment Variables
```bash
# ✅ DO: Use Railway's secure variables
BOT_TOKEN=secret_value_here

# ❌ DON'T: Hardcode in source
BOT_TOKEN = "1234567890:ABC..."  # Never do this!
```

### API Keys Management
1. **Separate environments**: Test vs Live keys
2. **Regular rotation**: Change keys monthly
3. **Minimal permissions**: Only required scopes
4. **Monitor usage**: Check for unusual activity

### Payment Security
```bash
# Always use HTTPS endpoints
# Validate webhook signatures  
# Log all transactions
# Monitor for fraud patterns
```

## 🚀 Advanced Deployment

### Custom Domains
1. Go to **Settings** → **Domains**
2. Add your domain: `bot.yourdomain.com`
3. Configure DNS: `CNAME` to Railway URL
4. Enable SSL automatically

### Multiple Environments
```bash
# Development Environment
ENVIRONMENT=development
RAZORPAY_KEY_ID=rzp_test_...

# Production Environment  
ENVIRONMENT=production
RAZORPAY_KEY_ID=rzp_live_...
```

### Database Integration (Future)
```bash
# Railway provides easy database add-ons:
- PostgreSQL (recommended)
- MySQL
- Redis (for caching)
- MongoDB
```

## 🛠️ Troubleshooting

### Common Issues

#### Bot Not Responding
```bash
# Check logs for:
❌ "Invalid bot token"
❌ "Gemini API quota exceeded"
❌ "Connection timeout"

# Solutions:
1. Verify BOT_TOKEN in variables
2. Check Gemini API quota
3. Restart deployment
```

#### Payment Errors
```bash
# Check logs for:
❌ "Razorpay authentication failed"
❌ "Invalid currency"
❌ "Webhook signature mismatch"

# Solutions:
1. Verify Razorpay keys
2. Check account status
3. Validate webhook setup
```

#### Performance Issues
```bash
# Monitor metrics for:
- High CPU usage (>80%)
- Memory leaks
- Slow response times

# Solutions:
1. Scale up resources
2. Optimize code
3. Add caching
```

### Debug Commands
```bash
# View recent logs
railway logs

# Connect to live environment
railway connect

# View environment variables
railway variables
```

## 📈 Scaling Strategies

### Phase 1: Launch (0-100 users)
- Use free tier
- Monitor conversion rates
- A/B testing pricing
- Collect user feedback

### Phase 2: Growth (100-1K users)  
- Upgrade to paid plan ($5-10/month)
- Add database for user states
- Implement analytics dashboard
- Optimize conversion funnels

### Phase 3: Scale (1K+ users)
- Multi-region deployment
- Load balancing
- Advanced analytics
- Team collaboration features

## 🎯 Success Metrics

### Technical KPIs
- **Uptime**: >99.9% availability
- **Response Time**: <500ms average
- **Error Rate**: <0.1% of requests
- **Deployment Time**: <2 minutes

### Business KPIs
- **Daily Active Users**: Growth rate
- **Conversion Rate**: Free → Paid
- **Revenue Per User**: ₹199-299 average
- **Customer Retention**: Monthly returns

## 🆘 Support & Resources

### Railway Resources
- 📖 [Railway Docs](https://docs.railway.app)
- 💬 [Railway Discord](https://discord.gg/railway)
- 📧 [Railway Support](mailto:team@railway.app)

### Bot Support
- 🐛 Report issues in GitHub repository
- 💬 Community support in Telegram
- 📧 Premium support available

---

**🚀 Ready to deploy? Your bot will be live in under 5 minutes!**

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/your-template-id) 