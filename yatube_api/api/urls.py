from rest_framework.authtoken import views
from rest_framework.routers import SimpleRouter
from django.urls import include, path
from .views import *


router = SimpleRouter()
router.register('posts', PostViewSet, basename='posts-list')
router.register('posts/<post_id>', PostViewSet, basename='posts-single')
router.register('groups', GroupViewSet, basename='groups-list')
router.register('groups/<group_id>', GroupViewSet, basename='groups-single')
router.register('follow', FollowViewSet, basename='following')


urlpatterns = [
    path('v1/api-token-auth/', views.obtain_auth_token),
    path('v1/posts/<int:post_id>/comments/', post_comments_view),
    path(
        'v1/posts/<int:post_id>/comments/<int:comment_id>/',
        single_comment_view
    ),
    path('v1/', include(router.urls)),

]
