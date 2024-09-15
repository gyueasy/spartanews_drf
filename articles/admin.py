from django.contrib import admin
from .models import Category, Article, Comment, Like

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']  # 카테고리 리스트에서 표시할 필드
    search_fields = ['name']  # 검색 필드 설정

# 다른 모델들도 어드민에 등록
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'updated_at', 'likes_count', 'category']
    search_fields = ['title', 'content']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['article', 'content', 'created_at', 'updated_at']
    search_fields = ['content']

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'article']