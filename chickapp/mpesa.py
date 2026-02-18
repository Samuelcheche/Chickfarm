"""
M-Pesa Daraja API Integration for Django
Handles STK Push (Lipa Na M-Pesa Online) payments
"""

import requests
import base64
import json
from datetime import datetime
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class MpesaClient:
    """
    M-Pesa API Client for handling payments through Safaricom's Daraja API
    """
    
    def __init__(self):
        self.consumer_key = settings.MPESA_CONSUMER_KEY
        self.consumer_secret = settings.MPESA_CONSUMER_SECRET
        self.business_shortcode = settings.MPESA_SHORTCODE
        self.passkey = settings.MPESA_PASSKEY
        self.callback_url = settings.MPESA_CALLBACK_URL
        self.environment = settings.MPESA_ENVIRONMENT
        
        # Set API URLs based on environment
        if self.environment == 'sandbox':
            self.base_url = 'https://sandbox.safaricom.co.ke'
        else:
            self.base_url = 'https://api.safaricom.co.ke'
    
    def get_access_token(self):
        """
        Generate OAuth access token for API authentication
        """
        url = f'{self.base_url}/oauth/v1/generate?grant_type=client_credentials'
        
        try:
            # Create basic auth credentials
            credentials = f'{self.consumer_key}:{self.consumer_secret}'
            encoded_credentials = base64.b64encode(credentials.encode()).decode()
            
            headers = {
                'Authorization': f'Basic {encoded_credentials}',
                'Content-Type': 'application/json'
            }
            
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            access_token = result.get('access_token')
            
            if not access_token:
                logger.error('No access token in M-Pesa response')
                return None
            
            return access_token
            
        except requests.exceptions.RequestException as e:
            logger.error(f'M-Pesa access token error: {str(e)}')
            return None
    
    def generate_password(self):
        """
        Generate password for STK Push request
        Format: base64(Shortcode + Passkey + Timestamp)
        """
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        data_to_encode = f'{self.business_shortcode}{self.passkey}{timestamp}'
        password = base64.b64encode(data_to_encode.encode()).decode()
        
        return password, timestamp
    
    def stk_push(self, phone_number, amount, account_reference, transaction_desc='Payment'):
        """
        Initiate STK Push (Lipa Na M-Pesa Online)
        
        Args:
            phone_number (str): Customer phone number in format 254XXXXXXXXX
            amount (int): Amount to be paid
            account_reference (str): Order code or reference
            transaction_desc (str): Description of transaction
            
        Returns:
            dict: Response from M-Pesa API or error details
        """
        access_token = self.get_access_token()
        
        if not access_token:
            return {
                'success': False,
                'message': 'Failed to get M-Pesa access token'
            }
        
        # Clean phone number
        phone_number = self.format_phone_number(phone_number)
        
        # Generate password and timestamp
        password, timestamp = self.generate_password()
        
        # Prepare request
        url = f'{self.base_url}/mpesa/stkpush/v1/processrequest'
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'BusinessShortCode': self.business_shortcode,
            'Password': password,
            'Timestamp': timestamp,
            'TransactionType': 'CustomerPayBillOnline',
            'Amount': int(amount),
            'PartyA': phone_number,
            'PartyB': self.business_shortcode,
            'PhoneNumber': phone_number,
            'CallBackURL': self.callback_url,
            'AccountReference': account_reference,
            'TransactionDesc': transaction_desc
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            result = response.json()
            
            logger.info(f'M-Pesa STK Push response: {result}')
            
            # Check response
            response_code = result.get('ResponseCode', '')
            
            if response_code == '0':
                return {
                    'success': True,
                    'message': 'STK Push sent successfully',
                    'merchant_request_id': result.get('MerchantRequestID'),
                    'checkout_request_id': result.get('CheckoutRequestID'),
                    'response_description': result.get('ResponseDescription')
                }
            else:
                return {
                    'success': False,
                    'message': result.get('ResponseDescription', 'STK Push failed'),
                    'error_code': response_code
                }
                
        except requests.exceptions.RequestException as e:
            logger.error(f'M-Pesa STK Push error: {str(e)}')
            return {
                'success': False,
                'message': f'Network error: {str(e)}'
            }
        except Exception as e:
            logger.error(f'M-Pesa unexpected error: {str(e)}')
            return {
                'success': False,
                'message': f'Unexpected error: {str(e)}'
            }
    
    def format_phone_number(self, phone):
        """
        Format phone number to 254XXXXXXXXX format
        """
        # Remove spaces, dashes, and other characters
        phone = ''.join(filter(str.isdigit, phone))
        
        # Handle different formats
        if phone.startswith('254'):
            return phone
        elif phone.startswith('0'):
            return '254' + phone[1:]
        elif phone.startswith('+254'):
            return phone[1:]
        elif phone.startswith('7') or phone.startswith('1'):
            return '254' + phone
        else:
            return phone
    
    def query_transaction_status(self, checkout_request_id):
        """
        Query the status of a transaction
        
        Args:
            checkout_request_id (str): CheckoutRequestID from STK Push
            
        Returns:
            dict: Transaction status
        """
        access_token = self.get_access_token()
        
        if not access_token:
            return {
                'success': False,
                'message': 'Failed to get access token'
            }
        
        password, timestamp = self.generate_password()
        
        url = f'{self.base_url}/mpesa/stkpushquery/v1/query'
        
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'BusinessShortCode': self.business_shortcode,
            'Password': password,
            'Timestamp': timestamp,
            'CheckoutRequestID': checkout_request_id
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            result = response.json()
            
            return {
                'success': True,
                'data': result
            }
            
        except Exception as e:
            logger.error(f'M-Pesa query error: {str(e)}')
            return {
                'success': False,
                'message': str(e)
            }


def initiate_mpesa_payment(phone_number, amount, order_code, description='Poultry Order Payment'):
    """
    Helper function to initiate M-Pesa payment
    
    Args:
        phone_number (str): Customer phone number
        amount (float): Payment amount
        order_code (str): Order reference code
        description (str): Payment description
        
    Returns:
        dict: Payment result
    """
    try:
        client = MpesaClient()
        result = client.stk_push(
            phone_number=phone_number,
            amount=amount,
            account_reference=order_code,
            transaction_desc=description
        )
        return result
    except Exception as e:
        logger.error(f'M-Pesa payment initiation error: {str(e)}')
        return {
            'success': False,
            'message': str(e)
        }
