# M-Pesa API Integration Setup Guide
# Nyandiwa Smart Poultry Connect

## 🎯 Overview
Your website now supports M-Pesa STK Push (Lipa Na M-Pesa Online) payments. When customers select M-Pesa as payment method, they receive a payment prompt on their phone to complete the transaction.

## 📋 Prerequisites

1. **Safaricom Daraja API Account**
   - Visit: https://developer.safaricom.co.ke/
   - Create an account
   - Create an app to get credentials

2. **Python Packages** (Already Installed)
   - requests==2.32.5
   - python-decouple==3.8

## 🔧 Step-by-Step Setup

### 1. Get M-Pesa API Credentials

#### Sandbox (Testing)
1. Login to https://developer.safaricom.co.ke/
2. Go to "My Apps" → "Create New App"
3. Select "Lipa Na M-Pesa Online"
4. Note down:
   - Consumer Key
   - Consumer Secret
   - Test Credentials (Shortcode: 174379)
   - Passkey

#### Production (Live)
1. Register your business with Safaricom
2. Apply for M-Pesa API access through Safaricom
3. Get your live credentials and shortcode

### 2. Configure Settings

Edit `ChickenFarm/settings.py` with your credentials:

```python
# M-Pesa Configuration
MPESA_ENVIRONMENT = 'sandbox'  # Change to 'production' when going live

# From Daraja Portal
MPESA_CONSUMER_KEY = 'your_actual_consumer_key'
MPESA_CONSUMER_SECRET = 'your_actual_consumer_secret'

# Sandbox test shortcode (change to your paybill for production)
MPESA_SHORTCODE = '174379'

# Passkey from Daraja Portal
MPESA_PASSKEY = 'your_actual_passkey'

# Callback URL (must be publicly accessible)
MPESA_CALLBACK_URL = 'https://yourdomain.com/mpesa/callback/'
```

### 3. Setup Callback URL

The callback URL must be publicly accessible for M-Pesa to send payment confirmations.

#### For Local Testing (Using ngrok)

1. **Install ngrok:**
   - Download from https://ngrok.com/
   - Extract and run: `ngrok http 8000`

2. **Get your public URL:**
   ```
   ngrok by @inconshreveable
   
   Session Status: online
   Forwarding: https://abc123.ngrok.io -> http://localhost:8000
   ```

3. **Update settings.py:**
   ```python
   MPESA_CALLBACK_URL = 'https://abc123.ngrok.io/mpesa/callback/'
   ```

4. **Add to ALLOWED_HOSTS:**
   ```python
   ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'abc123.ngrok.io']
   ```

#### For Production

Use your actual domain:
```python
MPESA_CALLBACK_URL = 'https://www.yourchickenfarm.com/mpesa/callback/'
```

### 4. Test the Integration

#### Using Sandbox Test Credentials

| Phone Number | Purpose | PIN |
|-------------|---------|-----|
| 254708374149 | Success | 1234 |
| 254708374150 | Insufficient Funds | 1234 |
| 254708374151 | Wrong PIN | 1234 |

**Testing Steps:**

1. Start your server:
   ```bash
   .\chick\Scripts\python.exe manage.py runserver
   ```

2. If using ngrok, start it in another terminal:
   ```bash
   ngrok http 8000
   ```

3. Visit your website (via ngrok URL if testing locally)

4. Go to Products page → Add items to cart

5. Click "Proceed to Checkout"

6. Fill in customer details

7. Select "M-Pesa" payment method

8. Enter test phone number: 254708374149

9. Click "Confirm Order"

10. Check your phone (or simulated response) for STK Push prompt

11. Enter PIN: 1234

12. Payment confirmation will be received via callback

## ✅ What Has Been Implemented

### Files Created/Modified:

1. **chickapp/mpesa.py**
   - MpesaClient class for API communication
   - STK Push initiation
   - Transaction status queries
   - Phone number formatting

2. **chickapp/views.py**
   - process_payment: Initiates M-Pesa STK Push
   - mpesa_callback: Receives payment confirmations
   - check_payment_status: Checks order payment status

3. **chickapp/models.py** (Order model)
   - mpesa_checkout_request_id
   - mpesa_merchant_request_id
   - mpesa_receipt_number

4. **static/js/payment.js**
   - Automatic payment status checking
   - M-Pesa-specific notifications
   - Receipt number display

5. **chickapp/urls.py**
   - /mpesa/callback/ - Receives M-Pesa callbacks
   - /check-payment-status/ - Status checking endpoint

## 🔄 Payment Flow

1. **Customer initiates payment:**
   - Selects items, proceeds to checkout
   - Chooses M-Pesa, enters phone number
   - Submits order

2. **Backend processing:**
   - Order created with status "pending"
   - STK Push request sent to M-Pesa API
   - CheckoutRequestID saved to order

3. **Customer receives prompt:**
   - M-Pesa popup on their phone
   - Enters PIN to confirm payment

4. **Payment confirmation:**
   - M-Pesa sends callback to your server
   - Order status updated to "completed"
   - Receipt number saved

5. **Frontend notification:**
   - JavaScript checks payment status every 5 seconds
   - Shows success message with receipt number
   - Redirects to dashboard

## 🔍 Monitoring Payments

### Admin Panel
Check orders in Django admin:
```
http://localhost:8000/admin/chickapp/order/
```

View fields:
- Payment Status
- M-Pesa Receipt Number
- Checkout Request ID

### Logs
Check application logs for M-Pesa API responses:
```python
logger.info('M-Pesa STK Push response: ...')
logger.info('Payment successful for order ...')
logger.warning('Payment failed for order ...')
```

## 🐛 Troubleshooting

### Issue: "Failed to get M-Pesa access token"
**Solution:** 
- Check Consumer Key and Secret are correct
- Confirm internet connectivity
- Verify environment setting (sandbox/production)

### Issue: "STK Push failed"
**Solution:**
- Ensure phone number format is correct (254XXXXXXXXX)
- Check shortcode is valid
- Verify passkey matches shortcode

### Issue: "Callback not received"
**Solution:**
- Confirm callback URL is publicly accessible
- Check ngrok is running (for local testing)
- Verify URL in settings.py matches ngrok URL
- Check server logs for callback errors

### Issue: "Invalid phone number"
**Solution:**
- Phone must be Safaricom (starts with 254)
- Format: 254712345678 or 0712345678
- Remove spaces and special characters

## 🚀 Going to Production

### Checklist:

1. ✅ Get production credentials from Safaricom
2. ✅ Update settings.py with production credentials
3. ✅ Change MPESA_ENVIRONMENT to 'production'
4. ✅ Update callback URL to production domain
5. ✅ Set DEBUG = False
6. ✅ Configure proper ALLOWED_HOSTS
7. ✅ Use environment variables for sensitive data
8. ✅ Enable HTTPS on your domain
9. ✅ Test with small real transaction
10. ✅ Monitor logs and callbacks

### Using Environment Variables (Recommended)

Create `.env` file:
```
MPESA_CONSUMER_KEY=your_key
MPESA_CONSUMER_SECRET=your_secret
MPESA_SHORTCODE=your_shortcode
MPESA_PASSKEY=your_passkey
MPESA_CALLBACK_URL=https://yourdomain.com/mpesa/callback/
```

Update settings.py:
```python
from decouple import config

MPESA_CONSUMER_KEY = config('MPESA_CONSUMER_KEY')
MPESA_CONSUMER_SECRET = config('MPESA_CONSUMER_SECRET')
MPESA_SHORTCODE = config('MPESA_SHORTCODE')
MPESA_PASSKEY = config('MPESA_PASSKEY')
MPESA_CALLBACK_URL = config('MPESA_CALLBACK_URL')
```

## 📞 Support

### Safaricom Support
- Email: apisupport@safaricom.co.ke
- Developer Portal: https://developer.safaricom.co.ke/

### Testing Resources
- API Documentation: https://developer.safaricom.co.ke/Documentation
- Postman Collection: Available on Daraja Portal
- Test Credentials: https://developer.safaricom.co.ke/test_credentials

## 🎉 Features

✅ Real-time STK Push payments
✅ Automatic payment verification
✅ Receipt number tracking
✅ Payment status updates
✅ Customer notifications
✅ Shopping cart integration
✅ Order history with payment details
✅ Admin panel payment monitoring
✅ Failed payment handling
✅ Sandbox testing support

## 📊 Next Steps

1. **Get your Daraja credentials** (most important!)
2. **Test in sandbox mode**
3. **Apply for production access**
4. **Configure production settings**
5. **Go live!**

---

**Note:** Remember to keep your API credentials secure and never commit them to version control. Use environment variables or Django's secret management.
