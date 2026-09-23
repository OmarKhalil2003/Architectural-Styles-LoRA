import os
import urllib.request
import urllib.parse
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_API_URL = "https://huggingface.co/api/datasets/axel-riben/arcdataset-brutalism-extension"
RAW_BASE_URL = "https://huggingface.co/datasets/axel-riben/arcdataset-brutalism-extension/resolve/main"

STYLE_MAP = {
    "Brutalism architecture": "brutalism",
    "Bauhaus architecture": "bauhaus",
    "International style": "international_style",
    "Postmodern architecture": "postmodern"
}

TARGET_PER_STYLE = 40  # Download 40 candidates per style to audit down to 25-30 best
DEST_ROOT = r"d:\Architectural-Styles-LoRA\data\raw"

def get_file_list():
    print("Fetching dataset file list from Hugging Face API...")
    req = urllib.request.Request(BASE_API_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    siblings = [s["rfilename"] for s in data.get("siblings", [])]
    return siblings

def download_file(rel_path, dest_dir):
    parts = rel_path.split("/")
    encoded_parts = [urllib.parse.quote(p) for p in parts]
    url = f"{RAW_BASE_URL}/{'/'.join(encoded_parts)}"
    
    filename = os.path.basename(rel_path)
    out_path = os.path.join(dest_dir, filename)
    
    if os.path.exists(out_path) and os.path.getsize(out_path) > 0:
        return out_path
        
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as resp, open(out_path, "wb") as f:
        f.write(resp.read())
    return out_path

def main():
    siblings = get_file_list()
    
    # Also download brutalism_downloaded.jsonl for complete provenance
    print("Downloading brutalism_downloaded.jsonl...")
    download_file("brutalism_downloaded.jsonl", DEST_ROOT)

    tasks = []
    with ThreadPoolExecutor(max_workers=8) as executor:
        for style_name, slug in STYLE_MAP.items():
            dest_dir = os.path.join(DEST_ROOT, slug)
            os.makedirs(dest_dir, exist_ok=True)
            
            style_files = [s for s in siblings if s.startswith(f"data/{style_name}/") and s.lower().endswith((".jpg", ".jpeg", ".png"))]
            print(f"Found {len(style_files)} available files for [{style_name}]. Selecting top {TARGET_PER_STYLE} candidates.")
            
            selected = style_files[:TARGET_PER_STYLE]
            for fpath in selected:
                tasks.append(executor.submit(download_file, fpath, dest_dir))

        completed = 0
        for future in as_completed(tasks):
            try:
                res = future.result()
                completed += 1
                if completed % 20 == 0 or completed == len(tasks):
                    print(f"Downloaded {completed}/{len(tasks)} candidate images...")
            except Exception as e:
                print(f"Download error: {e}")

    print("Candidate image downloads completed.")

if __name__ == "__main__":
    main()
