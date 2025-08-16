# 🚨 Railway Deployment Troubleshooting

Quick fixes for common Railway deployment issues with DevDrishti Bot.

## ❌ "FAILED" Status - Build Errors

**Problem**: Deployment shows "FAILED" status with pip installation errors.

**Error Message**: `ERROR: failed to build: failed to solve: process '/bin/bash...' did not complete successfully`

**Solution**: This is a dependency conflict issue. The repository has been updated with compatible versions.

### Quick Fix:
1. **Pull latest changes** from GitHub repository
2. **Redeploy** - Railway will use the updated `requirements.txt`
3. **Check Build Logs** - Should now install successfully

### What was fixed:
- Updated `requirements.txt` with compatible versions
- Changed Python version to 3.10 (more stable)
- Added `runtime.txt` for explicit version control

---

## ❌ "CRASHED" Status - Missing Environment Variables

**Problem**: Bot shows "CRASHED" status with missing environment variables error.

**Solution**: Set required environment variables in Railway dashboard:

### Step-by-Step Fix:

1. **Go to Railway Dashboard**
   - Visit: https://railway.app/dashboard
   - Select your `devdrishti-bot` project

2. **Set Environment Variables**
   - Click on **"Variables"** tab
   - Add these **REQUIRED** variables:

   ```
   BOT_TOKEN=your_telegram_bot_token
   BOT_USERNAME=your_bot_username
   GEMINI_API_KEY=your_gemini_api_key
   RAZORPAY_KEY_ID=rzp_test_or_live_key
   RAZORPAY_KEY_SECRET=your_razorpay_secret
   ```

3. **Get Your API Keys**:

   ### Telegram Bot Token
   - Message [@BotFather](https://t.me/BotFather)
   - Send `/newbot`
   - Follow instructions
   - Copy the token → `BOT_TOKEN`
   - Set username → `BOT_USERNAME`

   ### Gemini API Key
   - Go to: https://aistudio.google.com/app/apikey
   - Click "Create API Key"
   - Copy the key → `GEMINI_API_KEY`

   ### Razorpay Keys
   - Go to: https://dashboard.razorpay.com/signup
   - Complete signup/KYC
   - Go to: https://dashboard.razorpay.com/app/keys
   - Copy Key ID → `RAZORPAY_KEY_ID`
   - Copy Secret → `RAZORPAY_KEY_SECRET`

4. **Deploy**
   - After adding all variables, click **"Deploy"**
   - Bot should restart and show "RUNNING" status

---

## 🔄 Common Error Messages & Fixes

### Build Phase Errors:
- **"pip install failed"** → Fixed with updated `requirements.txt`
- **"Python version conflict"** → Fixed with `runtime.txt`
- **"Docker build failed"** → Updated Railway configuration

### Runtime Errors:
- **"Missing BOT_TOKEN and GEMINI_API_KEY"** → Add variables in Railway
- **"Failed to initialize Razorpay client"** → Check Razorpay credentials
- **"Analytics module not found"** → ✅ Normal (optional module)

---

## 📊 Verify Deployment

### Check Build Logs:
1. Go to Railway dashboard
2. Click **"Build Logs"** tab
3. Look for successful installation:
   ```
   ✅ Installing requirements from requirements.txt
   ✅ Successfully installed pyTelegramBotAPI aiohttp requests razorpay fpdf2
   ```

### Check Deploy Logs:
1. Click **"Deploy Logs"** tab
2. Look for these success messages:
   ```
   ✅ Razorpay client initialized successfully
   ✅ Telegram bot initialized successfully
   🚀 DevDrishti Bot initialization complete!
   ```

### Test Bot:
1. Find your bot on Telegram: `@YourBotUsername`
2. Send `/start`
3. Should receive welcome message
4. Send `daily` - should get free reading

---

## 🆘 Still Not Working?

### Check Railway Status:
- Project should show **"RUNNING"** (green)
- If "FAILED" (red), check Build Logs first
- If "CRASHED" (red), check Deploy Logs for runtime errors

### Verify All Variables:
Required variables in Railway dashboard:
- [x] `BOT_TOKEN` (starts with numbers:letters)
- [x] `BOT_USERNAME` (your bot's username without @)
- [x] `GEMINI_API_KEY` (starts with AIzaSy...)
- [x] `RAZORPAY_KEY_ID` (rzp_test_xxx or rzp_live_xxx)
- [x] `RAZORPAY_KEY_SECRET` (long alphanumeric string)

### Test API Keys:
Test each API key individually:
- **Telegram**: Message your bot manually
- **Gemini**: Check quotas at https://aistudio.google.com/app/apikey
- **Razorpay**: Login to dashboard to verify keys

---

## 📞 Get Help

If still having issues:

1. **Check Build Logs**: Copy exact error message
2. **Check Deploy Logs**: Copy runtime errors
3. **Verify Variables**: Screenshot of Railway Variables tab (hide secrets)
4. **GitHub Issues**: Report issue with error details

**Quick Contact**: Create issue with "Railway Deployment" label

---

**💡 Pro Tip**: Railway deployment happens in two phases - Build (install dependencies) then Deploy (run app). Check both logs if issues occur! 