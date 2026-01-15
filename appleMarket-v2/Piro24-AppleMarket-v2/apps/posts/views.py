
import traceback
from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import numpy as np
import cv2
from .services.ocr_service import OCRService

# Create your views here.
def main(request):
    posts = Post.objects.all()

    search_txt = request.GET.get('search_txt')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if search_txt:
        posts = posts.filter(title__icontains=search_txt)  # 대소문자 구분 없이 검색
    
    try:
        if min_price:
            posts = posts.filter(price__gte=int(min_price))
        if max_price:
            posts = posts.filter(price__lte=int(max_price))
    except (ValueError, TypeError):
        pass  # 필터를 무시하되, 기존 검색 필터를 유지

    context = {
        'posts': posts,
        'search_txt': search_txt,
        'min_price': min_price,
        'max_price': max_price,
    }
    return render(request, 'posts/list.html', context=context)

def create(request):
    if request.method == 'GET':
        form = PostForm()
        context = { 'form': form }
        return render(request, 'posts/create.html', context=context)
    else:
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('/')

def detail(request, pk):
    target_post = Post.objects.get(id = pk)
    context = { 'post': target_post }
    return render(request, 'posts/detail.html', context=context)

def update(request, pk):
    post = Post.objects.get(id=pk)
    if request.method == 'GET':
        form = PostForm(instance=post)
        context = {
            'form': form, 
            'post': post
        }
        return render(request, 'posts/update.html', context=context)
    else:
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
        return redirect('posts:detail', pk=pk)

def delete(request, pk):
    post = Post.objects.get(id=pk)
    post.delete()
    return redirect('/')

@csrf_exempt
def ocr_extract(request):
    if request.method == 'POST' and request.FILES.get('image'):
        try:
            image_file = request.FILES['image']
            
            file_bytes = np.frombuffer(image_file.read(), np.uint8)
            decoded_image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

            if decoded_image is None:
                raise ValueError("이미지 변환 실패: 손상된 파일이거나 지원하지 않는 형식입니다.")

            # 서비스 호출 (변환된 이미지를 넘김)
            service = OCRService()
            nutrient_data = service.extract_nutrient_from_image(decoded_image)

            return JsonResponse({'success': True, 'data': nutrient_data})
        except Exception as e:
            print("🚨 상세 에러 로그 시작")
            traceback.print_exc()  # 이게 진짜 에러 위치를 다 보여줍니다.
            print("🚨 상세 에러 로그 끝")
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'message': 'No image provided'})