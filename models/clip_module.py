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
        prompts.append(' '.join(tmp))

    return prompts

def analyze_mood(image, keywords, top):
    prompts = make_prompts_from_keywords(keywords)
    inputs = clip_processor(text=prompts, images=image, return_tensors="pt", padding=True).to(device)
    outputs = clip_model(**inputs)

    logits_per_image = outputs.logits_per_image
    probs = logits_per_image.softmax(dim=1)

    topk = torch.topk(probs, k=top)
    top_keywords = []
    scores = []

    for idx, score in zip(topk.indices[0].tolist(), topk.values[0].tolist()):
        match = re.search(r"conveys a (.+?) mood", prompts[idx])
        kw = match.group(1)
        top_keywords.append(kw)
        scores.append(f"{score*100:.1f}")

    return top_keywords, scores

def find_mood(target):
    for key, values in keyword_mapping.items():
        if target in values:
            return key

def make_answer(state, kw, top_mood, top_mood_specific):
    if state == "perfect":
        result = f"완벽합니다!!🥳 {kw} 느낌을 아주 잘 담으셨어요!"
        
    elif state == "good":
        result = f"훌륭합니다☺️ {kw} 느낌이 잘 담겨 있습니다!"
        
    elif state == "not_bad":
        result = f"조금만 더 {kw} 느낌을 담아 보세요🙂 현재는 {top_mood[0]} 느낌이 더 강합니다!\n"
        result += f"현재 이 사진으로부터 강하게 인식한 키워드 2개는 다음과 같습니다!\n"
        for i, m in enumerate(top_mood_specific):
            result += f"{i+1}. {m}({top_mood[i]})\n"
            if i == 1:
                break

    elif state == "bad":
        result = f"아쉽습니다...🥲 {kw} 감성이 잘 보이지 않습니다.\n"
        result += f"현재 이 사진으로부터 인식한 키워드는 다음과 같습니다.\n"
        for i, m in enumerate(top_mood_specific):
            result += f"{i+1}. {m}({top_mood[i]})\n"
        result += f"\n💡 {feedback_guide[kw]['desc']}\n\n"
        result += "📷 이러한 키워드를 참고해보세요:\n"
        for eng, kor in feedback_guide[kw]["keywords"].items():
            result += f" - {kor}\n"
    
    return result

def check_with_clip(image, kw):
    print(f"오늘의 미션: {kw} 분위기, 감성을 지니고 있는 곳을 직접 찍어보세요!")
    label_pairs = make_label_pairs(keyword_mapping)
    
    if kw in kw_strong:
        top_keywords, scores = analyze_mood(image, label_pairs, 5)
        top_mood = []
        top_mood_specific = []

        for key in top_keywords:
            top_mood.append(find_mood(key))
            top_mood_specific.append(feedback_guide[find_mood(key)]["keywords"][key])

        if top_mood[0] == kw and top_mood[1] == kw:
            state = "perfect"
            
        elif top_mood[0] == kw or sum(k == kw for k in top_mood) >= 3:
            state = "good"
            
        elif kw in top_mood:
            state = "not_bad"
                
        else:
            state = "bad"

        result = make_answer(state, kw, top_mood, top_mood_specific)

    elif kw in kw_middle:
        top_keywords, scores = analyze_mood(image, label_pairs, 7)
        top_mood = []
        top_mood_specific = []

        for key in top_keywords:
            top_mood.append(find_mood(key))
            top_mood_specific.append(feedback_guide[find_mood(key)]["keywords"][key])

        if top_mood[0] == kw or sum(k == kw for k in top_mood[:5]) >= 2:
            state = "perfect"
            
        elif sum(k == kw for k in top_mood) >= 2:
            state = "good"

        elif kw in top_mood:
            state = "not_bad"

        else:
            state = "bad"

        result = make_answer(state, kw, top_mood, top_mood_specific)

    elif kw in kw_weak:
        top_keywords, scores = analyze_mood(image, label_pairs, 9)
        top_mood = []
        top_mood_specific = []

        for key in top_keywords:
            top_mood.append(find_mood(key))
            top_mood_specific.append(feedback_guide[find_mood(key)]["keywords"][key])

        if top_mood[0] == kw or sum(k == kw for k in top_mood[:7]) >= 2:
            state = "perfect"
        
        elif kw in top_mood[:7]:
            state = "good"
            
        elif kw in top_mood:
            state = "not_bad"
            
        else:
            state = "bad"
        
        result = make_answer(state, kw, top_mood, top_mood_specific)
    
    is_success = state in ["perfect", "good"]
    clip_result = {
            "mission_keyword": kw,
            "is_success": False,
            "state": state,
            "top_moods": top_mood[:5],
            "feedback_message": result,
            "suggested_keywords": list(feedback_guide[kw]["keywords"].values())
        }

    return is_success, clip_result
        
if __name__ == "__main__":
    # 예시 실행
    # 돌려보고 싶으면 python models/clip_module.py
    
    kw = "옛스러운"
    image_path = os.path.join(PROJECT_ROOT, "data", "지혜의숲 조각상", "IMG_9802.jpg")
    image = Image.open(image_path).convert("RGB")

    is_success, hint = check_with_clip(image, kw)
    print("is_success:", is_success, "hint:", hint)