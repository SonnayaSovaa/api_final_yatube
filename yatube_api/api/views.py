from posts.models import Comment, Follow, Group, Post, User
from .serializers import (
    CommentSerializer,
    FollowSerializer,
    GroupSerializer,
    PostSerializer,
    CustomUserSerializer
)
from rest_framework import filters, permissions, viewsets
from rest_framework.pagination import LimitOffsetPagination
from djoser.views import UserViewSet
from .permissions import AuthorOrReadOnly
from django.shortcuts import get_object_or_404


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer


class CommentsViewSet(viewsets.ModelViewSet):
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


class GetPostMixin:
    def get_queryset(self):
        follows = self.queryset.filter(user=self.request.user)
        follows = self.filter_queryset(follows)
        return follows

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FollowViewSet(GetPostMixin, viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated, )
    filter_backends = (filters.SearchFilter, )
    search_fields = ('=following__username', )


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
