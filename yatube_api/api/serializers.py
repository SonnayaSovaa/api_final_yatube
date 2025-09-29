from rest_framework import serializers
from posts.models import Comment, Follow, Group, Post, User
from djoser.serializers import UserSerializer
from posts.models import Follow
from rest_framework.validators import UniqueTogetherValidator


class CustomUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Group


class PostSerializer(serializers.ModelSerializer):
    group = serializers.SlugRelatedField(
        slug_field='id', queryset=Group.objects.all(),
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
        read_only=True, slug_field='username',  required=False
    )

    class Meta:
        fields = '__all__'
        read_only_fields = ('post', 'author')
        model = Comment


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        queryset=User.objects.all(),

        slug_field='username',  required=False
    )
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username',
    )

    def validate_following(self, value):
        if value == self.context['request'].user:
            raise serializers.ValidationError("Нельзя подписаться на себя")
        return value

    def validate(self, attrs):
        user = self.context['request'].user
        following = attrs['following']

        try:
            Follow.objects.get(user=user, following=following)
            raise serializers.ValidationError(
                "Пользователь уже подписан на указанного автора."
            )
        except Follow.DoesNotExist:
            pass

        return attrs

    class Meta:
        fields = ('user', 'following')
        model = Follow
        read_only_fields = ('user', )
