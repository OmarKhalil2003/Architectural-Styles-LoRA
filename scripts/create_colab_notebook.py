import json
import os

NOTEBOOK_PATH = r"d:\Architectural-Styles-LoRA\colab\brutalism_sdxl_lora.ipynb"
os.makedirs(os.path.dirname(NOTEBOOK_PATH), exist_ok=True)

cells = []

def add_md(source):
    cells.append({
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in source.split("\n")]
    })

def add_code(source):
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in source.split("\n")]
    })

# -------------------------------------------------------------
# Title & Introduction
# -------------------------------------------------------------
add_md("""# Brutalism Architecture SDXL LoRA: Pilot Training & Evaluation

**Project**: Architectural-Styles-LoRA / Architectural Styles LoRA  
**Experiment**: `brutalism_sdxl_lora_v1`  
**Objective**: Train and evaluate an SDXL LoRA on a curated 22-image training set of Brutalist architecture to determine whether the model learns target architectural vocabulary (board-marked raw concrete, cantilevered volumes, deep-set window embrasures, structural piers) without style leakage or memorization.

---
### Workflow Overview
1. **Mount Google Drive**
2. **Configure Hyperparameters & Paths**
3. **Verify GPU Hardware (T4 / L4 / A100)**
4. **Install Pinned Dependencies**
5. **Verify Dataset Integrity (22 train, 3 val, 3 test)**
6. **Load Base SDXL 1.0 & Generate Baseline Samples**
7. **Execute LoRA Fine-Tuning** (`START TRAINING HERE`)
8. **Inspect Checkpoints & Load Final LoRA**
9. **Generate Evaluation Samples (Identical Seeds)**
10. **Run Style Leakage Probes**
11. **Check Memorization against Training Specimens**
12. **Package Results for Download**
""")

# -------------------------------------------------------------
# Section 1: Mount Google Drive
# -------------------------------------------------------------
add_md("## 1. Mount Google Drive\nConnect your Google Drive where the project repository is located.")
add_code("""from google.colab import drive
import os

# Mount Google Drive
drive.mount('/content/drive')
""")

# -------------------------------------------------------------
# Section 2: Global Configuration
# -------------------------------------------------------------
add_md("""## 2. Configuration & Paths
Define project paths and training hyperparameters. You only need to modify `PROJECT_ROOT` if your directory structure differs.""")
add_code("""import os

# ==============================================================================
# PROJECT & RUNTIME CONFIGURATION
# ==============================================================================
# Base directory where Architectural-Styles-LoRA repository is located on Google Drive:
PROJECT_ROOT = "/content/drive/MyDrive/Architectural-Styles-LoRA"

EXPERIMENT_NAME = "brutalism_sdxl_lora_v1"
MODEL_ID = "stabilityai/stable-diffusion-xl-base-1.0"
VAE_ID = "madebyollin/sdxl-vae-fp16-fix"

# Training Hyperparameters
RESOLUTION = 768            # Conservative 768px for pilot stability and VRAM headroom
BATCH_SIZE = 1              # Batch size per device
GRADIENT_ACCUMULATION = 4   # Effective batch size = 4
LEARNING_RATE = 1e-4        # Learning rate for UNet LoRA
LORA_RANK = 16              # Rank 16 prevents memorization on small 22-image dataset
LORA_ALPHA = 16             # Standard rank:alpha ratio 1:1
NUM_EPOCHS = 15             # 15 epochs across 22 images
MAX_TRAIN_STEPS = 330       # Total training steps (Set to 50 for quick dry run)
SEED = 42

# Directory Paths
DATA_DIR = os.path.join(PROJECT_ROOT, "data", "clean")
IMAGES_DIR = os.path.join(DATA_DIR, "images", "brutalism")
TRAIN_CSV = os.path.join(DATA_DIR, "metadata", "train.csv")
VAL_CSV = os.path.join(DATA_DIR, "metadata", "val.csv")
TEST_CSV = os.path.join(DATA_DIR, "metadata", "test.csv")

OUTPUT_DIR = os.path.join(PROJECT_ROOT, "outputs", EXPERIMENT_NAME)
BASELINE_DIR = os.path.join(OUTPUT_DIR, "baseline")
LORA_DIR = os.path.join(OUTPUT_DIR, "lora")
VAL_DIR = os.path.join(OUTPUT_DIR, "validation")
EVAL_DIR = os.path.join(OUTPUT_DIR, "evaluation")
FINAL_DIR = os.path.join(OUTPUT_DIR, "final")

for d in [OUTPUT_DIR, BASELINE_DIR, LORA_DIR, VAL_DIR, EVAL_DIR, FINAL_DIR]:
    os.makedirs(d, exist_ok=True)

print(f"Project Root     : {PROJECT_ROOT}")
print(f"Output Directory : {OUTPUT_DIR}")
print(f"Max Train Steps  : {MAX_TRAIN_STEPS}")
""")

# -------------------------------------------------------------
# Section 3: GPU Verification
# -------------------------------------------------------------
add_md("""## 3. GPU Verification & Guardrails
Audit GPU model and available VRAM. Halts execution if GPU is missing or VRAM is insufficient (<11 GB).""")
add_code("""import sys
import torch

print("=== Colab Environment & Hardware Verification ===")
print(f"Python version : {sys.version.split()[0]}")
print(f"PyTorch version: {torch.__version__}")
print(f"CUDA available : {torch.cuda.is_available()}")

if not torch.cuda.is_available():
    raise RuntimeError("CRITICAL ERROR: No GPU detected! Go to Runtime -> Change runtime type -> Select T4, L4, or A100 GPU.")

gpu_name = torch.cuda.get_device_name(0)
props = torch.cuda.get_device_properties(0)
total_vram_gb = props.total_memory / (1024**3)

print(f"GPU Model      : {gpu_name}")
print(f"Total VRAM     : {total_vram_gb:.2f} GB")
print(f"CUDA Capability: {props.major}.{props.minor}")

if total_vram_gb < 11.0:
    raise RuntimeError(
        f"INSUFFICIENT VRAM: {gpu_name} has only {total_vram_gb:.2f} GB VRAM. "
        "SDXL LoRA training requires at least 11 GB VRAM. "
        "Please select a T4 (16 GB), L4 (24 GB), or A100 (40 GB) runtime in Google Colab."
    )
else:
    print(f"SUCCESS: {gpu_name} with {total_vram_gb:.2f} GB VRAM is sufficient for SDXL LoRA pilot training!")
""")

# -------------------------------------------------------------
# Section 4: Dependency Installation
# -------------------------------------------------------------
add_md("""## 4. Install Pinned Dependencies
Installs verified versions of Hugging Face Diffusers, Accelerate, PEFT, and bitsandbytes.""")
add_code("""!pip install -q \\
    "torch>=2.1.0" \\
    "torchvision>=0.16.0" \\
    "diffusers>=0.30.0" \\
    "transformers>=4.44.0" \\
    "accelerate>=0.33.0" \\
    "peft>=0.12.0" \\
    "safetensors>=0.4.0" \\
    "bitsandbytes>=0.43.0" \\
    "scipy" \\
    "scikit-learn" \\
    "pandas" \\
    "pillow"
""")

# -------------------------------------------------------------
# Section 5: Dependency Verification
# -------------------------------------------------------------
add_md("## 5. Verify Installed Dependencies\nVerify package imports and version compatibility.")
add_code("""import importlib

packages = [
    "torch", "torchvision", "diffusers", "transformers",
    "accelerate", "peft", "safetensors", "bitsandbytes"
]

print("=== Installed Package Versions ===")
for pkg in packages:
    try:
        mod = importlib.import_module(pkg)
        ver = getattr(mod, "__version__", "available")
        print(f"  {pkg:15}: {ver}")
    except ImportError as e:
        print(f"  {pkg:15}: ERROR - {e}")
""")

# -------------------------------------------------------------
# Section 6: Dataset Verification
# -------------------------------------------------------------
add_md("""## 6. Dataset Verification
Checks that exactly 22 training images, 3 validation images, and 3 test images exist, open correctly, and meet resolution standards.""")
add_code("""import os
import pandas as pd
from PIL import Image

print("=== Verifying Brutalism Pilot Dataset ===")

for path_name, path_val in [("Train CSV", TRAIN_CSV), ("Val CSV", VAL_CSV), ("Test CSV", TEST_CSV)]:
    if not os.path.exists(path_val):
        raise FileNotFoundError(f"Missing required metadata file: {path_val}")

train_df = pd.read_csv(TRAIN_CSV)
val_df = pd.read_csv(VAL_CSV)
test_df = pd.read_csv(TEST_CSV)

brut_train = train_df[train_df["style"] == "Brutalism architecture"].copy()
brut_val = val_df[val_df["style"] == "Brutalism architecture"].copy()
brut_test = test_df[test_df["style"] == "Brutalism architecture"].copy()

print(f"Brutalism Training records   : {len(brut_train)}")
print(f"Brutalism Validation records : {len(brut_val)}")
print(f"Brutalism Test records       : {len(brut_test)}")

if len(brut_train) != 22:
    raise ValueError(f"Expected exactly 22 training images, but found {len(brut_train)}!")
if len(brut_val) != 3:
    raise ValueError(f"Expected exactly 3 validation images, but found {len(brut_val)}!")
if len(brut_test) != 3:
    raise ValueError(f"Expected exactly 3 test images, but found {len(brut_test)}!")

all_brut = pd.concat([brut_train, brut_val, brut_test], ignore_index=True)
for idx, row in all_brut.iterrows():
    img_file = os.path.join(IMAGES_DIR, f"{row['image_id']}.jpg")
    if not os.path.exists(img_file):
        raise FileNotFoundError(f"Missing image on disk: {img_file}")
    with Image.open(img_file) as im:
        if im.mode != "RGB":
            raise ValueError(f"Image {img_file} is not RGB: {im.mode}")
        if min(im.size) < 768:
            raise ValueError(f"Image {img_file} shortest side is {min(im.size)}px (< 768px)")
        if not str(row["caption"]).strip():
            raise ValueError(f"Image {row['image_id']} has empty caption!")

print("SUCCESS: All 28 Brutalism images verified on disk (22 train, 3 val, 3 test), all RGB >= 768px.")
""")

# -------------------------------------------------------------
# Section 7: Load Base Model Pipeline
# -------------------------------------------------------------
add_md("""## 7. Load Base SDXL 1.0 Pipeline
Loads base SDXL 1.0 with the FP16-safe VAE to prevent NaN / black-image artifacts.""")
add_code("""import torch
from diffusers import StableDiffusionXLPipeline, AutoencoderKL

print(f"Loading Base SDXL Pipeline ({MODEL_ID}) and VAE ({VAE_ID})...")

vae = AutoencoderKL.from_pretrained(
    VAE_ID,
    torch_dtype=torch.float16
)

pipe = StableDiffusionXLPipeline.from_pretrained(
    MODEL_ID,
    vae=vae,
    torch_dtype=torch.float16,
    variant="fp16",
    use_safetensors=True
).to("cuda")

pipe.enable_attention_slicing()
print("Base SDXL 1.0 pipeline successfully loaded in FP16!")
""")

# -------------------------------------------------------------
# Section 8: Baseline Generation
# -------------------------------------------------------------
add_md("""## 8. Baseline SDXL Generation (Before LoRA)
Generates baseline images using predefined evaluation prompts and fixed seeds for direct before/after comparison.""")
add_code("""import os
import pandas as pd
import torch

print("=== Generating Baseline SDXL 1.0 Images (Before LoRA) ===")

eval_prompts_file = os.path.join(PROJECT_ROOT, "evaluation", "brutalism_prompts.txt")
with open(eval_prompts_file, "r", encoding="utf-8") as f:
    eval_lines = [line.strip() for line in f if line.strip() and not line.startswith("#")]

# Select top 6 representative evaluation prompts
baseline_prompts = eval_lines[:6]
baseline_records = []

for idx, prompt_text in enumerate(baseline_prompts):
    clean_prompt = prompt_text.split(". ", 1)[-1] if ". " in prompt_text[:4] else prompt_text
    seed = SEED + idx
    generator = torch.Generator(device="cuda").manual_seed(seed)
    
    print(f"Generating Baseline [{idx+1}/{len(baseline_prompts)}] Seed={seed}: {clean_prompt[:60]}...")
    image = pipe(
        prompt=clean_prompt,
        num_inference_steps=30,
        guidance_scale=7.5,
        generator=generator,
        height=RESOLUTION,
        width=RESOLUTION
    ).images[0]
    
    out_name = f"baseline_eval_{idx+1:02d}.jpg"
    out_path = os.path.join(BASELINE_DIR, out_name)
    image.save(out_path, "JPEG", quality=95)
    
    baseline_records.append({
        "prompt_id": f"BASE_{idx+1:02d}",
        "prompt": clean_prompt,
        "seed": seed,
        "output_path": out_path
    })

baseline_df = pd.DataFrame(baseline_records)
baseline_df.to_csv(os.path.join(OUTPUT_DIR, "baseline_results.csv"), index=False)
print(f"Saved {len(baseline_records)} baseline images to {BASELINE_DIR}")
""")

# -------------------------------------------------------------
# Section 9: START TRAINING HERE
# -------------------------------------------------------------
add_md("""---
# >>> 9. START TRAINING HERE <<<
Execute the cell below to start the SDXL LoRA pilot training run.

- **Training Images**: 22 curated Brutalism photographs
- **Resolution**: 768×768
- **Rank / Alpha**: 16 / 16
- **Batch Size / Acc**: 1 / 4 (Effective batch size = 4)
- **Max Steps**: 330 steps (~15–20 min on Colab T4)
---
""")
add_code("""import os
import urllib.request

# Unload baseline pipeline from VRAM to free GPU memory for training
del pipe
torch.cuda.empty_cache()

# Download official Hugging Face diffusers SDXL LoRA training script
script_url = "https://raw.githubusercontent.com/huggingface/diffusers/v0.30.0/examples/text_to_image/train_text_to_image_lora_sdxl.py"
train_script = os.path.join(PROJECT_ROOT, "scripts", "train_text_to_image_lora_sdxl.py")
os.makedirs(os.path.dirname(train_script), exist_ok=True)

if not os.path.exists(train_script):
    print("Downloading train_text_to_image_lora_sdxl.py...")
    urllib.request.urlretrieve(script_url, train_script)
    print("Download complete.")

# Prepare training metadata in image directory format for diffusers
# (diffusers expects metadata.csv or metadata.jsonl inside the image folder)
brut_train_diffusers = brut_train[["image_id", "caption"]].copy()
brut_train_diffusers["file_name"] = brut_train_diffusers["image_id"] + ".jpg"
meta_csv_path = os.path.join(IMAGES_DIR, "metadata.csv")
brut_train_diffusers[["file_name", "caption"]].to_csv(meta_csv_path, index=False)
print(f"Prepared training metadata at {meta_csv_path}")

# Construct accelerate command
cmd = f\"\"\"accelerate launch --mixed_precision="fp16" "{train_script}" \\
    --pretrained_model_name_or_path="{MODEL_ID}" \\
    --pretrained_vae_model_name_or_path="{VAE_ID}" \\
    --train_data_dir="{IMAGES_DIR}" \\
    --output_dir="{FINAL_DIR}" \\
    --resolution={RESOLUTION} \\
    --random_flip \\
    --train_batch_size={BATCH_SIZE} \\
    --gradient_accumulation_steps={GRADIENT_ACCUMULATION} \\
    --max_train_steps={MAX_TRAIN_STEPS} \\
    --learning_rate={LEARNING_RATE} \\
    --lr_scheduler="constant_with_warmup" \\
    --lr_warmup_steps=30 \\
    --rank={LORA_RANK} \\
    --seed={SEED} \\
    --mixed_precision="fp16" \\
    --gradient_checkpointing \\
    --checkpointing_steps=110 \\
    --checkpoints_total_limit=3
\"\"\"

print("Executing LoRA training command:")
print(cmd)
!{cmd}
""")

# -------------------------------------------------------------
# Section 10: Checkpoint Inspection
# -------------------------------------------------------------
add_md("""## 10. Checkpoint Inspection
Inspect saved LoRA weights and verify `pytorch_lora_weights.safetensors`.""")
add_code("""import os

print(f"=== Inspecting Output Directory: {FINAL_DIR} ===")
for root, dirs, files in os.walk(FINAL_DIR):
    for f in files:
        if f.endswith((".safetensors", ".bin", ".json")):
            fpath = os.path.join(root, f)
            size_mb = os.path.getsize(fpath) / (1024 * 1024)
            print(f"  {os.path.relpath(fpath, FINAL_DIR)} ({size_mb:.2f} MB)")
""")

# -------------------------------------------------------------
# Section 11: Final LoRA Generation
# -------------------------------------------------------------
add_md("""## 11. Final LoRA Evaluation Generation
Loads the fine-tuned LoRA weights and generates outputs for all 12 evaluation prompts using the exact same seeds as baseline.""")
add_code("""import os
import pandas as pd
import torch
from diffusers import StableDiffusionXLPipeline, AutoencoderKL

print("Loading SDXL pipeline with trained Brutalism LoRA...")

vae = AutoencoderKL.from_pretrained(VAE_ID, torch_dtype=torch.float16)
lora_pipe = StableDiffusionXLPipeline.from_pretrained(
    MODEL_ID,
    vae=vae,
    torch_dtype=torch.float16,
    variant="fp16",
    use_safetensors=True
).to("cuda")

# Load trained LoRA weights
lora_pipe.load_lora_weights(FINAL_DIR)
lora_pipe.enable_attention_slicing()
print("LoRA weights successfully loaded into pipeline!")

eval_records = []
for idx, prompt_text in enumerate(eval_lines):
    clean_prompt = prompt_text.split(". ", 1)[-1] if ". " in prompt_text[:4] else prompt_text
    seed = SEED + idx
    generator = torch.Generator(device="cuda").manual_seed(seed)
    
    print(f"Generating LoRA [{idx+1}/{len(eval_lines)}] Seed={seed}: {clean_prompt[:60]}...")
    image = lora_pipe(
        prompt=clean_prompt,
        num_inference_steps=30,
        guidance_scale=7.5,
        generator=generator,
        height=RESOLUTION,
        width=RESOLUTION
    ).images[0]
    
    out_name = f"lora_eval_{idx+1:02d}.jpg"
    out_path = os.path.join(LORA_DIR, out_name)
    image.save(out_path, "JPEG", quality=95)
    
    eval_records.append({
        "prompt_id": f"LORA_EVAL_{idx+1:02d}",
        "prompt": clean_prompt,
        "seed": seed,
        "output_path": out_path
    })

eval_df = pd.DataFrame(eval_records)
eval_df.to_csv(os.path.join(OUTPUT_DIR, "evaluation_results.csv"), index=False)
print(f"Saved {len(eval_records)} LoRA evaluation images to {LORA_DIR}")
""")

# -------------------------------------------------------------
# Section 12: Style Leakage Evaluation
# -------------------------------------------------------------
add_md("""## 12. Style Leakage Probing
Tests whether the model inappropriately injects Gothic arches, Classical pediments, Baroque ornament, or Postmodern motifs.""")
add_code("""LEAKAGE_DIR = os.path.join(OUTPUT_DIR, "leakage_tests")
os.makedirs(LEAKAGE_DIR, exist_ok=True)

with open(leakage_prompts_file, "r", encoding="utf-8") as f:
    leak_lines = [line.strip() for line in f if line.strip() and not line.startswith("#") and "[" in line]

leakage_records = []
for idx, line in enumerate(leak_lines):
    tag, prompt_text = line.split("] ", 1)
    tag = tag.replace("[", "")
    seed = SEED + 100 + idx
    generator = torch.Generator(device="cuda").manual_seed(seed)
    
    print(f"Testing Leakage [{idx+1}/{len(leak_lines)}] {tag}...")
    image = lora_pipe(
        prompt=prompt_text,
        num_inference_steps=30,
        guidance_scale=7.5,
        generator=generator,
        height=RESOLUTION,
        width=RESOLUTION
    ).images[0]
    
    out_name = f"leakage_test_{idx+1:02d}_{tag}.jpg"
    out_path = os.path.join(LEAKAGE_DIR, out_name)
    image.save(out_path, "JPEG", quality=95)
    
    leakage_records.append({
        "test_tag": tag,
        "prompt": prompt_text,
        "seed": seed,
        "output_path": out_path
    })

leak_df = pd.DataFrame(leakage_records)
leak_df.to_csv(os.path.join(OUTPUT_DIR, "leakage_results.csv"), index=False)
print(f"Saved {len(leakage_records)} leakage test images to {LEAKAGE_DIR}")
""")

# -------------------------------------------------------------
# Section 13: Memorization Inspection
# -------------------------------------------------------------
add_md("""## 13. Memorization vs. Generalization Inspection
Computes feature similarity between generated evaluation images and the 22 training images using ResNet-34.""")
add_code("""import torchvision.models as models
import torchvision.transforms as transforms
import numpy as np

print("=== Running Memorization Check ===")
model = models.resnet34(weights=models.ResNet34_Weights.DEFAULT).to("cuda")
feat_extractor = torch.nn.Sequential(*(list(model.children())[:-1]))
feat_extractor.eval()

transform = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.CenterCrop((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# Extract embeddings for 22 training images
train_embs = {}
with torch.no_grad():
    for _, r in brut_train.iterrows():
        fpath = os.path.join(IMAGES_DIR, f"{r['image_id']}.jpg")
        with Image.open(fpath) as im:
            t = transform(im.convert("RGB")).unsqueeze(0).to("cuda")
            e = feat_extractor(t).squeeze().cpu().numpy()
            train_embs[r['image_id']] = e / (np.linalg.norm(e) + 1e-9)

# Compare each generated LoRA image against training images
mem_records = []
with torch.no_grad():
    for r in eval_records:
        gen_path = r["output_path"]
        with Image.open(gen_path) as im:
            t = transform(im.convert("RGB")).unsqueeze(0).to("cuda")
            e = feat_extractor(t).squeeze().cpu().numpy()
            gen_emb = e / (np.linalg.norm(e) + 1e-9)
            
        best_sim = -1.0
        best_id = ""
        for tr_id, tr_emb in train_embs.items():
            sim = float(np.dot(gen_emb, tr_emb))
            if sim > best_sim:
                best_sim = sim
                best_id = tr_id
                
        flag = "HIGH_SIMILARITY" if best_sim >= 0.85 else ("MODERATE_SIMILARITY" if best_sim >= 0.70 else "NOVEL_COMPOSITION")
        mem_records.append({
            "generated_image": os.path.basename(gen_path),
            "closest_training_image": best_id,
            "similarity": round(best_sim, 4),
            "flag": flag
        })

mem_df = pd.DataFrame(mem_records)
mem_df.to_csv(os.path.join(OUTPUT_DIR, "memorization_results.csv"), index=False)
print("Memorization inspection complete. Results:")
print(mem_df.to_string(index=False))
""")

# -------------------------------------------------------------
# Section 14: Results Packaging
# -------------------------------------------------------------
add_md("""## 14. Package Results for Download
Compresses outputs into a zip archive on Google Drive for easy local inspection.""")
add_code("""import shutil

zip_filename = os.path.join(PROJECT_ROOT, f"{EXPERIMENT_NAME}_results.zip")
print(f"Creating archive: {zip_filename}...")
shutil.make_archive(zip_filename.replace(".zip", ""), 'zip', OUTPUT_DIR)
print(f"SUCCESS: Results packaged at {zip_filename}")
print(f"File size: {os.path.getsize(zip_filename) / (1024*1024):.2f} MB")
""")

notebook_dict = {
    "cells": cells,
    "metadata": {
        "accelerator": "GPU",
        "colab": {
            "gpuType": "T4",
            "provenance": []
        },
        "kernelspec": {
            "display_name": "Python 3",
            "name": "python3"
        },
        "language_info": {
            "name": "python"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 0
}

with open(NOTEBOOK_PATH, "w", encoding="utf-8") as f:
    json.dump(notebook_dict, f, indent=2)

print(f"Generated Colab notebook with {len(cells)} cells at {NOTEBOOK_PATH}")
