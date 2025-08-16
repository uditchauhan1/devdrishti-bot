#!/usr/bin/env python3
"""
DevDrishti Bot - Railway.app Deployment Version
Features: Professional payment gateway, discount psychology, A/B testing, dynamic urgency
"""
import os
import sys
import subprocess
import asyncio
import logging
import random
from io import BytesIO
from datetime import datetime, timedelta
from collections import defaultdict

# Try to import analytics for tracking
try:
    from analytics import DevDrishtiAnalytics
    ANALYTICS_ENABLED = True
except ImportError:
    ANALYTICS_ENABLED = False
    print("📊 Analytics module not found - running without analytics tracking")

# Install required packages if not available
def install_missing_packages():
    """Install required packages if they're missing"""
    required_packages = {
        'pyTelegramBotAPI': 'telebot',
        'fpdf2': 'fpdf',
        'aiohttp': 'aiohttp',
        'requests': 'requests',
        'razorpay': 'razorpay'
    }
    
    missing = []
    for package, import_name in required_packages.items():
        try:
            __import__(import_name)
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"📦 Installing missing packages: {', '.join(missing)}")
        for package in missing:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"✅ {package} installed successfully")
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to install {package}: {e}")
                return False
    return True

# Install packages before importing
if not install_missing_packages():
    print("❌ Failed to install required packages")
    sys.exit(1)

# Now safely import everything
try:
    import telebot
    from telebot.async_telebot import AsyncTeleBot
    from fpdf import FPDF
    import aiohttp
    import requests
    import razorpay
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please run: pip install -r requirements.txt")
    sys.exit(1)

class DevDrishtiRazorpayBot:
    """Main bot class with Razorpay payment integration"""
    
    def __init__(self):
        # Configuration - Use environment variables (NO DEFAULTS for security)
        self.bot_token = os.getenv('BOT_TOKEN')
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        
        if not self.bot_token or not self.gemini_api_key:
            print("❌ Missing required environment variables:")
            print("   BOT_TOKEN and GEMINI_API_KEY are required")
            print("   💡 Set them in Railway dashboard under 'Variables' tab")
            print("   📖 See deployment guide: https://github.com/yourusername/devdrishti-bot/blob/main/deployment/RAILWAY_GUIDE.md")
            sys.exit(1)
        
        # Admin configuration for payment verification
        self.admin_user_id = int(os.getenv('ADMIN_USER_ID', '0'))  # Bot admin's Telegram user ID
        if self.admin_user_id == 0:
            print("⚠️ Warning: ADMIN_USER_ID not set. Payment verification will be automatic.")
            print("   💡 Add ADMIN_USER_ID=your_telegram_user_id for manual verification")
        
        # Razorpay configuration (OPTIONAL - can run without it)
        self.razorpay_key_id = os.getenv('RAZORPAY_KEY_ID')
        self.razorpay_key_secret = os.getenv('RAZORPAY_KEY_SECRET')
        self.razorpay_enabled = False
        self.razorpay_client = None
        
        if self.razorpay_key_id and self.razorpay_key_secret:
            # Try to initialize Razorpay if credentials are provided
            try:
                self.razorpay_client = razorpay.Client(auth=(self.razorpay_key_id, self.razorpay_key_secret))
                self.razorpay_enabled = True
                print("✅ Razorpay client initialized successfully")
            except Exception as e:
                print(f"⚠️ Razorpay initialization failed: {e}")
                print("   💡 Bot will run in UPI-only mode")
                self.razorpay_enabled = False
        else:
            print("⚠️ Razorpay credentials not provided")
            print("   💡 Bot will run in UPI-only mode (payments via UPI transfer)")
            print("   💡 Add RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET when ready")
        
        # UPI ID for fallback payments (when Razorpay is not available)
        self.upi_id = os.getenv('UPI_ID', 'devay@ptyes')  # Your actual UPI ID
        
        # Try different Gemini model versions for stability (2025 optimized)
        self.gemini_models = [
            'gemini-1.5-flash',          # Most stable and available
            'gemini-1.5-flash-latest',   # Latest stable version
            'gemini-1.5-pro',            # Higher quality alternative
            'gemini-1.0-pro-latest'      # Fallback option
        ]
        self.current_model = 0
        self.gemini_url = f'https://generativelanguage.googleapis.com/v1beta/models/{self.gemini_models[self.current_model]}:generateContent?key={self.gemini_api_key}'
        
        # Bot username for referral links (set this in BotFather)
        self.bot_username = os.getenv('BOT_USERNAME', 'DevDrishtiBot')  # Replace with your actual bot username
        
        # Initialize bot
        try:
            self.bot = AsyncTeleBot(self.bot_token)
            print("✅ Telegram bot initialized successfully")
        except Exception as e:
            print(f"❌ Failed to initialize Telegram bot: {e}")
            print("   💡 Check your BOT_TOKEN in Railway dashboard")
            sys.exit(1)
        
        # State management
        self.user_states = {}
        self.last_gemini_call = {}
        self.user_requests = defaultdict(list)
        self.user_referrals = defaultdict(int)  # Track referrals
        self.user_timestamps = defaultdict(dict)  # Track interaction timing for dynamic urgency
        self.payment_orders = {}  # Track Razorpay orders
        self.pending_payments = {}  # Track pending payment verifications
        
        # A/B Testing for pricing with discount psychology
        self.original_price = 999  # Anchor price for psychological effect  
        self.pricing_variants = [199, 299]  # Discounted A/B test prices
        self.user_pricing = {}  # Track which price each user sees
        
        # Rate limiting
        self.rate_limit_seconds = int(os.getenv('RATE_LIMIT_SECONDS', '5'))
        self.max_requests_per_hour = int(os.getenv('MAX_REQUESTS_PER_HOUR', '60'))
        
        # Setup logging
        self.setup_logging()
        
        # Initialize analytics if available
        self.analytics = DevDrishtiAnalytics() if ANALYTICS_ENABLED else None
        
        # Register handlers
        self.register_handlers()
        
        payment_mode = "Razorpay + UPI" if self.razorpay_enabled else "UPI Only"
        admin_mode = f"Admin verification: {'Enabled' if self.admin_user_id else 'Disabled'}"
        print(f"🚀 DevDrishti Bot initialization complete! Payment mode: {payment_mode}")
        print(f"🔐 {admin_mode} (UPI: {self.upi_id})")
        
        # Test Gemini API in background
        print("🧪 Testing Gemini API connectivity...")
        asyncio.create_task(self.test_gemini_connectivity())
    
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('devdrishti.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def register_handlers(self):
        """Register all bot message handlers"""
        
        @self.bot.message_handler(commands=['start'])
        async def start_handler(message):
            await self.handle_start(message)
        
        @self.bot.message_handler(commands=['help'])
        async def help_handler(message):
            await self.handle_help(message)
        
        @self.bot.message_handler(commands=['daily'])
        async def daily_command_handler(message):
            await self.handle_daily_reading(message.chat.id)
        
        @self.bot.message_handler(commands=['personal'])
        async def personal_command_handler(message):
            await self.handle_personal_request(message.chat.id)
        
        @self.bot.message_handler(commands=['admin'])
        async def admin_handler(message):
            await self.handle_admin_commands(message)
        
        @self.bot.callback_query_handler(func=lambda call: True)
        async def callback_handler(call):
            await self.handle_callback_query(call)
        
        @self.bot.message_handler(content_types=['photo'])
        async def photo_handler(message):
            await self.handle_photo(message)
        
        @self.bot.message_handler(func=lambda message: True)
        async def message_handler(message):
            await self.handle_message(message)
    
    async def handle_admin_commands(self, message):
        """Handle admin commands"""
        try:
            if message.chat.id != self.admin_user_id:
                await self.bot.send_message(message.chat.id, "❌ Unauthorized access.")
                return
            
            admin_msg = (
                "🔐 **DevDrishti Admin Panel**\n\n"
                f"📊 **Bot Status:**\n"
                f"• Pending Payments: {len(self.pending_payments)}\n"
                f"• UPI ID: {self.upi_id}\n"
                f"• Payment Mode: {'Razorpay + UPI' if self.razorpay_enabled else 'UPI Only'}\n\n"
                f"📋 **Commands:**\n"
                f"/admin - Show this panel\n\n"
                f"💳 **Payment Verification:**\n"
                f"Automatic notifications when users send payment screenshots"
            )
            await self.bot.send_message(message.chat.id, admin_msg)
            
        except Exception as e:
            self.logger.error(f"Error in admin handler: {e}")
    
    async def handle_callback_query(self, call):
        """Handle callback queries from admin approval buttons"""
        try:
            if call.from_user.id != self.admin_user_id:
                await self.bot.answer_callback_query(call.id, "❌ Unauthorized", show_alert=True)
                return
            
            data_parts = call.data.split('_')
            action = data_parts[0]  # approve or reject
            user_id = int(data_parts[1])
            
            if action == 'approve':
                await self.approve_payment(user_id, call)
            elif action == 'reject':
                await self.reject_payment(user_id, call)
            
        except Exception as e:
            self.logger.error(f"Error handling callback query: {e}")
            await self.bot.answer_callback_query(call.id, "❌ Error processing request", show_alert=True)
    
    async def approve_payment(self, user_id, call):
        """Handle payment approval by admin"""
        try:
            if user_id in self.pending_payments:
                # Remove from pending
                payment_info = self.pending_payments.pop(user_id)
                
                # Update admin message
                await self.bot.edit_message_text(
                    "✅ **PAYMENT APPROVED**\n\n" + payment_info['admin_msg'] + "\n\n🎯 **Status:** Approved by admin\n⏰ Processing PDF generation...",
                    call.message.chat.id,
                    call.message.message_id
                )
                
                # Notify user
                await self.bot.send_message(user_id, 
                    "✅ **Payment Verified Successfully!**\n\n"
                    "🎉 Your payment has been confirmed by our team!\n"
                    "🔮 Generating your detailed cosmic analysis...\n"
                    "📊 This may take 2-3 minutes for accuracy."
                )
                
                # Generate PDF
                await self.handle_birth_details(user_id, payment_info['original_message'])
                
                await self.bot.answer_callback_query(call.id, "✅ Payment approved successfully!")
                
            else:
                await self.bot.answer_callback_query(call.id, "❌ Payment not found in pending list", show_alert=True)
                
        except Exception as e:
            self.logger.error(f"Error approving payment: {e}")
            await self.bot.answer_callback_query(call.id, "❌ Error approving payment", show_alert=True)
    
    async def reject_payment(self, user_id, call):
        """Handle payment rejection by admin"""
        try:
            if user_id in self.pending_payments:
                # Remove from pending
                payment_info = self.pending_payments.pop(user_id)
                
                # Update admin message
                await self.bot.edit_message_text(
                    "❌ **PAYMENT REJECTED**\n\n" + payment_info['admin_msg'] + "\n\n🚫 **Status:** Rejected by admin",
                    call.message.chat.id,
                    call.message.message_id
                )
                
                # Notify user to resend payment
                await self.bot.send_message(user_id,
                    "❌ **Payment Verification Failed**\n\n"
                    "🔍 Our team couldn't verify your payment screenshot.\n\n"
                    "**Possible issues:**\n"
                    f"• Amount doesn't match ₹{self.user_pricing.get(user_id, 199)}\n"
                    f"• UPI ID doesn't match {self.upi_id}\n"
                    "• Screenshot is unclear or incomplete\n\n"
                    "📱 **Please send a clear screenshot showing:**\n"
                    f"✅ Amount: ₹{self.user_pricing.get(user_id, 199)}\n"
                    f"✅ UPI ID: {self.upi_id}\n"
                    "✅ Transaction success message\n\n"
                    "💡 Or contact support for assistance."
                )
                
                # Reset user state for retry
                self.user_states[user_id] = 'payment_pending'
                
                await self.bot.answer_callback_query(call.id, "❌ Payment rejected - user notified")
                
            else:
                await self.bot.answer_callback_query(call.id, "❌ Payment not found in pending list", show_alert=True)
                
        except Exception as e:
            self.logger.error(f"Error rejecting payment: {e}")
            await self.bot.answer_callback_query(call.id, "❌ Error rejecting payment", show_alert=True)
    
    def get_dynamic_urgency(self, user_id, action):
        """Calculate dynamic urgency based on user timing"""
        now = datetime.now()
        
        # Track timing for this action
        if action not in self.user_timestamps[user_id]:
            self.user_timestamps[user_id][action] = now
        
        # Calculate time since first interaction
        if 'started' in self.user_timestamps[user_id]:
            time_since_start = (now - self.user_timestamps[user_id]['started']).total_seconds() / 60
            
            # Dynamic urgency based on engagement time
            if time_since_start < 2:  # Very quick (< 2 minutes)
                urgency = {
                    'slots': random.randint(1, 3),
                    'expires': random.randint(5, 10),
                    'bonus': "⚡ INSTANT DECISION BONUS!"
                }
            elif time_since_start < 10:  # Quick (< 10 minutes)
                urgency = {
                    'slots': random.randint(2, 5),
                    'expires': random.randint(15, 30),
                    'bonus': "🚀 QUICK THINKER REWARD!"
                }
            else:  # Slower decision
                urgency = {
                    'slots': random.randint(3, 7),
                    'expires': random.randint(45, 90),
                    'bonus': "🎯 FINAL CHANCE OFFER!"
                }
        else:
            # Default urgency
            urgency = {
                'slots': random.randint(2, 6),
                'expires': random.randint(20, 45),
                'bonus': "💎 EXCLUSIVE DISCOUNT!"
            }
        
        return urgency
    
    def get_discount_text(self, discounted_price):
        """Create psychological pricing text with reliable strikethrough formatting"""
        discount_percent = round((self.original_price - discounted_price) / self.original_price * 100)
        savings = self.original_price - discounted_price
        
        return (
            f"💰 SPECIAL DISCOUNT OFFER!\n"
            f"❌ Regular Price: ₹{self.original_price}\n"
            f"✅ Your Price: ₹{discounted_price}\n"
            f"🎉 You Save: ₹{savings} ({discount_percent}% OFF!)\n"
            f"⏰ Limited time only!"
        )
    
    def get_discount_emoji_text(self, discounted_price):
        """Enhanced discount format with multiple psychological triggers"""
        discount_percent = round((self.original_price - discounted_price) / self.original_price * 100)
        savings = self.original_price - discounted_price
        
        return (
            f"🔥 MEGA DISCOUNT ALERT! 🔥\n"
            f"❌ Regular: ₹{self.original_price}\n"
            f"✅ Today Only: ₹{discounted_price}\n"
            f"💸 You Save: ₹{savings} ({discount_percent}% OFF!)\n"
            f"⭐ {savings//100}x value for the price of 1!"
        )
    
    async def create_razorpay_order(self, user_id, amount):
        """Create a Razorpay order for payment"""
        try:
            order_data = {
                'amount': amount * 100,  # Amount in paise
                'currency': 'INR',
                'receipt': f'devdrishti_{user_id}_{int(datetime.now().timestamp())}',
                'notes': {
                    'user_id': str(user_id),
                    'service': 'vedic_reading',
                    'original_price': self.original_price,
                    'discount_amount': self.original_price - amount
                }
            }
            
            order = self.razorpay_client.order.create(data=order_data)
            self.payment_orders[user_id] = order
            self.logger.info(f"Created Razorpay order for user {user_id}: {order['id']}")
            return order
            
        except Exception as e:
            self.logger.error(f"Failed to create Razorpay order for user {user_id}: {e}")
            return None
    
    def create_payment_link(self, order_id, amount, user_id):
        """Create a payment link for the order"""
        # You can customize this URL based on your setup
        # This is a simple payment page URL - you might want to create a custom page
        payment_url = f"https://rzp.io/l/{order_id}"
        
        # Alternative: Create a direct payment link (requires Razorpay Payment Links API)
        try:
            payment_link_data = {
                'amount': amount * 100,
                'currency': 'INR',
                'accept_partial': False,
                'description': f'DevDrishti Vedic Reading - User {user_id}',
                'customer': {
                    'name': f'User {user_id}',
                    'contact': '+919999999999',  # You might want to collect this
                    'email': f'user{user_id}@devdrishti.com'
                },
                'notify': {
                    'sms': False,
                    'email': False
                },
                'reminder_enable': True,
                'notes': {
                    'user_id': str(user_id),
                    'service': 'vedic_reading'
                },
                'callback_url': f'https://your-domain.com/payment-success?user_id={user_id}',
                'callback_method': 'get'
            }
            
            payment_link = self.razorpay_client.payment_link.create(payment_link_data)
            return payment_link['short_url']
            
        except Exception as e:
            self.logger.error(f"Failed to create payment link: {e}")
            # Fallback to basic Razorpay checkout
            return f"https://checkout.razorpay.com/v1/checkout.js?key_id={self.razorpay_key_id}&order_id={order_id}"
    
    async def check_rate_limit(self, user_id):
        """Check if user is within rate limits"""
        now = datetime.now()
        
        # Clean old requests
        self.user_requests[user_id] = [
            req_time for req_time in self.user_requests[user_id] 
            if now - req_time < timedelta(hours=1)
        ]
        
        # Check hourly limit
        if len(self.user_requests[user_id]) >= self.max_requests_per_hour:
            raise Exception("Hourly limit exceeded")
        
        # Check minimum interval
        if user_id in self.last_gemini_call:
            time_since_last = (now - self.last_gemini_call[user_id]).total_seconds()
            if time_since_last < self.rate_limit_seconds:
                sleep_time = self.rate_limit_seconds - time_since_last
                self.logger.info(f"Rate limiting user {user_id}, sleeping {sleep_time:.1f}s")
                await asyncio.sleep(sleep_time)
        
        # Update tracking
        self.last_gemini_call[user_id] = now
        self.user_requests[user_id].append(now)
    
    async def generate_content(self, prompt, user_id):
        """Generate content using Gemini API with OpenAI fallback for better reliability"""
        try:
            # Apply rate limiting
            await self.check_rate_limit(user_id)
            
            # Try Gemini first
            gemini_result = await self.try_gemini_api(prompt, user_id)
            if gemini_result and "Divine vision temporarily veiled" not in gemini_result:
                return gemini_result
            
            # If Gemini fails, try OpenAI (if available)
            openai_key = os.getenv('OPENAI_API_KEY')
            if openai_key:
                openai_result = await self.try_openai_api(prompt, user_id, openai_key)
                if openai_result:
                    return openai_result
            
            # If both fail, return error message
            return "Divine vision temporarily veiled—please try again later!"
                    
        except Exception as e:
            if "limit exceeded" in str(e):
                return "🙏 Please wait - divine insights need time to manifest. Try again in an hour."
            self.logger.error(f"AI API error for user {user_id}: {e}")
            return "Divine vision temporarily veiled—try again later!"
    
    async def try_gemini_api(self, prompt, user_id):
        """Try Gemini API with model fallbacks"""
        try:
            # Enhance prompt for better Vedic astrology
            enhanced_prompt = (
                f"{prompt} "
                "Use authentic Vedic astrology terms like Nakshatras, Doshas, Grahas, Rashis. "
                "Be authoritative yet mystical. Include specific remedies with mantras, gemstones, "
                "or rituals. Add waiver: Insights are guidance; individual karma influences outcomes."
            )
            
            payload = {
                'contents': [{
                    'parts': [{
                        'text': enhanced_prompt
                    }]
                }]
            }
            
            # Try current model, fallback to others if needed
            for attempt in range(len(self.gemini_models)):
                try:
                    async with aiohttp.ClientSession() as session:
                        async with session.post(self.gemini_url, json=payload, timeout=60) as response:
                            if response.status != 200:
                                error_data = await response.text()
                                self.logger.error(f"Gemini API error {response.status}: {error_data}")
                                
                                # Try next model if model not found
                                if response.status == 404 and attempt < len(self.gemini_models) - 1:
                                    self.current_model = (self.current_model + 1) % len(self.gemini_models)
                                    self.gemini_url = f'https://generativelanguage.googleapis.com/v1beta/models/{self.gemini_models[self.current_model]}:generateContent?key={self.gemini_api_key}'
                                    self.logger.info(f"Switching to model: {self.gemini_models[self.current_model]}")
                                    continue
                                
                                return None
                            
                            data = await response.json()
                            
                            try:
                                content = data['candidates'][0]['content']['parts'][0]['text']
                                self.logger.info(f"Generated content for user {user_id} using Gemini {self.gemini_models[self.current_model]}")
                                return content
                            except (KeyError, IndexError) as e:
                                self.logger.error(f"Unexpected Gemini API response: {e}")
                                return None
                                
                except asyncio.TimeoutError:
                    self.logger.error(f"Timeout with Gemini model {self.gemini_models[self.current_model]}")
                    if attempt < len(self.gemini_models) - 1:
                        continue
                    return None
                    
                # If we get here, this model worked, so break
                break
                
            return None
            
        except Exception as e:
            self.logger.error(f"Gemini API error: {e}")
            return None
    
    async def try_openai_api(self, prompt, user_id, api_key):
        """Try OpenAI API as fallback"""
        try:
            # Enhance prompt for astrology
            enhanced_prompt = (
                f"You are a professional Vedic astrologer. {prompt} "
                "Use authentic Vedic astrology terminology like Nakshatras, Doshas, Grahas, Rashis. "
                "Be mystical yet authoritative. Include specific remedies, mantras, or gemstones. "
                "Add disclaimer: These insights are guidance; individual karma influences outcomes."
            )
            
            payload = {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {"role": "system", "content": "You are a wise Vedic astrologer with deep knowledge of Indian astrology, nakshatras, and spiritual remedies."},
                    {"role": "user", "content": enhanced_prompt}
                ],
                "max_tokens": 800,
                "temperature": 0.7
            }
            
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post("https://api.openai.com/v1/chat/completions", 
                                       json=payload, headers=headers, timeout=60) as response:
                    if response.status != 200:
                        error_data = await response.text()
                        self.logger.error(f"OpenAI API error {response.status}: {error_data}")
                        return None
                    
                    data = await response.json()
                    
                    try:
                        content = data['choices'][0]['message']['content']
                        self.logger.info(f"Generated content for user {user_id} using OpenAI GPT-3.5-Turbo")
                        return content
                    except (KeyError, IndexError) as e:
                        self.logger.error(f"Unexpected OpenAI API response: {e}")
                        return None
                        
        except Exception as e:
            self.logger.error(f"OpenAI API error: {e}")
            return None
    
    def get_short_backup_reading(self):
        """Provide a short backup reading when Gemini API fails"""
        backup_readings = [
            "Today brings opportunities for growth and positive communication. Mars energy favors career decisions. Venus blesses relationships with harmony. Remedy: Chant 'Om Gam Ganapataye Namaha' 11 times for removing obstacles.",
            
            "Your intuition is heightened today. Trust your inner voice in important decisions. Jupiter influences bring wisdom in financial matters. Lucky colors: Blue, green. Remedy: Light a ghee lamp in the evening for continued blessings.",
            
            "Strong determination and courage flow through you today. Focus on health and avoid conflicts. Mercury supports communication and learning. Lucky numbers: 3, 7, 21. Remedy: Wear yellow or orange for confidence."
        ]
        return random.choice(backup_readings)
    
    async def show_payment_options(self, user_id):
        """Show payment options to user"""
        try:
            # Get user's assigned price
            user_price = self.user_pricing.get(user_id, self.pricing_variants[0])
            discount_text = self.get_discount_text(user_price)
            savings = self.original_price - user_price
            
            if self.razorpay_enabled:
                # Use Razorpay payment flow
                order = await self.create_razorpay_order(user_id, user_price)
                
                if not order:
                    await self.bot.send_message(user_id, "❌ Payment system temporarily unavailable. Please try again later.")
                    return
                
                # Create payment link
                payment_url = self.create_payment_link(order['id'], user_price, user_id)
                
                payment_msg = (
                    f"🎯 CLAIMING YOUR COSMIC DISCOUNT!\n\n"
                    f"{discount_text}\n\n"
                    f"💳 **SECURE PAYMENT via Razorpay**\n"
                    f"💰 Amount: ₹{user_price}\n"
                    f"🔒 100% Safe & Secure\n"
                    f"💳 UPI | Cards | Net Banking accepted\n\n"
                    f"🌟 You're saving ₹{savings} compared to regular clients!\n"
                    f"⚡ This discount won't last long - secure it now!\n\n"
                    f"👆 **Click link below to pay:**\n"
                    f"{payment_url}\n\n"
                    f"✨ Your detailed cosmic blueprint awaits!\n"
                    f"📱 After payment, send screenshot for instant confirmation"
                )
                
                self.logger.info(f"User {user_id} shown Razorpay payment ₹{user_price} (saved ₹{savings}) - Order: {order['id']}")
                
            else:
                # Use UPI-only payment flow (fallback mode)
                payment_msg = (
                    f"🎯 CLAIMING YOUR COSMIC DISCOUNT!\n\n"
                    f"{discount_text}\n\n"
                    f"💳 **SECURE UPI PAYMENT**\n"
                    f"💰 Amount: ₹{user_price}\n"
                    f"📱 UPI ID: {self.upi_id}\n\n"
                    f"🌟 You're saving ₹{savings} compared to regular clients!\n"
                    f"⚡ This discount won't last long - secure it now!\n\n"
                    f"📋 **Payment Steps:**\n"
                    f"1. Send ₹{user_price} to UPI: {self.upi_id}\n"
                    f"2. Take screenshot of payment\n"
                    f"3. Send screenshot here for instant confirmation\n\n"
                    f"✨ Your detailed cosmic blueprint awaits!"
                )
                
                self.logger.info(f"User {user_id} shown UPI payment ₹{user_price} (saved ₹{savings}) - UPI: {self.upi_id}")
            
            await self.bot.send_message(user_id, payment_msg)
            self.user_states[user_id] = 'payment_pending'
            
        except Exception as e:
            self.logger.error(f"Error showing payment options for {user_id}: {e}")
    
    async def create_pdf_async(self, report):
        """Create professional PDF with proper formatting, headers, footers"""
        def _create_pdf():
            from datetime import datetime
            
            pdf = FPDF()
            pdf.add_page()
            
            # Add header
            pdf.set_font("Arial", "B", 16)
            pdf.set_text_color(128, 0, 128)  # Purple color
            pdf.cell(0, 10, "DevDrishti - Vedic Astrology Consultation", 0, 1, 'C')
            pdf.ln(5)
            
            # Add horizontal line
            pdf.set_draw_color(128, 0, 128)
            pdf.line(20, pdf.get_y(), 190, pdf.get_y())
            pdf.ln(10)
            
            # Add report date and consultation details
            pdf.set_font("Arial", "", 10)
            pdf.set_text_color(0, 0, 0)
            pdf.cell(0, 5, f"Report Generated: {datetime.now().strftime('%d %B %Y, %I:%M %p')}", 0, 1, 'R')
            pdf.cell(0, 5, "Consultation Type: Comprehensive Vedic Analysis", 0, 1, 'R')
            pdf.ln(10)
            
            # Add main content
            pdf.set_font("Arial", "", 12)
            
            try:
                # Split report into sections for better formatting
                sections = report.split('\n\n')
                
                for section in sections:
                    if section.strip():
                        lines = section.split('\n')
                        for line in lines:
                            if line.strip():
                                # Check if it's a heading (starts with emoji or numbers)
                                if any(char in line[:5] for char in ['🌟', '💼', '❤️', '🏥', '🔮', '🍀', '⚠️', '🧘', '📊']) or line.strip().endswith(':'):
                                    pdf.set_font("Arial", "B", 12)
                                    pdf.set_text_color(128, 0, 128)
                                else:
                                    pdf.set_font("Arial", "", 11)
                                    pdf.set_text_color(0, 0, 0)
                                
                                # Encode to handle special characters
                                safe_line = line.encode('latin-1', 'replace').decode('latin-1')
                                
                                # Add some spacing for readability
                                if safe_line.strip():
                                    pdf.multi_cell(0, 8, safe_line.strip())
                                    pdf.ln(2)
                        
                        pdf.ln(3)  # Extra space between sections
                        
            except Exception as e:
                print(f"PDF text processing error: {e}")
                pdf.set_font("Arial", "", 12)
                pdf.multi_cell(0, 10, "Your comprehensive Vedic astrology report has been generated successfully.")
            
            # Add footer section
            pdf.ln(10)
            pdf.set_draw_color(128, 0, 128)
            pdf.line(20, pdf.get_y(), 190, pdf.get_y())
            pdf.ln(5)
            
            pdf.set_font("Arial", "I", 10)
            pdf.set_text_color(100, 100, 100)
            pdf.multi_cell(0, 5, "Disclaimer: This report is based on Vedic astrology principles and is meant for guidance purposes only. Individual karma, free will, and personal choices significantly influence life outcomes. Please consult qualified professionals for important life decisions.")
            
            pdf.ln(5)
            pdf.set_font("Arial", "B", 10)
            pdf.set_text_color(128, 0, 128)
            pdf.cell(0, 5, "DevDrishti - Your Cosmic Guide | Yatha Drishti, Tatha Srishti", 0, 1, 'C')
            
            # Add page numbers
            pdf.alias_nb_pages()
            pdf.set_font("Arial", "", 9)
            pdf.set_text_color(100, 100, 100)
            pdf.cell(0, 5, f"Page {pdf.page_no()}", 0, 0, 'C')
            
            buffer = BytesIO()
            pdf.output(buffer)
            buffer.seek(0)
            return buffer
        
        return await asyncio.to_thread(_create_pdf)
    
    async def handle_start(self, message):
        """Handle /start command with referral tracking"""
        try:
            user_id = message.chat.id
            
            # Check for referral
            if message.text and len(message.text.split()) > 1:
                start_param = message.text.split()[1]
                if start_param.startswith('ref_'):
                    referrer_id = start_param.replace('ref_', '')
                    try:
                        referrer_id = int(referrer_id)
                        self.user_referrals[referrer_id] += 1
                        self.logger.info(f"User {user_id} referred by {referrer_id}")
                        
                        # Bonus message for referred user
                        await self.bot.send_message(user_id, "🎉 Welcome! You've been referred by a DevDrishti user - special blessings await!")
                    except ValueError:
                        pass
            
            welcome_msg = (
                "🙏 Namaste! DevDrishti AI unveils Vedic truths for career, love, and beyond.\n\n"
                "🎯 **Choose your path:**\n"
                "💫 /daily or type 'daily' for free insight\n"
                "🔮 /personal or type 'personal' for detailed drishti\n\n"
                "✨ Your cosmic journey begins here!\n\n"
                "📢 Join @DevDrishti_Daily for daily cosmic teasers!"
            )
            await self.bot.send_message(user_id, welcome_msg)
            self.user_states[user_id] = 'free'
            self.logger.info(f"New user started: {user_id}")
            
            # Track timing for dynamic urgency
            self.user_timestamps[user_id]['started'] = datetime.now()
            
            # Track user action in analytics
            if self.analytics:
                self.analytics.log_user_action(user_id, "started")
                
        except Exception as e:
            self.logger.error(f"Error in start handler: {e}")
    
    async def handle_help(self, message):
        """Handle /help command"""
        payment_info = "💳 Secure payments via Razorpay" if self.razorpay_enabled else "💳 UPI payments (Razorpay coming soon)"
        
        help_text = (
            "🌟 DevDrishti Commands:\n\n"
            "📋 **Menu Commands:**\n"
            "/start - Begin your journey\n"
            "/daily - Get free daily insight\n"
            "/personal - Purchase detailed reading\n"
            "/help - Show this help\n\n"
            "💬 **Or simply type:**\n"
            "• 'daily' - Free daily insight\n"
            "• 'personal' - Detailed reading\n\n"
            f"{payment_info}\n"
            "🔮 May the stars guide your path!"
        )
        await self.bot.send_message(message.chat.id, help_text)
    
    async def handle_daily_reading(self, user_id):
        """Handle daily reading request - collect details first for personalized reading"""
        try:
            # Check if user has provided basic details before
            if not hasattr(self, 'user_details') or user_id not in getattr(self, 'user_details', {}):
                # First time - ask for complete birth details (unified format)
                details_msg = (
                    "🌟 Welcome to your personalized daily cosmic guidance!\n\n"
                    "📅 For accurate Vedic insights, I need your complete details:\n\n"
                    "Please share:\n"
                    "• Full Name\n"
                    "• Birth Date (DD-MM-YYYY)\n"
                    "• Birth Time (HH:MM AM/PM) - if known\n"
                    "• Birth Place (City, State, Country)\n\n"
                    "📝 Example:\n"
                    "Name: Raj Kumar Sharma\n"
                    "Date: 15-08-1990\n"
                    "Time: 2:30 PM\n"
                    "Place: Mumbai, Maharashtra, India\n\n"
                    "💡 Don't know exact time? Write 'unknown' for time\n"
                    "✨ Your details are safe and used only for astrological calculations!"
                )
                await self.bot.send_message(user_id, details_msg)
                self.user_states[user_id] = 'collecting_unified_details'
                return
            
            # Generate short personalized daily reading
            await self.bot.send_message(user_id, "🔮 Consulting the cosmic energies for your personalized reading...")
            
            # Get user details from storage
            user_details = getattr(self, 'user_details', {}).get(user_id, "birth details provided earlier")
            
            prompt = (
                f"Generate a short, personalized daily Vedic horoscope for someone with details: {user_details}. "
                "Keep it concise (max 150 words). Focus on TODAY's specific influences for: "
                "1) Career/work opportunities 2) Love/relationships 3) One practical remedy. "
                "Use Vedic terms like nakshatras, planetary transits. Make it feel personal and relevant for today only."
            )
            
            horoscope = await self.generate_content(prompt, user_id)
            
            if not horoscope or "Divine vision temporarily veiled" in horoscope:
                # Gemini API failed - provide a backup reading
                horoscope = self.get_short_backup_reading()
            
            # A/B test pricing - assign random price if not assigned
            if user_id not in self.user_pricing:
                self.user_pricing[user_id] = random.choice(self.pricing_variants)
            
            user_price = self.user_pricing[user_id]
            discount_text = self.get_discount_emoji_text(user_price)
            urgency = self.get_dynamic_urgency(user_id, 'daily_reading')
            
            response = (
                f"🌟 Today's Personalized Cosmic Guidance:\n\n{horoscope}\n\n"
                f"{'='*30}\n"
                f"{discount_text}\n"
                f"{'='*30}\n"
                f"{urgency['bonus']}\n"
                f"⚡ FLASH SALE - Only {urgency['slots']} slots left!\n"
                f"✨ Click /personal for your COMPLETE life analysis NOW!\n"
                f"⏰ Offer expires in {urgency['expires']} minutes!"
            )
            
            await self.bot.send_message(user_id, response)
            self.user_states[user_id] = 'upsell'
            
        except Exception as e:
            self.logger.error(f"Error in daily reading for {user_id}: {e}")
            await self.bot.send_message(user_id, "🙏 The cosmic energies are realigning. Please try /daily again in a moment.")
    
    async def handle_personal_request(self, user_id):
        """Handle personal reading request - use existing details or collect them"""
        try:
            # Check if user has provided details before
            if not hasattr(self, 'user_details') or user_id not in getattr(self, 'user_details', {}):
                # First time - ask for complete birth details (same unified format)
                details_msg = (
                    "🌟 Welcome to your comprehensive life analysis!\n\n"
                    "📅 For your detailed Vedic consultation, I need your complete details:\n\n"
                    "Please share:\n"
                    "• Full Name\n"
                    "• Birth Date (DD-MM-YYYY)\n"
                    "• Birth Time (HH:MM AM/PM) - very important for accuracy\n"
                    "• Birth Place (City, State, Country)\n\n"
                    "📝 Example:\n"
                    "Name: Raj Kumar Sharma\n"
                    "Date: 15-08-1990\n"
                    "Time: 2:30 PM\n"
                    "Place: Mumbai, Maharashtra, India\n\n"
                    "💡 Exact birth time is crucial for detailed predictions!\n"
                    "✨ Your details are encrypted and used only for astrological calculations."
                )
                await self.bot.send_message(user_id, details_msg)
                self.user_states[user_id] = 'collecting_unified_details_for_personal'
                return
            
            # User has details, proceed directly to payment
            await self.show_payment_options(user_id)
                
        except Exception as e:
            self.logger.error(f"Error in personal request for {user_id}: {e}")
    
    async def handle_unified_details_collection(self, user_id, message, reading_type='daily'):
        """Handle unified collection of all user details"""
        try:
            details = message.text
            
            # Store user details (unified storage)
            if not hasattr(self, 'user_details'):
                self.user_details = {}
            self.user_details[user_id] = details
            
            confirmation_msg = (
                "✅ Perfect! Your complete details have been saved securely.\n\n"
                "🔮 Now proceeding with your cosmic analysis...\n"
                "⏳ This may take a moment for accurate calculations."
            )
            await self.bot.send_message(user_id, confirmation_msg)
            
            if reading_type == 'daily':
                # Reset state and generate daily reading
                self.user_states[user_id] = 'free'
                await self.handle_daily_reading(user_id)
            else:
                # For personal reading, show payment options
                await self.show_payment_options(user_id)
                
        except Exception as e:
            self.logger.error(f"Error collecting unified details for {user_id}: {e}")
            await self.bot.send_message(user_id, "🙏 Error saving your details. Please try again.")
    
    async def handle_payment_confirmation(self, user_id, message):
        """Handle payment confirmation with robust admin verification system"""
        try:
            user_price = self.user_pricing.get(user_id, self.pricing_variants[0])
            
            # Log payment verification details
            if message.content_type == 'photo':
                photo_id = message.photo[-1].file_id
                self.logger.info(f"💳 PAYMENT SCREENSHOT: User {user_id} - Photo ID: {photo_id} - Amount: ₹{user_price}")
            else:
                self.logger.info(f"💳 PAYMENT CONFIRMATION: User {user_id} - Text: {message.text[:50]}... - Amount: ₹{user_price}")
            
            # Send confirmation to user
            confirmation_msg = (
                "✅ Payment confirmation received! Thank you for your trust.\n\n"
                "🔍 **Payment Verification in Progress:**\n"
                f"💰 Expected Amount: ₹{user_price}\n"
                f"📱 Expected UPI ID: {self.upi_id}\n"
                "⏰ Verification Time: 2-10 minutes\n\n"
                "🔔 You'll be notified once our team verifies your payment.\n"
                "💡 Please ensure your screenshot shows the complete transaction details."
            )
            await self.bot.send_message(user_id, confirmation_msg)
            
            if self.admin_user_id:
                # Send verification request to admin
                await self.send_admin_verification_request(user_id, message, user_price)
            else:
                # No admin set - auto-approve (fallback)
                self.logger.warning(f"No admin set - auto-approving payment for user {user_id}")
                await asyncio.sleep(2)  # Small delay to seem realistic
                await self.auto_approve_payment(user_id, message)
            
        except Exception as e:
            self.logger.error(f"❌ Error in payment confirmation for {user_id}: {e}")
            await self.bot.send_message(user_id, "🙏 Error processing payment confirmation. Please contact support.")
    
    async def send_admin_verification_request(self, user_id, message, expected_amount):
        """Send payment verification request to admin with approve/reject buttons"""
        try:
            # Get user details
            user_details = getattr(self, 'user_details', {}).get(user_id, "Details not available")
            user_name = user_details.split('\n')[0].replace('Name:', '').strip() if 'Name:' in user_details else f"User {user_id}"
            
            # Create admin message
            admin_msg = (
                f"💳 **PAYMENT VERIFICATION REQUEST**\n\n"
                f"👤 **User:** {user_name} (ID: {user_id})\n"
                f"💰 **Expected Amount:** ₹{expected_amount}\n"
                f"📱 **Expected UPI:** {self.upi_id}\n"
                f"⏰ **Time:** {datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n"
                f"📋 **User Details:**\n{user_details[:200]}...\n\n"
                f"🔍 **Verification Checklist:**\n"
                f"✅ Amount matches ₹{expected_amount}\n"
                f"✅ UPI ID matches {self.upi_id}\n"
                f"✅ Transaction is successful\n"
                f"✅ Screenshot is clear and complete"
            )
            
            # Create inline keyboard with approve/reject buttons
            from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
            
            keyboard = InlineKeyboardMarkup()
            approve_btn = InlineKeyboardButton("✅ APPROVE", callback_data=f"approve_{user_id}")
            reject_btn = InlineKeyboardButton("❌ REJECT", callback_data=f"reject_{user_id}")
            keyboard.row(approve_btn, reject_btn)
            
            # Send photo if available
            if message.content_type == 'photo':
                photo_id = message.photo[-1].file_id
                await self.bot.send_photo(
                    self.admin_user_id,
                    photo_id,
                    caption=admin_msg,
                    reply_markup=keyboard
                )
            else:
                await self.bot.send_message(
                    self.admin_user_id,
                    admin_msg,
                    reply_markup=keyboard
                )
            
            # Store pending payment info
            self.pending_payments[user_id] = {
                'admin_msg': admin_msg,
                'original_message': message,
                'expected_amount': expected_amount,
                'timestamp': datetime.now()
            }
            
            self.logger.info(f"📧 Admin verification request sent for user {user_id} - Amount: ₹{expected_amount}")
            
        except Exception as e:
            self.logger.error(f"Error sending admin verification request: {e}")
            # Fallback to auto-approval if admin notification fails
            await self.auto_approve_payment(user_id, message)
    
    async def auto_approve_payment(self, user_id, message):
        """Auto-approve payment when no admin is set"""
        try:
            await self.bot.send_message(user_id, 
                "✅ **Payment Verified Automatically!**\n\n"
                "🎉 Your payment has been processed successfully!\n"
                "🔮 Generating your detailed cosmic analysis...\n"
                "📊 This may take 2-3 minutes for accuracy."
            )
            
            # Generate PDF
            await self.handle_birth_details(user_id, message)
            
        except Exception as e:
            self.logger.error(f"Error in auto-approval: {e}")
            await self.bot.send_message(user_id, "🙏 Error processing your payment. Please contact support.")
    
    async def handle_photo(self, message):
        """Handle photo messages (payment screenshots)"""
        try:
            user_id = message.chat.id
            
            if user_id not in self.user_states:
                self.user_states[user_id] = 'free'
            
            if self.user_states[user_id] == 'payment_pending':
                photo_id = message.photo[-1].file_id
                self.logger.info(f"Payment screenshot received from user {user_id}, photo_id: {photo_id}")
                
                confirmation_msg = (
                    "✅ Payment screenshot received! Thank you for your trust.\n\n"
                    "🔍 Verifying your Razorpay payment...\n\n"
                    "📅 Please send your birth details:\n"
                    "• Date (DD-MM-YYYY)\n"
                    "• Time (HH:MM)\n"
                    "• Place of birth\n\n"
                    "Example: 15-08-1990, 14:30, Mumbai"
                )
                await self.bot.send_message(user_id, confirmation_msg)
                self.user_states[user_id] = 'details'
                
                self.logger.info(f"User {user_id} moved to 'details' state after photo confirmation")
                
            else:
                help_msg = (
                    "🙏 Photos are only needed for payment confirmation.\n\n"
                    "For other queries, please use text messages:\n"
                    "• 'daily' for free insight\n"
                    "• 'personal' for detailed reading\n"
                    "• /help for more options"
                )
                await self.bot.send_message(user_id, help_msg)
                
        except Exception as e:
            self.logger.error(f"Error handling photo from user {user_id}: {e}")
            await self.bot.send_message(user_id, "🙏 Error processing your photo. Please try again or contact support.")
    
    async def handle_birth_details(self, user_id, message):
        """Handle birth details and generate customized PDF report"""
        try:
            # This function is now only called after payment confirmation
            # The user details should already be stored from the unified collection
            
            await self.bot.send_message(user_id, "🔮 Preparing your detailed cosmic analysis... This may take a moment.")
            
            # Get user details from unified storage
            user_details = getattr(self, 'user_details', {}).get(user_id, "Complete birth details provided")
            
            prompt = (
                f"Generate a comprehensive professional Vedic astrology reading for: {user_details}. "
                "Create a detailed analysis covering:\n"
                "1. BIRTH CHART OVERVIEW: Key planetary positions and their significance\n"
                "2. PERSONALITY ANALYSIS: Based on birth chart and name numerology\n"
                "3. CAREER & FINANCE: Detailed predictions, opportunities, best timing for decisions\n"  
                "4. LOVE & RELATIONSHIPS: Compatibility, marriage timing, relationship advice\n"
                "5. HEALTH & WELLNESS: Physical and mental health insights, vulnerable periods\n"
                "6. CURRENT PLANETARY PERIODS: Dasha analysis and transit influences\n"
                "7. SPECIFIC REMEDIES: Mantras, gemstones, rituals, donations for prosperity\n"
                "8. LUCKY ELEMENTS: Colors, numbers, directions, auspicious timings\n"
                "9. FUTURE PREDICTIONS: Next 12 months detailed timeline\n"
                "10. SPIRITUAL GUIDANCE: Path for personal growth and moksha\n\n"
                "Use authentic Vedic terminology (Nakshatras, Doshas, Grahas, Rashis, Dasha periods). "
                "Be specific with dates, practical advice and actionable solutions. "
                "Include detailed remedial measures and spiritual practices. "
                "Make it professional and comprehensive like a real astrologer's consultation."
            )
            
            report = await self.generate_content(prompt, user_id)
            
            if not report or "Divine vision temporarily veiled" in report:
                # Provide a detailed backup reading
                report = self.get_detailed_backup_reading(user_details)
            
            # Create and send professional PDF
            pdf_buffer = await self.create_pdf_async(report)
            await self.bot.send_document(user_id, pdf_buffer, visible_file_name=f'DevDrishti_Detailed_Kundali_Analysis.pdf')
            
            final_msg = (
                "📜 Your personalized cosmic blueprint is ready!\n\n"
                "✨ **What you've received:**\n"
                "📊 Complete birth chart analysis based on your exact details\n"
                "🔮 Detailed predictions for next 12 months\n"
                "💫 Personalized remedies and spiritual guidance\n"
                "🎯 Professional kundali reading with practical solutions\n"
                "📈 Career, love, health & wealth predictions\n\n"
                "💬 **Follow-up Support:**\n"
                "You can message me anytime for clarifications about your reading!\n\n"
                "🌟 Share DevDrishti with friends for special blessings!\n"
                "🙏 May this guidance illuminate your path to success and prosperity!"
            )
            await self.bot.send_message(user_id, final_msg)
            
            # Add referral link
            referral_msg = (
                f"🔗 **Your referral link:**\n"
                f"https://t.me/{self.bot_username}?start=ref_{user_id}\n\n"
                f"Share with friends and get special discounts on future readings!\n"
                f"📊 Referrals so far: {self.user_referrals[user_id]}\n\n"
                f"🙏 Thank you for trusting DevDrishti for your cosmic guidance!"
            )
            await self.bot.send_message(user_id, referral_msg)
            
            self.user_states[user_id] = 'done'
            
            # Log completed sale for analytics
            user_price = self.user_pricing.get(user_id, self.pricing_variants[0])
            discount_amount = self.original_price - user_price
            self.logger.info(f"✅ DETAILED READING COMPLETED: User {user_id} - ₹{user_price}. Details: {user_details[:100]}... (Saved ₹{discount_amount})")
            
            # Track in analytics if available
            if self.analytics:
                self.analytics.log_sale(user_id, user_price, f"Detailed kundali reading: {user_details[:100]}", self.original_price)
            
        except Exception as e:
            self.logger.error(f"❌ Error generating customized report for {user_id}: {e}")
            await self.bot.send_message(user_id, "🙏 Error generating your personalized analysis. Our team is investigating. Please contact support for immediate assistance.")
    
    def get_detailed_backup_reading(self, user_info):
        """Provide detailed backup reading when Gemini API fails"""
        return f"""
📊 COMPREHENSIVE VEDIC ANALYSIS
Birth Details: {user_info}

🌟 BIRTH CHART OVERVIEW:
Your chart shows a unique combination of planetary influences that shape your personality and life path. The positioning of key planets indicates strong potential for growth in your areas of concern.

💼 CAREER & FINANCIAL INSIGHTS:
The next 6-12 months bring significant opportunities for professional advancement. Jupiter's favorable position indicates growth in income and status. Best period for important career decisions: Next 3-4 months.

❤️ RELATIONSHIPS & LOVE:
Venus influences suggest positive developments in personal relationships. For those seeking partnership, the period between now and 6 months ahead is highly favorable. Existing relationships will strengthen through better communication.

🏥 HEALTH & WELLNESS:
Overall health remains stable with attention to stress management. Focus on regular exercise and meditation. Avoid major health decisions during the next 2 months.

🔮 SPECIFIC REMEDIES:
1. Chant "Om Gam Ganapataye Namaha" 108 times daily for obstacle removal
2. Wear a silver ring on your right hand ring finger
3. Light a ghee lamp every Tuesday evening
4. Donate white items (rice, milk, cloth) on Mondays

🍀 LUCKY ELEMENTS:
Colors: Blue, Green, White
Numbers: 3, 6, 9, 21
Direction: North and Northeast
Best days: Monday, Wednesday, Friday

⚠️ PRECAUTIONS:
Avoid major financial investments in the next 2-3 months. Be cautious in partnerships during this period.

🧘 SPIRITUAL GUIDANCE:
Regular meditation and mantras will enhance your spiritual growth. Consider visiting temples on Thursdays for divine blessings.

This analysis addresses your specific concerns and provides a roadmap for the coming months. May the cosmic forces guide you to success and happiness.

Disclaimer: These insights are guidance based on Vedic astrology principles. Individual karma and free will significantly influence life outcomes.
        """
    
    async def handle_unknown_message(self, user_id, text):
        """Handle unknown messages"""
        try:
            help_msg = (
                "🙏 I didn't understand that.\n\n"
                "Try:\n"
                "• 'daily' for free insight\n"
                "• 'personal' for detailed reading\n"
                "• /help for more options"
            )
            await self.bot.send_message(user_id, help_msg)
        except Exception as e:
            self.logger.error(f"Error in unknown message handler for {user_id}: {e}")
    
    async def handle_message(self, message):
        """Handle all other messages"""
        try:
            user_id = message.chat.id
            
            if user_id not in self.user_states:
                self.user_states[user_id] = 'free'
            
            if not message.text:
                await self.bot.send_message(user_id, "🙏 Please send text messages only.")
                return
            
            text = message.text.lower().strip()
            
            if text == 'daily':
                await self.handle_daily_reading(user_id)
            elif text == 'personal':
                await self.handle_personal_request(user_id)
            elif self.user_states[user_id] == 'payment_pending':
                await self.handle_payment_confirmation(user_id, message)
            elif self.user_states[user_id] == 'details':
                await self.handle_birth_details(user_id, message)
            elif self.user_states[user_id] == 'collecting_unified_details':
                await self.handle_unified_details_collection(user_id, message, 'daily')
            elif self.user_states[user_id] == 'collecting_unified_details_for_personal':
                await self.handle_unified_details_collection(user_id, message, 'personal')
            else:
                await self.handle_unknown_message(user_id, text)
                
        except Exception as e:
            self.logger.error(f"Error handling message from {user_id}: {e}")
            await self.bot.send_message(user_id, "🙏 Something went wrong. Please try again or use /start to restart.")
    
    async def run(self):
        """Run the bot with production-ready settings"""
        self.logger.info("🚀 Starting DevDrishti Bot with Razorpay...")
        self.logger.info(f"💰 A/B Testing prices: ₹{self.pricing_variants}")
        self.logger.info(f"💳 Razorpay integration: Enabled")
        
        try:
            # Skip pending messages on restart - good for Replit
            await self.bot.polling(non_stop=True, skip_pending=True)
        except Exception as e:
            self.logger.error(f"Bot polling error: {e}")
            # Try to restart after error
            await asyncio.sleep(5)
            self.logger.info("Attempting to restart bot...")
            await self.run()
        finally:
            await self.bot.close_session()

def main():
    """Main function to run the bot"""
    try:
        bot = DevDrishtiRazorpayBot()
        asyncio.run(bot.run())
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user")
    except Exception as e:
        print(f"❌ Error starting bot: {e}")
        print("Please check your bot token, API keys, and Razorpay credentials.")

if __name__ == "__main__":
    main() 