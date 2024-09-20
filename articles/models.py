from django.db import models
from django.conf import settings
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=120)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views_count = models.PositiveIntegerField(default=0)
    link = models.URLField(null=True, blank=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_articles', blank=True)

    def __str__(self):
        return self.title

    def calculate_likes_count(self):
        return self.likes.count()

    def calculate_score(self):
        from accounts.models import User  # 지연 임포트

        now = timezone.now()
        days_since_created = (now - self.created_at).days
        max_days = 30
        recency_score = max(0, 100 - (days_since_created / max_days * 100))

        bookmark_count = User.objects.filter(bookmarked_articles=self).count()
        bookmark_score = min(bookmark_count * 2, 20)
        
        like_score = min(self.likes_count * 100, 20)
        
        total_score = recency_score + bookmark_score + like_score
        return total_score

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comments")
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
