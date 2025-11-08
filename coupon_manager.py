# coupon_manager.py
import random
import string
from datetime import datetime


def generate_coupon_code():
    """쿠폰 코드를 생성합니다."""
    # 8자리 랜덤 코드 생성 (대문자 + 숫자)
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    return code


def give_coupon(landmark_name):
    """
    미션 성공 시 쿠폰을 발급합니다.
    
    Args:
        landmark_name (str): 정답 랜드마크 이름
        
    Returns:
        dict: 쿠폰 정보
            - code: 쿠폰 코드
            - description: 쿠폰 설명
            - landmark: 랜드마크 이름
            - issued_at: 발급 시간
    """
    coupon_code = generate_coupon_code()
    
    return {
        "code": coupon_code,
        "description": f"{landmark_name} 미션 완료 쿠폰",
        "landmark": landmark_name,
        "issued_at": datetime.now().isoformat()
    }

