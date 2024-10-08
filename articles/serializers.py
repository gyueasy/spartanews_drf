from rest_framework import serializers
from .models import Article, Comment, Category

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ["article"]

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret.pop("article")
        return ret

class ArticleSerializer(serializers.ModelSerializer):
    score = serializers.SerializerMethodField()
    likes_count = serializers.IntegerField(read_only=True) # likes ManyToManyField의 count를 직렬화하기 위해 필드 추가
    class Meta:
        model = Article
        fields = "__all__"

    def get_score(self, obj):
        return obj.calculate_score()

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
        
class ArticleDetailSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.IntegerField(source="comments.count", read_only=True)
    likes_count = serializers.IntegerField(source="likes.count", read_only=True)
    score = serializers.SerializerMethodField()
    category = CategorySerializer()  # CategorySerializer를 사용하여 category 필드를 직렬화


    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'created_at', 'updated_at', 'likes_count', 'category', 'comments', 'comments_count', 'score']

    def get_score(self, obj):
        # 객체에서 score를 계산하여 반환합니다.
        return obj.calculate_score()