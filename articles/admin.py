from django.contrib import admin
from .models import Category, Article, Comment

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']  # 카테고리 리스트에서 표시할 필드
    search_fields = ['name']  # 검색 필드 설정

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'updated_at', 'likes_count', 'category']
    search_fields = ['title', 'content']

    # 'likes_count' 필드를 계산하는 함수 추가
    def likes_count(self, obj):
        return obj.likes.count()  # 좋아요 개수 반환
    likes_count.short_description = 'Likes Count'  # Admin에서 필드 이름 지정

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['article', 'content', 'created_at', 'updated_at']
    search_fields = ['content']