from datetime import datetime
import six
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text


class TokenGenerator(PasswordResetTokenGenerator):
    """generate code"""
    def _make_hash_value(self, user, timestamp):
        """creating a value to current user"""
        now = datetime.now().minute
        user_now = six.text_type(user.pk) + six.text_type(now)
        hashed_string = user_now + six.text_type(user.is_activate)
        return hashed_string

    def make_token(self, user):
        """
            returns a token that can be user once to do a password reset
            for the given user.
        """
        date_now = datetime.now()
        now = int(date_now.strftime('%Y%m%d'))
        token_generated = self._make_hash_value(user, now)
        return token_generated


def encode_user_id(Id):
    """encode user ID"""
    return urlsafe_base64_encode(force_bytes(Id))

def decode_user_id(Id):
    """decode user ID"""
    return force_text(urlsafe_base64_decode(Id))

def make_user_token(user):
    """make user token"""
    generator = TokenGenerator()
    return generator.make_token(user)
