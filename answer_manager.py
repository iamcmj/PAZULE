import os, json, random
from datetime import date

# ======================================
# ✅ 루트 기준 절대 경로 계산
# ======================================
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
ANSWER_FILE = os.path.join(DATA_DIR, "answer.json")
STATE_FILE = os.path.join(DATA_DIR, "current_answer.json")


def load_missions1():
    """missions1 리스트 로드"""
    with open(ANSWER_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("missions1", [])


def load_missions2():
    """missions2 리스트 로드"""
    with open(ANSWER_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("missions2", [])


def get_today_answer(admin_choice=None, mission_type=None):
    """
    오늘의 정답과 힌트를 가져옵니다.
    
    Args:
        admin_choice (str, optional): 관리자가 지정한 정답
        mission_type (str, optional): 미션 타입 ("photo" -> missions2, "location" -> missions1)
                                     None이면 missions1 사용 (기본값)
    
    Returns:
        tuple: (answer, hint)
    """
    today = str(date.today())

    # 이미 오늘 정답이 있으면 그대로 사용
    if not admin_choice:
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                state = json.load(f)
                if state.get("date") == today:
                    # mission_type에 따라 다른 힌트 반환
                    if mission_type == "photo" and "hint2" in state:
                        return state["answer"], state["hint2"]
                    elif "hint" in state:
                        return state["answer"], state["hint"]
        except FileNotFoundError:
            print("⚠️ current_answer.json이 아직 없습니다. 새로 생성합니다.")

    # mission_type에 따라 다른 리스트에서 선택
    if mission_type == "photo":
        candidates = load_missions2()
    else:
        candidates = load_missions1()

    if admin_choice:
        match = next((m for m in candidates if m["answer"] == admin_choice), None)
        if match:
            answer, hint = match["answer"], match["hint"]
        else:
            raise ValueError(f"관리자 지정 '{admin_choice}'은 후보에 없습니다.")
    else:
        choice = random.choice(candidates)
        answer, hint = choice["answer"], choice["hint"]

    return answer, hint


def get_today_answers():
    """
    오늘의 정답과 두 가지 힌트(missions1, missions2)를 모두 가져옵니다.
    같은 answer를 사용하되, missions1과 missions2에서 각각 다른 hint를 가져옵니다.
    
    Returns:
        tuple: (answer, hint1, hint2)
    """
    today = str(date.today())
    
    # ✅ data 폴더 없으면 자동 생성
    os.makedirs(DATA_DIR, exist_ok=True)
    
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            state = json.load(f)
            if state.get("date") == today:
                # 오늘 날짜면 기존 값 반환
                return state.get("answer"), state.get("hint"), state.get("hint2")
    except FileNotFoundError:
        pass
    
    # 새로운 정답 생성
    # missions1에서 answer와 hint1 선택
    missions1_candidates = load_missions1()
    missions1_choice = random.choice(missions1_candidates)
    answer = missions1_choice["answer"]
    hint1 = missions1_choice["hint"]
    
    # 같은 answer를 가진 missions2 항목 찾기
    missions2_candidates = load_missions2()
    missions2_match = next((m for m in missions2_candidates if m["answer"] == answer), None)
    
    if missions2_match:
        # 같은 answer가 있으면 그 hint 사용
        hint2 = missions2_match["hint"]
    else:
        # 같은 answer가 없으면 missions2에서 랜덤 선택 (answer는 missions1의 것을 사용)
        missions2_choice = random.choice(missions2_candidates)
        hint2 = missions2_choice["hint"]
        # answer는 missions1에서 선택한 것을 그대로 사용
    
    # 상태 저장
    state = {
        "date": today,
        "answer": answer,
        "hint": hint1,  # missions1 힌트
        "hint2": hint2  # missions2 힌트
    }
    
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    
    return answer, hint1, hint2


if __name__ == "__main__":
    answer, hint = get_today_answer(admin_choice="피노키오")
    print(f"오늘의 정답: {answer} / 힌트: {hint}")
