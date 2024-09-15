import django_filters
from .models import Article

class ArticleFilter(django_filters.FilterSet):
    # 제목을 부분 일치로 필터링
    title = django_filters.CharFilter(lookup_expr='icontains')
    
    # 작성자의 사용자 이름을 부분 일치로 필터링 (user 필드의 username을 참조)
    user_username = django_filters.CharFilter(field_name='user__username', lookup_expr='icontains')
    
    # 콘텐츠를 부분 일치로 필터링
    content = django_filters.CharFilter(lookup_expr='icontains')
    
    # 카테고리 이름을 부분 일치로 필터링 (카테고리 필드의 name을 참조)
    category = django_filters.CharFilter(field_name='category__name', lookup_expr='icontains')  # 카테고리 필터 추가

    class Meta:
        model = Article  # Article 모델을 기준으로 필터링
        fields = ['title', 'user_username', 'content', 'category']  # 필터링 가능한 필드 목록
