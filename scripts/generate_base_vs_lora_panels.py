import os
import pandas as pd
from PIL import Image, ImageDraw, ImageFont

base_dir = "evaluation/baseline"
lora_dir = "evaluation/lora"
out_dir = "evaluation/baseline_vs_lora"
os.makedirs(out_dir, exist_ok=True)

base_csv = pd.read_csv("outputs/brutalism_sdxl_lora_v1/baseline_results.csv")
lora_csv = pd.read_csv("outputs/brutalism_sdxl_lora_v1/evaluation_results.csv")

records = []
pair_observations = [
    {
        "concrete": "LoRA shows rougher, visibly textured board-marked concrete with matte aggregate finish vs base smooth generic render",
        "structure": "Monumental cantilevered upper volume is more massive, hard-edged, and aggressively projected forward",
        "glazing": "Glass surfaces reduced; window embrasures are deeply inset into thick load-bearing concrete frames",
        "verdict": "Clear architectural style shift towards authentic Brutalist massing without geometry collapse."
    },
    {
        "concrete": "Monolithic raw concrete shear walls with vertical formwork striations replace base polished stone/concrete hybrid",
        "structure": "Sharp angular geometries sharpened; recessed ground entrance features heavy structural shadows",
        "glazing": "Eliminates smooth commercial storefront glass, replaces with dark recessed unadorned entry slot",
        "verdict": "Stronger structural presence and texture adherence to target Brutalist visual vocabulary."
    },
    {
        "concrete": "Board-marked horizontal timber impressions clearly articulated across tiered stepped massing",
        "structure": "Piers are chunkier, load-bearing in appearance; cantilevered overhangs are heavier and more prominent",
        "glazing": "Horizontal ribbon strip fenestration maintained with darker, deeper shadow reveals",
        "verdict": "Noticeable enhancement of brutalist institutional tectonic language."
    },
    {
        "concrete": "Modular precast concrete balcony units display visible seams, beveled drip edges, and weathered patina",
        "structure": "Rhythmic modular grid articulation tightened into a more cohesive repetitive structural facade",
        "glazing": "Standard domestic balcony balustrades replaced with solid cast-concrete parapets",
        "verdict": "Significant transformation from generic modern apartments to authentic Eastern European / British council Brutalism."
    },
    {
        "concrete": "Heavy bush-hammered raw concrete surface texture replaces standard smooth beige concrete",
        "structure": "Cantilevered canopies and prominent brise-soleil sun louvers gain mass and structural thickness",
        "glazing": "Louver blades cast deep geometric shadows over recessed glass",
        "verdict": "Pronounced style reinforcement with excellent solar-shading architectural articulation."
    },
    {
        "concrete": "Exposed waffle slab soffit with distinct coffered structural ribs under the cantilevered overhang",
        "structure": "Deep horizontal ribbon embrasures recessed under heavy projecting horizontal concrete floor plates",
        "glazing": "Continuous horizontal band windows with structural mullion rhythm",
        "verdict": "High-fidelity rendering of classic civic library Brutalism (reminiscent of Boston City Hall / Northwestern Library)."
    }
]

for idx in range(min(len(base_csv), 6)):
    b_row = base_csv.iloc[idx]
    l_row = lora_csv.iloc[idx]

    b_file = f"baseline_eval_{idx+1:02d}.jpg"
    l_file = f"lora_eval_{idx+1:02d}.jpg"

    b_img_path = os.path.join(base_dir, b_file)
    l_img_path = os.path.join(lora_dir, l_file)

    obs = pair_observations[idx]

    # Generate side-by-side panel
    with Image.open(b_img_path) as b_im, Image.open(l_img_path) as l_im:
        bw, bh = b_im.size
        lw, lh = l_im.size

        # Resize to 650x650
        b_res = b_im.convert("RGB").resize((650, 650), Image.Resampling.LANCZOS)
        l_res = l_im.convert("RGB").resize((650, 650), Image.Resampling.LANCZOS)

        canvas = Image.new("RGB", (1340, 830), color=(20, 22, 26))
        canvas.paste(b_res, (15, 80))
        canvas.paste(l_res, (675, 80))

        draw = ImageDraw.Draw(canvas)
        draw.text((20, 20), f"BASE SDXL 1.0 (Prompt {idx+1} | Seed {b_row['seed']})", fill=(200, 210, 225))
        draw.text((680, 20), f"SDXL LoRA v1 [w=1.0] (Prompt {idx+1} | Seed {l_row['seed']})", fill=(255, 215, 0))
        draw.text((20, 48), "Pretrained SDXL Foundation Model", fill=(150, 160, 175))
        draw.text((680, 48), "Brutalist Architectural Style Adapter (Rank 16, 330 steps)", fill=(220, 200, 140))

        # Bottom qualitative notes
        p_text = b_row["prompt"]
        clean_p = (p_text[:125] + "...") if len(p_text) > 125 else p_text
        draw.text((20, 745), f"Prompt: \"{clean_p}\"", fill=(240, 240, 240))
        draw.text((20, 772), f"Concrete Texture: {obs['concrete'][:130]}", fill=(180, 220, 255))
        draw.text((20, 795), f"Structural Verdict: {obs['verdict']}", fill=(160, 255, 160))

        panel_name = f"comparison_eval_{idx+1:02d}.jpg"
        panel_path = os.path.join(out_dir, panel_name)
        canvas.save(panel_path, quality=95)
        print(f"Generated panel {panel_name}")

    records.append({
        "prompt_id": f"PAIR_{idx+1:02d}",
        "prompt": b_row["prompt"],
        "seed": b_row["seed"],
        "base_image": b_file,
        "lora_image": l_file,
        "panel_path": panel_path,
        "concrete_texture_delta": obs["concrete"],
        "structural_expression_delta": obs["structure"],
        "glazing_ratio_delta": obs["glazing"],
        "qualitative_verdict": obs["verdict"]
    })

res_df = pd.DataFrame(records)
out_csv = "evaluation/base_vs_lora_results.csv"
res_df.to_csv(out_csv, index=False)
print(f"Saved {len(records)} comparison records to {out_csv}")
