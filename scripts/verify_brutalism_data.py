import os
import pandas as pd
from PIL import Image

PROJECT_ROOT = r"d:\Architectural-Styles-LoRA"
CLEAN_DIR = os.path.join(PROJECT_ROOT, "data", "clean")
BRUTALISM_IMG_DIR = os.path.join(CLEAN_DIR, "images", "brutalism")
TRAIN_CSV = os.path.join(CLEAN_DIR, "metadata", "train.csv")
VAL_CSV = os.path.join(CLEAN_DIR, "metadata", "val.csv")
TEST_CSV = os.path.join(CLEAN_DIR, "metadata", "test.csv")

train_df = pd.read_csv(TRAIN_CSV)
val_df = pd.read_csv(VAL_CSV)
test_df = pd.read_csv(TEST_CSV)

# Filter for Brutalism architecture
brut_train = train_df[train_df["style"] == "Brutalism architecture"].copy()
brut_val = val_df[val_df["style"] == "Brutalism architecture"].copy()
brut_test = test_df[test_df["style"] == "Brutalism architecture"].copy()

print("=" * 60)
print("STEP 1: VERIFY TRAINING DATA (BRUTALISM SUBSET)")
print("=" * 60)

total_records = len(brut_train) + len(brut_val) + len(brut_test)
print(f"Total images: {total_records}")
print(f"Training images: {len(brut_train)}")
print(f"Validation images: {len(brut_val)}")
print(f"Test images: {len(brut_test)}")

all_brut = pd.concat([brut_train, brut_val, brut_test], ignore_index=True)

missing_count = 0
invalid_count = 0
empty_captions = 0
non_rgb_count = 0
low_res_count = 0
duplicate_filenames = 0

seen_filenames = set()

for idx, r in all_brut.iterrows():
    img_id = r["image_id"]
    filename = f"{img_id}.jpg"
    img_path = os.path.join(BRUTALISM_IMG_DIR, filename)
    caption = str(r["caption"]).strip() if pd.notna(r["caption"]) else ""
    
    if filename in seen_filenames:
        duplicate_filenames += 1
    seen_filenames.add(filename)
    
    if not os.path.exists(img_path):
        missing_count += 1
        print(f"Missing image: {img_path}")
        continue
        
    try:
        with Image.open(img_path) as im:
            w, h = im.size
            mode = im.mode
            if mode != "RGB":
                non_rgb_count += 1
            if min(w, h) < 768:
                low_res_count += 1
    except Exception as e:
        invalid_count += 1
        print(f"Invalid image file {img_path}: {e}")
        
    if len(caption) == 0:
        empty_captions += 1

print(f"Missing images: {missing_count}")
print(f"Invalid images: {invalid_count}")
print(f"Non-RGB images: {non_rgb_count}")
print(f"Low resolution (<768px): {low_res_count}")
print(f"Empty captions: {empty_captions}")
print(f"Duplicate filenames: {duplicate_filenames}")

print("\n" + "=" * 60)
print("STEP 2: VERIFY CAPTIONS (BRUTALISM SUBSET)")
print("=" * 60)

key_tokens = [
    "exposed concrete", "raw concrete", "board-marked", "massing",
    "cantilever", "cantilevered", "deep-set windows", "window embrasures",
    "geometric", "structural", "piers", "facade", "architectural photography"
]

problematic_captions = []
for idx, r in all_brut.iterrows():
    img_id = r["image_id"]
    split = r["split"]
    cap = str(r["caption"]).strip()
    
    # Check for presence of key visual tokens
    found_tokens = [tok for tok in key_tokens if tok in cap.lower()]
    
    # Check for unwanted historical fluff
    unwanted = ["famous architect", "built in", "historic example", "important monument", "beautiful"]
    has_unwanted = [u for u in unwanted if u in cap.lower()]
    
    if len(found_tokens) < 3 or len(has_unwanted) > 0:
        problematic_captions.append((img_id, cap, has_unwanted))
        
    print(f"[{img_id}] ({split}): {cap}")
    print(f"   -> Visual tokens found ({len(found_tokens)}): {', '.join(found_tokens)}\n")

print(f"Problematic captions identified: {len(problematic_captions)}")
if problematic_captions:
    for pid, pcap, punw in problematic_captions:
        print(f"  Flagged: {pid} (unwanted: {punw}) -> {pcap}")
