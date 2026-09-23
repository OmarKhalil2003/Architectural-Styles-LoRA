import os
import torch
import torchvision.models as models
import torchvision.transforms as transforms
import pandas as pd
import numpy as np
from PIL import Image, ImageDraw

print("=== RERUNNING FEATURE-SPACE SIMILARITY (RESNET-34) ===")
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

model = models.resnet34(weights=models.ResNet34_Weights.DEFAULT).to(device)
feat_extractor = torch.nn.Sequential(*(list(model.children())[:-1])).to(device)
feat_extractor.eval()

transform = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.CenterCrop((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

train_df = pd.read_csv("data/clean/metadata/train.csv")
brut_train = train_df[train_df["style"] == "Brutalism architecture"].copy()
train_img_dir = "data/clean/images/brutalism"

train_embs = {}
train_meta = {}
train_emb_list = []
with torch.no_grad():
    for _, r in brut_train.iterrows():
        img_id = r["image_id"]
        fpath = os.path.join(train_img_dir, f"{img_id}.jpg")
        with Image.open(fpath) as im:
            t = transform(im.convert("RGB")).unsqueeze(0).to(device)
            feat = feat_extractor(t).squeeze().cpu().numpy()
            norm_feat = feat / (np.linalg.norm(feat) + 1e-9)
            train_embs[img_id] = norm_feat
            train_meta[img_id] = r["building_name"]
            train_emb_list.append(norm_feat)

# Compute clean train-vs-train baseline excluding self-similarity (diagonal)
tr_array = np.array(train_emb_list)
tr_sim_matrix = np.dot(tr_array, tr_array.T)
diag_mask = ~np.eye(len(tr_sim_matrix), dtype=bool)
tr_off_diag = tr_sim_matrix[diag_mask]
print(f"Train vs Train (excluding diagonal self-similarity): mean={tr_off_diag.mean():.4f}, std={tr_off_diag.std():.4f}, max={tr_off_diag.max():.4f}, min={tr_off_diag.min():.4f}")

eval_csv_path = "outputs/brutalism_sdxl_lora_v1/evaluation_results.csv"
eval_df = pd.read_csv(eval_csv_path)
lora_img_dir = "evaluation/lora"

results = []
panels_to_generate = []

with torch.no_grad():
    for idx, r in eval_df.iterrows():
        gen_filename = f"lora_eval_{idx+1:02d}.jpg"
        gen_path = os.path.join(lora_img_dir, gen_filename)
        with Image.open(gen_path) as im:
            t = transform(im.convert("RGB")).unsqueeze(0).to(device)
            feat = feat_extractor(t).squeeze().cpu().numpy()
            gen_emb = feat / (np.linalg.norm(feat) + 1e-9)

        sims = {tr_id: float(np.dot(gen_emb, tr_emb)) for tr_id, tr_emb in train_embs.items()}
        sorted_sims = sorted(sims.items(), key=lambda x: x[1], reverse=True)
        top1_id, top1_sim = sorted_sims[0]
        top2_id, top2_sim = sorted_sims[1]
        top3_id, top3_sim = sorted_sims[2]

        if top1_sim >= 0.85:
            cat = "HIGH_FEATURE_SIMILARITY_TRIGGER"
        elif top1_sim >= 0.75:
            cat = "MODERATE_FEATURE_SIMILARITY"
        elif top1_sim >= 0.65:
            cat = "LOW_FEATURE_SIMILARITY"
        else:
            cat = "NOVEL_COMPOSITION"

        results.append({
            "generated_image": gen_filename,
            "prompt_id": r["prompt_id"],
            "prompt": r["prompt"],
            "closest_training_image": top1_id,
            "building_name": train_meta[top1_id],
            "similarity": round(top1_sim, 4),
            "top2_match": f"{top2_id} ({round(top2_sim, 4)})",
            "top3_match": f"{top3_id} ({round(top3_sim, 4)})",
            "inspection_category": cat
        })

        if top1_sim >= 0.75:
            panels_to_generate.append((gen_filename, r["prompt"], top1_id, train_meta[top1_id], top1_sim))

res_df = pd.DataFrame(results)
out_csv = "evaluation/memorization_results.csv"
res_df.to_csv(out_csv, index=False)
print(f"Saved verified memorization results to {out_csv}")
print(res_df[["generated_image", "closest_training_image", "similarity", "inspection_category"]].to_string(index=False))

# Generate comparison panels with neutral label (no pre-judged architectural conclusions)
print(f"\nGenerating {len(panels_to_generate)} comparison panels (similarity >= 0.75)...")
panel_dir = "evaluation/memorization"
for gen_name, prompt, tr_id, bname, sim in panels_to_generate:
    gen_p = os.path.join(lora_img_dir, gen_name)
    tr_p = os.path.join(train_img_dir, f"{tr_id}.jpg")

    with Image.open(gen_p) as im_gen, Image.open(tr_p) as im_tr:
        g_resized = im_gen.convert("RGB").resize((600, 600), Image.Resampling.LANCZOS)
        t_resized = im_tr.convert("RGB").resize((600, 600), Image.Resampling.LANCZOS)

        canvas = Image.new("RGB", (1240, 750), color=(25, 27, 32))
        canvas.paste(g_resized, (15, 80))
        canvas.paste(t_resized, (625, 80))

        draw = ImageDraw.Draw(canvas)
        draw.text((20, 20), f"Generated: {gen_name} (LoRA w=1.0)", fill=(255, 255, 255))
        draw.text((630, 20), f"Nearest Training Exemplar: {tr_id}.jpg", fill=(255, 255, 255))
        draw.text((20, 45), f"Cosine Similarity: {sim:.4f} | Feature-Space Inspection Trigger", fill=(255, 215, 0) if sim >= 0.85 else (180, 220, 255))
        draw.text((630, 45), f"Site: {bname[:45]}", fill=(200, 200, 200))

        clean_p = (prompt[:115] + "...") if len(prompt) > 115 else prompt
        draw.text((20, 695), f"Prompt: \"{clean_p}\"", fill=(220, 220, 220))
        draw.text((20, 720), "Architectural comparison — manual inspection required", fill=(200, 200, 200))

        base_gen = gen_name.replace(".jpg", "")
        panel_filename = f"panel_{base_gen}_vs_{tr_id}.jpg"
        canvas.save(os.path.join(panel_dir, panel_filename), quality=95)
        print(f"  Saved neutral panel: {panel_filename}")
