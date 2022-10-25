from rest_framework import serializers
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from account.models import RequestUpdateProfile, User, UserQuery
from django.core.files.uploadedfile import UploadedFile
from io import BytesIO
import requests
import os
from account.utils import Base64ImageField

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[
                                   UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'name', 'company', 'experience', 'starting_charge_price', 'mode_of_service',
                  'dob', 'preferred_name', 'user_type', 'pronoun', 'location', 'description', 'profile_image')
        extra_kwargs = {
            'name': {'required': True},
            'user_type': {'required': True}
        }

    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data.get('email'),
            name=validated_data.get('name'),
            company=validated_data.get('company'),
            experience=validated_data.get('experience'),
            starting_charge_price=validated_data.get('starting_charge_price'),
            mode_of_service=validated_data.get('mode_of_service'),
            user_type=validated_data.get('user_type'),
            dob=validated_data.get('dob'),
            preferred_name=validated_data.get('preferred_name'),
            pronoun=validated_data.get('pronoun'),
            location=validated_data.get('location'),
            description=validated_data.get('description')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    is_professional = serializers.BooleanField(required=True)

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        token['email'] = user.email
        return token


class UserSerializer(serializers.ModelSerializer):
    profile_image_url = serializers.CharField(required=False, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'company', 'experience', 'starting_charge_price', 'mode_of_service',
                  'dob', 'preferred_name', 'user_type', 'pronoun', 'location', 'description', 'profile_image', 'profile_image_url')
        extra_kwargs = {
            'email': {'required': False},
            'password': {'required': False}
        }

    def update(self, obj, validated_data):
        if 'profile_image_url' in validated_data:
            url = validated_data['profile_image_url']
            name = os.path.basename(url)
            r= requests.get(url)
            validated_data['profile_image'] = UploadedFile(
                BytesIO(r.content), name=name)
            validated_data.pop('profile_image_url')

        obj.name = validated_data.get('name', obj.name)
        obj.user_type = validated_data.get('user_type', obj.user_type)
        obj.company = validated_data.get('company', obj.company)
        obj.experience = validated_data.get('experience', obj.experience)
        obj.starting_charge_price = validated_data.get(
            'starting_charge_price', obj.starting_charge_price)
        obj.mode_of_service = validated_data.get(
            'mode_of_service', obj.mode_of_service)
        obj.dob = validated_data.get('dob', obj.dob)
        obj.preferred_name = validated_data.get(
            'preferred_name', obj.preferred_name)
        obj.pronoun = validated_data.get('pronoun', obj.pronoun)
        obj.location = validated_data.get('location', obj.location)
        obj.description = validated_data.get('description', obj.description)
        obj.profile_image = validated_data.get(
            'profile_image', obj.profile_image)
        obj.save()
        return obj


class UserQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserQuery
        fields = '__all__'

    def create(self, validated_data):
        userQuery = UserQuery.objects.create(
            name=validated_data.get('name'),
            pronoun=validated_data.get('pronoun'),
            phone=validated_data.get('phone'),
            email=validated_data.get('email'),
            query=validated_data.get('query'),
            status="New"
        )
        return userQuery


class UserSnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'preferred_name',
                  'pronoun', 'user_type', 'profile_image']

# reset password


class SetNewPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2, required=True)
    old_password = serializers.CharField(
        min_length=6, max_length=68, write_only=True)
    new_password = serializers.CharField(
        min_length=6, max_length=68, write_only=True,validators=[validate_password])

    class Meta:
        model = User
        fields = ['email', 'old_password', 'new_password']


# forgot password serializers


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    redirect_url = serializers.CharField(max_length=500, required=False)

    class Meta:
        fields = ['email']


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=6, max_length=68, write_only=True, validators=[validate_password])
    token = serializers.CharField(
        min_length=1, write_only=True)
    uidb64 = serializers.CharField(
        min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)

            user.set_password(password)
            user.save()

            return (user)
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)
        return super().validate(attrs)


# change password


class UserPasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, max_length=30)
    password = serializers.CharField(
        required=True, max_length=30, validators=[validate_password])
    confirmed_password = serializers.CharField(
        required=True, max_length=30, validators=[validate_password])

    def validate(self, data):
        # add here additional check for password strength if needed
        if not self.context['request'].user.check_password(data.get('old_password')):
            raise serializers.ValidationError(
                {'old_password': 'Wrong password.'})

        if data.get('confirmed_password') != data.get('password'):
            raise serializers.ValidationError(
                {'password': 'Password must be confirmed correctly.'})

        return data

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance

    def create(self, validated_data):
        pass

    @property
    def data(self):
        # just return success dictionary. you can change this to your need, but i dont think output should be user data after password change
        return {'detail': 'Your Password Changed Successfully!'}

class RequestUpdateProfileSerializer(serializers.ModelSerializer):
    profile_image = Base64ImageField(
        max_length=None, use_url=True,
    )
    class Meta:
        model = RequestUpdateProfile
        fields = "__all__"
        extra_kwargs = {
            'id': {'read_only': True},
            'profie_image': {'read_only': True},
        }

