from django.urls import include, path
from . import views
from .views import SignupView, SigninView, SignoutView, ChangePasswordView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.SignupView.as_view()),
    path('login/', views.SigninView.as_view()),
    path('logout/', views.SignoutView.as_view()),
    path('password/', ChangePasswordView.as_view()),
    path("<str:username>/", views.UserProfileView.as_view()),
    path("<str:username>/profile_image/", views.ProfileImageView.as_view()),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)