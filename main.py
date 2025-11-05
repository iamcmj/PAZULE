# ========================================
# main.py
# ========================================
import argparse
import os

from metadata.metadata import quick_photo_summary, is_in_bbox

# from blip.mission1 import run_landmark_mission   # Mission1
# from clip.mission2 import run_mood_mission       # Mission2


def validate_metadata(image_path):
    """사진 메타데이터 유효성 검사"""
    print("\n[STEP 1] Checking metadata...")
    try:
        result = quick_photo_summary(image_path)
        return result
    except Exception as e:
        print(f"❌ Metadata validation failed: {e}")
        return False


def run_mission(mission_id, image_path, hint_or_keyword):
    """Mission별 실행"""
    if mission_id == 1:
        result = run_landmark_mission(image_path, hint_or_keyword)
    elif mission_id == 2:
        result = run_mood_mission(image_path, hint_or_keyword)
    else:
        raise ValueError("mission_id는 1 또는 2여야 합니다.")

    if result["success"]:
        print(f"✅ 미션 성공! 쿠폰 지급: {result['reward']}")
    else:
        print("❌ 미션 실패, 다시 시도하세요.")
        if "feedback" in result:
            print(f"💬 피드백: {result['feedback']}")


def main():
    parser = argparse.ArgumentParser(description="Group5 Project Main Controller")
    parser.add_argument(
        "--mission", type=int, required=True, help="1: 랜드마크 / 2: 분위기"
    )
    parser.add_argument("--image", type=str, required=True, help="이미지 경로")
    parser.add_argument(
        "--hint", type=str, default=None, help="사용자에게 제시할 힌트/키워드"
    )
    args = parser.parse_args()

    # ✅ 메타데이터 검증
    if not validate_metadata(args.image):
        print("⚠️  메타데이터 검증 실패로 미션 진행 불가.")
        return

    # ✅ 미션 실행
    run_mission(args.mission, args.image, args.hint)


if __name__ == "__main__":
    main()
