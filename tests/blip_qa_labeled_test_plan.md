# BLIP VQA Labeled Test Plan

## 목표
기존의 YES 비율 기반 평가에서 **True/False 비율 기반 평가**로 전환하여, negative 라벨링을 통해 더 정교한 랜드마크 인식 평가 수행

## 기존 방식의 문제점
- 모든 질문이 해당 랜드마크에 대해 YES를 기대하는 질문만 존재
- "피노키오" 이미지에 "사람 모양 동상이 있나요?"를 물으면 YES
- 하지만 "네모탑" 이미지에 같은 질문을 하면 NO여야 하는데, 이를 평가할 수 없음

## 새로운 방식: Labeled Q&A
각 랜드마크마다 **[질문, 기대 답변(yes/no)]** 쌍으로 구성

### 예시: 네모탑
```json
{
  "네모탑": [
    ["Is this object shaped like a tower?", "yes"],
    ["Is the height much longer than the width?", "yes"],
    ["Is there a prominent human-shaped statue in the picture?", "no"],
    ["Does the sculpture wear a suit?", "no"],
    ["Is this picture taken inside a building?", "no"],
    ...
  ]
}
```

### 평가 방식
- **True**: BLIP 답변 == 기대 답변
- **False**: BLIP 답변 != 기대 답변
- **True 비율** = True 개수 / 전체 질문 개수

## 데이터 구조 변경

### 기존: `landmark_qa.json`
```json
{
  "피노키오": ["질문1", "질문2", ...],
  "네모탑": ["질문1", "질문2", ...],
  "지혜의숲 조각상": ["질문1", "질문2", ...]
}
```

### 신규: `landmark_qa_labeled.json`
```json
{
  "피노키오": [
    ["Is there a prominent human-shaped statue in the picture?", "yes"],
    ["Is this object shaped like a tower?", "no"],
    ["Does the statue have a particularly long nose?", "yes"],
    ["Is this picture taken inside a building?", "no"],
    ...
  ],
  "네모탑": [
    ["Is this object shaped like a tower?", "yes"],
    ["Is there a prominent human-shaped statue in the picture?", "no"],
    ["Is the height much longer than the width?", "yes"],
    ["Does the sculpture wear a suit?", "no"],
    ...
  ],
  "지혜의숲 조각상": [
    ["Is this picture taken inside a building?", "yes"],
    ["Is this object shaped like a tower?", "no"],
    ["Is the main object a human-shaped sculpture?", "yes"],
    ["Does the statue have a particularly long nose?", "no"],
    ...
  ]
}
```

## 구현 단계

### Step 1: 데이터 준비
- [ ] `landmark_qa_labeled.json` 파일 생성
- [ ] 각 랜드마크별로 positive 질문 (yes 라벨) 추가
- [ ] 각 랜드마크별로 negative 질문 (no 라벨) 추가
  - 다른 랜드마크의 특징적인 질문들을 가져와서 no 라벨로 활용

### Step 2: 노트북 코드 수정
- [ ] JSON 로드 부분 수정 (질문 리스트 → [질문, 라벨] 리스트)
- [ ] VQA 실행 로직 수정
  - BLIP 답변과 기대 라벨 비교
  - True/False 카운트
- [ ] 결과 저장 구조 수정
  ```python
  {
    "image": "이미지명",
    "true_count": 10,
    "false_count": 4,
    "true_ratio": 0.714,
    "false_questions": [
      ["질문1", "기대:yes", "답변:no"],
      ["질문2", "기대:no", "답변:yes"],
      ...
    ],
    "total_questions": 14
  }
  ```

### Step 3: 최종 출력 형식
```
==================================================
    '네모탑' VQA 이미지별 평가 결과
==================================================

이미지: 1685886446687.jpg
  - True  : 12 / 14
  - False : 2
  - 정확도: 85.71%

  ❌ False 질문 목록:
    1. Q: "Is the surface smooth?"
       Expected: yes, Got: no

    2. Q: "Is there a prominent human-shaped statue?"
       Expected: no, Got: yes

-------------------------
전체 평균 정확도: 78.5%
성공 여부: ✅ PASS (threshold: 70%)
```

### Step 4: 성공 판정 기준
- True 비율 임계값 설정 (예: 70% 이상)
- 임계값 이상이면 ✅ PASS
- 미만이면 ❌ FAIL

## 추가 고려사항

### Negative 질문 선정 전략
1. **다른 랜드마크의 핵심 질문 가져오기**
   - 네모탑 → "사람 모양 동상인가?" (피노키오/지혜의숲 특징)
   - 피노키오 → "실내에서 촬영되었나?" (지혜의숲 특징)

2. **반대 속성 질문 추가**
   - "Is the color bright and colorful?" (어두운 색 랜드마크에 대해)
   - "Is it made of soft material?" (단단한 재질 랜드마크에 대해)

3. **균형 유지**
   - Positive (yes) 질문: 60-70%
   - Negative (no) 질문: 30-40%
   - 너무 많은 negative는 모델에게 불리할 수 있음

### 추후 활용
- LLM 힌트 생성기와 연동 시, False 질문들을 전달
- "이 질문들에서 틀렸으니 이 부분을 힌트로 활용"
- CLIP 감정 분석과 결합하여 종합 평가

## 예상 파일 구조
```
C:\CLIP\github\
├── data/
│   ├── landmark_qa.json (기존)
│   └── landmark_qa_labeled.json (신규)
├── tests/
│   ├── blip_qa_test.ipynb (기존)
│   └── blip_qa_labeled_test.ipynb (신규)
└── models/
    └── llm_hint_generator.py
```

## 다음 스텝
1. ✅ 계획 문서 작성 완료
2. ⏭️ `landmark_qa_labeled.json` 데이터 파일 생성
3. ⏭️ `blip_qa_labeled_test.ipynb` 노트북 작성
4. ⏭️ 테스트 및 결과 분석
