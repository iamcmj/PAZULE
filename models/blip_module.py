<<<<<<< HEAD
# /models/blip_module.py

import os
import json
import torch
from PIL import Image
from transformers import BlipProcessor, BlipForQuestionAnswering


# --- 디바이스 설정 ---
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print(f"BLIP Module: Using device '{DEVICE}'")

# --- 모델 이름 ---
MODEL_NAME = "Salesforce/blip-vqa-base"

# --- 랜드마크별 Q&A JSON 파일 경로 ---
MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(MODULE_DIR)
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
LANDMARK_QA_FILE = os.path.join(DATA_DIR, "landmark_qa.json")

# --- 미션 성공 기준 (75%) ---
SUCCESS_THRESHOLD = 0.75


# =====================================
# 모델 및 데이터 전역 로드 (성능 최적화)
# =====================================

def load_model():
    """BLIP VQA 모델과 프로세서를 로드합니다."""
    print(f"Loading BLIP VQA model '{MODEL_NAME}'...")
    try:
        processor = BlipProcessor.from_pretrained(MODEL_NAME)
        model = BlipForQuestionAnswering.from_pretrained(MODEL_NAME).to(DEVICE)
        print("BLIP VQA model loaded successfully.")
        return processor, model
    except Exception as e:
        print(f"Error loading BLIP model: {e}")
        return None, None

def load_landmark_qa():
    """랜드마크별 Q&A 데이터를 JSON 파일에서 로드합니다."""
    try:
        with open(LANDMARK_QA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            print(f"Landmark Q&A data loaded from '{LANDMARK_QA_FILE}'.")
            return data
    except FileNotFoundError:
        print(f"Error: Landmark Q&A file not found at '{LANDMARK_QA_FILE}'.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from '{LANDMARK_QA_FILE}'.")
        return {}

# --- 모델과 데이터 로드 ---
processor, model = load_model()
landmark_qa_data = load_landmark_qa()


# =====================================
# 메인 함수
# =====================================

def check_with_blip(user_image_path, landmark_name):
    """
    BLIP VQA를 사용해 사용자 이미지가 해당 랜드마크가 맞는지 검증합니다.
    JSON에 정의된 질문 리스트를 수행하고 'yes' 답변의 비율을 계산합니다.

    Args:
        user_image_path (str): 사용자가 업로드한 이미지 파일 경로
        landmark_name (str): 오늘의 정답 랜드마크 이름 (예: "피노키오")

    Returns:
        tuple: (is_success, hint_payload)
               is_success (bool): 미션 성공 여부 (True/False)
               hint_payload (list): 'no'로 답변된 질문 목록 (LLM 힌트 생성용)
    """
    
    # --- 0. 모델 로드 확인 ---
    if not processor or not model:
        print("Error: BLIP model is not loaded. Aborting mission.")
        return False, []
        
    # --- 1. 랜드마크에 해당하는 질문 리스트 가져오기 ---
    question_list = landmark_qa_data.get(landmark_name)

    if not question_list:
        print(f"Warning: No Q&A data found for landmark '{landmark_name}'.")
        return False, []

    total_questions = len(question_list)
    if total_questions == 0:
        print(f"Warning: Empty Q&A list for landmark '{landmark_name}'.")
        return False, []

    # --- 2. 이미지 로드 ---
    try:
        raw_image = Image.open(user_image_path).convert('RGB')
    except FileNotFoundError:
        print(f"Error: User image not found at '{user_image_path}'.")
        return False, []
    except Exception as e:
        print(f"Error loading image '{user_image_path}': {e}")
        return False, []

    # --- 3. VQA 실행 및 'yes' 카운트 ---
    yes_count = 0
    no_questions_list = [] # 'no' 답변된 질문 저장용

    try:
        pixel_values = processor(images=raw_image, return_tensors="pt").pixel_values.to(DEVICE)
    except Exception as e:
        print(f"Error processing image with BLIP: {e}")
        return False, []

    print(f"Running VQA for landmark '{landmark_name}' ({total_questions} questions)...")

    for question in question_list:
        try:
            inputs = processor(text=question, return_tensors="pt").to(DEVICE)
            
            out = model.generate(
                pixel_values=pixel_values, 
                input_ids=inputs.input_ids,
                attention_mask=inputs.attention_mask,
                max_new_tokens=10 
            )
            
            model_answer = processor.decode(out[0], skip_special_tokens=True).strip().lower()
            
            # [수정] 모델의 답변이 'yes'인지 확인
            if model_answer == "yes":
                yes_count += 1
            else:
                # 'yes'가 아니면 (즉, 'no' 또는 다른 답변) 힌트 목록에 질문 추가
                no_questions_list.append(question)
                
        except Exception as e:
            print(f"Error during VQA processing for question '{question}': {e}")
            # 오류 발생 시에도 'no'로 간주하고 목록에 추가
            no_questions_list.append(question)

    # --- 4. 최종 성공 여부 판별 ---
    match_ratio = yes_count / total_questions
    is_success = match_ratio >= SUCCESS_THRESHOLD

    print(f"VQA Result: {yes_count}/{total_questions} 'yes' answers ({match_ratio:.2%}). Success: {is_success}")

    if is_success:
        return True, []
    else:
        # [수정] 실패 시 'no'로 답변된 질문 리스트를 반환
        return False, no_questions_list
    

if __name__ == "__main__":
    main(user_image="./metadata/test_image/test1.HEIC", mission_type="mission1")
=======
# blip_module.py
>>>>>>> 9e40d90ebe096e8e036d4f14aff84f9a2c41a978
