from django.urls import re_path
from django.views.decorators.csrf import csrf_exempt

from apps.user.views import LoginView, LogoutView

urlpatterns = [
    re_path(r"^login/$", csrf_exempt(LoginView.as_view()), name="login"),
    re_path(r"^logout/$", csrf_exempt(LogoutView.as_view()), name="logout"),
]
