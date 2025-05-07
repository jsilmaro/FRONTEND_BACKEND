from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer):
<<<<<<< HEAD
=======
    class Meta:
        model = CustomUser
        fields = ["email", "name", "password"]

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data["email"],
            name=validated_data["name"],
            password=validated_data["password"]
        )
        return user


class UserSerializer(serializers.ModelSerializer):
>>>>>>> cbfd5a5cd942fd8a2048e338c61911d4fb0d398d
    class Meta:
        model = CustomUser
        fields = ["email", "name", "password"]

<<<<<<< HEAD
    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data["email"],
            name=validated_data["name"],
            password=validated_data["password"]
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = CustomUser
        fields = ["id", "name", "email", "password", "avatar", "preferences"]
        extra_kwargs = {
            'password': {'write_only': True}
        }

=======
>>>>>>> cbfd5a5cd942fd8a2048e338c61911d4fb0d398d
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data["email"], password=data["password"])
        
        if not user or not user.is_active:
            raise serializers.ValidationError("Invalid credentials.")
        return data
    
    
