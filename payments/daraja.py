import requests
import base64
from django.conf import settings
from datetime import datetime

def get_access_token():
    consumer_key = settings.DARAJA_CONSUMER_KEY
    consumer_secret = settings.DARAJA_CONSUMER_SECRET

    auth = base64.b64encode(
        f"{consumer_key}:{consumer_secret}".encode()
    ).decode()

    headers = {"Authorization": f"Basic {auth}"}
    response = requests.get(
        "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials",
        headers=headers
    )

    return response.json().get("access_token")


def stk_push(phone, amount, callback_url, account_ref, desc):
    token = get_access_token()
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    shortcode = settings.DARAJA_SHORTCODE
    passkey = settings.DARAJA_PASSKEY

    password = base64.b64encode(
        f"{shortcode}{passkey}{timestamp}".encode()
    ).decode()

    payload = {
        "BusinessShortCode": shortcode,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": int(amount),
        "PartyA": phone,
        "PartyB": shortcode,
        "PhoneNumber": phone,
        "CallBackURL": callback_url,
        "AccountReference": account_ref,
        "TransactionDesc": desc,
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    response = requests.post(
        "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest",
        json=payload,
        headers=headers
    )

    return response.json()
