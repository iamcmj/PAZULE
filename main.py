# main.py
from answer_manager import get_today_answer
from mission_manager import run_mission

def main(user_image, mission_type, admin_choice=None):
    # 1️⃣ 오늘의 정답/힌트 결정
    answer, hint = get_today_answer(admin_choice)
    print(f"오늘의 힌트: {hint}")

    # 2️⃣ 사용자 입력 (예시: 이미지)
    result = run_mission(user_image, mission_type, answer)

    # 3️⃣ 결과 출력
    if result["success"]:
        print(f"🎉 정답입니다! 쿠폰: {result['coupon']}")
    else:
        print(f"❌ 오답! 힌트: {result['hint']}")

if __name__ == "__main__":
    main(user_image="user_photo.jpg", mission_type="mission1")