from django.shortcuts import get_object_or_404
from django.db.models import F
from rest_framework import status, generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    ArticleSerializer,
    ArticleDetailSerializer,
    CommentSerializer,
)
from .models import Article, Comment
from .filters import ArticleFilter

# ''' 페이지네이션 설정 '''
class ArticlePagination(PageNumberPagination):
    list_query_param = 'page'  # 페이지 번호를 나타내는 쿼리 매개변수
    page_size = 10  # 페이지당 10개의 상품을 보여줌
    page_size_query_param = 'page_size'  # URL에서 페이지 크기를 조정 가능
    max_page_size = 100  # 최대 페이지 크기

# ''' 게시글 목록 조회 및 생성 API '''
class ArticleListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ArticleFilter
    pagination_class = ArticlePagination

    def get(self, request):
        ''' 게시글 목록 조회 '''
        # 필터링 적용
        articles = Article.objects.all()
        filtered_articles = ArticleFilter(request.GET, queryset=articles).qs

        # 필터링된 결과를 동적으로 정렬
        filter_type = request.GET.get('filter_type')
        if filter_type == 'score':
            # score를 계산하여 정렬
            articles_with_scores = [(article, article.calculate_score()) for article in filtered_articles]
            articles_with_scores.sort(key=lambda x: x[1], reverse=True)
            sorted_articles = [article for article, _ in articles_with_scores]
        elif filter_type == 'old':
            # created_at 기준으로 오름차순 정렬 (오래된 순)
            sorted_articles = filtered_articles.order_by('created_at')
        else:
            # 기본 정렬: created_at 기준 내림차순 (최신 순)
            sorted_articles = filtered_articles.order_by('-created_at')

        # 페이지네이션 적용
        paginator = self.pagination_class()
        paginated_articles = paginator.paginate_queryset(sorted_articles, request)
        serializer = ArticleSerializer(paginated_articles, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    def post(self, request):
        ''' 게시글 생성 '''
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


# ''' 게시글 상세 조회, 수정, 삭제 API '''
class ArticleDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 가능

    def get_object(self, pk):
        ''' 특정 게시글 조회 '''
        return get_object_or_404(Article, pk=pk)

    def get(self, request, pk):
        ''' 게시글 상세 조회 '''
        article = self.get_object(pk)
        serializer = ArticleDetailSerializer(article)
        return Response(serializer.data)

    def put(self, request, pk):
        ''' 게시글 수정 '''
        article = self.get_object(pk)
        article_data = request.data.copy()
        serializer = ArticleDetailSerializer(article, data=article_data, partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, pk):
        ''' 게시글 삭제 '''
        article = self.get_object(pk)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# ''' 댓글 목록 조회 및 생성 API '''
class CommentListAPIView(APIView):
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 가능

    def get(self, request, pk):
        ''' 특정 게시글의 댓글 목록 조회 '''
        article = get_object_or_404(Article, pk=pk)  # 'article'을 'Article'로 수정
        comments = article.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        ''' 특정 게시글에 댓글 생성 '''
        article = get_object_or_404(Article, pk=pk)  # 'article'을 'Article'로 수정
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(article=article)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

# ''' 댓글 수정 및 삭제 API '''
class CommentDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 가능

    def get_object(self, pk):
        ''' 특정 댓글 조회 '''
        return get_object_or_404(Comment, pk=pk)

    def put(self, request, pk):
        ''' 댓글 수정 '''
        comment = self.get_object(pk)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, pk):
        ''' 댓글 삭제 '''
        comment = self.get_object(pk)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# ''' 게시글 좋아요 기능 API '''
class LikeArticleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, article_id):
        ''' 게시글 좋아요 처리 '''
        user = request.user
        article = get_object_or_404(Article, id=article_id)

        if article.likes.filter(id=user.id).exists():
            return Response({'error': '이미 좋아요를 눌렀습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        article.likes.add(user)  # ManyToManyField를 사용하여 좋아요 추가
        return Response({'message': '게시글에 좋아요를 눌렀습니다.'}, status=status.HTTP_201_CREATED)

    def delete(self, request, article_id):
        ''' 게시글 좋아요 취소 처리 '''
        user = request.user
        article = get_object_or_404(Article, id=article_id)

        if not article.likes.filter(id=user.id).exists():
            return Response({'error': '좋아요를 누르지 않았습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        article.likes.remove(user)  # ManyToManyField를 사용하여 좋아요 삭제
        return Response({'message': '게시글 좋아요가 취소되었습니다.'}, status=status.HTTP_204_NO_CONTENT)