# 한국어 감정 분류 프로젝트 (Korean Sentiment Classification)

Boostcamp AI Tech 8기 | NAVER Connect Foundation  
한국어 리뷰 데이터를 기반으로 4단계 감정(강부정, 약부정, 약긍정, 강긍정)을 분류하는 Transformer 기반 NLP 프로젝트입니다.

---

## 🔍 프로젝트 개요
- 목표: 텍스트의 **감정 방향(긍/부정)** 및 **강도(약/강)** 분류
- 데이터: 약 279,650건의 한국어 리뷰 데이터
- 클래스 불균형 비율: 약 4.19:1
- 기간: 2025.10.23 ~ 10.31  
- 플랫폼: NAVER AI Stages (Ubuntu 20.04 / GPU 환경)

---

## 🚀 주요 특징

| 항목 | 설명 |
|------|------|
| **언어 모델** | kykim/bert-kor-base, monologg/koelectra-base-v3, klue/bert-base, kcbert-base, klue/roberta-base |
| **학습 구조** | Stratified 5-Fold 교차 검증 |
| **모델 헤드 구조** | Polarity(긍/부정) + Intensity(강/약) 이중 헤드 구조 |
| **앙상블** | Soft/Hard Voting, Correlation-based Stacking |
| **최종 성능** | Validation Accuracy 0.857 / Hold-out 0.837 |

---

## 🧠 모델 아키텍처

```text
Input Text
  ↓
Tokenization (BERT Tokenizer)
  ↓
Transformer Encoder (Pretrained Model)
  ↓
├── Head A: Polarity Classifier (긍/부정)
└── Head B: Intensity Classifier (강/약)
  ↓
Final Combination → 4-class 감정 확률
