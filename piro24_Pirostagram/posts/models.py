from django.db import models

class Post(models.Model):
    # 1. 작성자 (유저가 삭제되면 게시글도 삭제: CASCADE)
    # settings.AUTH_USER_MODEL을 사용하는 것이 모범 사례입니다.
    author = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='posts')
    
    # 2. 내용물 (이미지 필수, 글은 선택)
    image = models.ImageField(upload_to='posts/')
    content = models.TextField(blank=True)
    
    # 3. 날짜
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # 4. 좋아요 (유저와 M:N 관계)
    # like_users.count() 로 좋아요 개수를 셀 수 있음
    like_users = models.ManyToManyField('users.User', related_name='like_posts', blank=True)

    def __str__(self):
        return f'{self.author}의 게시글 ({self.pk})'

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey('users.User', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.content