# answer_manager.py
import json, random
from datetime import date

ANSWER_FILE = "../data/answers.json"
STATE_FILE = "../data/current_answer.json"

def load_candidates():
    with open(ANSWER_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def get_today_answer(admin_choice=None):
    today = str(date.today())

	
    # 이미 오늘 정답이 저장돼 있으면 그대로 사용
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            state = json.load(f)
            if state.get("date") == today:
                return state["answer"], state["hint"]
    except FileNotFoundError:
        print("오류남")

    # 새 정답 결정 (관리자 모드 or 랜덤)
    candidates = load_candidates()
    if admin_choice and admin_choice in candidates:
        answer, hint = admin_choice, candidates[admin_choice]
    else:
        answer, hint = random.choice(list(candidates.items()))

    # 상태 저장
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump({"date": today, "answer": answer, "hint": hint}, f, ensure_ascii=False, indent=2)

    return answer, hint
