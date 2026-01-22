# 나만의 AI 사이트 (Django)

---
## 사용 모델 (3개 이상)

### 1. Helsinki-NLP/opus-mt-ko-en
-**태스크**: Translation (한영 번역)
-**입력 예시**
안녕하세요, 오늘 날씨가 참 좋네요.
-**출력 예시**
Good morning. Good day.
- 실행 화면 예시
<img width="506" height="469" alt="Image" src="https://github.com/user-attachments/assets/020a0919-2aca-423b-8ad9-c48440e72573" />


### 2. sshleifer/distilbart-cnn-12-6
-**태스크**: Summarization (영어 문서 요약)
-**입력 예시**
It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text, and a search for 'lorem ipsum' will uncover many web sites still in their infancy. Various versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).
-**출력 예시**
Many desktop publishing packages and web page editors now use Lorem Ipsum as their default model text . Various versions have evolved over the years, sometimes by accident, sometimes on purpose.
- 실행 화면 예시
<img width="488" height="739" alt="Image" src="https://github.com/user-attachments/assets/07fa7c0e-4fbe-4ba1-90c8-e0fd754dd421" />

### 3. google/flan-t5-base
-**태스크**: Text Generation (텍스트 생성, 이어쓰기)
-**입력 예시**
I want to
-**출력 예시**
watch a movie with my friends.
- 실행 화면 예시
<img width="485" height="456" alt="Image" src="https://github.com/user-attachments/assets/3102b076-b4ef-4f06-a5ff-80fd205ab880" />

---
## 로그인 제한(Access Control)

- 비로그인 사용자는**1개 탭만 사용 가능**
- 제한 탭 접근 시**“로그인 후 이용해주세요” alert 후 로그인 페이지로 이동**
- 로그인 성공 시**원래 페이지로 복귀(next)**

---
## 구현 체크리스트

- [x] 탭 3개 이상 + 각 탭 별 URL 분리
- [x] 각 탭: 입력 → 실행 → 결과 출력
- [x] 에러 처리: 모델 호출 실패 시 사용자에게 메시지 표시
- [x] 로딩 표시(최소한 “처리 중…” 텍스트라도)
- [x] 요청 히스토리 5개
- [x] `.env` 사용 (토큰/API Key 노출 금지)
- [x] `README.md`에 모델 정보/사용 예시/실행 방법 작성 후 GitHub push

### 로그인 제한 체크
- [x] 비로그인 사용자는 1개 탭만 접근 가능
- [x] 제한 탭 접근 시 alert 후 로그인 페이지로 redirect
- [x] 로그인 성공 시 원래 페이지로 복귀(next)

---
## 🛠 실행 방법 (How to Run)

**1. 가상환경 생성 및 활성화**

```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
# venv\Scripts\activate  # Windows

```

**2. 패키지 설치**

```bash
pip install django python-dotenv torch transformers sentencepiece accelerate

```

**3. 마이그레이션 (DB 생성)**

```bash
python manage.py makemigrations
python manage.py migrate

```

**4. 서버 실행**

```bash
python3 manage.py runserver

```