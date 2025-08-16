# 🔮 DevDrishti Bot - AI Vedic Astrology Telegram Bot

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/your-template-id)

**Professional Telegram bot for Vedic astrology readings with AI-powered insights, psychological pricing, and secure payments.**

## ✨ Features

- 🤖 **AI-Powered**: Gemini 2.5 Flash for authentic Vedic readings
- 💰 **Smart Pricing**: A/B testing with discount psychology (₹999 → ₹199/299)
- ⚡ **Dynamic Urgency**: Time-based psychological triggers
- 💳 **Professional Payments**: Razorpay integration (UPI, Cards, Net Banking)
- 📊 **Advanced Analytics**: Revenue tracking and conversion optimization
- 🔗 **Viral Growth**: Built-in referral system
- 📱 **Photo Payments**: Accept payment screenshots
- 📄 **PDF Reports**: Beautiful astrology reports

## 🚀 Quick Deploy to Railway

1. **Click the Railway button above** ⬆️
2. **Connect your GitHub account**
3. **Set environment variables** (see below)
4. **Deploy!** 🚀

## 🔧 Environment Variables

Set these in Railway dashboard:

### Required Variables
```bash
# Telegram Bot
BOT_TOKEN=your_telegram_bot_token
BOT_USERNAME=YourBotUsername

# Google Gemini AI
GEMINI_API_KEY=your_gemini_api_key

# Razorpay Payment Gateway
RAZORPAY_KEY_ID=rzp_live_xxxxxxxxxxxxxxxx
RAZORPAY_KEY_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxx
```

### Optional Variables
```bash
# Analytics (Google Sheets)
GOOGLE_CREDS_FILE=service-account.json
SHEETS_ID=your_google_sheet_id

# Advanced Configuration
RATE_LIMIT_SECONDS=5
MAX_REQUESTS_PER_HOUR=60
```

## 📋 Setup Guide

### 1. Get Telegram Bot Token
1. Message [@BotFather](https://t.me/BotFather) on Telegram
2. Send `/newbot`
3. Choose name: `Your Bot Name`
4. Choose username: `YourBotUsername`
5. Copy the token → `BOT_TOKEN`
6. Set username → `BOT_USERNAME`

### 2. Get Gemini API Key
1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create new API key
3. Copy → `GEMINI_API_KEY`

### 3. Setup Razorpay
1. Sign up at [Razorpay](https://dashboard.razorpay.com/signup)
2. Complete KYC verification
3. Get API keys from dashboard
4. **Test Keys** (for testing): `rzp_test_xxx`
5. **Live Keys** (for production): `rzp_live_xxx`

### 4. Deploy to Railway
1. Fork this repository
2. Connect to Railway
3. Set environment variables
4. Deploy!

## 💰 Revenue Model

### Psychological Pricing Strategy
- **Anchor Price**: ₹999 (reference point)
- **A/B Testing**: ₹199 (80% off) vs ₹299 (70% off)
- **Conversion Triggers**: Scarcity, urgency, FOMO

### Expected Revenue
| Users/Day | Conversion Rate | Daily Revenue | Monthly Revenue |
|-----------|----------------|---------------|-----------------|
| 10 | 15% | ₹300 | ₹9,000 |
| 50 | 15% | ₹1,500 | ₹45,000 |
| 100 | 15% | ₹3,000 | ₹90,000 |
| 200 | 15% | ₹6,000 | ₹180,000 |

## 📊 Analytics & Tracking

### Built-in Analytics
- Revenue tracking
- A/B test results
- Conversion funnel analysis
- User behavior patterns

### Google Sheets Integration (Optional)
- Automatic sales logging
- Real-time dashboards
- Advanced reporting

## 🔒 Security Features

- ✅ Environment variable configuration
- ✅ No hardcoded secrets
- ✅ Rate limiting (prevents abuse)
- ✅ Secure payment processing
- ✅ Transaction logging
- ✅ Error handling

## 🎯 User Flow

1. **Discovery**: User starts bot (`/start`)
2. **Engagement**: Free daily reading (`daily`)
3. **Conversion**: Discount offer shown
4. **Payment**: Secure Razorpay checkout (`personal`)
5. **Delivery**: AI-generated PDF report
6. **Referral**: Viral sharing link

## 📱 Bot Commands

- `/start` - Begin your cosmic journey
- `/help` - Show available commands
- `daily` - Get free daily insight
- `personal` - Purchase detailed reading

## 🛠️ Development

### Local Setup
```bash
# Clone repository
git clone https://github.com/yourusername/devdrishti-bot.git
cd devdrishti-bot

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Edit .env with your values

# Run bot
python main.py
```

### File Structure
```
devdrishti-bot/
├── main.py                 # Main bot application
├── requirements.txt        # Python dependencies
├── railway.json           # Railway configuration
├── Procfile               # Process configuration
├── .env.example           # Environment template
├── analytics.py           # Analytics module
├── deployment/            # Deployment guides
└── docs/                  # Documentation
```

## 🚀 Deployment Options

### Railway.app (Recommended)
- ✅ Easy deployment
- ✅ Automatic scaling
- ✅ Environment variables
- ✅ Free tier available

### Alternative Platforms
- **Heroku**: Classic choice
- **DigitalOcean**: App Platform
- **Vercel**: Serverless functions
- **AWS**: Lambda + API Gateway

## 📈 Scaling Guide

### Phase 1: Launch (0-1K users)
- Deploy basic bot
- Monitor analytics
- Optimize conversion

### Phase 2: Growth (1K-10K users)
- A/B test pricing
- Add more features
- Improve user experience

### Phase 3: Scale (10K+ users)
- Database integration
- Multiple bot instances
- Advanced analytics

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- 📧 Email: support@devdrishti.com
- 💬 Telegram: [@DevDrishti_Support](https://t.me/DevDrishti_Support)
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/devdrishti-bot/issues)

## 🙏 Acknowledgments

- Google Gemini AI for intelligent responses
- Razorpay for secure payment processing
- Railway.app for seamless deployment
- Telegram Bot API for messaging platform

---

**Built with ❤️ for the Vedic astrology community**

[![Star this repo](https://img.shields.io/github/stars/yourusername/devdrishti-bot?style=social)](https://github.com/yourusername/devdrishti-bot/stargazers) 