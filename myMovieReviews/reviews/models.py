from django.db import models

# Create your models here.
class Review(models.Model):
    title = models.CharField(max_length=50)
    release_year = models.IntegerField()
    genre = models.CharField(max_length=30)
    director = models.CharField(max_length=30)
    actors = models.CharField(max_length=100)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    running_time = models.IntegerField()
    content = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.rating}점"