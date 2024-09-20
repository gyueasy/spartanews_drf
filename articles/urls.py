from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views
from .views import LikeArticleView
from accounts.views import BookmarkArticleView

app_name = "articles"
urlpatterns = [
    path("", views.ArticleListAPIView.as_view()),
    path("<int:pk>/", views.ArticleDetailAPIView.as_view()),
    path('<int:article_id>/like/', LikeArticleView.as_view()),
    path("<int:pk>/comments/", views.CommentListAPIView.as_view()),
    path("comments/<int:pk>/", views.CommentDetailAPIView.as_view()),
    path('<int:article_id>/bookmark/', BookmarkArticleView.as_view()),

]   