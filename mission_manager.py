# mission_manager.py
from models.blip_module import check_with_blip
from models.clip_module import check_with_clip
from models.llm_hint_generator import generate_hint
from coupon_manager import give_coupon

def run_mission(user_image, mission_type, candidates):
    if mission_type == "mission1":
        result, _ = check_with_blip(user_image, candidates)
    elif mission_type == "mission2":
        result, _ = check_with_clip(user_image, candidates)
    else:
        raise ValueError("Unknown mission type")

    if result:
        coupon = give_coupon(result)
        return {"success": True, "coupon": coupon, "hint": None}
    else:
        hint = generate_hint(candidates)
        return {"success": False, "hint": hint}
