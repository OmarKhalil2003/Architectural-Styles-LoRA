import os
import hashlib
import glob
import json
import numpy as np
import pandas as pd
from PIL import Image
import torch
import torchvision.transforms as transforms
import torchvision.models as models

PROCESSED_DIR = r"d:\Architectural-Styles-LoRA\data\processed\images"
MASTER_CSV = r"d:\Architectural-Styles-LoRA\metadata\dataset_master.csv"
AUDIT_DIR = r"d:\Architectural-Styles-LoRA\metadata\audit"

os.makedirs(AUDIT_DIR, exist_ok=True)

df_master = pd.read_csv(MASTER_CSV)
image_files = sorted(glob.glob(os.path.join(PROCESSED_DIR, "*.jpg")))

print(f"Total processed image files: {len(image_files)}")
print(f"Total master CSV rows: {len(df_master)}")

# ==========================================
# STEP 1: INVENTORY THE ACTUAL FILES
# ==========================================
inventory_rows = []
csv_ids = set(df_master["image_id"])
file_ids = set()

for fpath in image_files:
    fname = os.path.basename(fpath)
    img_id = os.path.splitext(fname)[0]
    file_ids.add(img_id)
    fsize = os.path.getsize(fpath)
    
    try:
        with Image.open(fpath) as im:
            w, h = im.size
            fmt = im.format
            mode = im.mode
            readable = True
            err = ""
    except Exception as e:
        w, h = 0, 0
        fmt = "UNKNOWN"
        mode = "UNKNOWN"
        readable = False
        err = str(e)
        
    ar = f"{w/h:.2f}" if h > 0 else "0.00"
    in_csv = img_id in csv_ids
    
    inventory_rows.append({
        "image_id": img_id,
        "filename": fname,
        "width": w,
        "height": h,
        "aspect_ratio": ar,
        "file_size_bytes": fsize,
        "image_format": fmt,
        "color_mode": mode,
        "readable": readable,
        "in_master_csv": in_csv,
        "error_notes": err
    })

inv_df = pd.DataFrame(inventory_rows)
inv_csv = os.path.join(AUDIT_DIR, "file_inventory.csv")
inv_df.to_csv(inv_csv, index=False)
print(f"Saved Step 1 File Inventory to {inv_csv}")

missing_in_files = csv_ids - file_ids
orphan_files = file_ids - csv_ids
print(f"Missing images referenced in CSV: {len(missing_in_files)}")
print(f"Orphan images on disk: {len(orphan_files)}")

# ==========================================
# STEP 2: EXACT DUPLICATE DETECTION (SHA-256)
# ==========================================
hashes = {}
hash_records = []

for fpath in image_files:
    fname = os.path.basename(fpath)
    img_id = os.path.splitext(fname)[0]
    with open(fpath, "rb") as f:
        sha = hashlib.sha256(f.read()).hexdigest()
    
    if sha not in hashes:
        hashes[sha] = []
    hashes[sha].append((img_id, fname))

exact_dup_rows = []
group_idx = 1
for sha, items in hashes.items():
    if len(items) > 1:
        for img_id, fname in items:
            exact_dup_rows.append({
                "group_id": f"EXACT_DUP_{group_idx:03d}",
                "image_id": img_id,
                "filename": fname,
                "sha256": sha
            })
        group_idx += 1

exact_df = pd.DataFrame(exact_dup_rows, columns=["group_id", "image_id", "filename", "sha256"])
exact_csv = os.path.join(AUDIT_DIR, "exact_duplicates.csv")
exact_df.to_csv(exact_csv, index=False)
print(f"Saved Step 2 Exact Duplicates to {exact_csv} ({len(exact_df)} rows, {len(exact_df['group_id'].unique()) if len(exact_df)>0 else 0} groups)")

# ==========================================
# STEP 3: PERCEPTUAL DUPLICATE DETECTION (pHash & dHash)
# ==========================================
def compute_phash(image, hash_size=8, highfreq_factor=4):
    import scipy.fftpack
    img = image.convert("L").resize((hash_size * highfreq_factor, hash_size * highfreq_factor), Image.Resampling.LANCZOS)
    pixels = np.asarray(img, dtype=np.float32)
    dct = scipy.fftpack.dct(scipy.fftpack.dct(pixels, axis=0), axis=1)
    dctlowfreq = dct[:hash_size, :hash_size]
    med = np.median(dctlowfreq[1:, 1:])
    diff = dctlowfreq > med
    return diff.flatten()

def compute_dhash(image, hash_size=8):
    img = image.convert("L").resize((hash_size + 1, hash_size), Image.Resampling.LANCZOS)
    pixels = np.asarray(img)
    diff = pixels[:, 1:] > pixels[:, :-1]
    return diff.flatten()

phashes = {}
dhashes = {}

for fpath in image_files:
    img_id = os.path.splitext(os.path.basename(fpath))[0]
    with Image.open(fpath) as im:
        phashes[img_id] = compute_phash(im)
        dhashes[img_id] = compute_dhash(im)

perceptual_rows = []
all_ids = sorted(list(phashes.keys()))
group_counter = 1

for i in range(len(all_ids)):
    for j in range(i + 1, len(all_ids)):
        id1 = all_ids[i]
        id2 = all_ids[j]
        
        # Hamming distance
        p_dist = int(np.sum(phashes[id1] != phashes[id2]))
        d_dist = int(np.sum(dhashes[id1] != dhashes[id2]))
        
        # Combined distance metric
        if p_dist == 0:
            sim_level = "EXACT_VISUAL_DUPLICATE"
            dec = "EXACT_VISUAL_DUPLICATE"
            flag = True
        elif p_dist <= 4 or d_dist <= 4:
            sim_level = "NEAR_DUPLICATE"
            dec = "NEAR_DUPLICATE"
            flag = True
        elif p_dist <= 10 or d_dist <= 8:
            sim_level = "POSSIBLE_DUPLICATE"
            dec = "POSSIBLE_DUPLICATE"
            flag = True
        else:
            flag = False
            
        if flag:
            perceptual_rows.append({
                "group_id": f"PERC_DUP_{group_counter:03d}",
                "image_id_1": id1,
                "image_id_2": id2,
                "filename_1": f"{id1}.jpg",
                "filename_2": f"{id2}.jpg",
                "hash_distance": p_dist,
                "similarity_level": sim_level,
                "decision": dec
            })
            group_counter += 1

perc_df = pd.DataFrame(perceptual_rows)
perc_csv = os.path.join(AUDIT_DIR, "perceptual_duplicates.csv")
perc_df.to_csv(perc_csv, index=False)
print(f"Saved Step 3 Perceptual Duplicates to {perc_csv} ({len(perc_df)} flagged pairs)")

# ==========================================
# STEP 4: IMAGE EMBEDDING SIMILARITY (ResNet-34)
# ==========================================
print("Loading local ResNet-34 feature extractor...")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

weights_path = os.path.expanduser("~/.cache/torch/hub/checkpoints/resnet34-b627a593.pth")
model = models.resnet34(weights=None)
if os.path.exists(weights_path):
    model.load_state_dict(torch.load(weights_path, map_location=device))
    print("Successfully loaded pre-trained weights from local cache.")
else:
    print("Local checkpoint not found, running standard initialization.")

# Strip classification head to get 512-dim embedding
feature_extractor = torch.nn.Sequential(*(list(model.children())[:-1])).to(device)
feature_extractor.eval()

transform = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.CenterCrop((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

embeddings = {}
with torch.no_grad():
    for fpath in image_files:
        img_id = os.path.splitext(os.path.basename(fpath))[0]
        with Image.open(fpath) as im:
            tensor = transform(im.convert("RGB")).unsqueeze(0).to(device)
            emb = feature_extractor(tensor).squeeze().cpu().numpy()
            emb_norm = emb / (np.linalg.norm(emb) + 1e-9)
            embeddings[img_id] = emb_norm

# Map styles
id_to_style = dict(zip(df_master["image_id"], df_master["style"]))

embedding_rows = []
for style_name in df_master["style"].unique():
    style_ids = [k for k, v in id_to_style.items() if v == style_name]
    for i in range(len(style_ids)):
        for j in range(i + 1, len(style_ids)):
            id1 = style_ids[i]
            id2 = style_ids[j]
            cos_sim = float(np.dot(embeddings[id1], embeddings[id2]))
            
            if cos_sim >= 0.85:
                flag = "VERY_HIGH_SIMILARITY"
            elif cos_sim >= 0.75:
                flag = "HIGH_SIMILARITY"
            elif cos_sim >= 0.65:
                flag = "MODERATE_SIMILARITY"
            else:
                flag = "LOW_SIMILARITY"
                
            if cos_sim >= 0.70:
                embedding_rows.append({
                    "style": style_name,
                    "image_id_1": id1,
                    "image_id_2": id2,
                    "similarity": round(cos_sim, 4),
                    "flag": flag
                })

emb_df = pd.DataFrame(embedding_rows)
emb_csv = os.path.join(AUDIT_DIR, "embedding_similarity.csv")
emb_df.to_csv(emb_csv, index=False)
print(f"Saved Step 4 Embedding Similarities to {emb_csv} ({len(emb_df)} flagged pairs >= 0.70)")
