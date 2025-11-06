import os, json, random
from datetime import date

# ======================================
# ✅ 루트 기준 절대 경로 계산
# ======================================
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
ANSWER_FILE = os.path.join(DATA_DIR, "answer.json")
STATE_FILE = os.path.join(DATA_DIR, "current_answer.json")


def load_candidates():
    with open(ANSWER_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["missions"]


def get_today_answer(admin_choice=None):
    today = str(date.today())

    # 이미 오늘 정답이 있으면 그대로 사용
    if not admin_choice:
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                state = json.load(f)
                if state.get("date") == today:
                    return state["answer"], state["hint"]
        except FileNotFoundError:
            print("⚠️ current_answer.json이 아직 없습니다. 새로 생성합니다.")

    candidates = load_candidates()

    if admin_choice:
        match = next((m for m in candidates if m["answer"] == admin_choice), None)
        if match:
            answer, hint = match["answer"], match["hint"]
            print("saksldka")
        else:
            raise ValueError(f"관리자 지정 '{admin_choice}'은 후보에 없습니다.")
    else:
        choice = random.choice(candidates)
        answer, hint = choice["answer"], choice["hint"]

    # ✅ data 폴더 없으면 자동 생성
    os.makedirs(DATA_DIR, exist_ok=True)

    # ✅ 상태 저장
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(
            {"date": today, "answer": answer, "hint": hint},
            f,
            ensure_ascii=False,
            indent=2,
        )

    return answer, hint


if __name__ == "__main__":
<<<<<<< HEAD
    answer, hint = get_today_answer(admin_choice="피노키오")
=======
    answer, hint = get_today_answer("피노키오")
>>>>>>> 4f2a9744b6d14b00fb414cf91aecd679ca49ff9e
    print(f"오늘의 정답: {answer} / 힌트: {hint}")
