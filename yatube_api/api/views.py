from posts.models import Comment, Follow, Group, Post, User
from .serializers import (
    CommentSerializer,
    FollowSerializer,
    GroupSerializer,
    PostSerializer,
    CustomUserSerializer
)
from rest_framework.response import Response
from rest_framework import filters, permissions, status, viewsets
from rest_framework.pagination import LimitOffsetPagination
from djoser.views import UserViewSet
from .permissions import AuthorOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from rest_framework.mixins import CreateModelMixin
from django.shortcuts import get_object_or_404 


class GetPostMixin:
    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user = request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer


class CommentsViewSet(viewsets.ModelViewSet, CreateModelMixin):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        AuthorOrReadOnly
        )

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        return Comment.objects.filter(post_id=post_id)

    def perform_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        postt = get_object_or_404(Post, id=post_id)
        serializer.save(author=self.request.user, post=postt)


class FollowViewSet(viewsets.ModelViewSet, GetPostMixin):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated, AuthorOrReadOnly)
    filter_backends = (filters.SearchFilter, )
    search_fields = ('=following__username', )

    def get_queryset(self):
        follows = self.queryset.filter(user=self.request.user)
        follows = self.filter_queryset(follows)
        return follows

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        AuthorOrReadOnly
        )
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ('text', 'author') 

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.AllowAny,)
