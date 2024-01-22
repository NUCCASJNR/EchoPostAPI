#!/usr/bin/env python3

"""Contains view for handling user signup"""

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from blog.serializers.signup import SignupSerializer
from blog.models.user import MainUser as User
from blog.utils.email_utils import EmailUtils
from blog.serializers.verification import EmailVerificationSerializer
from blog.utils.redis_utils import RedisClient

class SignupViewSet(viewsets.ModelViewSet):
    serializer_class = SignupSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        # Check if the email or username already exists
        email_exists = User.custom_get(**{'email': request.data['email']})
        username_exists = User.custom_get(**{'username': request.data['username']})
        code = EmailUtils.generate_verification_code()
        if email_exists:
            return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        if username_exists:
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            user = User.custom_save(verification_code=code, **serializer.validated_data)
            EmailUtils.send_verification_email(user, code)
            response_data = {
                'message': 'Signup successful!, check your email for the verification code',
                'staus_code': 201
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class EmailVerificationViewSet(viewsets.ModelViewSet):
    serializer_class = EmailVerificationSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        user = User.custom_get(**{'verification_code': request.data['verification_code']})
        if not user:
            return Response({'error': 'Invalid or expired verification code'}, status=status.HTTP_400_BAD_REQUEST)
        redis_client = RedisClient()
        key = f'user_id:{user.id}:{user.verification_code}'
        # Get the key from the redis-cli
        if redis_client.get_key(key):
            if serializer.is_valid():
                User.custom_update(filter_kwargs={"verification_code": request.data['verification_code']},
                                update_kwargs={'verified': True})
                response_data = {
                    'message': 'Email verifcation sucessful!, You can now log in into your account',
                    'staus_code': 200
                }
                # Delete the key after verification
                redis_client.delete_key(key)
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Invalid or expired verification code'}, status=status.HTTP_400_BAD_REQUEST)