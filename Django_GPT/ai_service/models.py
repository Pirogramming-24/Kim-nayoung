# ai_service/models.py

from django.db import models
from django.contrib.auth.models import User

class AIHistory(models.Model):
    # 누가 했는지 (로그인한 유저)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # 어떤 작업인지 (translate, summarize, generate)
    task = models.CharField(max_length=50)
    # 질문 내용
    input_text = models.TextField()
    # AI 답변 내용
    output_text = models.TextField()
    # 언제 했는지 (자동 저장)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.task}] {self.user.username} - {self.created_at}"