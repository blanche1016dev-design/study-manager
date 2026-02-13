import datetime

from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render

from .forms import LeaningLogForm
from .models import Goal, LearningLog


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

    logs = LearningLog.objects.all().order_by("-created_at")
    # 3. 今月の合計時間を計算する
    now = datetime.datetime.now()

    # 今月のデータだけを絞り込み、study_tijme を合計（Sum）する
    total = LearningLog.objects.filter(
        created_at__year=now.year, created_at__month=now.month
    ).aggregate(Sum("study_time"))

    # 結果を取り出す（データが空なら、Noneになるので０にする）
    total_time = total["study_time__sum"] or 0

    # データベースから最新の目標設定を1つ取ってくる
    latest_goal = Goal.objects.last()

    if latest_goal:
        # 設定があればその数値を使う
        goal_time = latest_goal.target_time
    else:
        goal_time = 1200

    # 進捗率（％）を計算
    if goal_time > 0:
        progress_rate = int(total_time / goal_time) * 100
    else:
        progress_rate = 0

    # 100%を超えたら100%にする（見た目のため）
    display_rate = min(progress_rate, 100)

    # 残り時間を計算
    remaining_time = max(goal_time - total_time, 0)

    context = {
        "logs": logs,
        "form": form,
        "total_time": total_time,
        "goal_time": goal_time,
        "progress_rate": progress_rate,
        "display_rate": display_rate,
        "remaining_time": remaining_time,
    }
    return render(request, "tracker/index.html", context)


def delete_log(request, pk):
    # データを1つ特定する（見つからなかったら404エラーを出す）
    log = get_object_or_404(LearningLog, pk=pk)

    # 削除を実行
    log.delete()

    # 一覧ページに戻る
    return redirect("index")


def edit_log(request, pk):
    # 1. 編集したいデータを特定する（Modelにお願い）
    log = get_object_or_404(LearningLog, pk=pk)

    # 2. 【2周目】修正データが送られてきたとき（POST）
    if request.method == "POST":
        # フォームに「送られてきたデータ」と「元のデータ（instance）」を渡す
        form = LeaningLogForm(request.POST, instance=log)
        if form.is_valid():
            form.save()  # 上書き保存
            return redirect("index")

    # 3 【1周目】最初に編集ページを開いたとき（GET）
    else:
        # フォームに「元のデータ（instance）」を入れておく（これが初期値になる）
        form = LeaningLogForm(instance=log)

        # 4 編集画面を表示（Templateへ）
        context = {
            "form": form,
            "log": log,  # "○○の編集"と表示するためにデータも渡す
        }
        return render(request, "tracker/edit.html", context)
