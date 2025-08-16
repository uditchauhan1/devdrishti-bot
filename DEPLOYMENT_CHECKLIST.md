# ✅ Deployment Checklist

**Pre-deployment checklist to ensure your DevDrishti Bot is ready for Railway.app**

## 🎯 Pre-Deployment (Setup APIs)

### Telegram Bot Setup
- [ ] Created bot with @BotFather
- [ ] Got `BOT_TOKEN` (format: `1234567890:ABC...`)
- [ ] Set `BOT_USERNAME` (without @)
- [ ] Configured bot commands with @BotFather
- [ ] Set bot description and profile picture

### Google Gemini API
- [ ] Created API key at [Google AI Studio](https://aistudio.google.com/app/apikey)
- [ ] Copied `GEMINI_API_KEY` (format: `AIzaSy...`)
- [ ] Tested API access (optional)
- [ ] Verified free tier quotas (15 req/min, 1500/day)

### Razorpay Payment Gateway
- [ ] Signed up at [Razorpay Dashboard](https://dashboard.razorpay.com/signup)
- [ ] Got test keys: `rzp_test_...` and secret
- [ ] Completed KYC for live keys (2-3 days)
- [ ] Got live keys: `rzp_live_...` and secret
- [ ] Added bank account for settlements

### Google Sheets Analytics (Optional)
- [ ] Created Google Cloud project
- [ ] Enabled Sheets API
- [ ] Created service account
- [ ] Downloaded JSON credentials
- [ ] Created analytics spreadsheet
- [ ] Shared sheet with service account email

---

## 🚀 Railway Deployment

### Repository Setup
- [ ] Forked/cloned this repository
- [ ] All files present and updated
- [ ] No sensitive data in code
- [ ] `.gitignore` properly configured

### Railway Configuration
- [ ] Created Railway account
- [ ] Connected GitHub repository
- [ ] Selected correct repository
- [ ] Auto-build started successfully

### Environment Variables
Set these in Railway dashboard under **Variables**:

**Required Variables:**
- [ ] `BOT_TOKEN` = `1234567890:ABC...`
- [ ] `BOT_USERNAME` = `your_bot_username`
- [ ] `GEMINI_API_KEY` = `AIzaSy...`
- [ ] `RAZORPAY_KEY_ID` = `rzp_live_...` (or `rzp_test_...`)
- [ ] `RAZORPAY_KEY_SECRET` = `your_secret_key`

**Optional Variables:**
- [ ] `RATE_LIMIT_SECONDS` = `5`
- [ ] `MAX_REQUESTS_PER_HOUR` = `60`
- [ ] `GOOGLE_CREDS_FILE` = `service-account.json` (if using analytics)
- [ ] `SHEETS_ID` = `your_sheet_id` (if using analytics)

---

## 🧪 Testing Phase

### Basic Functionality
- [ ] Bot responds to `/start` command
- [ ] Welcome message displays correctly
- [ ] `/help` command works
- [ ] `daily` command generates free reading
- [ ] Error messages are user-friendly

### Payment Flow (Test Mode)
- [ ] `personal` command shows discount offer
- [ ] Razorpay payment link is generated
- [ ] Test payment completes successfully
- [ ] PDF report is generated and sent
- [ ] Analytics data is logged (if enabled)

### Advanced Features
- [ ] A/B testing shows different prices (₹199/₹299)
- [ ] Photo handler accepts payment screenshots
- [ ] Referral links work correctly
- [ ] Rate limiting prevents spam
- [ ] Dynamic urgency messages appear

---

## 🔄 Production Switch

### Go Live Checklist
- [ ] Switch to live Razorpay keys in Railway
- [ ] Test one real payment (small amount)
- [ ] Verify money reaches your bank account
- [ ] Update bot description if needed
- [ ] Monitor logs for any errors

### Final Verification
- [ ] Bot is accessible to public
- [ ] All features work in production
- [ ] Payment notifications are working
- [ ] Analytics are being recorded
- [ ] Performance is acceptable

---

## 📊 Post-Launch Monitoring

### Daily Checks (First Week)
- [ ] Check Railway logs for errors
- [ ] Monitor user interactions
- [ ] Verify payments are processing
- [ ] Check analytics data
- [ ] Respond to user feedback

### Weekly Optimization
- [ ] Analyze A/B test results
- [ ] Review conversion rates
- [ ] Check API usage and costs
- [ ] Update content if needed
- [ ] Plan feature improvements

---

## 🎯 Success Metrics to Track

### Technical KPIs
- **Uptime**: >99% availability
- **Response Time**: <2 seconds average
- **Error Rate**: <1% of requests
- **Payment Success**: >95% completion rate

### Business KPIs
- **Daily Users**: Track growth
- **Conversion Rate**: Free → Paid (target: 15%)
- **Revenue**: Daily/Monthly tracking
- **User Retention**: Repeat customers

---

## 🆘 Troubleshooting Quick Fixes

### Bot Not Responding
```bash
# Check in Railway logs:
1. "Invalid bot token" → Verify BOT_TOKEN
2. "Connection timeout" → Check network
3. "Rate limit exceeded" → Wait or increase limits
```

### Payment Issues
```bash
# Common Razorpay problems:
1. "Authentication failed" → Check keys
2. "Invalid currency" → Use INR only
3. "Account suspended" → Complete KYC
```

### Performance Issues
```bash
# Railway optimization:
1. High CPU → Optimize code or scale up
2. Memory leaks → Check logs for errors
3. Slow response → Add caching
```

---

## 🚀 Launch Strategy

### Soft Launch (Days 1-7)
- Start with friends and family
- Test all features thoroughly
- Gather initial feedback
- Fix any critical issues

### Marketing Launch (Days 8-30)
- Share on social media
- Create viral content
- Optimize based on analytics
- Scale up infrastructure if needed

### Growth Phase (Month 2+)
- A/B test marketing messages
- Add new features
- Expand to other platforms
- Consider premium features

---

**🎉 Ready to Launch?**

1. ✅ Complete this checklist
2. 🚀 Deploy to Railway
3. 🧪 Test thoroughly
4. 📢 Start marketing
5. 📊 Monitor & optimize

**Your bot will be live and generating revenue within hours!**

---

### 📞 Support

If you encounter any issues:
1. Check the logs in Railway dashboard
2. Review [API Setup Guide](docs/API_SETUP.md)
3. Follow [Railway Guide](deployment/RAILWAY_GUIDE.md)
4. Create issue in GitHub repository

**Good luck with your launch! 🌟** 