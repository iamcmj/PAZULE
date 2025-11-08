# ========================================
# main.py
# ========================================
import os
import sys

# ✅ 프로젝트 루트 경로를 sys.path에 추가
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

# ✅ 모듈 임포트
from answer_manager import get_today_answers
from mission_manager import run_mission
from metadata.validator import validate_metadata


def execute_mission(user_image_path, answer1, answer2):
    """
    미션을 실행하는 메인 함수
    server.py에서 호출하여 사용

    Args:
        user_image_path (str): 사용자가 업로드한 이미지 파일 경로
        answer1 (str): Mission1(BLIP)용 정답 랜드마크 이름
        answer2 (str): Mission2(CLIP)용 정답 감정/분위기 키워드

    Returns:
        dict: 미션 결과 정보
            - 성공: {"success": True, "mission1": True, "mission2": True, "coupon": str}
            - 실패: {"success": False, "mission1": bool, "mission2": bool, "hint": str, "message": str}
        None: 메타데이터 검증 실패 시
    """
    # 1️⃣ 메타데이터 유효성 검사
    if not validate_metadata(user_image_path):
        return None

    # 2️⃣ 미션 실행 (answer1과 answer2를 각각 전달)
    result = run_mission(user_image_path, "both", answer1, answer2)

    # 3️⃣ 결과 포맷 변환 (프론트엔드 형식에 맞춤)
    if result.get("mission1") and result.get("mission2"):
        return {
            "success": True,
            "mission1": result.get("mission1"),
            "mission2": result.get("mission2"),
            "coupon": result.get("coupon"),
        }
    else:
        return {
            "success": False,
            "mission1": result.get("mission1"),
            "mission2": result.get("mission2"),
            "hint": result.get("hint"),
            "message": result.get("message"),
        }


def main(user_image, mission_type, admin_choice1=None, admin_choice2=None):
    """
    CLI 테스트용 함수 (개발/디버깅용)
    """
    # 1️⃣ 오늘의 정답/힌트 결정 (mission1과 mission2 각각)
    answer1, answer2, hint1, hint2 = get_today_answers(admin_choice1, admin_choice2)
    print(f"Mission1 정답: {answer1}, 힌트: {hint1}")
    print(f"Mission2 정답: {answer2}, 힌트: {hint2}")

    # 2️⃣ 미션 실행
    result = execute_mission(user_image, answer1, answer2)

    # 3️⃣ 결과 출력
    if result is None:
        print("❌ 메타데이터 검증 실패")
    elif result.get("success"):
        print(f"🎉 정답입니다! 쿠폰: {result.get('coupon')}")
    else:
        print(f"❌ 오답! 힌트: {result.get('hint')}")


if __name__ == "__main__":
    main(user_image="./metadata/test_image/test1.HEIC", mission_type="mission1")
