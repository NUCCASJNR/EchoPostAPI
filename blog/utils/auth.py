#!/usr/bin/env python3

from django.contrib.auth.backends import ModelBackend
from blog.models.user import MainUser as User

class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is not None and password is not None:
            if '@' in username:
                kwargs = {'email': username}
            else:
                kwargs = {'username': username}

            try:
                user = User.objects.get(**kwargs)
                if user.check_password(password):
                    return user
            except User.DoesNotExist:
                return None

        return None
