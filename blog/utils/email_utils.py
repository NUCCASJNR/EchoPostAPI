#!/usr/bin/env python3

"""
Handles all utils relating to sending emails and also generating tokens
"""

from django.conf import settings
from os import getenv
from blog.utils.redis_utils import RedisClient
from blog.models.user import MainUser as User
import secrets
import random
import requests


API_KEY = getenv("ELASTIC_EMAIL_KEY")


class EmailUtils:
    @staticmethod
    def generate_verification_code(length=6):
        """
        Generate a random verification code.
        :param length: Length of the verification code (default is 6)
        :return: Random verification code
        """
        charset = "0123456789"
        verification_code = ''.join(secrets.choice(charset) for _ in range(length))
        return verification_code

    @staticmethod
    def send_verification_email(user: User, verification_code: int):
        """
        Sends a verification email to the user
        """
        # verification_code = EmailUtils.generate_verification_code()
        redis_client = RedisClient()
        key = f'user_id:{user.id}:{verification_code}'
        redis_client.set_key(key, verification_code, expiry=30)
        # user.verified = False
        # user.verification_code = verification_code
        # user.save()
        url = "https://api.elasticemail.com/v2/email/send"
        request_payload = {
            "apikey": API_KEY,
            "from": getenv("EMAIL_SENDER"),
            "to": user.email,
            "subject": "Verify your account",
            "bodyHtml": f"Hello {user.username},<br> Your verification code is: {verification_code}</br>",
            "isTransactional": False
        }
        try:
            response = requests.post(url, data=request_payload)
            if response.status_code == 200:
                print(response.json())
                return True
            else:
                print(f'Error sending verification email to {user.email}')
                return False
        except Exception as e:
            print(f'Error sending verification email to {user.email}: {e}')
            return False

    @staticmethod
    def send_password_reset_email(user: User, reset_code: int, email: str):
        """
        Sends a password-reset email to the user
        """
        redis_client = RedisClient()
        key = f'reset_token:{user.id}:{reset_code}'
        redis_client.set_key(key, reset_code, expiry=30)
        url = "https://api.elasticemail.com/v2/email/send"
        request_payload = {
            "apikey": API_KEY,
            "from": getenv("EMAIL_SENDER"),
            "to": email,
            "subject": "Reset your password",
            "bodyHtml": f"Hello {user.username},<br> Your password reset code is: {reset_code}</br>",
            "isTransactional": False
        }
        try:
            response = requests.post(url, data=request_payload)
            if response.status_code == 200:
                print(f'Email Successfully sent to {user.email}')
                return True
            else:
                print(f'Error sending password reset email to {user.email}')
                return False
        except Exception as e:
            print(f'Error sending password reset email to {user.email}: {e}')
            return False
