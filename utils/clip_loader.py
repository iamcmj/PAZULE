# clip_loader.py
import torch
from transformers import CLIPModel, CLIPProcessor

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

clip_model = CLIPModel.from_pretrained(
    "openai/clip-vit-base-patch32",
    dtype=torch.float16,
    attn_implementation="sdpa").to(device) # sdpa=scaled dot product attention
clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")