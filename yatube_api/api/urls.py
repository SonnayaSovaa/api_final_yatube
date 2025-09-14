from rest_framework.authtoken import views
from rest_framework.routers import SimpleRouter
from django.urls import include, path
from .views import *


router = SimpleRouter()
router.register(r'posts', PostViewSet, basename='posts-list')
router.register(r'posts/<post_id>', PostViewSet, basename='posts-single')
router.register(r'groups', GroupViewSet, basename='groups-list')
router.register(r'groups/<group_id>', GroupViewSet, basename='groups-single')
router.register(r'follow', FollowViewSet, basename='following')


urlpatterns = [
    path(r'v1/api-token-auth/', views.obtain_auth_token),
    path(r'v1/posts/<int:post_id>/comments/', post_comments_view),
    path(
        r'v1/posts/<int:post_id>/comments/<int:comment_id>/',
        single_comment_view
    ),
    path(r'v1/', include(router.urls)),

]
