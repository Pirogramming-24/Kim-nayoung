import os
import django
from pathlib import Path
from dotenv import load_dotenv

# 1. Django 환경 설정 (DB 접근을 위해 필수)
import sys
# 현재 파일 위치 기준으로 프로젝트 루트를 찾음
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

# 2. 필요한 모듈 임포트
from reviews.models import Review  # 내 영화 모델 가져오기
from langchain_core.documents import Document
from langchain_upstage import UpstageEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

VS_DIR = BASE_DIR / "vector_store"  # 벡터 DB 저장 위치

def build_index():
    print("🎬 영화 데이터 로딩 중...")
    movies = Review.objects.all()
    
    if not movies.exists():
        print("⚠️ 저장된 영화 데이터가 없습니다. 먼저 데이터를 채워주세요.")
        return

    docs = []
    for movie in movies:
        # RAG가 이해하기 좋게 텍스트로 변환
        content = (
            f"영화 제목: {movie.title}\n"
            f"장르: {movie.get_genre_display()}\n"
            f"개봉년도: {movie.release_year}\n"
            f"감독: {movie.director}\n"
            f"주연: {movie.actors}\n"
            f"평점: {movie.rating}\n"
            f"줄거리 및 리뷰: {movie.content}"
        )
        # 메타데이터에는 출처 표시
        metadata = {"source": "MovieDB", "title": movie.title}
        docs.append(Document(page_content=content, metadata=metadata))

    print(f"📚 총 {len(docs)}개의 영화 정보를 변환했습니다.")

    # 텍스트 청크 (영화 정보는 보통 짧아서 chunk_size를 크게 안 해도 됨)
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    splits = splitter.split_documents(docs)

    # 임베딩 & 벡터DB 저장
    print("💾 벡터 DB에 저장 중... (Upstage Embeddings)")
    embeddings = UpstageEmbeddings(model="solar-embedding-1-large")
    
    # 기존 DB가 있다면 덮어쓰거나 새로 만듦
    if os.path.exists(VS_DIR):
        import shutil
        shutil.rmtree(VS_DIR) # 깨끗하게 지우고 다시 생성 (선택사항)

    Chroma.from_documents(
        documents=splits,
        embedding=embeddings,
        persist_directory=str(VS_DIR),
    )
    print(f"✅ 인덱싱 완료! 저장 경로: {VS_DIR}")

if __name__ == "__main__":
    build_index()