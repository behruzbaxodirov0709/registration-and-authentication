from rest_framework import serializers
from . import models
import re
from django.core.mail import send_mail
from django.conf import settings






class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirmation_password = serializers.CharField(write_only=True)
    class Meta:
        model = models.CustomUser
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'auth_type', 'image', 'address', 'language', 'created_at', 'password', 'confirmation_password']
        read_only_fields = ['id', 'created_at'] 


    def validate_email(self, email):
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.fullmatch(pattern=pattern, string=email):
            raise serializers.ValidationError(
                detail={
                    "message": (
                    "Email noto'g'ri formatda kiritildi. "
                    "Masalan: example@gmail.com"
                    )
                }
            )
        
        return email


    def validate(self, attrs):
        password = attrs.get('password')
        confirmation_password = attrs.get('confirmation_password')

        if password != confirmation_password:
            raise serializers.ValidationError({
                "confirm_password": "Kiritilgan parollar bir-biriga mos kelmadi."
            })

        errors = []
        if len(password) < 8:
            errors.append("Parol kamida 8 ta belgidan iborat bo'lishi kerak.")
        if not any(char.isdigit() for char in password):
            errors.append("Parolda kamida bitta raqam qatnashishi kerak.")
        if not any(char.isalpha() for char in password):
            errors.append("Parolda kamida bitta harf qatnashishi kerak.")

        if errors:
            raise serializers.ValidationError({"password": errors})

        return attrs


    def create(self, validated_data):
        validated_data.pop('confirmation_password')
        user = models.CustomUser.objects.create_user(**validated_data)

        emial_object = models.EmailOTP.objects.create(user=user)

        send_mail(
            subject="Kissa — Tasdiqlash kodi",
            message=f"Sizning tasdiqlash kodingiz: {emial_object.code}",
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'bekzodovich0709@gmail.com'),
            recipient_list=[user.email],
            fail_silently=False,
        )

        return user