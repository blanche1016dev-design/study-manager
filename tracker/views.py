from django.shortcuts import render

from .models import LearningLog


def index(request):
    # 1. データベースから全ての学習記録を取得する
    logs = LearningLog.objects.all().order_by("-created_at")  # 新しい順に並び変え

    # 2. HTML（テンプレート）にデータを渡す
    context = {"logs": logs}
    return render(request, "tracker/index.html", context)
