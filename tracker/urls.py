from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),  # 空文字=トップページ
    path("delete/<int:pk>/", views.delete_log, name="delete_log"),
    path('edit/<int:pk>/',views.edit_log,name='edit_log'),
]
