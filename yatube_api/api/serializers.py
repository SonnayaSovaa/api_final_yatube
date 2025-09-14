from rest_framework import serializers
from rest_framework.relations import SlugRelatedField


from posts.models import Comment, Follow, Group, Post


class PostSerializer(serializers.ModelSerializer):
    group = serializers.SlugRelatedField(
        slug_field='slug', queryset=Group.objects.all(),
        required=False
    )
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    image = serializers.ImageField(required=False)

    class Meta:
        fields = '__all__'
        read_only_fields = ('post', )
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    post = serializers.PrimaryKeyRelatedField(read_only=True)
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        read_only_fields = ('post', 'author')
        model = Comment


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'title', 'slug', 'description')
        model = Group


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    following = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Follow
