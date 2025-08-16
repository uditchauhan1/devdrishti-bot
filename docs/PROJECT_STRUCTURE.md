# 📁 Project Structure

Complete overview of the DevDrishti Bot repository structure and file purposes.

## 🏗️ Repository Overview

```
devdrishti-bot/
├── 📄 README.md              # Main project documentation
├── 🚀 main.py                # Core bot application
├── 📦 requirements.txt       # Python dependencies
├── ⚙️ railway.json           # Railway deployment config
├── 🔧 Procfile              # Process configuration
├── 📝 env.example           # Environment variables template
├── 🙈 .gitignore            # Git ignore rules
├── 📄 LICENSE               # MIT license
├── 📊 analytics.py          # Analytics & tracking module
├── 📁 docs/                 # Documentation
│   ├── 🔑 API_SETUP.md      # API configuration guide
│   └── 📁 PROJECT_STRUCTURE.md # This file
├── 📁 deployment/           # Deployment guides
│   └── 🚀 RAILWAY_GUIDE.md  # Railway deployment guide
└── 📁 .git/                # Git version control (hidden)
```

---

## 📄 Core Files

### `main.py` - Bot Application
**Purpose**: Main Telegram bot application with all features
**Key Features**:
- Asynchronous bot framework (`AsyncTeleBot`)
- AI content generation with Gemini 2.5
- Razorpay payment integration
- Psychological pricing & A/B testing
- Rate limiting & user state management
- PDF report generation
- Analytics integration
- Referral system

**Key Components**:
```python
class DevDrishtiBot:
    def __init__(self):
        # Configuration and initialization
    
    async def handle_start(self, message):
        # Welcome message with viral hooks
    
    async def handle_daily_reading(self, user_id):
        # Free daily reading with upsell
    
    async def handle_personal_request(self, user_id):
        # Paid reading with Razorpay payment
    
    async def create_razorpay_order(self, user_id, amount):
        # Payment order creation
    
    async def generate_pdf_report(self, content, user_id):
        # PDF generation with branding
```

### `requirements.txt` - Dependencies
**Purpose**: Python package dependencies for production deployment
**Contents**:
- `pyTelegramBotAPI==4.14.0` - Telegram bot framework
- `aiohttp==3.9.1` - Async HTTP client for Gemini API
- `requests==2.31.0` - HTTP requests for Razorpay
- `razorpay==1.4.0` - Payment gateway integration
- `fpdf2==2.7.6` - PDF generation library

### `analytics.py` - Analytics Module
**Purpose**: Track user behavior, sales, and conversions
**Features**:
- User action logging
- Sales tracking with discount analysis
- A/B test conversion tracking
- Google Sheets integration (optional)
- Revenue analytics and reporting

**Key Methods**:
```python
class DevDrishtiAnalytics:
    def log_user_action(self, user_id, action, details="")
    def log_sale(self, user_id, price, details="", original_price=999)
    def log_referral(self, referrer_id, new_user_id)
    def get_conversion_summary(self)
    def print_dashboard(self)
```

---

## ⚙️ Configuration Files

### `railway.json` - Railway Deployment
**Purpose**: Railway.app deployment configuration
**Settings**:
- Build system: `NIXPACKS` (auto-detection)
- Start command: `python main.py`
- Restart policy: On failure, max 10 retries
- Python version: 3.11
- Unbuffered output for real-time logs

### `Procfile` - Process Definition
**Purpose**: Define how to run the application
**Content**: `web: python main.py`
**Compatibility**: Works with Railway, Heroku, and similar platforms

### `env.example` - Environment Template
**Purpose**: Template for required environment variables
**Sections**:
- **Required**: Bot token, Gemini API, Razorpay keys
- **Optional**: Analytics, rate limiting settings
- **Instructions**: Step-by-step setup guide

### `.gitignore` - Git Ignore Rules
**Purpose**: Exclude sensitive and temporary files from version control
**Excludes**:
- Environment files (`.env`, `*.env`)
- Python cache (`__pycache__/`, `*.pyc`)
- Logs (`*.log`, `devdrishti.log`)
- Credentials (`service-account.json`)
- Generated files (`*.pdf`, `analytics.json`)

---

## 📁 Documentation (`docs/`)

### `API_SETUP.md` - API Configuration Guide
**Purpose**: Complete guide to set up all required APIs
**Sections**:
1. **Telegram Bot API**: BotFather setup, commands configuration
2. **Google Gemini API**: API key generation, quotas, testing
3. **Razorpay API**: Account creation, KYC, test vs live keys
4. **Google Sheets API**: Service account, permissions, integration
5. **Security**: Best practices, rate limiting, error handling
6. **Troubleshooting**: Common issues and solutions

### `PROJECT_STRUCTURE.md` - This File
**Purpose**: Explain repository organization and file purposes
**Content**: Detailed breakdown of every file and directory

---

## 📁 Deployment (`deployment/`)

### `RAILWAY_GUIDE.md` - Railway Deployment
**Purpose**: Complete Railway.app deployment guide
**Sections**:
- Quick 2-minute deployment
- Environment variables setup
- Monitoring and logs
- Cost management and scaling
- Security best practices
- Troubleshooting common issues
- Advanced features (custom domains, webhooks)

---

## 🔧 Development Files

### Version Control (`.git/`)
**Purpose**: Git version control system (hidden directory)
**Contents**: Commit history, branches, remote configurations

### IDE Configuration (Optional)
```
.vscode/          # VS Code settings
.idea/            # PyCharm settings
*.swp, *.swo      # Vim temporary files
```
*Note: These are excluded by `.gitignore`*

---

## 📊 Generated Files (Runtime)

### `analytics.json` - Analytics Data
**Purpose**: Store user actions, sales, and conversion data
**Structure**:
```json
{
  "users": {},
  "sales": [],
  "actions": [],
  "referrals": [],
  "pricing_test": {"199": 0, "299": 0},
  "daily_stats": {}
}
```
*Note: Excluded from Git, persists on Railway deployment*

### `*.pdf` - Generated Reports
**Purpose**: User astrology reports
**Naming**: `astrology_report_{user_id}_{timestamp}.pdf`
**Content**: Personalized Vedic astrology readings
*Note: Excluded from Git, automatically cleaned up*

### `devdrishti.log` - Application Logs
**Purpose**: Detailed application logging
**Content**: User actions, API calls, errors, payments
**Rotation**: Automatic log rotation on Railway
*Note: Excluded from Git, viewable in Railway dashboard*

---

## 🚀 Deployment-Ready Features

### Railway.app Optimizations
- **Auto-detection**: Python environment automatically configured
- **Environment variables**: Secure secrets management
- **Persistent storage**: Analytics data survives deployments
- **Auto-scaling**: Handles traffic spikes automatically
- **Monitoring**: Built-in logs and metrics
- **SSL**: HTTPS encryption by default

### Production Readiness Checklist
- [x] Async/await for performance
- [x] Error handling and graceful failures
- [x] Rate limiting to prevent abuse
- [x] Secure environment variables
- [x] Comprehensive logging
- [x] Payment gateway integration
- [x] Analytics and conversion tracking
- [x] User state management
- [x] PDF generation with branding
- [x] Referral system for viral growth

---

## 🔄 Development Workflow

### Local Development
1. **Clone repository**: `git clone <repo-url>`
2. **Install dependencies**: `pip install -r requirements.txt`
3. **Set environment**: `cp env.example .env`
4. **Configure APIs**: Fill in `.env` with actual keys
5. **Run locally**: `python main.py`

### Testing
1. **Use test keys**: Razorpay test mode
2. **Check logs**: Monitor `devdrishti.log`
3. **Test payments**: Use test cards/UPI
4. **Verify analytics**: Check `analytics.json`

### Deployment
1. **Push to GitHub**: `git push origin main`
2. **Deploy to Railway**: Auto-deployment from Git
3. **Set environment**: Configure variables in Railway
4. **Monitor logs**: Real-time logging in dashboard
5. **Test production**: Verify all features work

### Scaling
1. **Monitor metrics**: CPU, memory, requests
2. **Analyze conversions**: A/B test results
3. **Optimize costs**: API usage and Railway resources
4. **Add features**: Based on user feedback
5. **Database upgrade**: For > 1K concurrent users

---

## 🎯 Future Enhancements

### Planned Features
- **Webhook support**: Replace polling with webhooks
- **Database integration**: PostgreSQL for user data
- **Multi-language**: Hindi, Tamil, Bengali support
- **Voice messages**: Audio astrology readings
- **Image analysis**: Palmistry from hand photos
- **Subscription model**: Monthly unlimited readings
- **Mobile app**: React Native companion app

### Technical Improvements
- **Redis caching**: Faster response times
- **Load balancing**: Multiple bot instances
- **OCR integration**: Automatic payment verification
- **Machine learning**: Personalized recommendations
- **API rate optimization**: Intelligent caching
- **Security enhancements**: Advanced fraud detection

---

**📁 Repository is production-ready and optimized for Railway.app deployment!**

Next: [API Setup Guide](API_SETUP.md) → [Railway Deployment](../deployment/RAILWAY_GUIDE.md) 