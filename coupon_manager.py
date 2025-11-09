# coupon_manager.py
import random
import string
from datetime import datetime


def generate_coupon_code():
    """쿠폰 코드를 생성합니다."""
    # 8자리 랜덤 코드 생성 (대문자 + 숫자)
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    return code


def give_coupon(mission_type, answer):
    """
    미션 성공 시 쿠폰을 발급합니다.
    
    Args:
        mission_type (str): 미션 타입 ("mission1" 또는 "mission2")
        answer (str): 정답 (Mission1: 랜드마크 이름, Mission2: 감정 키워드)
        
    Returns:
        dict: 쿠폰 정보
            - code: 쿠폰 코드
            - description: 쿠폰 설명
            - mission_type: 미션 타입
            - answer: 정답
            - issued_at: 발급 시간
    """
    coupon_code = generate_coupon_code()
    
    if mission_type == "mission1":
        description = f"{answer} 장소 찾기 미션 완료 쿠폰"
    else:
        description = f"{answer} 감정 사진 촬영 미션 완료 쿠폰"
    
    return {
        "code": coupon_code,
        "description": description,
        "mission_type": mission_type,
        "answer": answer,
        "issued_at": datetime.now().isoformat()
    }

