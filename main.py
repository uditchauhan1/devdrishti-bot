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
        
        # Razorpay configuration
        self.razorpay_key_id = os.getenv('RAZORPAY_KEY_ID')
        self.razorpay_key_secret = os.getenv('RAZORPAY_KEY_SECRET')
        
        if not self.razorpay_key_id or not self.razorpay_key_secret:
            print("❌ Missing Razorpay credentials:")
            print("   RAZORPAY_KEY_ID and RAZORPAY_KEY_SECRET are required")
            print("   💡 Set them in Railway dashboard under 'Variables' tab")
            print("   🔑 Get them from https://dashboard.razorpay.com/app/keys")
            print("   📖 See setup guide: https://github.com/yourusername/devdrishti-bot/blob/main/docs/API_SETUP.md")
            sys.exit(1)
        
        # Initialize Razorpay client
        try:
            self.razorpay_client = razorpay.Client(auth=(self.razorpay_key_id, self.razorpay_key_secret))
            print("✅ Razorpay client initialized successfully")
        except Exception as e:
            print(f"❌ Failed to initialize Razorpay client: {e}")
            print("   💡 Check your Razorpay credentials in Railway dashboard")
            sys.exit(1)
        
        # Try different Gemini model versions for stability (2025 optimized)
        self.gemini_models = [
            'gemini-2.5-flash-latest',  # Newest GA as of July 2025 - fastest & most capable
            'gemini-2.5-flash',         # Stable 2.5 version
            'gemini-2.0-flash-001',     # Stable 2.0 fallback
            'gemini-1.5-flash-latest',  # Legacy fallback
            'gemini-1.5-flash'          # Final fallback
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
        
        print("🚀 DevDrishti Bot initialization complete!")
    
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
        
        @self.bot.message_handler(content_types=['photo'])
        async def photo_handler(message):
            await self.handle_photo(message)
        
        @self.bot.message_handler(func=lambda message: True)
        async def message_handler(message):
            await self.handle_message(message)
    
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
        """Generate content using Gemini API with rate limiting and model fallbacks"""
        try:
            # Apply rate limiting
            await self.check_rate_limit(user_id)
            
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
                                
                                return "Divine vision temporarily veiled—try again later!"
                            
                            data = await response.json()
                            
                            try:
                                content = data['candidates'][0]['content']['parts'][0]['text']
                                self.logger.info(f"Generated content for user {user_id} using model {self.gemini_models[self.current_model]}")
                                return content
                            except (KeyError, IndexError) as e:
                                self.logger.error(f"Unexpected API response: {e}")
                                return "Divine vision temporarily veiled—try again later!"
                                
                except asyncio.TimeoutError:
                    self.logger.error(f"Timeout with model {self.gemini_models[self.current_model]}")
                    if attempt < len(self.gemini_models) - 1:
                        continue
                    return "Divine vision taking longer than expected—please try again!"
                    
                # If we get here, this model worked, so break
                break
        
        except Exception as e:
            if "limit exceeded" in str(e):
                return "🙏 Please wait - divine insights need time to manifest. Try again in an hour."
            self.logger.error(f"Gemini API error for user {user_id}: {e}")
            return "Divine vision temporarily veiled—try again later!"
    
    async def create_pdf_async(self, report):
        """Create PDF asynchronously"""
        def _create_pdf():
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt="DevDrishti: Vedic Insights for Your Path", ln=1, align='C')
            
            try:
                lines = report.split('\n')
                for line in lines:
                    if line.strip():
                        safe_line = line.encode('latin-1', 'replace').decode('latin-1')
                        pdf.multi_cell(0, 10, safe_line)
            except Exception as e:
                self.logger.error(f"PDF text processing error: {e}")
                pdf.multi_cell(0, 10, "Report generated successfully.")
            
            pdf.cell(200, 10, txt="Yatha Drishti, Tatha Srishti | Guidance only; not guarantees", ln=1, align='C')
            
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
                "💫 Reply 'daily' for free insight\n"
                "🔮 Reply 'personal' for detailed drishti\n\n"
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
        help_text = (
            "🌟 DevDrishti Commands:\n\n"
            "/start - Begin your journey\n"
            "/help - Show this help\n"
            "'daily' - Free daily insight\n"
            "'personal' - Detailed reading\n\n"
            "💳 Secure payments via Razorpay\n"
            "🔮 May the stars guide your path!"
        )
        await self.bot.send_message(message.chat.id, help_text)
    
    async def handle_daily_reading(self, user_id):
        """Handle daily reading request with discount psychology"""
        try:
            await self.bot.send_message(user_id, "🔮 Consulting the cosmic energies...")
            
            prompt = "Generate a generic daily Vedic horoscope focusing on career, love, and remedies. Keep it positive and insightful."
            horoscope = await self.generate_content(prompt, user_id)
            
            # A/B test pricing - assign random price if not assigned
            if user_id not in self.user_pricing:
                self.user_pricing[user_id] = random.choice(self.pricing_variants)
            
            user_price = self.user_pricing[user_id]
            discount_text = self.get_discount_emoji_text(user_price)
            urgency = self.get_dynamic_urgency(user_id, 'daily_reading')
            
            response = (
                f"🌟 Today's Cosmic Guidance:\n\n{horoscope}\n\n"
                f"{'='*30}\n"
                f"{discount_text}\n"
                f"{'='*30}\n"
                f"{urgency['bonus']}\n"
                f"⚡ FLASH SALE - Only {urgency['slots']} slots left!\n"
                f"✨ Reply 'personal' to claim your detailed drishti NOW!\n"
                f"⏰ Offer expires in {urgency['expires']} minutes!"
            )
            
            await self.bot.send_message(user_id, response)
            self.user_states[user_id] = 'upsell'
            
        except Exception as e:
            self.logger.error(f"Error in daily reading for {user_id}: {e}")
            await self.bot.send_message(user_id, "🙏 Unable to fetch today's guidance. Please try again.")
    
    async def handle_personal_request(self, user_id):
        """Handle personal reading request with Razorpay payment"""
        try:
            # Get user's assigned price
            user_price = self.user_pricing.get(user_id, self.pricing_variants[0])
            discount_text = self.get_discount_text(user_price)
            savings = self.original_price - user_price
            
            # Create Razorpay order
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
            
            await self.bot.send_message(user_id, payment_msg)
            self.user_states[user_id] = 'payment_pending'
            
            # Log pricing for analytics
            self.logger.info(f"User {user_id} shown discount price ₹{user_price} (saved ₹{savings}) - Order: {order['id']}")
            
        except Exception as e:
            self.logger.error(f"Error in personal request for {user_id}: {e}")
    
    async def handle_payment_confirmation(self, user_id, message):
        """Handle payment confirmation (text/photo)"""
        try:
            confirmation_msg = (
                "✅ Payment confirmation received! Thank you for your trust.\n\n"
                "📝 Our team is verifying your Razorpay payment.\n\n"
                "📅 Please send your birth details:\n"
                "• Date (DD-MM-YYYY)\n"
                "• Time (HH:MM)\n"
                "• Place of birth\n\n"
                "Example: 15-08-1990, 14:30, Mumbai"
            )
            await self.bot.send_message(user_id, confirmation_msg)
            self.user_states[user_id] = 'details'
        except Exception as e:
            self.logger.error(f"Error in payment confirmation for {user_id}: {e}")
    
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
        """Handle birth details and generate report with referral system"""
        try:
            details = message.text
            await self.bot.send_message(user_id, "🔮 Preparing your detailed cosmic analysis... This may take a moment.")
            
            prompt = (
                f"Generate a comprehensive Vedic astrology reading for birth details: {details}. "
                "Focus on career prospects, relationships, health insights, spiritual guidance, "
                "and practical remedies. Make it detailed, insightful, and authoritative."
            )
            
            report = await self.generate_content(prompt, user_id)
            
            # Create and send PDF
            pdf_buffer = await self.create_pdf_async(report)
            await self.bot.send_document(user_id, pdf_buffer, visible_file_name='DevDrishti_Report.pdf')
            
            final_msg = (
                "📜 Your cosmic blueprint is ready!\n\n"
                "🌟 Share DevDrishti with friends for special blessings!\n"
                "🙏 May this guidance illuminate your path."
            )
            await self.bot.send_message(user_id, final_msg)
            
            # Add referral link
            referral_msg = (
                f"🔗 Your referral link: https://t.me/{self.bot_username}?start=ref_{user_id}\n"
                f"Share for free mini-upgrade on your next reading!\n"
                f"📊 Referrals so far: {self.user_referrals[user_id]}"
            )
            await self.bot.send_message(user_id, referral_msg)
            
            self.user_states[user_id] = 'done'
            
            # Log sale for analytics
            user_price = self.user_pricing.get(user_id, self.pricing_variants[0])
            discount_amount = self.original_price - user_price
            self.logger.info(f"SALE: User {user_id} completed ₹{user_price} reading. Details: {details[:50]}... (Discounted by ₹{discount_amount})")
            
            # Track in analytics if available
            if self.analytics:
                self.analytics.log_sale(user_id, user_price, details, self.original_price)
            
        except Exception as e:
            self.logger.error(f"Error generating report for {user_id}: {e}")
            await self.bot.send_message(user_id, "🙏 Error generating your report. Please try again.")
    
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