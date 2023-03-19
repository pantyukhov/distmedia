from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from . import views

from apps.articles.views import ArticleViewSet
from apps.xrpl.views.account import AccountViewSet
from apps.xrpl.views.subscription import SubscriptionViewSet

router = DefaultRouter()
router.register("article", ArticleViewSet, basename="article")
router.register("account", AccountViewSet, basename="account")
router.register("subscription", SubscriptionViewSet, basename="subscription")

urlpatterns = [
    path('', views.index, name="index"),
    re_path('^api/', include(router.urls)),
    re_path(r"^api/user/", include("apps.user.urls")),
]

urlpatterns += staticfiles_urlpatterns()