# 🚨 Railway Deployment Troubleshooting

Quick fixes for common Railway deployment issues with DevDrishti Bot.

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

### "Missing BOT_TOKEN and GEMINI_API_KEY"
- **Fix**: Add both variables in Railway Variables tab
- **Check**: Ensure no extra spaces in variable names/values

### "Failed to initialize Razorpay client"
- **Fix**: Check your Razorpay keys are correct
- **Test vs Live**: Use `rzp_test_xxx` for testing, `rzp_live_xxx` for production

### "Analytics module not found"
- **Status**: ✅ Normal - this is optional
- **Fix**: No action needed (analytics will be disabled)

### "Import error: No module named 'razorpay'"
- **Fix**: Check `requirements.txt` includes `razorpay==1.4.0`
- **Auto-fix**: Bot should auto-install missing packages

---

## 📊 Verify Deployment

### Check Logs:
1. Go to Railway dashboard
2. Click **"Deploy Logs"** tab
3. Look for these success messages:
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
- If "CRASHED" (red), check Deploy Logs for errors

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

1. **Check Deploy Logs**: Copy exact error message
2. **Verify Variables**: Screenshot of Railway Variables tab (hide secrets)
3. **GitHub Issues**: Report issue with error details
4. **Documentation**: Review [API Setup Guide](docs/API_SETUP.md)

**Quick Contact**: Create issue with "Railway Deployment" label

---

**💡 Pro Tip**: Use test keys initially to verify deployment works, then switch to live keys for production! 