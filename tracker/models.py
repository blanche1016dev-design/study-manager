from django.db import models


class LearningLog(models.Model):
    # 1. 科目（短い文字）
    subject = models.CharField(max_length=100, verbose_name="科目")

    # 2. 学習内容（長い文章もOK）
    content = models.TextField(verbose_name="学習内容")

    # 3. 学習時間（分単位の整数）
    study_time = models.IntegerField(verbose_name="学習時間(分)")

    # 4. 作成日時（保存した瞬間に自動で現在時刻が入る）
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")

    # 5. 更新日時
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日時")

    def __str__(self):
        # 管理画面で表示される名前
        return f"{self.subject}: {self.content[:20]}..."
