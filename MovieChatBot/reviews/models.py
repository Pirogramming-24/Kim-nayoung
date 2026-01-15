from django.db import models

# Create your models here.
class Review(models.Model):
    GENRE_CHOICES = [
        ('action', '액션'),
        ('romance', '로맨스'),
        ('comedy', '코미디'),
        ('thriller', '스릴러'),
        ('fantasy', '판타지'),
        ('drama', '드라마'),
    ]
    title = models.CharField(max_length=50)
    release_year = models.IntegerField()
    genre = models.CharField(max_length=30, choices=GENRE_CHOICES)
    director = models.CharField(max_length=30)
    actors = models.CharField(max_length=100)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    running_time = models.IntegerField()
    content = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.rating}점"
    
    @property
    def running_time_display(self):
        hours = self.running_time // 60  # 몫 (시간)
        minutes = self.running_time % 60 # 나머지 (분)
        
        if hours > 0:
            return f"{hours}시간 {minutes}분"
        else:
            return f"{minutes}분"