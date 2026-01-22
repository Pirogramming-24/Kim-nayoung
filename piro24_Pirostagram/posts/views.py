from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment, Story
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .forms import PostForm, StoryForm
from django.db.models import Q

@login_required(login_url='users:login')
def post_list(request):
    # 1. 내가 팔로우한 유저들 가져오기
    followings = request.user.following.all()
    
    # 2. 작성자가 '내 팔로잉'에 속하거나(OR) '나'인 게시글만 가져오기
    posts = Post.objects.filter(
        Q(author__in=followings) | Q(author=request.user)
    ).order_by('-created_at')
    
    one_day_ago = timezone.now() - timedelta(days=1)

    stories = Story.objects.filter(
        Q(author__in=followings) | Q(author=request.user), # 나 + 친구들 포함
        created_at__gte=one_day_ago 
    ).order_by('created_at')

    context = {
        'posts': posts,
        'stories': stories,
    }
    return render(request, 'posts/post_list.html', context)

# 게시글 수정
@login_required
def post_update(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    # 작성자 체크 (본인이 아니면 튕겨냄)
    if post.author != request.user:
        return redirect('posts:post_list')

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post) # instance=post 필수
        if form.is_valid():
            form.save()
            return redirect('posts:post_list')
    else:
        form = PostForm(instance=post)
    
    return render(request, 'posts/post_form.html', {'form': form})

# 게시글 삭제
@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if post.author == request.user:
        post.delete()
        
    return redirect('posts:post_list')

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
    
@login_required
@csrf_exempt
def add_comment(request):
    if request.method == 'POST':
        req = json.loads(request.body)
        post_id = req.get('post_id')
        content = req.get('content')
        
        post = Post.objects.get(id=post_id)
        
        # 댓글 생성
        comment = Comment.objects.create(
            post=post,
            author=request.user,
            content=content
        )
        
        # 생성된 댓글 정보를 JSON으로 리턴
        return JsonResponse({
            'id': comment.id,
            'content': comment.content,
            'author': comment.author.username
        })
    
@login_required
@csrf_exempt
def comment_delete(request):
    if request.method == 'POST':
        req = json.loads(request.body)
        comment_id = req.get('comment_id')
        
        comment = get_object_or_404(Comment, id=comment_id)
        
        # 댓글 작성자거나, 게시글 작성자면 삭제 가능 권한 부여
        if comment.author == request.user or comment.post.author == request.user:
            comment.delete()
            return JsonResponse({'message': 'success', 'comment_id': comment_id})
        else:
            return JsonResponse({'message': 'error'}, status=403)
        
@login_required
@csrf_exempt
def comment_update(request):
    if request.method == 'POST':
        req = json.loads(request.body)
        comment_id = req.get('comment_id')
        new_content = req.get('content')
        
        comment = get_object_or_404(Comment, id=comment_id)
        
        # 댓글 작성자만 수정 가능
        if comment.author == request.user:
            comment.content = new_content
            comment.save()
            return JsonResponse({'message': 'success', 'content': comment.content})
        return JsonResponse({'message': 'error'}, status=403)
    
@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES) # 이미지 파일은 request.FILES에 있음 (중요!)
        if form.is_valid():
            post = form.save(commit=False) # DB 저장 잠시 대기
            post.author = request.user     # 작성자 정보 채워넣기
            post.save()                    # 최종 저장
            return redirect('posts:post_list') # 저장 후 메인으로 이동
    else:
        form = PostForm() # GET 요청이면 빈 폼 보여주기
        
    return render(request, 'posts/post_form.html', {'form': form})

@login_required
def story_create(request):
    if request.method == 'POST':
        form = StoryForm(request.POST, request.FILES)
        if form.is_valid():
            story = form.save(commit=False)
            story.author = request.user
            story.save()
            return redirect('posts:post_list')
    else:
        form = StoryForm()
    return render(request, 'posts/story_form.html', {'form': form})

def story_view(request, story_id):
    story = get_object_or_404(Story, id=story_id)
    return render(request, 'posts/story_view.html', {'story': story})