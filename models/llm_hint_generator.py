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


def generate_hint(answer, blip_failed_questions=None, clip_emotions=None, mission_status=None):
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
        for i, question in enumerate(blip_failed_questions, 1):
            blip_info += f"  {i}. {question}\n"
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

힌트 작성 가이드라인:
1. 정답 랜드마크 이름을 직접 언급하지 마세요
2. 2-3문장의 짧고 감성적인 힌트를 작성하세요
3. 은유적이고 시적인 표현을 사용하세요
4. BLIP 질문에서 부족한 특징을 간접적으로 암시하세요
5. CLIP 감정 분석 결과와 정답이 가진 감성의 차이를 활용하세요
6. 미션 상태 정보가 있다면 이를 반영하여 힌트를 작성하세요 (예: 장소는 맞지만 감정이 다르다면, 감정 측면에 집중)
7. 사용자가 다시 도전하고 싶은 마음이 들도록 격려하세요
8. 한국어로 작성하세요"""
    
    user_prompt = f"""정답 랜드마크: {answer}
{status_info}{blip_info}{clip_info}

위 정보를 바탕으로 사용자가 정답에 더 가까이 다가갈 수 있도록 추상적이고 창의적인 힌트를 생성해주세요."""
    
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.8,  # 창의적인 힌트를 위해 높은 temperature 설정
            max_tokens=200
        )
        
        hint = response.choices[0].message.content.strip()
        return hint
        
    except Exception as e:
        print(f"Error generating hint with GPT: {e}")
        # 오류 발생 시 기본 힌트 반환
        return f"다시 한 번 주변을 둘러보세요. '{answer}'와 관련된 특별한 장소가 있을 거예요! 💡"


if __name__ == "__main__":
    # 테스트 예시
    print("=== LLM Hint Generator 테스트 ===\n")
    
    # 예시 1: 피노키오 미션 둘 다 실패
    test_answer = "피노키오"
    test_blip_questions = [
        "Does the statue have a particularly long nose?",
        "Is the statue wearing green-colored clothes?",
        "Is the object the statue is holding a book?"
    ]
    test_clip_emotions = [
        "calm and peaceful",
        "warm and cozy",
        "natural and scenic"
    ]
    test_status = "두 미션 모두 아직 정답이 아니에요. 힌트를 참고해서 다시 도전해보세요!"
    
    print(f"정답: {test_answer}")
    print(f"BLIP 실패 질문 수: {len(test_blip_questions)}")
    print(f"CLIP 감정: {test_clip_emotions}")
    print(f"상태: {test_status}\n")
    
    hint = generate_hint(test_answer, test_blip_questions, test_clip_emotions, test_status)
    print("생성된 힌트:")
    print(hint)
    print("\n" + "="*50 + "\n")
    
    # 예시 2: Mission1 성공, Mission2 실패
    test_status2 = "Mission1(장소 인식)은 성공! Mission2(감정 분석)를 다시 도전해보세요."
    hint2 = generate_hint("지혜의숲 조각상", [], test_clip_emotions, test_status2)
    print("Mission1 성공, Mission2 실패 시 힌트:")
    print(hint2)
    print("\n" + "="*50 + "\n")
    
    # 예시 3: Mission1 실패, Mission2 성공
    test_status3 = "Mission2(감정 분석)은 성공! Mission1(장소 인식)를 다시 도전해보세요."
    hint3 = generate_hint("네모탑", test_blip_questions, [], test_status3)
    print("Mission1 실패, Mission2 성공 시 힌트:")
    print(hint3)

