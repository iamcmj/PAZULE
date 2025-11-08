# mission_manager.py
from models.blip_module import check_with_blip
from models.clip_module import check_with_clip
from models.llm_hint_generator import generate_hint
from coupon_manager import give_coupon


def run_mission(user_image, mission_type, answer1, answer2):
    """
    미션을 실행하고 성공/실패에 따라 결과를 반환합니다.
    항상 BLIP과 CLIP을 모두 실행하여 각각의 성공/실패를 확인합니다.

    Args:
        user_image (str): 사용자가 업로드한 이미지 파일 경로
        mission_type (str): 미션 타입 (미래 확장용, 현재는 둘 다 실행)
        answer1 (str): Mission1(BLIP)용 정답 랜드마크 이름
        answer2 (str): Mission2(CLIP)용 정답 감정/분위기 키워드

    Returns:
        dict: 미션 결과 정보
            - 둘 다 성공: {"mission1": True, "mission2": True, "coupon": str}
            - 일부 실패: {"mission1": bool, "mission2": bool, "hint": str}
    """
    # 항상 BLIP과 CLIP을 모두 실행
    # Mission1: BLIP으로 장소 인식 (answer1 사용)
    mission1_result, blip_info = check_with_blip(user_image, answer1)
    # Mission2: CLIP으로 감정 분석 (answer2 사용)
    mission2_result, clip_info = check_with_clip(user_image, answer2)

    # 결과에 따라 분기 처리
    if mission1_result and mission2_result:
        # 둘 다 성공 - 쿠폰 발급 (answer1 사용)
        coupon = give_coupon(answer1)
        return {"mission1": True, "mission2": True, "coupon": coupon, "hint": None}

    elif mission1_result and not mission2_result:
        # Mission1만 성공, Mission2 실패
        # CLIP 정보만 사용하여 힌트 생성 (answer2 사용)
        status_msg = (
            "Mission1(장소 인식)은 성공! Mission2(감정 분석)를 다시 도전해보세요."
        )
        hint = generate_hint(answer2, [], clip_info, status_msg)
        return {
            "mission1": True,
            "mission2": False,
            "hint": hint,
            "message": status_msg,
        }

    elif not mission1_result and mission2_result:
        # Mission1 실패, Mission2만 성공
        # BLIP 정보만 사용하여 힌트 생성 (answer1 사용)
        status_msg = (
            "Mission2(감정 분석)은 성공! Mission1(장소 인식)를 다시 도전해보세요."
        )
        hint = generate_hint(answer1, blip_info, [], status_msg)
        return {
            "mission1": False,
            "mission2": True,
            "hint": hint,
            "message": status_msg,
        }

    else:
        # 둘 다 실패
        # BLIP과 CLIP 정보를 모두 사용하여 종합 힌트 생성 (answer1 사용)
        status_msg = (
            "두 미션 모두 아직 정답이 아니에요. 힌트를 참고해서 다시 도전해보세요!"
        )
        hint = generate_hint(answer1, blip_info, clip_info, status_msg)
        return {
            "mission1": False,
            "mission2": False,
            "hint": hint,
            "message": status_msg,
        }
