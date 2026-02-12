from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),  # 空文字=トップページ
]
