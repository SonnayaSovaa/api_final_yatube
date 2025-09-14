from rest_framework import viewsets
from rest_framework.decorators import api_view
from posts.models import Comment, Group, Post
from .serializers import *
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
# from rest_framework import authentication, permissions


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.following != request.user.username:
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        post = self.get_object()
        serializer = self.get_serializer(post, data=request.data, partial=True)
        if request.user != serializer.instance.author:
            return Response(status=status.HTTP_403_FORBIDDEN)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        post = self.get_object()
        serializer = self.get_serializer(post, data=request.data, partial=True)
        if request.user != serializer.instance.author:
            return Response(status=status.HTTP_403_FORBIDDEN)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        if request.user != post.author:
            return Response(status=status.HTTP_403_FORBIDDEN)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def create(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, serializer):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, instance):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET', 'POST'])
def post_comments_view(request, post_id):
    post = get_object_or_404(Post.objects, id=post_id)
    if request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    comments = Comment.objects.filter(post=post)
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def single_comment_view(request, post_id, comment_id):
    post = get_object_or_404(Post.objects, id=post_id)
    comment = get_object_or_404(Comment.objects, post=post, id=comment_id)
    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.user != comment.author:
        return Response(status=status.HTTP_403_FORBIDDEN)

    if request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == 'PUT' or request.method == 'PATCH':
        serializer = CommentSerializer(
            comment, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
