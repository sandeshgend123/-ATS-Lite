from rest_framework import serializers
from django.contrib.auth.models import User
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class CustomUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['id', 'user', 'role', 'phone', 'company_name', 'bio', 'created_at', 'updated_at']


class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, max_length=150)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, min_length=8, write_only=True)
    password2 = serializers.CharField(required=True, min_length=8, write_only=True)
    first_name = serializers.CharField(required=False, max_length=150)
    last_name = serializers.CharField(required=False, max_length=150)
    role = serializers.ChoiceField(choices=['employer', 'candidate'])
    phone = serializers.CharField(required=False, max_length=20)
    company_name = serializers.CharField(required=False, max_length=255)
    bio = serializers.CharField(required=False)
    
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password': 'Passwords do not match'})
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({'username': 'Username already exists'})
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({'email': 'Email already exists'})
        return data
    
    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        role = validated_data.pop('role')
        phone = validated_data.pop('phone', None)
        company_name = validated_data.pop('company_name', None)
        bio = validated_data.pop('bio', None)
        
        user = User.objects.create_user(password=password, **validated_data)
        CustomUser.objects.create(
            user=user,
            role=role,
            phone=phone,
            company_name=company_name,
            bio=bio
        )
        return user
