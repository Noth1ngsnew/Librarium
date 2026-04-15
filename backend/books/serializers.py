from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Book, ReadingLog, Review, Badge, UserBadge


# serializers.Serializer (не ModelSerializer)

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email    = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=6)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already taken.")
        return value

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


# ModelSerializer

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Book
        fields = [
            'id', 'title', 'author', 'genre', 'description',
            'status', 'current_page', 'total_pages', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class ReadingLogSerializer(serializers.ModelSerializer):
    class Meta:
        model  = ReadingLog
        fields = ['id', 'book', 'status', 'date']
        read_only_fields = ['id', 'date']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Review
        fields = ['id', 'book', 'content', 'rating', 'created_at']
        read_only_fields = ['id', 'created_at']


class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Badge
        fields = ['id', 'name', 'icon', 'condition_key']


class UserBadgeSerializer(serializers.ModelSerializer):
    badge = BadgeSerializer(read_only=True)

    class Meta:
        model  = UserBadge
        fields = ['id', 'badge', 'earned_at']
