# mission_manager.py
from models.blip_module import check_with_blip
from models.clip_module import check_with_clip
from models.llm_hint_generator import generate_hint
from coupon_manager import give_coupon


def run_mission1(user_image, answer):
    """
    Mission1 (장소 찾기) 실행 - BLIP으로 장소 인식

    Args:
        user_image (str): 사용자가 업로드한 이미지 파일 경로
        answer (str): Mission1(BLIP)용 정답 랜드마크 이름

    Returns:
        dict: 미션 결과 정보
            - 성공: {"success": True, "coupon": str}
            - 실패: {"success": False, "hint": str, "message": str}
    """
    mission_result, blip_info = check_with_blip(user_image, answer)

    if mission_result:
        # 성공 - 쿠폰 발급
        coupon = give_coupon("mission1", answer)
        return {
            "success": True,
            "coupon": coupon,
        }
    else:
        # 실패 - 힌트 생성
        status_msg = "장소를 다시 찾아보세요!"
        hint = generate_hint(answer, blip_info, [], status_msg)
        return {
            "success": False,
            "hint": hint,
            "message": status_msg,
        }


def run_mission2(user_image, answer):
    """
    Mission2 (사진 촬영) 실행 - CLIP으로 감정 분석

    Args:
        user_image (str): 사용자가 업로드한 이미지 파일 경로
        answer (str): Mission2(CLIP)용 정답 감정/분위기 키워드

    Returns:
        dict: 미션 결과 정보
            - 성공: {"success": True, "coupon": str}
            - 실패: {"success": False, "hint": str, "message": str}
    """
    mission_result, clip_info = check_with_clip(user_image, answer)

    if mission_result:
        # 성공 - 쿠폰 발급
        coupon = give_coupon("mission2", answer)
        return {
            "success": True,
            "coupon": coupon,
            "message": "감정 분석 미션 성공!",
        }
    else:
        # 실패 - 힌트 생성
        status_msg = "감정이 담긴 사진을 다시 찍어보세요!"
        hint = generate_hint(answer, [], clip_info, status_msg)
        return {
            "success": False,
            "hint": hint,
            "message": status_msg,
        }
