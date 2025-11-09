# BLIP Standalone Game - Todo List

## 📊 전체 진행 상황

- **Phase 1**: 🟢 완료 (3/3)
- **Phase 2**: 🟢 완료 (4/4)
- **Phase 3**: 🟢 완료 (2/2)
- **Phase 4**: 🟡 진행 중 (0/2)

---

## Phase 1: 기본 구조 세팅

### ✅ 1. 폴더 구조 생성

- [X] `blip_standalone_game/` 폴더 생성
- [X] `utils/` 서브폴더 생성

### 🟡 2. 프로젝트 문서 작성

- [X] `project_plan.md` 작성
- [X] `todo_list.md` 작성 (본 파일)

### ✅ 3. 기본 파일 생성

- [X] `utils/__init__.py` 생성
- [ ] `.env` 파일 확인 (OPENAI_API_KEY)

---

## Phase 2: 유틸리티 모듈 구현

### ✅ 4. answer_loader.py 작성

- [X] `get_random_answer()` 함수 구현
- [X] `answer.json` 파일 로드 로직
- [X] 랜덤 선택 로직
- [X] 단위 테스트 (print로 확인)

**예상 코드**:

```python
def get_random_answer():
    # answer.json 로드
    # missions 배열에서 랜덤 선택
    # (answer, hint) 반환
```

---

### ✅ 5. blip_checker.py 작성

- [X] `blip_module.py` 코드 참고하여 이식
- [X] `check_answer_with_blip()` 함수 구현
- [X] BLIP 모델 로드 로직
- [X] `landmark_qa_labeled.json` 로드
- [X] VQA 실행 및 정확도 계산
- [X] 틀린 질문 리스트 추출
- [X] 단위 테스트 (테스트 이미지로 검증)

**핵심 로직**:

```python
def check_answer_with_blip(image_path, answer):
    # 1. 모델 로드 (전역 변수 활용)
    # 2. landmark_qa_labeled.json에서 질문 로드
    # 3. 이미지 로드
    # 4. VQA 실행
    # 5. 정확도 계산 (>= 75% → True)
    # 6. 틀린 질문 리스트 반환
    return (is_correct, failed_questions)
```

---

### ✅ 6. hint_generator.py 작성

- [X] `llm_hint_generator.py` 코드 참고하여 이식
- [X] `generate_hint_from_failures()` 함수 구현
- [X] OpenAI 클라이언트 초기화
- [X] 틀린 질문 기반 프롬프트 생성
- [X] GPT-4o-mini 호출
- [X] 힌트 반환
- [X] 단위 테스트 (샘플 질문으로 확인)

**핵심 로직**:

```python
def generate_hint_from_failures(answer, failed_questions):
    # 1. OpenAI 클라이언트 초기화
    # 2. failed_questions를 텍스트로 포맷팅
    # 3. 프롬프트 생성
    # 4. GPT 호출
    # 5. 힌트 반환
    return hint
```

---

### ✅ 7. coupon_manager.py 작성

- [X] `issue_coupon()` 함수 구현
- [X] 쿠폰 코드 생성 로직 (랜드마크 + 타임스탬프 + 랜덤)
- [X] (선택) 쿠폰 파일 저장
- [X] 단위 테스트

**핵심 로직**:

```python
def issue_coupon(answer):
    # 예: COUPON-네모탑-20250109-A7B3
    import datetime
    import random
    import string

    timestamp = datetime.datetime.now().strftime("%Y%m%d")
    random_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    coupon = f"COUPON-{answer}-{timestamp}-{random_code}"

    # (선택) 파일에 저장
    return coupon
```

---

## Phase 3: 메인 게임 로직

### ✅ 8. game.py 작성

- [X] 메인 게임 루프 구현
- [X] 오늘의 정답/힌트 출력
- [X] 사용자 입력 받기 (이미지 경로)
- [X] BLIP 검증 호출
- [X] 정답/오답 분기 처리
- [X] LLM 힌트 생성 및 출력
- [X] 쿠폰 발급 및 게임 종료

**게임 루프 구조**:

```python
def main():
    # 1. 정답 선택
    answer, hint = get_random_answer()
    print(f"오늘의 힌트: {hint}")

    # 2. 게임 루프
    attempt = 0
    while True:
        attempt += 1
        image_path = input("사진 경로: ")

        if image_path == 'quit':
            break

        is_correct, failed = check_answer_with_blip(image_path, answer)

        if is_correct:
            coupon = issue_coupon(answer)
            print(f"정답! 쿠폰: {coupon}")
            break
        else:
            hint = generate_hint_from_failures(answer, failed)
            print(f"오답! 힌트: {hint}")
```

---

### ✅ 9. README.md 작성

- [X] 프로젝트 설명
- [X] 설치 방법
- [X] 사용 방법
- [X] 예시 스크린샷/로그

---

## Phase 4: 테스트 및 디버깅

### ⏳ 10. 전체 플로우 테스트

- [ ] 테스트 이미지 준비 (정답 이미지, 오답 이미지)
- [ ] `game.py` 실행
- [ ] 오답 → 힌트 → 재시도 플로우 검증
- [ ] 정답 → 쿠폰 발급 검증

**테스트 시나리오**:

1. 오답 이미지 2회 제출 → 힌트 확인
2. 정답 이미지 제출 → 쿠폰 확인

---

### ⏳ 11. 오류 수정 및 최적화

- [ ] 경로 오류 수정
- [ ] 모델 로딩 최적화
- [ ] 예외 처리 추가
- [ ] 코드 리팩토링

**체크리스트**:

- [ ] 존재하지 않는 이미지 경로 입력 시 에러 처리
- [ ] answer.json 파일 없을 때 에러 처리
- [ ] landmark_qa_labeled.json 파일 없을 때 에러 처리
- [ ] OPENAI_API_KEY 없을 때 에러 처리
- [ ] BLIP 모델 로드 실패 시 에러 처리

---

## 🎯 완료 기준

- [X] Phase 1 완료
- [X] Phase 2 완료
- [X] Phase 3 완료
- [ ] Phase 4 완료
- [ ] 최종 테스트 통과
- [X] README.md 작성 완료

---

## 📅 진행 기록

### 2025-011-09

- ✅ 프로젝트 계획 수립
- ✅ 폴더 구조 생성
- ✅ `project_plan.md` 작성
- ✅ `todo_list.md` 작성

### 2025-11-09

- ✅ Phase 1 완료: 기본 구조 세팅
- ✅ Phase 2 완료: 유틸리티 모듈 구현
  - ✅ `utils/__init__.py` 생성
  - ✅ `answer_loader.py` 작성
  - ✅ `blip_checker.py` 작성
  - ✅ `hint_generator.py` 작성
  - ✅ `coupon_manager.py` 작성
- ✅ Phase 3 완료: 메인 게임 로직
  - ✅ `game.py` 작성
  - ✅ `README.md` 작성
- 🟡 Phase 4 진행 중: 테스트 및 디버깅

---

## 💡 메모

### 참고할 코드

- `C:\CLIP\github\models\blip_module.py` - BLIP 로직
- `C:\CLIP\github\models\llm_hint_generator.py` - LLM 힌트 생성

### 테스트용 이미지

- `C:\CLIP\github\metadata\test_image\` 폴더 활용
- 네모탑, 피노키오, 지혜의숲 조각상 이미지 사용

### 데이터 파일 경로

- `C:\CLIP\github\data\answer.json`
- `C:\CLIP\github\data\landmark_qa_labeled.json`

---

## 🐛 알려진 이슈

(여기에 개발 중 발견한 버그나 문제점 기록)

---

## ✨ 향후 개선 사항

1. 웹 인터페이스 추가
2. 시도 횟수 제한 (예: 5회)
3. 힌트 점진적 제공 (1차 힌트 → 2차 힌트 → ...)
4. 멀티플레이어 지원
5. 통계 기능 (평균 시도 횟수, 성공률 등)
