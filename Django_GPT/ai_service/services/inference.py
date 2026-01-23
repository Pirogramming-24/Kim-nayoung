import torch
from transformers import pipeline
from django.conf import settings

class AIModelHandler:
    _instance = None
    _pipelines = {}

    # Singleton 패턴: 모델을 메모리에 한 번만 로드하기 위함
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AIModelHandler, cls).__new__(cls)
        return cls._instance

    def _get_pipeline(self, task, model_name):
        """파이프라인을 로드하거나 캐시된 것을 반환"""
        key = f"{task}_{model_name}"
        if key not in self._pipelines:
            print(f"🔄 모델 로딩 중... ({model_name})")
            # GPU가 있으면 쓰고, 없으면 CPU 사용 (device=-1)
            device = 0 if torch.cuda.is_available() else -1
            # Mac(M1/M2) 사용자는 mps 사용 가능 시 처리 (선택사항)
            if torch.backends.mps.is_available():
                device = "mps"
            
            self._pipelines[key] = pipeline(task, model=model_name, device=device)
        
        return self._pipelines[key]

    def translate(self, text, target_lang="en"):
        """
        번역 기능
        - target_lang="en": 한글 -> 영어
        - target_lang="ko": 영어 -> 한글
        """
        if target_lang == "en":
            # 한->영: Helsinki-NLP (가벼움)
            model = "Helsinki-NLP/opus-mt-ko-en"
        else:
            # 영->한: Helsinki-NLP (가벼움, MBART보다 훨씬 빠름)
            model = "Helsinki-NLP/opus-mt-en-ko"
        
        translator = self._get_pipeline("translation", model)
        result = translator(text, max_length=512)
        return result[0]['translation_text']

    def summarize(self, text):
        """
        요약 기능 (영어 뉴스 요약에 특화)
        모델: sshleifer/distilbart-cnn-12-6 (가볍고 성능 준수)
        """
        model = "sshleifer/distilbart-cnn-12-6"
        summarizer = self._get_pipeline("summarization", model)
        
        # 입력 텍스트가 너무 짧으면 그냥 반환
        if len(text) < 50:
            return "문장이 너무 짧아 요약할 수 없습니다."

        result = summarizer(text, max_length=130, min_length=30, do_sample=False)
        return result[0]['summary_text']

    def generate(self, text):
        """
        텍스트 생성 기능
        모델: google/flan-t5-base
        """
        model = "google/flan-t5-base"
        generator = self._get_pipeline("text2text-generation", model)
        
        # 1. 입력 텍스트를 명확한 '명령어' 형태로 바꿈
        # 예: "Apple is" -> "Continue the following sentence: Apple is"
        input_prompt = f"Continue the following text: {text}"

        result = generator(
            input_prompt,
            max_new_tokens=150,     # 너무 길면 헛소리할 확률이 높으니 적당히 조절
            do_sample=True,         # 확률적 샘플링 (매번 조금 다른 결과)
            temperature=0.8,        # 창의성 수치 (높을수록 다양함, 낮으면 기계적)
            top_p=0.9,              # 상위 90% 확률 내에서 단어 선택
            repetition_penalty=1.5, # ⭐ 핵심: 반복 패널티 (같은 단어 쓰면 점수 깎음)
            no_repeat_ngram_size=3  # ⭐ 핵심: 3단어 이상 똑같은 구절 반복 금지
        )
        
        return result[0]['generated_text']

# 외부에서 쉽게 부를 수 있도록 인스턴스 생성
ai_handler = AIModelHandler()