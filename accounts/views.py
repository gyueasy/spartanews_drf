from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from .models import User
from .serializers import UserSerializer, ProfileImageSerializer
from .validators import validate_signup, validate_password_change
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.exceptions import APIException
from rest_framework.decorators import permission_classes
from rest_framework import status
from django.shortcuts import get_object_or_404
from articles.models import Article


class SignupView(APIView):
    def post(self, request):
        is_valid, err_msg_list = validate_signup(request.data)
        if not is_valid:
            return Response({'error': err_msg_list}, status=400)
        
        # 사용자 생성
        user = User.objects.create_user(
            # **request.data
            username = request.data.get('username'),
            password = request.data.get('password'),
            nickname = request.data.get('nickname'),
            email = request.data.get('email'),
        )

        # 사용자 정보 직렬화 및 JWT 토큰 생성
        serializer = UserSerializer(user)
        res_data = serializer.data
        refresh = RefreshToken.for_user(user)
        res_data["tokens"] = {
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }
        
        return Response(res_data, status=201)
    # 인증된 사용자만 접근 가능
    @permission_classes([IsAuthenticated])

    def delete(self, request):
        user = request.user
        
        # 회원 탈퇴 처리
        try:
            user.delete()
            return Response({'message': '유저 데이터가 삭제되었습니다.'}, status=200)
        except Exception as e:
            raise APIException(f"An error occurred: {str(e)}")

class SigninView(APIView):
    def post(self, request):
        username=request.data.get('username')
        password=request.data.get('password')
        user=authenticate(username=username, password=password)
        
        if not user:
            return Response({'error': '일치하는 사용자가 없습니다.'}, status=400)

        serializer=UserSerializer(user)
        res_data = serializer.data
        
        #token
        refresh = RefreshToken.for_user(user)
        refresh_token = str(refresh)
        access_token = str(refresh.access_token)
        res_data["tokens"] = {
            "access": access_token,
            "refresh": refresh_token
        }
        # res_data['access_token'] = access_token
        # res_data['refresh_token'] = refresh_token
        return Response(res_data)

class SignoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            refresh_token_str = request.data.get('refresh_token')
            if not refresh_token_str:
                return Response({'error': '리프레시토큰이 필요합니다.'}, status=400)
            
            refresh_token = RefreshToken(refresh_token_str)            
            refresh_token.blacklist()
            
            return Response({'message': '로그아웃 완료'}, status=200)
        except TokenError as e:
            raise APIException(f"Token is invalid or expired: {e}")
        except Exception as e:
            raise APIException(f"An unexpected error occurred: {e}")

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, username):
        user = User.objects.get(username=username)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, username):
        user = User.objects.get(username=username)
        user_data = request.data.copy()
        serializer = UserSerializer(user, data=user_data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

class ProfileImageView(APIView):
    permission_classes = [IsAuthenticated]  # 인증된 사용자만 접근 가능

    def put(self, request, *args, **kwargs):
        user = request.user  # 현재 로그인한 사용자
        serializer = ProfileImageSerializer(user, data=request.data, partial=True)  # 프로필 이미지만 업데이트

        if serializer.is_valid():
            serializer.save()
            return Response({'message': '프로필 이미지 변경이 완료되었습니다.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookmarkArticleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, article_id):
        user = request.user
        article = get_object_or_404(Article, id=article_id)
        
        if article in user.bookmarked_articles.all():
            return Response({'error': '이미 즐겨찾기한 게시글입니다.'}, status=status.HTTP_400_BAD_REQUEST)
        
        user.bookmarked_articles.add(article)
        return Response({'message': '게시글이 즐겨찾기에 추가되었습니다.'}, status=status.HTTP_201_CREATED)
    
    def delete(self, request, article_id):
        user = request.user
        article = get_object_or_404(Article, id=article_id)
        
        if article not in user.bookmarked_articles.all():
            return Response({'error': '즐겨찾기하지 않은 게시글입니다.'}, status=status.HTTP_400_BAD_REQUEST)
        
        user.bookmarked_articles.remove(article)
        return Response({'message': '게시글의 즐겨찾기가 취소되었습니다.'}, status=status.HTTP_204_NO_CONTENT)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        current_password = request.data.get('current_password')
        new_password = request.data.get('new_password')

        # Validate password change through the validator
        is_valid, err_msg_list = validate_password_change(user, current_password, new_password)
        if not is_valid:
            return Response({"error": err_msg_list}, status=status.HTTP_400_BAD_REQUEST)

        # Update password
        user.set_password(new_password)
        user.save()

        return Response({"message": "패스워드가 성공적으로 변경되었습니다."}, status=status.HTTP_200_OK)