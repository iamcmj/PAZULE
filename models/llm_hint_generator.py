# models/llm_hint_generator.py

import os
from openai import OpenAI
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# GPT 모델 설정
MODEL_NAME = "gpt-4o-mini"


def generate_hint(
    answer, blip_failed_questions=None, clip_emotions=None, mission_status=None
):
    """
    BLIP과 CLIP의 실패 정보를 바탕으로 GPT-4o-mini를 사용하여 추상적 힌트를 생성합니다.

    Args:
        answer (str): 정답 랜드마크 이름 (예: "피노키오")
        blip_failed_questions (list): BLIP에서 'no'로 답변된 질문 리스트
        clip_emotions (list): CLIP에서 분석된 감정 키워드 리스트 (top 순서)
        mission_status (str): 미션 성공/실패 상태 메시지

    Returns:
        str: 생성된 힌트 메시지
    """
    if blip_failed_questions is None:
        blip_failed_questions = []
    if clip_emotions is None:
        clip_emotions = []

    # BLIP 실패 질문을 한국어로 요약할 정보 준비
    blip_info = ""
    if blip_failed_questions:
        blip_info = "\n사용자 사진에서 부족한 특징 (BLIP VQA 결과):\n"
        for i, item in enumerate(blip_failed_questions, 1):
            question = item.get("question", "N/A")
            model_answer = item.get("model_answer", "N/A")
            expected_answer = item.get("expected_answer", "N/A")
            blip_info += f'  {i}. 질문: "{question}"\n'
            blip_info += f"     - 모델 답변: '{model_answer}', 기대 답변: '{expected_answer}'\n"
    else:
        blip_info = "\n사용자 사진에서 부족한 특징: (정보 없음)\n"

    # CLIP 감정 분석 정보 준비
    clip_info = ""
    if clip_emotions:
        clip_info = "\n사용자 사진에서 감지된 감정 (상위 순):\n"
        for i, emotion in enumerate(clip_emotions, 1):
            clip_info += f"  {i}. {emotion}\n"
    else:
        clip_info = "\n사용자 사진에서 감지된 감정: (정보 없음)\n"

    # 미션 상태 정보 준비
    status_info = ""
    if mission_status:
        status_info = f"\n미션 상태: {mission_status}\n"

    # 프롬프트 생성
    system_prompt = """당신은 파주 출판단지 보물찾기 게임의 힌트 제공자입니다.
사용자가 촬영한 사진이 정답 랜드마크가 아닐 때, 추상적이고 창의적인 힌트를 제공하는 역할을 합니다.

### 힌트 작성 가이드라인:
1. 정답 랜드마크 이름을 직접 언급하지 마세요.
2. 2-3문장의 짧고 감성적인 힌트를 작성하세요.
3. 은유적이고 시적인 표현을 사용하세요.
4. BLIP VQA 결과를 바탕으로 사진에 없는 특징을 간접적으로 암시하거나, 잘못 인식된 특징을 정답과 대조하세요.
5. CLIP 감정 분석 결과와 정답이 가진 감성의 차이를 활용하세요.
6. 미션 상태 정보가 있다면 이를 반영하여 힌트를 작성하세요 (예: 장소는 맞지만 감정이 다르다면, 감정 측면에 집중).
7. 사용자가 다시 도전하고 싶은 마음이 들도록 격려하세요.
8. 항상 한국어로 작성하세요.
9. 너무 들뜨거나 장난스러운 톤은 피해주세요.

### 힌트 작성 예시:

**예시 1: 정답의 특징이 사진에 없을 때 (기대 답변 'yes', 모델 답변 'no')**
- **정답:** 피노키오
- **입력 정보:**
    - 질문: "코가 긴 조각상인가요?"
    - 모델 답변: 'no', 기대 답변: 'yes'
- **좋은 힌트:** "진실의 무게를 코 끝으로 증명하는 친구를 찾아보세요. 때로는 작은 거짓말이 가장 큰 특징이 되기도 한답니다."
- **나쁜 힌트:** "코가 긴 인형을 찾아보세요." (너무 직접적임)

**예시 2: 정답이 아닌 다른 대상을 찍었을 때 (기대 답변 'no', 모델 답변 'yes')**
- **정답:** 네모탑
- **입력 정보:**
    - 질문: "사진에 책이 있나요?"
    - 모델 답변: 'yes', 기대 답변: 'no' (사용자가 책이 많은 '지혜의 숲'을 찍었다고 가정)
- **좋은 힌트:** "이야기가 잠든 고요한 숲도 아름답지만, 우리가 찾는 보물은 하늘을 향해 지혜를 층층이 쌓아 올린 곳에 숨겨져 있어요."
- **나쁜 힌트:** "책이 아니라 탑을 찍어야 해요." (너무 직접적임)

### **주의: 잘못된 힌트 생성의 예**
- **상황:** 정답은 '지혜의숲 조각상'이지만, 사용자가 유리로 된 다른 조형물을 찍었을 경우.
- **입력 정보:**
    - 질문: "유리로 만들어진 조각상인가요?"
    - 모델 답변: 'yes', 기대 답변: 'no'
- **의도:** "정답은 유리가 아니다"라는 사실을 알려주어야 합니다.
- **잘못된 힌트:** "투명한 유리의 세계에서... 조각을 찾아보세요." 
    - **(문제점: '유리'라는 오답의 특징을 정답의 특징인 것처럼 묘사함)**
- **올바른 힌트:** "반짝이는 유리도 아름답지만, 우리가 찾는 현자는 조금 더 따뜻하고 소박한 재료로 만들어졌답니다. 가만히 앉아 책의 지혜를 탐구하는 모습을 찾아보세요."
    - **(개선점: '유리'가 아님을 명확히 하고, '앉아서 책을 보는' 올바른 특징을 제시함)"""
    
    user_prompt = f"""정답 랜드마크: {answer}
{status_info}{blip_info}{clip_info}

위 정보를 바탕으로 사용자가 정답에 더 가까이 다가갈 수 있도록 추상적이고 창의적인 힌트를 생성해주세요."""

    # ✅ API 키 확인 및 로깅
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print(f"✅ LLM 힌트 생성 시도 (API 키 설정됨, 길이: {len(api_key)}자)")
    else:
        print("⚠️ OPENAI_API_KEY가 설정되지 않았습니다. 기본 힌트를 사용합니다.")
        return f"다시 한 번 주변을 둘러보세요. '{answer}'와 관련된 특별한 장소가 있을 거예요! 💡"

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.6,  # 창의적인 힌트를 위해 높은 temperature 설정
            max_tokens=200,
        )

        hint = response.choices[0].message.content.strip()
        print("✅ LLM 힌트 생성 성공")
        return hint

    except Exception as e:
        print(f"❌ Error generating hint with GPT: {e}")
        # 오류 발생 시 기본 힌트 반환
        return f"다시 한 번 주변을 둘러보세요. '{answer}'와 관련된 특별한 장소가 있을 거예요! 💡"


if __name__ == "__main__":
    # 테스트 예시
    print("=== LLM Hint Generator 테스트 ===\n")

    # 예시 1: 피노키오 미션 둘 다 실패
    print("--- 예시 1: 피노키오 ---")
    test_answer_1 = "피노키오"
    test_blip_questions_1 = [
        {
            "question": "Does the statue have a particularly long nose?",
            "model_answer": "no",
            "expected_answer": "yes"
        },
        {
            "question": "Is the statue wearing green-colored clothes?",
            "model_answer": "no",
            "expected_answer": "yes"
        },
        {
            "question": "Is the object the statue is holding a book?",
            "model_answer": "yes",
            "expected_answer": "no"
        }
    ]
    test_clip_emotions_1 = [
        "calm and peaceful",
        "warm and cozy",
        "natural and scenic"
    ]
    test_status_1 = "두 미션 모두 아직 정답이 아니에요. 힌트를 참고해서 다시 도전해보세요!"
    
    print(f"정답: {test_answer_1}")
    print(f"BLIP 실패 질문 수: {len(test_blip_questions_1)}")
    
    hint_1 = generate_hint(test_answer_1, test_blip_questions_1, test_clip_emotions_1, test_status_1)
    print("\n생성된 힌트:")
    print(hint_1)
    print("\n" + "="*50 + "\n")
    
    # 예시 2: 지혜의숲 조각상 미션 실패
    print("--- 예시 2: 지혜의숲 조각상 ---")
    test_answer_2 = "지혜의숲 조각상"
    test_blip_questions_2 = [
        {"question": "Is the sculpture made of glass?", "model_answer": "yes", "expected_answer": "no"},
        {"question": "Does the sculpture have a tail?", "model_answer": "yes", "expected_answer": "no"},
        {"question": "Is the sculpture standing up?", "model_answer": "yes", "expected_answer": "no"},
        {"question": "Is the sculpture holding an object to its eyes?", "model_answer": "no", "expected_answer": "yes"},
        {"question": "Is the sculpture in a sitting position?", "model_answer": "no", "expected_answer": "yes"}
    ]
    test_clip_emotions_2 = [
        "modern and sleek",
        "transparent and clear",
        "upright and tall"
    ]
    test_status_2 = "아직 정답이 아닌 것 같아요. 다른 장소를 찾아볼까요?"

    print(f"정답: {test_answer_2}")
    print(f"BLIP 실패 질문 수: {len(test_blip_questions_2)}")

    hint_2 = generate_hint(test_answer_2, test_blip_questions_2, test_clip_emotions_2, test_status_2)
    print("\n생성된 힌트:")
    print(hint_2)
    print("\n" + "="*50 + "\n")

