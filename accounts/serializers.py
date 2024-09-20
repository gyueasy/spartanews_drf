from .models import User
from rest_framework import serializers
from articles.serializers import ArticleSerializer

class UserSerializer(serializers.ModelSerializer):
    bookmarked_articles = ArticleSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'nickname', 'email', 'introduction', 'profile_image', 'bookmarked_articles']

class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['profile_image']  # 이미지 필드만 처리