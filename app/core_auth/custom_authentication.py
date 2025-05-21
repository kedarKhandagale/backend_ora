from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model
from .models import UserActiveToken

User = get_user_model()

class CustomTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header or not auth_header.startswith('Bearer '):
            return None

        token = auth_header.split(' ')[1]

        try:
            access_token_obj = AccessToken(token)
        except Exception:
            raise AuthenticationFailed('Invalid or expired token')

        user_id = access_token_obj['user_id']

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise AuthenticationFailed('User not found')

        try:
            user_token = UserActiveToken.objects.get(user=user)
        except UserActiveToken.DoesNotExist:
            raise AuthenticationFailed('Token not found for user')

        if user_token.token != token:
            raise AuthenticationFailed('Token mismatch or logged out from other device')

        return (user, token)
