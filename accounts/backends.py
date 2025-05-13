from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailOrUsernameModelBackend(ModelBackend):
    """
    Custom authentication backend that allows login with either username or email.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = None
        try:
            # First, try to find the user by username
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            try:
                # If no user is found with the username, try to find the user by email
                user = User.objects.get(email=username)
            except User.DoesNotExist:
                # If no user is found with either username or email, return None
                return None

        if user and user.check_password(password):
            # If the user is found and the password matches, return the user object
            return user
        return None  # If user is found but password doesn't match, return None
