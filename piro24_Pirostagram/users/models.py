from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # 추가 필드: 프로필 사진, 소개글
    profile_image = models.ImageField(upload_to='profile/', blank=True)
    short_description = models.TextField(blank=True)

    # 핵심 기능: 팔로우 (User가 User를 팔로우함)
    # symmetrical=False: 내가 너를 팔로우한다고 해서, 너가 나를 팔로우하는 건 아님 (인스타 방식)
    following = models.ManyToManyField(
        'self',
        verbose_name='팔로우 중',
        symmetrical=False,
        related_name='followers',
        blank=True
    )

    def __str__(self):
        return self.username