# 1. 파이썬 3.10 버전의 리눅스 환경을 가져온다 (가볍고 빠른 slim 버전)
FROM python:3.10-slim

# 2. 컨테이너 내부에서 작업할 폴더를 정한다
WORKDIR /app

# 3. 파이썬이 .pyc 파일을 생성하지 않도록 하고, 로그를 즉시 출력하게 설정 (도커 최적화)
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 4. 필수 패키지 설치 (이미지 처리용 라이브러리 등)
RUN apt-get update && apt-get install -y \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# 5. 내 컴퓨터의 requirements.txt를 컨테이너로 복사하고 설치
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 6. 내 프로젝트의 모든 코드를 컨테이너로 복사
COPY . /app/

# 7. 장고 서버가 사용할 8000번 포트를 열어둠
EXPOSE 8000

# 8. 컨테이너가 시작될 때 실행할 명령어 (runserver 0.0.0.0:8000)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]