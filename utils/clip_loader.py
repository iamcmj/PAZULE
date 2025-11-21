# clip_loader.py
import torch
from transformers import CLIPModel, CLIPProcessor

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# CPU/GPU 호환성: CPU일 때는 float32 사용, GPU일 때는 float16 사용
dtype = torch.float16 if device.type == "cuda" else torch.float32

# SDPA는 CUDA에서만 지원되므로 조건부 적용
model_kwargs = {
    "dtype": dtype,
}
if device.type == "cuda":
    model_kwargs["attn_implementation"] = "sdpa"

clip_model = CLIPModel.from_pretrained(
    "openai/clip-vit-base-patch32",
    **model_kwargs
).to(device)

clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")