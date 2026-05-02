from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from .base_service import BaseService


class RegisterService(BaseService):
    def register_user(self, *, email: str, password: str):
        User = get_user_model()
        normalized = email.lower().strip()
        return User.objects.create(
            username=normalized,
            email=normalized,
            password=make_password(password),
        )
