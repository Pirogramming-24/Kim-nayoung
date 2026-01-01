from django.db import models
from django.conf import settings

# Create your models here.
class DevTool(models.Model):
    name = models.CharField(max_length=50, verbose_name="이름")
    kind = models.CharField(max_length=50, verbose_name="종류")
    content = models.TextField(verbose_name="개발툴 설명")

    def __str__(self):
        return self.name

class Idea(models.Model):
    title = models.CharField(max_length=50, verbose_name="아이디어 명")
    image = models.ImageField(upload_to='ideas/', verbose_name="이미지") 
    content = models.TextField(verbose_name="아이디어 설명")
    interest = models.IntegerField(default=0, verbose_name="관심도")
    devtool = models.ForeignKey(DevTool, on_delete=models.CASCADE, verbose_name="예상 개발툴")
    # is_starred = models.BooleanField(default=False, verbose_name="찜 여부")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class IdeaStar(models.Model):
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, related_name='stars')