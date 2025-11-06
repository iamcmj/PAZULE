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
from answer_manager import get_today_answer
from mission_manager import run_mission
from metadata.validator import validate_metadata


def main(user_image, mission_type, admin_choice=None):
    # 1️⃣ 오늘의 정답/힌트 결정
    answer, hint = get_today_answer(admin_choice)
    print(f"오늘의 힌트: {hint}")

    # 2️⃣ 메타데이터 유효성 검사
    if not validate_metadata(user_image):
        return

    # 3️⃣ 미션 실행
    result = run_mission(user_image, mission_type, answer)

    # 4️⃣ 결과 출력
    if result["success"]:
        print(f"🎉 정답입니다! 쿠폰: {result['coupon']}")
    else:
        print(f"❌ 오답! 힌트: {result['hint']}")


if __name__ == "__main__":
    main(user_image="./metadata/test_image/test1.HEIC", mission_type="mission1")
