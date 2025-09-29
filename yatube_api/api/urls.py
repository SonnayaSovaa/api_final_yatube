from rest_framework.routers import SimpleRouter
from django.urls import include, path
from .views import (
    CommentsViewSet,
    GroupViewSet,
    FollowViewSet,
    PostViewSet,
)


router = SimpleRouter()
router.register(r'posts', PostViewSet, basename='posts')
router.register(r'groups', GroupViewSet, basename='groups')
router.register(r'follow', FollowViewSet, basename='following')
router.register(
    r'posts/(?P<post_id>\d+)/comments',
    CommentsViewSet,
    basename='comments'
)



urlpatterns = [
    path(r'', include('djoser.urls.jwt')),
    path(r'', include(router.urls)),

]
