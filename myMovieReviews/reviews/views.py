from django.shortcuts import render, get_object_or_404, redirect
from .forms import ReviewForm
from .models import Review

# Create your views here.
def review_list(request):
    # 1. URL에서 정렬 기준(sort)을 가져온다. 없으면 기본값은 '최신순'으로 한다.
    sort = request.GET.get('sort', 'recent') 
    
    # 2. 정렬 기준에 따라 데이터를 다르게 가져온다.
    if sort == 'rating':
        # 별점 높은 순 (-를 붙이면 내림차순)
        reviews = Review.objects.all().order_by('-rating')
    elif sort == 'running_time':
        # 러닝타임 짧은 순 (오름차순)
        reviews = Review.objects.all().order_by('running_time')
    else:
        # 기본: 최신순 (pk 역순 or created_at 역순)
        reviews = Review.objects.all().order_by('-pk')
    
    context = {
        'reviews': reviews
    }
    return render(request, 'reviews/review_list.html', context)
    # # 1. DB에서 모든 리뷰 데이터를 가져온다.
    # reviews = Review.objects.all()
    
    # # 2. 가져온 데이터를 딕셔너리 형태로 포장한다.
    # context = {
    #     'reviews': reviews
    # }
    
    # # 3. HTML 파일(템플릿)과 데이터를 합쳐서 보내준다.
    # return render(request, 'reviews/review_list.html', context)

def review_detail(request, pk):
    # pk에 해당하는 리뷰를 찾고, 없으면 404 에러를 띄웁니다 (안전장치)
    review = get_object_or_404(Review, pk=pk)
    
    context = {
        'review': review
    }
    return render(request, 'reviews/review_detail.html', context)

def review_create(request):
    if request.method == 'POST':
        # 1. 입력된 데이터를 폼에 채워넣는다.
        form = ReviewForm(request.POST)
        # 2. 유효성 검사 (빈칸은 없는지 등)
        if form.is_valid():
            # 3. 저장
            form.save()
            # 4. 리스트 페이지로 이동
            return redirect('reviews:review_list')
    else:
        # GET 요청일 때는 빈 폼을 보여준다.
        form = ReviewForm()
    
    context = {
        'form': form
    }
    return render(request, 'reviews/review_form.html', context)

def review_update(request, pk):
    review = get_object_or_404(Review, pk=pk) # 수정할 객체 가져오기

    if request.method == 'POST':
        # form에 request.POST(수정 내용)와 instance=review(기존 데이터)를 같이 넣어줌
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('reviews:review_detail', pk=review.pk)
    else:
        # 기존 정보가 채워진 폼을 보여줌
        form = ReviewForm(instance=review)

    context = {
        'form': form,
        'review': review
    }
    return render(request, 'reviews/review_form.html', context)


def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk) # 삭제할 객체 가져오기

    if request.method == 'POST':
        review.delete() # DB에서 삭제
        return redirect('reviews:review_list')
    
    return redirect('reviews:review_detail', pk=pk)