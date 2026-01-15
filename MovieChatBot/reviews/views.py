import requests
from django.shortcuts import render, get_object_or_404, redirect
from django.core.files.base import ContentFile
from .forms import ReviewForm
from .models import Review
from .services import TMDBService
from django.db.models import Q

def fetch_and_save_tmdb():
    tmdb_service = TMDBService()
    popular_movies = tmdb_service.get_popular_movies(page=1)

    # 장르 매핑 (models.py의 choices와 일치시킴)
    genre_map = {
        28: 'action', 12: 'action', 10752: 'action',
        35: 'comedy',
        10749: 'romance',
        53: 'thriller', 27: 'thriller', 9648: 'thriller', 80: 'thriller',
        14: 'fantasy', 878: 'fantasy', 16: 'fantasy',
        18: 'drama', 99: 'drama', 10751: 'drama', 36: 'drama'
    }

    count = 0
    for movie_basic in popular_movies:
        # 이미 DB에 있는 영화면 건너뜀 (중복 방지)
        if Review.objects.filter(title=movie_basic['title']).exists():
            continue

        # 상세 정보 요청
        movie_detail = tmdb_service.get_movie_detail(movie_basic['id'])
        if not movie_detail:
            continue

        # 1) 감독
        director = "정보 없음"
        if 'credits' in movie_detail and 'crew' in movie_detail['credits']:
            for person in movie_detail['credits']['crew']:
                if person['job'] == 'Director':
                    director = person['name']
                    break
        
        # 2) 주연 (3명)
        actors = []
        if 'credits' in movie_detail and 'cast' in movie_detail['credits']:
            for person in movie_detail['credits']['cast'][:3]:
                actors.append(person['name'])
        actors_str = ", ".join(actors) if actors else "정보 없음"

        # 3) 장르
        tmdb_genre_ids = movie_basic.get('genre_ids', [])
        my_genre = genre_map.get(tmdb_genre_ids[0], 'drama') if tmdb_genre_ids else 'drama'

        # 4) 기타 정보
        release_date = movie_detail.get('release_date', '')
        release_year = int(release_date.split('-')[0]) if release_date else 2024
        rating = round(movie_detail.get('vote_average', 0) / 2, 1)
        running_time = movie_detail.get('runtime', 0)

        # 객체 생성
        new_review = Review(
            title=movie_detail['title'],
            content=movie_detail.get('overview', ''),
            release_year=release_year,
            genre=my_genre,
            director=director,   # 실제 감독 이름
            actors=actors_str,   # 실제 배우 이름
            rating=rating,
            running_time=running_time,
            is_tmdb=True
        )

        # 포스터 저장
        poster_path = movie_detail.get('poster_path')
        if poster_path:
            image_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
            image_res = requests.get(image_url)
            if image_res.status_code == 200:
                file_name = f"{new_review.title}_poster.jpg"
                new_review.poster.save(file_name, ContentFile(image_res.content), save=False)

        new_review.save()
        count += 1
    
    return count

# ---------------------------------------------------------
# [View 함수]
# ---------------------------------------------------------
def review_list(request):
    sort = request.GET.get('sort', 'recent')
    source = request.GET.get('source', 'all')
    q = request.GET.get('q', '')

    # 사용자가 'TMDB' 버튼을 눌렀는데(source=='tmdb'),
    # 아직 DB에 TMDB 영화가 하나도 없다면? -> 자동으로 가져온다!
    if source == 'tmdb':
        if Review.objects.count() == 0:
            fetch_and_save_tmdb()
            
    # 1. 전체 데이터 준비
    reviews = Review.objects.all()

    if q:
        reviews = reviews.filter(
            Q(title__icontains=q) |
            Q(director__icontains=q) |
            Q(actors__icontains=q)
        )

    # 2. 필터링
    if source == 'tmdb':
        # TMDB 탭: 데이터 없으면 가져오고, is_tmdb=True인 것만 보여줌
        if not Review.objects.filter(is_tmdb=True).exists():
            fetch_and_save_tmdb()
        reviews = reviews.filter(is_tmdb=True)

    elif source == 'manual':
        # 직접 쓴 리뷰: is_tmdb=False인 것만
        reviews = reviews.filter(is_tmdb=False)
    
    # 3. 정렬
    if sort == 'rating':
        reviews = reviews.order_by('-rating')
    elif sort == 'running_time':
        reviews = reviews.order_by('running_time')
    else:
        reviews = reviews.order_by('-pk')
    
    context = {
        'reviews': reviews,
        'sort': sort,
        'source': source,
        'q': q,
    }
    return render(request, 'reviews/review_list.html', context)

def review_detail(request, pk):
    review = get_object_or_404(Review, pk=pk)
    context = {'review': review}
    return render(request, 'reviews/review_detail.html', context)

def review_create(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('reviews:review_list')
    else:
        form = ReviewForm()
    context = {'form': form}
    return render(request, 'reviews/review_form.html', context)

def review_update(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES, instance=review)
        if form.is_valid():
            form.save()
            return redirect('reviews:review_detail', pk=review.pk)
    else:
        form = ReviewForm(instance=review)
    context = {'form': form, 'review': review}
    return render(request, 'reviews/review_form.html', context)

def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.method == 'POST':
        review.delete()
        return redirect('reviews:review_list')
    return redirect('reviews:review_detail', pk=pk)