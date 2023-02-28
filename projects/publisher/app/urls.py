from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

from apps.articles.views import ArticleViewSet

router = DefaultRouter()
router.register("article", ArticleViewSet, basename="article")

urlpatterns = [
    re_path('^api/', include(router.urls)),
    re_path(r"^api/user/", include("apps.user.urls")),
]
