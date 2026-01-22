from django.shortcuts import render
from .models import Post
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

def post_list(request):
    # 모든 게시글을 가져와서 created_at 역순(최신순)으로 정렬
    posts = Post.objects.all().order_by('-created_at')
    context = {
        'posts': posts,
    }
    return render(request, 'posts/post_list.html', context)

@login_required
@csrf_exempt # 지금은 편의상 CSRF 예외 처리 (나중엔 JS에서 토큰 보내는 게 정석)
def like_post(request):
    if request.method == 'POST':
        # 1. 프론트엔드에서 보낸 데이터(post_id) 꺼내기
        req = json.loads(request.body)
        post_id = req.get('post_id')
        
        # 2. 어떤 게시글인지 찾기
        post = Post.objects.get(id=post_id)
        
        # 3. 로직: 이미 좋아요 눌렀으면 취소, 아니면 추가
        if request.user in post.like_users.all():
            post.like_users.remove(request.user)
            liked = False
        else:
            post.like_users.add(request.user)
            liked = True
            
        # 4. 결과 돌려주기 (JSON 형식)
        context = {
            'liked': liked,
            'like_count': post.like_users.count()
        }
        return JsonResponse(context)