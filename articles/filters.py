import django_filters
from .models import Article

class ArticleFilter(django_filters.FilterSet):
    # 제목을 부분 일치로 필터링
    title = django_filters.CharFilter(lookup_expr='icontains')
    
    # 작성자의 사용자 이름을 부분 일치로 필터링
    user_username = django_filters.CharFilter(field_name='user__username', lookup_expr='icontains')
    
    # 콘텐츠를 부분 일치로 필터링
    content = django_filters.CharFilter(lookup_expr='icontains')
    
    # 카테고리 이름을 부분 일치로 필터링
    category = django_filters.CharFilter(field_name='category__name', lookup_expr='icontains')
    
    old = django_filters.BooleanFilter(field_name='created_at', method='filter_by_old')

    def filter_by_old(self, queryset, name, value):
        if value:
            return queryset.order_by('created_at')  # 오름차순 (오래된 순)
        return queryset.order_by('-created_at')  # 내림차순 (최신순)

    class Meta:
        model = Article
        fields = ['title', 'user_username', 'content', 'category', 'old']