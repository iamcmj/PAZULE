# BLIP Standalone Treasure Hunt Game - Project Plan

## 📋 프로젝트 개요

BLIP VQA만을 사용한 단일 모듈 보물찾기 게임
- 기존 `main.py` → `mission_manager.py` → `blip_module.py` → `llm_hint_generator.py` 구조를 참고
- **BLIP만 사용**하여 간소화된 게임 로직 구현
- 사용자는 사진을 반복 제출하며, 정답 시 쿠폰 지급, 오답 시 LLM 힌트 제공

---

## 🎯 게임 플로우

```
[게임 시작]
    ↓
[1] answer.json에서 랜덤하게 오늘의 정답 선택
    ↓
[2] 사용자에게 힌트 제공
    "오늘의 보물찾기 힌트: 마트료시카"
    ↓
[3] 사용자가 사진 업로드
    ↓
[4] BLIP VQA로 정답 여부 판별
    ├─ [정답] → 쿠폰 지급 → [게임 종료]
    └─ [오답] → 틀린 질문 리스트 추출
                   ↓
               [5] LLM으로 힌트 생성
                   ↓
               [6] 힌트를 사용자에게 제공
                   ↓
               [3]으로 돌아가서 재시도
```

---

## 📂 파일 구조

```
C:\CLIP\github\blip_standalone_game\
├── project_plan.md           # 본 계획 문서
├── todo_list.md               # 진행 상황 체크리스트
├── game.py                    # 메인 게임 로직
├── utils/
│   ├── __init__.py
│   ├── answer_loader.py       # answer.json 랜덤 로드
│   ├── blip_checker.py        # BLIP VQA 체커 (blip_module.py 참고)
│   ├── hint_generator.py      # LLM 힌트 생성 (llm_hint_generator.py 참고)
│   └── coupon_manager.py      # 쿠폰 발급 로직
└── README.md                  # 사용법 안내
```

---

## 🔧 주요 모듈 설계

### 1. `answer_loader.py`

**역할**: `answer.json`에서 랜덤하게 오늘의 정답 선택

**함수**:
```python
def get_random_answer():
    """
    Returns:
        tuple: (answer, hint)
        예: ("네모탑", "마트료시카")
    """
```

**참고 파일**: `C:\CLIP\github\data\answer.json`

---

### 2. `blip_checker.py`

**역할**: BLIP VQA를 사용하여 사진이 정답인지 판별

**함수**:
```python
def check_answer_with_blip(image_path, answer):
    """
    Args:
        image_path (str): 사용자가 업로드한 이미지 경로
        answer (str): 정답 랜드마크 이름

    Returns:
        tuple: (is_correct, failed_questions)
        - is_correct (bool): True=정답, False=오답
        - failed_questions (list): 틀린 질문들의 상세 정보
            [{"question": str, "expected": str, "got": str}, ...]
    """
```

**참고 파일**: `C:\CLIP\github\models\blip_module.py`
- `landmark_qa_labeled.json` 사용
- 임계값: 75% (SUCCESS_THRESHOLD = 0.75)
- 오답 시 틀린 질문 리스트 반환

---

### 3. `hint_generator.py`

**역할**: LLM을 사용하여 틀린 질문 기반 힌트 생성

**함수**:
```python
def generate_hint_from_failures(answer, failed_questions):
    """
    Args:
        answer (str): 정답 랜드마크 이름
        failed_questions (list): 틀린 질문 리스트

    Returns:
        str: LLM이 생성한 힌트 메시지
    """
```

**참고 파일**: `C:\CLIP\github\models\llm_hint_generator.py`
- OpenAI GPT-4o-mini 사용
- 틀린 질문들을 프롬프트에 포함하여 추상적 힌트 생성

---

### 4. `coupon_manager.py`

**역할**: 정답 시 쿠폰 발급

**함수**:
```python
def issue_coupon(answer):
    """
    Args:
        answer (str): 정답 랜드마크 이름

    Returns:
        str: 쿠폰 코드 (예: "COUPON-네모탑-20250109-ABCD")
    """
```

**로직**:
- 랜드마크 이름 + 타임스탬프 + 랜덤 문자열로 쿠폰 생성
- (선택) 쿠폰을 파일이나 DB에 저장

---

### 5. `game.py` (메인 게임 로직)

**역할**: 전체 게임 플로우 제어

**함수**:
```python
def main():
    """
    메인 게임 루프
    1. 오늘의 정답/힌트 출력
    2. 사용자 입력 대기 (이미지 경로 or 'quit')
    3. BLIP으로 검증
    4. 정답 → 쿠폰 지급 및 종료
       오답 → LLM 힌트 생성 및 재시도
    """
```

**게임 루프 의사코드**:
```python
# 1. 정답 선택
answer, initial_hint = get_random_answer()
print(f"🎯 오늘의 보물찾기 힌트: {initial_hint}")

# 2. 게임 루프
attempt = 0
while True:
    attempt += 1
    print(f"\n--- 시도 #{attempt} ---")

    # 사용자 입력
    image_path = input("사진 경로를 입력하세요 (또는 'quit' 입력): ")
    if image_path == 'quit':
        break

    # BLIP 검증
    is_correct, failed_questions = check_answer_with_blip(image_path, answer)

    if is_correct:
        # 정답!
        coupon = issue_coupon(answer)
        print(f"🎉 정답입니다! 쿠폰: {coupon}")
        break
    else:
        # 오답
        print("❌ 오답입니다!")
        hint = generate_hint_from_failures(answer, failed_questions)
        print(f"💡 힌트: {hint}")
        print("다시 도전해보세요!\n")
```

---

## 📦 의존성

### 필수 라이브러리
```
torch
transformers
pillow
openai
python-dotenv
```

### 데이터 파일
- `C:\CLIP\github\data\answer.json`
- `C:\CLIP\github\data\landmark_qa_labeled.json`

### 환경 변수
- `.env` 파일에 `OPENAI_API_KEY` 필요

---

## 🎮 사용 예시

```bash
$ python game.py

🎯 오늘의 보물찾기 힌트: 마트료시카

--- 시도 #1 ---
사진 경로를 입력하세요 (또는 'quit' 입력): test1.jpg
❌ 오답입니다!
💡 힌트: 층층이 쌓인 구조를 찾아보세요. 어두운 색감의 탑 모양 조형물이에요.
다시 도전해보세요!

--- 시도 #2 ---
사진 경로를 입력하세요 (또는 'quit' 입력): test2.jpg
🎉 정답입니다! 쿠폰: COUPON-네모탑-20250109-A7B3

게임을 종료합니다. 감사합니다!
```

---

## 🚀 구현 순서

### Phase 1: 기본 구조 세팅
1. ✅ 폴더 구조 생성
2. ⏳ `todo_list.md` 생성
3. ⏳ `utils/__init__.py` 생성

### Phase 2: 유틸리티 모듈 구현
4. ⏳ `answer_loader.py` 작성
5. ⏳ `blip_checker.py` 작성 (blip_module.py 참고)
6. ⏳ `hint_generator.py` 작성 (llm_hint_generator.py 참고)
7. ⏳ `coupon_manager.py` 작성

### Phase 3: 메인 게임 로직
8. ⏳ `game.py` 작성
9. ⏳ README.md 작성

### Phase 4: 테스트 및 디버깅
10. ⏳ 테스트 이미지로 전체 플로우 검증
11. ⏳ 오류 수정 및 최적화

---

## ⚠️ 주의사항

### 경로 이슈
- BLIP 모듈이 `landmark_qa_labeled.json`을 참조하므로, 경로를 올바르게 설정해야 함
- 상대 경로 대신 절대 경로 사용 권장

### 모델 로딩
- BLIP 모델은 처음 로드 시 시간이 소요됨 (GPU 권장)
- 모델을 한 번만 로드하도록 전역 변수 활용

### LLM API 비용
- OpenAI API 호출 시 비용 발생
- 개발 중에는 테스트용 짧은 프롬프트 사용

---

## 📈 향후 확장 가능성

1. **웹 인터페이스**
   - Flask/FastAPI로 웹 서버 구축
   - 사용자가 브라우저에서 사진 업로드

2. **CLIP 추가**
   - 감정 분석 미션 추가
   - 2단계 검증 (장소 + 감정)

3. **리더보드**
   - 시도 횟수/시간 기록
   - 순위 시스템

4. **데이터베이스 연동**
   - 쿠폰을 DB에 저장
   - 사용자 프로필 관리

---

## 📝 참고 파일

- `C:\CLIP\github\main.py`
- `C:\CLIP\github\mission_manager.py`
- `C:\CLIP\github\models\blip_module.py`
- `C:\CLIP\github\models\llm_hint_generator.py`
- `C:\CLIP\github\data\answer.json`
- `C:\CLIP\github\data\landmark_qa_labeled.json`
