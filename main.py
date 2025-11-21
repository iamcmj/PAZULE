# ========================================
# main.py - 로컬 테스트용 (CLI)
# ========================================
"""
로컬 환경에서 미션을 테스트하기 위한 스크립트입니다.
서버를 거치지 않고 직접 미션을 실행할 수 있습니다.
"""
import os
import sys

# ✅ 프로젝트 루트 경로를 sys.path에 추가
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

# ✅ 모듈 임포트
from answer_manager import get_today_answers
from mission_manager import run_mission1, run_mission2
from metadata.validator import validate_metadata


def test_mission1(user_image_path, admin_choice1=None):
    """
    Mission1 (장소 찾기) 로컬 테스트

    Args:
        user_image_path (str): 테스트할 이미지 파일 경로
        admin_choice1 (str, optional): 관리자가 지정한 mission1 정답
    """
    print("=" * 60)
    print("Mission1 (장소 찾기) 테스트")
    print("=" * 60)

    # 오늘의 정답 가져오기
    answer1, answer2, hint1, hint2 = get_today_answers(admin_choice1, None)
    print(f"정답: {answer1}")
    print(f"힌트: {hint1}\n")

    # 메타데이터 검증
    if not validate_metadata(user_image_path):
        print("❌ 메타데이터 검증 실패")
        return

    # 미션 실행
    result = run_mission1(user_image_path, answer1)

    # 결과 출력
    if result.get("success"):
        print(f"🎉 Mission1 성공! 쿠폰: {result.get('coupon')}")
    else:
        print(f"❌ Mission1 실패!")
        print(f"힌트: {result.get('hint')}")
        print(f"메시지: {result.get('message')}")


def test_mission2(user_image_path, admin_choice2=None):
    """
    Mission2 (사진 촬영) 로컬 테스트

    Args:
        user_image_path (str): 테스트할 이미지 파일 경로
        admin_choice2 (str, optional): 관리자가 지정한 mission2 정답
    """
    print("=" * 60)
    print("Mission2 (사진 촬영) 테스트")
    print("=" * 60)

    # 오늘의 정답 가져오기
    answer1, answer2, hint1, hint2 = get_today_answers(None, admin_choice2)
    print(f"정답: {answer2}")
    print(f"힌트: {hint2}\n")

    # 메타데이터 검증
    if not validate_metadata(user_image_path):
        print("❌ 메타데이터 검증 실패")
        return

    # 미션 실행
    result = run_mission2(user_image_path, answer2)

    # 결과 출력
    if result.get("success"):
        print(f"🎉 Mission2 성공! {result.get('message')}")
    else:
        print(f"❌ Mission2 실패!")
        print(f"힌트: {result.get('hint')}")
        print(f"메시지: {result.get('message')}")


if __name__ == "__main__":
    # 테스트 이미지 경로
    test_image = "./data/활판 공방/13518647321211.jpg"

    # Mission1 테스트
    # test_mission1(test_image, admin_choice1="피노키오")

    # Mission2 테스트
    test_mission2(test_image, admin_choice2="차분한")
