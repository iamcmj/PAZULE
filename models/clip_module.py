# clip_module.py
import os
import re
import sys
import json
import torch
from PIL import Image

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)
from utils.clip_loader import clip_model, clip_processor, device
from config.keyword import keyword_mapping, kw_strong, kw_middle, kw_weak, rules, feedback_guide

def make_label_pairs(keyword_mapping):
    label_pairs = []
    for _, value in keyword_mapping.items():
        for v in value:
            label_pairs.append(v)
    return label_pairs


def make_prompts_from_keywords(keywords, templates=None):
    if templates is None:
        templates = [
            "A photo that conveys a {} mood.",
            "An image evoking a feeling of {}.",
            "A picture that feels {}.",
            # "A scene with a {} atmosphere.", # 필요시 추가할 것
            # "A photo expressing {} emotions."
        ]

    prompts = []
    for kw in keywords:
        tmp = []
        for t in templates:
            tmp.append(t.format(kw))
        prompts.append(" ".join(tmp))

    return prompts

def analyze_mood(image, keywords, top):
    prompts = make_prompts_from_keywords(keywords)
    inputs = clip_processor(
        text=prompts, images=image, return_tensors="pt", padding=True
    ).to(device)
    outputs = clip_model(**inputs)

    logits_per_image = outputs.logits_per_image
    probs = logits_per_image.softmax(dim=1)

    topk = torch.topk(probs, k=top)
    top_keywords = []

    for idx in topk.indices[0].tolist():
        match = re.search(r"conveys a (.+?) mood", prompts[idx])
        kw = match.group(1)
        top_keywords.append(kw)

    return top_keywords

def find_mood(target):
    for key, values in keyword_mapping.items():
        if target in values:
            return key

def check_with_clip(image, kw):
    """
    CLIP을 사용하여 이미지의 감정/분위기를 분석하고 목표 키워드와 일치하는지 확인합니다.

    Args:
        image (str or PIL.Image): 이미지 파일 경로 또는 PIL Image 객체
        kw (str): 목표 감정/분위기 키워드 (예: "고요함", "즐거움", "활기찬")

    Returns:
        tuple: (is_success, clip_info)
               is_success (bool): 미션 성공 여부 (True/False)
               clip_info (list): 감지된 감정 키워드 리스트 (힌트 생성용)
    """
    print(f"오늘의 미션: {kw} 분위기, 감성을 지니고 있는 곳을 직접 찍어보세요!")

    # 이미지 로드 (파일 경로인 경우)
    if isinstance(image, str):
        pil_image = Image.open(image).convert("RGB")
    else:
        pil_image = image  # 이미 PIL Image 객체인 경우

    label_pairs = make_label_pairs(keyword_mapping)
    is_success = False
    result = ""
    top_mood = []
    top_mood_specific = []
    clip_info = []

    if kw in kw_strong:
        top_keywords = analyze_mood(pil_image, label_pairs, 5)

        for key in top_keywords:
            top_mood.append(find_mood(key))
            top_mood_specific.append(feedback_guide[find_mood(key)]["keywords"][key])

        # 성공 여부 판단
        if top_mood[0] == kw and top_mood[1] == kw:
            is_success = True
        elif top_mood[0] == kw or sum(k == kw for k in top_mood) >= 3:
            is_success = True
        elif kw in top_mood:
            is_success = False
        else:
            is_success = False

    elif kw in kw_middle:
        top_keywords = analyze_mood(pil_image, label_pairs, 7)

        for key in top_keywords:
            top_mood.append(find_mood(key))
            top_mood_specific.append(feedback_guide[find_mood(key)]["keywords"][key])

        # 성공 여부 판단
        if top_mood[0] == kw or sum(k == kw for k in top_mood[:5]) >= 2:
            is_success = True
        elif sum(k == kw for k in top_mood) >= 2:
            is_success = True
        elif kw in top_mood:
            is_success = False
        else:
            is_success = False

    elif kw in kw_weak:
        top_keywords = analyze_mood(pil_image, label_pairs, 9)

        for key in top_keywords:
            top_mood.append(find_mood(key))
            top_mood_specific.append(feedback_guide[find_mood(key)]["keywords"][key])

        # 성공 여부 판단
        if top_mood[0] == kw or sum(k == kw for k in top_mood[:7]) >= 2:
            is_success = True
        elif kw in top_mood[:7]:
            is_success = True
        elif kw in top_mood:
            is_success = False
        else:
            is_success = False
    
    # 감정 정보 반환 (힌트 생성용)
    clip_info = top_mood[:3] if not is_success else []
    return is_success, clip_info
        
        
if __name__ == "__main__":
    # 예시 실행
    # 돌려보고 싶으면 python models/clip_module.py
    
    kw = "웅장한"
    image_path = os.path.join(PROJECT_ROOT, "data", "지혜의숲 조각상", "IMG_9802.jpg")
    image = Image.open(image_path).convert("RGB")

    is_success, clip_info = check_with_clip(image, kw)
    print(is_success, clip_info)
