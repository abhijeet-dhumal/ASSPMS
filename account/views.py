import os
from django.http import HttpResponsePermanentRedirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import smart_str, smart_bytes, DjangoUnicodeDecodeError
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status, generics
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from account.utils import Util
from account.models import RequestUpdateProfile, User

from account.serializers import (
    RequestUpdateProfileSerializer,
    UserSerializer,
    RegisterSerializer,
    MyTokenObtainPairSerializer,
    UserQuerySerializer,
    UserSnippetSerializer,
    SetNewPasswordSerializer,
    ResetPasswordEmailRequestSerializer,
    UserPasswordChangeSerializer,
)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class Profile(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        from oauth2_provider.models import RefreshToken
        RefreshToken.objects.exclude(revoked__isnull=True).delete()
        user = User.objects.get(id=request.user.id)
        return Response(UserSerializer(user).data)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
                'company': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
                'experience': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
                'starting_charge_price': openapi.Schema(type=openapi.TYPE_INTEGER, description='string'),
                'mode_of_service': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
                'dob': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
                'preferred_name': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
                'pronoun': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
                'location': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
                'profile_image': openapi.Schema(type=openapi.TYPE_FILE, description='string'),
            }
        ),
        responses={
            201: "created",
            400: "not valid",
        }
    )
    def post(self, request, format=None):
        data = request.data
        userSerializer = UserSerializer(request.user, data=data)
        if userSerializer.is_valid():
            userSerializer.update(request.user, userSerializer.validated_data)
            return Response(UserSerializer(request.user).data, status=201)
        return Response(userSerializer.errors, status=400)


class MyObtainTokenPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        email = request.data['email']
        is_professional = request.data['is_professional']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            if user.user_type == 'Simple User':
                if not is_professional:
                    return super().post(request, *args, **kwargs)
                else:
                    return Response({'error': 'User is not a professional user!'}, status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
            else:
                if is_professional:
                    return super().post(request, *args, **kwargs)
                else:
                    return Response({'error': 'User is a professional user!'}, status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        else:
            return Response({'detail': 'Email is not registered!'})


class Query(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='Name'),
                'pronoun': openapi.Schema(type=openapi.TYPE_STRING, description='pronoun'),
                'phone': openapi.Schema(type=openapi.TYPE_STRING, description='phone'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='email'),
                'query': openapi.Schema(type=openapi.TYPE_STRING, description='message'),
            }
        ),
        responses={
            201: "created",
            400: "not valid"
        },
        tags=['Contact Us']
    )
    def post(self, request, *args, **kwargs):
        query = UserQuerySerializer(data=request.data)
        if query.is_valid():
            query.create(query.validated_data)
            return Response(query.data, 201)
        return Response(query.errors, 400)


class Snippet(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        serializer = UserSnippetSerializer(request.user)
        return Response(serializer.data)


# forgot password


class CustomRedirect(HttpResponsePermanentRedirect):

    allowed_schemes = [os.environ.get('APP_SCHEME'), 'http', 'https']


class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data.get('email', '')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            # current_site = get_current_site(
            #     request=request).domain
            # relativeLink = reverse(
            #     'password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})

            # redirect_url = request.data.get('redirect_url', '')
            absurl = f'https://queerspotindia.com/password-reset-complete/{uidb64}/{token}'
            email_body = 'Hello, \n Use link below to reset your password  \n' + absurl
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Reset your passsword'}
            Util.send_email(data)
        return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)


class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):

        redirect_url = request.GET.get('redirect_url')

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                if len(redirect_url) > 3:
                    return CustomRedirect(redirect_url+'?token_valid=False')
                else:
                    return CustomRedirect(os.environ.get('FRONTEND_URL', '')+'?token_valid=False')

            if redirect_url and len(redirect_url) > 3:
                return CustomRedirect(redirect_url+'?token_valid=True&message=Credentials Valid&uidb64='+uidb64+'&token='+token)
            else:
                return CustomRedirect(os.environ.get('FRONTEND_URL', '')+'?token_valid=False')

        except DjangoUnicodeDecodeError as identifier:
            try:
                if not PasswordResetTokenGenerator().check_token(user):
                    return CustomRedirect(redirect_url+'?token_valid=False')

            except UnboundLocalError as e:
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_400_BAD_REQUEST)


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)


# change password

class APIChangePasswordView(generics.UpdateAPIView):
    serializer_class = UserPasswordChangeSerializer
    model = User  # your user model
    permission_classes = (IsAuthenticated,)

    def patch(self, queryset=None):
        serializer = self.get_serializer(self.request.user, data=self.request.data,
                                         context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        serializer.update(self.request.user, self.request.data)
        return Response(serializer.data)


class RequestUpdateProfileView(generics.CreateAPIView):
    serializer_class = RequestUpdateProfileSerializer
    queryset = RequestUpdateProfile.objects.all()
    permission_classes = (IsAuthenticated,)

