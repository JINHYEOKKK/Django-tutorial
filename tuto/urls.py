
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # include 함수로 polls 앱 자체의 urls.py를 프로젝트에서 사용하도록 등록
    path("polls/", include("polls.urls")),
    path("admin/", admin.site.urls),
    path("polls2/", include("polls2.urls")),
]
