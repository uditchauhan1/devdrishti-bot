#!/usr/bin/env python3
"""
Advanced Analytics for DevDrishti Bot with Google Sheets Integration
Tracks sales, referrals, conversion funnels, and A/B test results
"""
import json
import os
import logging
from datetime import datetime, timedelta
from collections import defaultdict

try:
    import gspread
    from google.oauth2.service_account import Credentials
    SHEETS_AVAILABLE = True
except ImportError:
    SHEETS_AVAILABLE = False
    print("📊 Google Sheets not available - install: pip install gspread google-auth")

class DevDrishtiAdvancedAnalytics:
    def __init__(self, data_file='analytics.json', enable_sheets=False):
        self.data_file = data_file
        self.enable_sheets = enable_sheets and SHEETS_AVAILABLE
        self.data = self.load_data()
        self.logger = logging.getLogger(__name__)
        
        if self.enable_sheets:
            self.setup_sheets()
    
    def setup_sheets(self):
        """Setup Google Sheets integration"""
        try:
            # Use service account credentials (add service-account.json to Replit)
            scope = ['https://spreadsheets.google.com/feeds',
                    'https://www.googleapis.com/auth/drive']
            
            creds_file = os.getenv('GOOGLE_CREDS_FILE', 'service-account.json')
            if os.path.exists(creds_file):
                creds = Credentials.from_service_account_file(creds_file, scopes=scope)
                self.gc = gspread.authorize(creds)
                
                # Create or open spreadsheet
                sheet_id = os.getenv('SHEETS_ID')
                if sheet_id:
                    self.sheet = self.gc.open_by_key(sheet_id)
                else:
                    self.sheet = self.gc.create('DevDrishti Analytics')
                    print(f"📊 Created new sheet: {self.sheet.url}")
                
                self.setup_worksheets()
                print("✅ Google Sheets integration enabled")
            else:
                print("❌ Google credentials file not found")
                self.enable_sheets = False
                
        except Exception as e:
            print(f"❌ Sheets setup failed: {e}")
            self.enable_sheets = False
    
    def setup_worksheets(self):
        """Setup worksheet structure"""
        try:
            # Sales worksheet
            try:
                self.sales_ws = self.sheet.worksheet('Sales')
            except:
                self.sales_ws = self.sheet.add_worksheet('Sales', 1000, 10)
                headers = ['Timestamp', 'User ID', 'Price', 'Original Price', 
                          'Discount %', 'Savings', 'Details', 'Urgency Type', 'Time to Convert']
                self.sales_ws.append_row(headers)
            
            # Users worksheet
            try:
                self.users_ws = self.sheet.worksheet('Users')
            except:
                self.users_ws = self.sheet.add_worksheet('Users', 1000, 8)
                headers = ['Timestamp', 'User ID', 'Action', 'Price Variant', 
                          'Conversion Time', 'Referrer', 'Status']
                self.users_ws.append_row(headers)
                
        except Exception as e:
            self.logger.error(f"Worksheet setup error: {e}")
    
    def load_data(self):
        """Load analytics data"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        return {
            'sales': [],
            'users': {},
            'referrals': {},
            'pricing_test': {'199': 0, '299': 0},
            'conversion_funnel': {
                'started': 0,
                'daily_reading': 0,
                'personal_request': 0,
                'payment_sent': 0,
                'completed': 0
            },
            'urgency_test': {
                'instant': {'shown': 0, 'converted': 0},
                'quick': {'shown': 0, 'converted': 0},
                'final': {'shown': 0, 'converted': 0}
            },
            'daily_stats': defaultdict(lambda: {'users': 0, 'sales': 0, 'revenue': 0})
        }
    
    def save_data(self):
        """Save analytics data"""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.data, f, indent=2, default=str)
        except Exception as e:
            self.logger.error(f"Failed to save analytics: {e}")
    
    def log_sale(self, user_id, price, details="", original_price=999, urgency_type="", conversion_time=0):
        """Log sale with advanced metrics"""
        discount_amount = original_price - price
        discount_percent = round((discount_amount / original_price) * 100)
        
        sale = {
            'user_id': user_id,
            'price': price,
            'original_price': original_price,
            'discount_amount': discount_amount,
            'discount_percent': discount_percent,
            'urgency_type': urgency_type,
            'conversion_time_minutes': conversion_time,
            'timestamp': datetime.now().isoformat(),
            'details': details[:100]
        }
        
        self.data['sales'].append(sale)
        self.data['pricing_test'][str(price)] += 1
        self.data['conversion_funnel']['completed'] += 1
        
        # Update urgency test data
        if urgency_type in self.data['urgency_test']:
            self.data['urgency_test'][urgency_type]['converted'] += 1
        
        # Daily stats
        today = datetime.now().strftime('%Y-%m-%d')
        self.data['daily_stats'][today]['sales'] += 1
        self.data['daily_stats'][today]['revenue'] += price
        
        self.save_data()
        
        # Log to Google Sheets
        if self.enable_sheets:
            try:
                row = [
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    user_id, price, original_price, discount_percent,
                    discount_amount, details[:50], urgency_type, conversion_time
                ]
                self.sales_ws.append_row(row)
            except Exception as e:
                self.logger.error(f"Sheets logging error: {e}")
        
        print(f"💰 SALE: User {user_id} - ₹{price} ({discount_percent}% off, {urgency_type} urgency)")
    
    def log_funnel_action(self, user_id, action, urgency_type=""):
        """Log conversion funnel actions"""
        if action in self.data['conversion_funnel']:
            self.data['conversion_funnel'][action] += 1
        
        # Track urgency effectiveness
        if urgency_type in self.data['urgency_test']:
            self.data['urgency_test'][urgency_type]['shown'] += 1
        
        self.save_data()
    
    def get_conversion_rates(self):
        """Calculate conversion rates at each funnel stage"""
        funnel = self.data['conversion_funnel']
        rates = {}
        
        if funnel['started'] > 0:
            rates['daily_reading'] = round((funnel['daily_reading'] / funnel['started']) * 100, 2)
            rates['personal_request'] = round((funnel['personal_request'] / funnel['started']) * 100, 2)
            rates['payment_sent'] = round((funnel['payment_sent'] / funnel['started']) * 100, 2)
            rates['completed'] = round((funnel['completed'] / funnel['started']) * 100, 2)
        
        return rates
    
    def get_urgency_effectiveness(self):
        """Analyze urgency message effectiveness"""
        effectiveness = {}
        
        for urgency_type, data in self.data['urgency_test'].items():
            if data['shown'] > 0:
                conversion_rate = round((data['converted'] / data['shown']) * 100, 2)
                effectiveness[urgency_type] = {
                    'shown': data['shown'],
                    'converted': data['converted'],
                    'rate': conversion_rate
                }
        
        return effectiveness
    
    def print_advanced_dashboard(self):
        """Print comprehensive analytics dashboard"""
        funnel_rates = self.get_conversion_rates()
        urgency_data = self.get_urgency_effectiveness()
        
        print("=" * 60)
        print("📊 DEVDRISHTI ADVANCED ANALYTICS DASHBOARD")
        print("=" * 60)
        
        # Basic metrics
        total_sales = len(self.data['sales'])
        total_revenue = sum(sale['price'] for sale in self.data['sales'])
        
        print(f"💰 REVENUE METRICS:")
        print(f"   Total Sales: {total_sales}")
        print(f"   Total Revenue: ₹{total_revenue:,}")
        print(f"   Average Order Value: ₹{total_revenue//total_sales if total_sales > 0 else 0}")
        
        # Conversion funnel
        print(f"\n🎯 CONVERSION FUNNEL:")
        funnel = self.data['conversion_funnel']
        for stage, count in funnel.items():
            rate = funnel_rates.get(stage, 0)
            print(f"   {stage.title()}: {count} ({rate}%)")
        
        # A/B test results
        print(f"\n🧪 A/B PRICING TEST:")
        p199 = self.data['pricing_test']['199']
        p299 = self.data['pricing_test']['299']
        print(f"   ₹199 (80% off): {p199} sales (₹{p199 * 199:,} revenue)")
        print(f"   ₹299 (70% off): {p299} sales (₹{p299 * 299:,} revenue)")
        
        if p199 > 0 and p299 > 0:
            ratio = p299 / p199
            print(f"   ₹299 converts {ratio:.2f}x less than ₹199")
        
        # Urgency effectiveness
        print(f"\n⚡ URGENCY MESSAGE EFFECTIVENESS:")
        for urgency_type, data in urgency_data.items():
            print(f"   {urgency_type.title()}: {data['rate']}% ({data['converted']}/{data['shown']})")
        
        print("=" * 60)

if __name__ == "__main__":
    analytics = DevDrishtiAdvancedAnalytics(enable_sheets=True)
    analytics.print_advanced_dashboard() 