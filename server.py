# server.py
import os
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import date
import json

# ✅ 프로젝트 루트 경로를 sys.path에 추가
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

# ✅ 모듈 임포트
from answer_manager import get_today_answer
from mission_manager import run_mission
from metadata.validator import validate_metadata

app = Flask(__name__)
CORS(app)  # 프론트엔드와 통신을 위해 CORS 활성화

# ✅ 상태 파일 경로
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
STATE_FILE = os.path.join(DATA_DIR, "current_answer.json")

# ✅ 전역 변수로 오늘의 정답과 힌트 저장
today_answer = None
today_hint = None


def ensure_today_answer():
    """current_answer.json이 없거나 비어있거나 날짜가 다르면 새로 생성"""
    os.makedirs(DATA_DIR, exist_ok=True)
    
    today = str(date.today())
    
    try:
        # ✅ 파일 없거나 비어 있으면 새로 생성
        if not os.path.exists(STATE_FILE) or os.path.getsize(STATE_FILE) == 0:
            return get_today_answer()
        
        # ✅ 파일 내용 읽기
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            state = json.load(f)
        
        # ✅ 날짜가 오늘이면 그대로 유지
        if state.get("date") == today:
            return state["answer"], state["hint"]
        
        # ✅ 날짜가 다르면 새로 생성
        print("📅 날짜가 바뀌어 새 정답 생성")
        return get_today_answer()
        
    except Exception as e:
        print("⚠️ 상태 파일 로드 실패:", e)
        return get_today_answer()


# ✅ 서버 시작 시 자동으로 오늘의 정답 보장
today_answer, today_hint = ensure_today_answer()


@app.route("/get-today-hint", methods=["GET"])
def get_today_hint():
    """HTML에서 호출하는 API"""
    global today_answer, today_hint
    
    # 혹시 서버가 오래 켜져 있다면 날짜 갱신 체크
    today = str(date.today())
    
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            state = json.load(f)
        if state.get("date") != today:
            print("📅 날짜가 바뀌어 재갱신합니다.")
            today_answer, today_hint = get_today_answer()
    except FileNotFoundError:
        print("⚠️ current_answer.json 없음 → 새로 생성")
        today_answer, today_hint = get_today_answer()
    
    return jsonify({"answer": today_answer, "hint": today_hint})


@app.route("/api/mission", methods=["POST"])
def api_mission():
    """미션 실행 API"""
    global today_answer
    
    if "image" not in request.files:
        return jsonify({"error": "이미지 파일이 필요합니다."}), 400
    
    file = request.files["image"]
    if file.filename == "":
        return jsonify({"error": "이미지 파일이 선택되지 않았습니다."}), 400
    
    mission_type = request.form.get("mission_type", "photo")
    
    # ✅ 임시 파일로 저장
    import tempfile
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp_file:
        file.save(tmp_file.name)
        temp_path = tmp_file.name
    
    try:
        # ✅ 메타데이터 검증
        if not validate_metadata(temp_path):
            return jsonify({"error": "메타데이터 검증 실패"}), 400
        
        # ✅ 미션 실행
        result = run_mission(temp_path, mission_type, today_answer)
        
        # ✅ 결과 포맷 변환 (프론트엔드 형식에 맞춤)
        if result.get("mission1") and result.get("mission2"):
            return jsonify({
                "success": True,
                "coupon": result.get("coupon"),
                "mission1": result.get("mission1"),
                "mission2": result.get("mission2")
            })
        else:
            return jsonify({
                "success": False,
                "hint": result.get("hint"),
                "message": result.get("message"),
                "mission1": result.get("mission1"),
                "mission2": result.get("mission2")
            })
    except Exception as e:
        print(f"미션 실행 오류: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        # ✅ 임시 파일 삭제
        if os.path.exists(temp_path):
            os.remove(temp_path)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

