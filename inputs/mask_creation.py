import os
import torch
import torch.nn.functional as F
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from transformers import SegformerImageProcessor, AutoModelForSemanticSegmentation
from transformers import AutoImageProcessor


def generate_mask(image_path, model, processor):
    """Generates a segmentation mask for the given image."""
    image = Image.open(image_path).convert("RGB")
    inputs = processor(images=image, return_tensors="pt")
    outputs = model(**inputs)
    logits = outputs.logits
    upsampled_logits = F.interpolate(
        logits,
        size=image.size[::-1],
        mode='bilinear',
        align_corners=False
    )
    pred_seg = upsampled_logits.argmax(dim=1)[0].numpy()
    mask = (pred_seg > 0).astype(np.uint8) * 255  # Convert to binary mask (0 or 255)
    return Image.fromarray(mask)

def process_images_in_folder(folder_path):
    """Processes all front and back images in the folder, saving corresponding masks."""
    model = AutoModelForSemanticSegmentation.from_pretrained("mattmdjaga/segformer_b2_clothes")
    processor = AutoImageProcessor.from_pretrained("mattmdjaga/segformer_b2_clothes")
    
    for file in os.listdir(folder_path):
        if file.startswith("front_") and file.endswith(".jpg"):
            image_id = file.split("_")[1].split(".")[0]
            mask_path = os.path.join(folder_path, f"maskfront_{image_id}.jpg")
        elif file.startswith("back_") and file.endswith(".jpg"):
            image_id = file.split("_")[1].split(".")[0]
            mask_path = os.path.join(folder_path, f"maskback_{image_id}.jpg")
        else:
            continue
        
        found_images = True  # Found at least one image
        image_path = os.path.join(folder_path, file)
        print(f"Processing: {image_path}")  # Debugging
        mask = generate_mask(image_path, model, processor)
        mask.save(mask_path)
        print(f"Saved mask: {mask_path}")

    if not found_images:
        print("No matching images found in the folder.")  # Debugging

if __name__ == "__main__":
    current_directory = os.getcwd()
    process_images_in_folder(current_directory)
