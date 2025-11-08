# 파주 출판단지 보물찾기 AI

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/)
[![Transformers](https://img.shields.io/badge/Transformers-4.x-yellow.svg)](https://github.com/huggingface/transformers)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o--mini-green.svg)](https://openai.com/)
[![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)](https://opensource.org/licenses/MIT)

**AI 모델을 활용하여 파주 출판단지의 숨겨진 보물을 찾는 이미지 기반 미션 게임입니다.** 사용자가 랜드마크 사진을 업로드하면, AI가 사진을 분석하여 미션을 수행하고 성공 시 보상을 제공합니다. 미션 실패 시에는 사용자가 정답에 더 가까이 다가갈 수 있도록 창의적인 힌트를 생성합니다.

---

## How It Works

게임의 핵심 로직은 두 가지 AI 미션과 동적 힌트 생성 시스템으로 구성됩니다.

1.  **미션 1: 장소 인식 (BLIP-VQA)**
    *   사용자가 업로드한 이미지를 `Salesforce/blip-vqa-base` 모델이 분석합니다.
    *   `data/landmark_qa_labeled.json`에 정의된 질문-답변 쌍을 기반으로 사진 속 장소가 오늘의 정답 랜드마크인지 검증합니다.

2.  **미션 2: 감성 분석 (CLIP)**
    *   이미지의 전반적인 분위기와 감성을 CLIP 모델을 통해 분석합니다.
    *   정답 랜드마크가 가진 특정 감성 키워드와 사용자의 이미지 감성이 일치하는지 확인합니다.

3.  **힌트 생성 (GPT-4o-mini)**
    *   사용자가 미션에 실패하면, BLIP과 CLIP의 실패 정보를 종합하여 OpenAI의 `gpt-4o-mini` 모델이 힌트를 생성합니다.
    *   힌트는 정답을 직접 알려주지 않고, 은유적이고 시적인 표현을 통해 사용자의 추리를 돕습니다.

4.  **성공 및 보상**
    *   두 가지 미션을 모두 성공하면, `coupon_manager`를 통해 사용자에게 보상이 지급됩니다.

---

## Project Structure

```sh
.
├── main.py               # API 서버 실행 및 메인 로직
├── mission_manager.py      # 미션 수행 오케스트레이션
├── answer_manager.py       # 정답 및 쿠폰 관리
│
├── models/
│   ├── blip_module.py      # Mission 1: VQA 장소 인식 모델
│   ├── clip_module.py      # Mission 2: CLIP 감성 분석 모델
│   └── llm_hint_generator.py # GPT 기반 AI 힌트 생성기
│
├── data/
│   ├── landmark_qa_labeled.json # 장소별 VQA 질문 데이터
│   └── answer.json           # 일자별 정답 데이터
│
├── config/
│   └── keyword.py            # 미션 관련 키워드 설정
│
├── tests/                  # 테스트 코드
└── README.md               # 이 프로젝트의 설명서
```

---

## Key Features

-   **AI 기반 이미지 분석**: VQA와 CLIP 모델을 활용한 듀얼 미션 시스템
-   **동적 힌트 생성**: 실패 원인(장소, 감성)에 따라 LLM이 생성하는 맞춤형 힌트
-   **유연한 미션 설계**: `JSON` 파일 기반으로 새로운 랜드마크와 질문을 쉽게 추가 가능
-   **보상 시스템**: 미션 성공 시 쿠폰을 발급하여 게임의 재미와 동기 부여

---

## Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/paju-treasure-hunt.git
    cd paju-treasure-hunt
    ```

2.  **Create a virtual environment and install dependencies:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```
    *(Note: A `requirements.txt` file should be created for easy setup.)*

3.  **Set up environment variables:**
    *   `.env.example` 파일을 복사하여 `.env` 파일을 생성합니다.
    *   `OPENAI_API_KEY` 등 필요한 API 키와 설정을 입력합니다.
    ```
    OPENAI_API_KEY="sk-..."
    ```

---

## Usage

1.  **Run the application:**
    ```bash
    python main.py
    ```

2.  **Send a mission request:**
    *   애플리케이션이 실행되면, 지정된 엔드포인트(예: `/mission`)로 `POST` 요청을 보냅니다.
    *   요청 본문에는 사용자 이미지 파일과 오늘의 정답 정보가 포함되어야 합니다.

---

## Technology Stack

-   **Backend:** Python
-   **AI / ML:**
    -   PyTorch
    -   Hugging Face Transformers (BLIP, CLIP)
    -   OpenAI API (GPT-4o-mini)
-   **Others:**
    -   Pillow
    -   python-dotenv