from django.contrib import auth
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework import generics, status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from .serializers import SignUpSerializer, UserActivationSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from .models import User
import jwt
from django.conf import settings
from rest_framework.permissions import AllowAny, IsAuthenticated
from datetime import timedelta
from django.core.mail import send_mail
from drf_spectacular.utils import extend_schema


class RegisterAPIView(generics.GenericAPIView):
    serializer_class = SignUpSerializer
    permission_classes = [AllowAny]

    @extend_schema(
            summary="Registration",
            description="This endpoint allows you to register by providing email, username and password",
    )

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relative_link = reverse('email-verification')
        abs_url = 'http://'+current_site+relative_link+"?token="+str(token)
        subject = 'Verify your email'
        message = 'Hi '+user.username + \
            ' Use the link below to verify your email \n' + abs_url
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email, ]
        send_mail(subject, message, email_from, recipient_list)
        return Response(user_data, status=status.HTTP_201_CREATED)


class EmailVerificationAPIView(APIView):
    serializer_class = UserActivationSerializer

    @extend_schema(
            summary="Email Verification",
            description="This endpoint allows user to activate their account using the token sent by email",
    )

    def get(self, request):
        token = request.GET.get('token')
        print(token)
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    @extend_schema(
            summary="Login",
            description="This endpoint allows users to post their username and password and get access token for logging in",
    )

    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        user = auth.authenticate(username=username, password=password)
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        if not user.is_active:
            raise AuthenticationFailed('Account is disabled, contact admin')
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified, please activate')

        return Response(
            {
                'email': user.email,
                'username': user.username,
                'tokens': user.tokens()
            }, status=status.HTTP_200_OK
        )



