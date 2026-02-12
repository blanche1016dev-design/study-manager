from django.shortcuts import get_object_or_404, redirect, render

from .forms import LeaningLogForm
from .models import LearningLog


def index(request):
    # 1. 送信ボタンが押されたとき（POSTメソッド）
    if request.method == "POST":
        form = LeaningLogForm(request.POST)
        if form.is_valid():  # 中身が正しいかチェック
            form.save()  # 保存
            return redirect("index")  # 自分自身のページにリダイレクト（二重送信防止）

    # 2. 普通にページを開いたとき（GETメソッド）
    else:
        form = LeaningLogForm()  # 空のフォームを作る

    # 3. データを取得して表示
    logs = LearningLog.objects.all().order_by("-created_at")

    context = {
        "logs": logs,
        "form": form,  # フォームも画面に渡す
    }
    return render(request, "tracker/index.html", context)


def delete_log(request, pk):
    # データを1つ特定する（見つからなかったら404エラーを出す）
    log = get_object_or_404(LearningLog, pk=pk)

    # 削除を実行
    log.delete()

    # 一覧ページに戻る
    return redirect("index")
