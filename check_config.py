#!/usr/bin/env python3
"""
DevDrishti Bot - Configuration Checker
Run this to check your bot configuration
"""
import os

def check_config():
    print("🔍 DevDrishti Bot Configuration Check")
    print("=" * 50)
    
    # Required variables
    required_vars = {
        'BOT_TOKEN': 'Telegram Bot Token',
        'GEMINI_API_KEY': 'Google Gemini API Key',
        'UPI_ID': 'UPI ID for payments'
    }
    
    # Optional but important variables
    optional_vars = {
        'ADMIN_USER_ID': 'Admin Telegram User ID (for payment verification)',
        'RAZORPAY_KEY_ID': 'Razorpay Key ID',
        'RAZORPAY_KEY_SECRET': 'Razorpay Secret Key'
    }
    
    print("📋 Required Configuration:")
    for var, description in required_vars.items():
        value = os.getenv(var)
        status = "✅ SET" if value else "❌ MISSING"
        masked_value = f"{value[:10]}..." if value and len(value) > 10 else value or "Not set"
        print(f"  {var}: {status} - {description}")
        if value:
            print(f"    Value: {masked_value}")
    
    print("\n📋 Optional Configuration:")
    for var, description in optional_vars.items():
        value = os.getenv(var)
        status = "✅ SET" if value else "⚠️ NOT SET"
        masked_value = f"{value[:10]}..." if value and len(value) > 10 else value or "Not set"
        print(f"  {var}: {status} - {description}")
        if value:
            print(f"    Value: {masked_value}")
    
    # Admin verification check
    admin_id = os.getenv('ADMIN_USER_ID')
    print(f"\n🔐 Payment Verification Mode:")
    if admin_id:
        try:
            admin_id_int = int(admin_id)
            print(f"  ✅ MANUAL VERIFICATION - Admin ID: {admin_id_int}")
            print(f"  💡 Admin will receive approve/reject buttons for payments")
        except ValueError:
            print(f"  ❌ INVALID ADMIN_USER_ID - Must be numeric")
            print(f"  💡 Get your user ID from @userinfobot on Telegram")
    else:
        print(f"  ⚠️ AUTO-APPROVAL MODE - No admin verification")
        print(f"  💡 Set ADMIN_USER_ID for manual payment verification")
    
    print(f"\n💡 To get your Telegram User ID:")
    print(f"  1. Message @userinfobot on Telegram")
    print(f"  2. Copy the 'User ID' number")
    print(f"  3. Set ADMIN_USER_ID=your_user_id_number")
    
    print(f"\n🚀 To enable admin verification:")
    print(f"  1. Set ADMIN_USER_ID in Railway dashboard")
    print(f"  2. Redeploy the bot")
    print(f"  3. Test with /admin command")

if __name__ == "__main__":
    check_config() 