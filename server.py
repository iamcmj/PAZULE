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
from answer_manager import get_today_answers
from mission_manager import run_mission1, run_mission2
from metadata.validator import validate_metadata

app = Flask(__name__)
CORS(app)  # 프론트엔드와 통신을 위해 CORS 활성화

# ✅ 상태 파일 경로
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
STATE_FILE = os.path.join(DATA_DIR, "current_answer.json")

# ✅ 전역 변수로 오늘의 정답과 힌트 저장
today_answer1 = None  # Mission1 (BLIP) 정답
today_answer2 = None  # Mission2 (CLIP) 정답
today_hint1 = None  # Mission1 힌트
today_hint2 = None  # Mission2 힌트


def ensure_today_answer():
    """current_answer.json이 없거나 비어있거나 날짜가 다르면 새로 생성"""
    from answer_manager import get_today_answers

    os.makedirs(DATA_DIR, exist_ok=True)

    # ✅ 파일 없거나 비어 있으면 새로 생성
    if not os.path.exists(STATE_FILE) or os.path.getsize(STATE_FILE) == 0:
        print("📝 상태 파일이 없거나 비어있어 새로 생성합니다.")
        return get_today_answers()

    # ✅ 파일 내용 읽기 시도
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                # 파일이 비어있으면 새로 생성
                print("📝 상태 파일이 비어있어 새로 생성합니다.")
                return get_today_answers()

            state = json.loads(content)
            today = str(date.today())

            # ✅ 날짜가 오늘이면 그대로 유지
            if state.get("date") == today:
                # 하위 호환성: answer1이 없으면 answer 사용
                answer1 = state.get("answer1") or state.get("answer")
                answer2 = state.get("answer2")
                hint1 = state.get("hint1") or state.get("hint")
                hint2 = state.get("hint2")
                if answer1 and answer2 and hint1 and hint2:
                    return answer1, answer2, hint1, hint2

            # ✅ 날짜가 다르면 새로 생성
            print("📅 날짜가 바뀌어 새 정답 생성")
            return get_today_answers()

    except json.JSONDecodeError as e:
        # JSON 파싱 오류
        print(f"⚠️ 상태 파일 JSON 형식 오류: {e}. 새로 생성합니다.")
        return get_today_answers()
    except Exception as e:
        # 기타 오류
        print(f"⚠️ 상태 파일 로드 실패: {e}. 새로 생성합니다.")
        return get_today_answers()


# ✅ 서버 시작 시 자동으로 오늘의 정답 보장
today_answer1, today_answer2, today_hint1, today_hint2 = ensure_today_answer()


@app.route("/get-today-hint", methods=["GET"])
def get_today_hint():
    """HTML에서 호출하는 API - mission_type 파라미터로 힌트 선택"""
    global today_answer1, today_answer2, today_hint1, today_hint2

    # mission_type 파라미터 받기 (기본값: "location" -> missions1)
    mission_type = request.args.get("mission_type", "location")

    # 혹시 서버가 오래 켜져 있다면 날짜 갱신 체크
    today = str(date.today())

    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            state = json.load(f)
        if state.get("date") != today:
            print("📅 날짜가 바뀌어 재갱신합니다.")
            today_answer1, today_answer2, today_hint1, today_hint2 = (
                ensure_today_answer()
            )
        else:
            # 하위 호환성: answer1이 없으면 answer 사용
            today_answer1 = state.get("answer1") or state.get("answer")
            today_answer2 = state.get("answer2")
            today_hint1 = state.get("hint1") or state.get("hint")
            today_hint2 = state.get("hint2")
    except FileNotFoundError:
        print("⚠️ current_answer.json 없음 → 새로 생성")
        today_answer1, today_answer2, today_hint1, today_hint2 = ensure_today_answer()

    # mission_type에 따라 다른 힌트와 정답 반환
    if mission_type == "photo":
        # Mission2 (CLIP) - 감정 분석
        return jsonify({"answer": today_answer2, "hint": today_hint2})
    else:
        # Mission1 (BLIP) - 장소 인식
        return jsonify({"answer": today_answer1, "hint": today_hint1})


@app.route("/api/preview", methods=["POST"])
def api_preview():
    """HEIC 파일을 JPG로 변환하여 미리보기 제공"""
    if "image" not in request.files:
        return jsonify({"error": "이미지 파일이 필요합니다."}), 400

    file = request.files["image"]
    if file.filename == "":
        return jsonify({"error": "이미지 파일이 선택되지 않았습니다."}), 400

    # ✅ 임시 파일로 저장
    import tempfile
    from PIL import Image
    from pillow_heif import register_heif_opener
    import io

    # HEIC 포맷 지원 등록
    register_heif_opener()

    with tempfile.NamedTemporaryFile(
        delete=False, suffix=os.path.splitext(file.filename)[1]
    ) as tmp_file:
        file.save(tmp_file.name)
        temp_path = tmp_file.name

    try:
        # HEIC 파일을 JPG로 변환
        img = Image.open(temp_path)
        img_rgb = img.convert("RGB")

        # 메모리 버퍼에 JPG 저장
        output = io.BytesIO()
        img_rgb.save(output, format="JPEG", quality=90)
        output.seek(0)

        from flask import send_file

        return send_file(
            output,
            mimetype="image/jpeg",
            as_attachment=False,
            download_name="preview.jpg",
        )
    except Exception as e:
        print(f"미리보기 변환 오류: {e}")
        import traceback

        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    finally:
        # ✅ 임시 파일 삭제
        if os.path.exists(temp_path):
            os.remove(temp_path)


@app.route("/api/mission", methods=["POST"])
def api_mission():
    """미션 실행 API - mission_type에 따라 적절한 미션 실행"""
    global today_answer1, today_answer2

    # ✅ 이미지 파일 확인
    if "image" not in request.files:
        return jsonify({"error": "이미지 파일이 필요합니다."}), 400

    file = request.files["image"]
    if file.filename == "":
        return jsonify({"error": "이미지 파일이 선택되지 않았습니다."}), 400

    # ✅ mission_type 확인 (기본값: "location" -> mission1)
    mission_type = request.form.get("mission_type", "location")

    # ✅ 파일 확장자 확인 및 HEIC 지원
    file_ext = os.path.splitext(file.filename)[1].lower()
    allowed_extensions = [".jpg", ".jpeg", ".png", ".heic", ".heif"]

    if file_ext not in allowed_extensions:
        return (
            jsonify(
                {
                    "error": f"지원하지 않는 파일 형식입니다. 지원 형식: {', '.join(allowed_extensions)}"
                }
            ),
            400,
        )

    # ✅ 임시 파일로 저장 (HEIC 파일도 원본 확장자 유지)
    import tempfile

    with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
        file.save(tmp_file.name)
        temp_path = tmp_file.name

    try:
        # ✅ 메타데이터 유효성 검사
        if not validate_metadata(temp_path):
            return (
                jsonify(
                    {"error": "오늘 촬영한 사진이 아니거나 출판단지 내부가 아닙니다."}
                ),
                400,
            )

        # ✅ mission_type에 따라 적절한 미션 실행
        if mission_type == "photo":
            # Mission2 (사진 촬영) - CLIP 감정 분석
            result = run_mission2(temp_path, today_answer2)
        else:
            # Mission1 (장소 찾기) - BLIP 장소 인식
            result = run_mission1(temp_path, today_answer1)

        return jsonify(result)
    except Exception as e:
        print(f"미션 실행 오류: {e}")
        import traceback

        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    finally:
        # ✅ 임시 파일 삭제
        if os.path.exists(temp_path):
            os.remove(temp_path)


if __name__ == "__main__":
    
    app.run(host="0.0.0.0", port=8000)
