import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.shortcuts import render

from langchain_upstage import ChatUpstage, UpstageEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# 1. 벡터 스토어 로드 (서버 켜질 때 한 번만 로드)
VS_DIR = str(settings.BASE_DIR / "vector_store")
embeddings = UpstageEmbeddings(model="solar-embedding-1-large")
vectorstore = Chroma(persist_directory=VS_DIR, embedding_function=embeddings)
retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 3, "fetch_k": 10} # 다양성 있는 추천을 위해 k=3
)

# 2. 프롬프트 정의 (페르소나 부여)
SYSTEM_PROMPT = """
너는 친절하고 박식한 '영화 추천 AI 챗봇'이야.
아래 제공된 [Context]에 있는 영화 정보를 바탕으로 사용자의 질문에 답변해줘.

규칙:
1. [Context]에 없는 내용은 지어내지 말고 "제가 가진 데이터에는 없는 영화네요."라고 솔직하게 말해.
2. 영화를 추천할 때는 제목, 장르, 그리고 추천하는 이유를 간단히 설명해줘.
3. 답변은 한국어로, 친근한 말투(해요체)를 사용해줘.
4. 질문과 관련 없는 영화는 언급하지 마.

[Context]:
{context}
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", "{question}"),
])

# 3. LLM 설정
llm = ChatUpstage(model="solar-mini", temperature=0.7) # 약간의 창의성을 위해 0.7

# 체인 구성
chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# ---------------- View 함수 ----------------

def chatbot_page(request):
    """채팅 페이지 렌더링"""
    return render(request, 'chatbot/index.html')

@csrf_exempt
def chat_api(request):
    """실제 질문을 받아 답변하는 API"""
    if request.method != "POST":
        return HttpResponseBadRequest("POST method required")

    try:
        data = json.loads(request.body)
        question = data.get("question", "").strip()
        
        if not question:
            return JsonResponse({"error": "질문을 입력해주세요."}, status=400)

        # 체인 실행 (질문 -> 검색 -> 답변)
        response = chain.invoke(question)
        
        # (선택) 검색된 문서의 출처 정보도 같이 보내주기 위해 수동으로 retriever 한 번 더 호출 가능하지만,
        # 여기서는 심플하게 답변만 보냅니다.
        
        return JsonResponse({"answer": response})

    except Exception as e:
        print(f"Error: {e}")
        return JsonResponse({"error": "오류가 발생했습니다."}, status=500)