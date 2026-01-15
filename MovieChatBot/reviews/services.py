import requests
import os
from django.conf import settings

class TMDBService:
    def __init__(self):
        # settings.py에서 가져온 API 키 (없으면 빈 문자열)
        self.api_key = settings.TMDB_API_KEY
        self.base_url = "https://api.themoviedb.org/3"

    def get_popular_movies(self, page=1):
        # TMDB 인기 영화 목록을 가져옴
        url = f"{self.base_url}/movie/popular"
        params = {
            'api_key': self.api_key,
            'language': 'ko-KR',
            'page': page
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            return response.json().get('results', [])
        return []
    
    def get_movie_detail(self, movie_id):
        # 영화 상세 정보 조회 (감독, 출연진, 러닝타임 포함)
        url = f"{self.base_url}/movie/{movie_id}"
        params = {
            'api_key': self.api_key,
            'language': 'ko-KR',
            'append_to_response': 'credits'
        }
        response = requests.get(url, params=params)
        return response.json() if response.status_code == 200 else None