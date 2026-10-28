from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from . import serializers, models
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class RegisterView(APIView):
    def post(self, request):
        serializer = serializers.RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            'created successfully'
        )





