from django.core.validators import EmailValidator
from rest_framework import serializers, fields
from rest_framework.generics import get_object_or_404
from core.user import User
from core.encoder_tokens import encode_user_id
from core.encoder_tokens import make_user_token


class UserSerializer(serializers.ModelSerializer):
    """model user serializer"""
    
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "email", "password", "deleted")
        extra_kwargs = {
            "password": {"write_only": True, "min_length": 5},
            "deleted": {"write_only": True}
        }
        read_only_fields = ("id",)

    def create(self, validate_data):
        """create user"""
        user_instance = User.objects.create_user(**validate_data)
        return user_instance

    def update(self, instance, validate_data):
        """update password current user"""
        password = validate_data.pop("password", None)
        user = super().update(instance, validate_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class RecoveryPwdSerializer(serializers.ModelSerializer):
    """send to recovery password serializers"""
    email = fields.EmailField(validators=[EmailValidator()])
    
    class Meta:
        model = User
        fields = ("email",)
    
    def create(self, validate_data):
        """send email to recovery password"""
        user_instance = get_object_or_404(User, email=validate_data.get("email"))
        uid = encode_user_id(user.id)
        token = make_user_token(user)
        return user_instance


class PwdConfirmSerializer(serializers.ModelSerializer):
    """confirm password from recovery password"""
    password = fields.CharField(
        style={"input_style": "password"},
        required=True,
    )
    password_confirm = fields.CharField(
        style={"input_style": "password"},
        required=True,
    )

    class Meta:
        model = User
        fields = ("password", "password_confirm")

    def validate(self, attrs):
        """validation data password and confirm"""
        if attrs.get("password") != attrs.get("password_confirm"):
            raise serializers.ValidationError("Those passwords don't match")
        return attrs
