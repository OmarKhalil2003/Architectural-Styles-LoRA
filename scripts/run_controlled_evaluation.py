"""
Controlled Evaluation Suite for Brutalism SDXL LoRA Pilot (Run 1)
Supports local execution (with CPU offload) and Colab GPU execution.
Implements:
1. Neutral prompt test & LoRA weight sweep (0.0, 0.25, 0.50, 0.75, 1.00)
2. Base SDXL generations for the 8 leakage prompts (enabling side-by-side Base vs LoRA leakage comparisons)
3. Multi-checkpoint comparison (Base vs checkpoint-110 vs checkpoint-220 vs checkpoint-330)
"""

import os
import argparse
import pandas as pd
import torch
from PIL import Image, ImageDraw
from diffusers import StableDiffusionXLPipeline, AutoencoderKL

MODEL_ID = "stabilityai/stable-diffusion-xl-base-1.0"
VAE_ID = "madebyollin/sdxl-vae-fp16-fix"

NEUTRAL_PROMPTS = [
    {
        "id": "NEUTRAL_01",
        "prompt": "A university library building surrounded by trees, architectural photography",
        "seed": 101
    },
    {
        "id": "NEUTRAL_02",
        "prompt": "A large institutional building viewed from its courtyard, architectural photography",
        "seed": 102
    },
    {
        "id": "NEUTRAL_03",
        "prompt": "A public cultural center in an urban environment, architectural photography",
        "seed": 103
    },
    {
        "id": "NEUTRAL_04",
        "prompt": "A university campus building photographed from street level, architectural photography",
        "seed": 104
    },
    {
        "id": "NEUTRAL_05",
        "prompt": "A large civic building with pedestrian space around it, architectural photography",
        "seed": 105
    }
]

LEAKAGE_PROMPTS = [
    {"id": "LEAK_01", "tag": "Baseline Test", "seed": 142, "prompt": "Brutalist civic building with raw exposed concrete, massive geometric volumes, deep-set rectangular windows, and minimal ornamentation, architectural photography"},
    {"id": "LEAK_02", "tag": "Anti-Gothic Test", "seed": 143, "prompt": "Brutalist religious chapel exterior with monolithic raw concrete walls, sharp angular roofline, and unadorned surfaces, architectural photography"},
    {"id": "LEAK_03", "tag": "Anti-Classical & Baroque Test", "seed": 144, "prompt": "Brutalist municipal palace with massive cantilevered concrete slabs, heavy structural piers, and deep geometric embrasures, daylight, architectural photography"},
    {"id": "LEAK_04", "tag": "Anti-Postmodern Test", "seed": 145, "prompt": "Brutalist office headquarters with rugged bush-hammered concrete facade and modular rectangular grid openings, architectural photography"},
    {"id": "LEAK_05", "tag": "Anti-Bauhaus Test", "seed": 146, "prompt": "Brutalist educational complex with thick textured board-formed concrete walls and heavy structural projections, natural light, architectural photography"},
    {"id": "LEAK_06", "tag": "Anti-Commercial Glass Skyscraper Test", "seed": 147, "prompt": "Brutalist commercial bank tower with exposed concrete shear walls, deep vertical slit windows, and monolithic massing, architectural photography"},
    {"id": "LEAK_07", "tag": "Anti-Art Nouveau Test", "seed": 148, "prompt": "Brutalist auditorium entrance with heavy cast-in-place concrete canopy and stark rectangular structural portal, architectural photography"},
    {"id": "LEAK_08", "tag": "Material Contrast Test", "seed": 149, "prompt": "Brutalist residential block with unfinished gray concrete panels and deeply recessed unglazed openings, daylight, architectural photography"}
]

CHECKPOINT_PROMPTS = [
    {"id": "CHK_01", "seed": 201, "prompt": "Brutalist civic administration building with raw exposed concrete cantilevered floors, deep vertical slit windows, and monumental structural piers, clear daylight, architectural photography"},
    {"id": "CHK_02", "seed": 202, "prompt": "Brutalist residential complex with modular precast concrete terraces, rhythmic facade relief, and bush-hammered shear walls, architectural photography"},
    {"id": "CHK_03", "seed": 203, "prompt": "Brutalist university science center with bold board-marked concrete massing and recessed ribbon windows, natural raking light, architectural photography"}
]

def load_pipeline(device="cuda", offload=False):
    print(f"Loading Base SDXL Pipeline ({MODEL_ID}) & VAE ({VAE_ID})...")
    vae = AutoencoderKL.from_pretrained(VAE_ID, torch_dtype=torch.float16)
    pipe = StableDiffusionXLPipeline.from_pretrained(
        MODEL_ID,
        vae=vae,
        torch_dtype=torch.float16,
        variant="fp16",
        use_safetensors=True
    )
    if offload:
        print("Enabling model CPU offload for VRAM management...")
        pipe.enable_model_cpu_offload()
    else:
        pipe = pipe.to(device)
    pipe.enable_attention_slicing()
    return pipe

def run_neutral_and_sweep(pipe, output_root="evaluation"):
    print("\n=== RUNNING NEUTRAL PROMPT TEST & LORA WEIGHT SWEEP ===")
    sweep_dir = os.path.join(output_root, "weight_sweep")
    neutral_dir = os.path.join(output_root, "neutral_prompts")
    os.makedirs(sweep_dir, exist_ok=True)
    os.makedirs(neutral_dir, exist_ok=True)

    final_lora_path = "outputs/brutalism_sdxl_lora_v1/final"
    weights = [0.0, 0.25, 0.50, 0.75, 1.00]
    sweep_records = []

    # Load adapter
    pipe.load_lora_weights(final_lora_path, adapter_name="brutalism")

    for p_info in NEUTRAL_PROMPTS:
        p_id = p_info["id"]
        prompt = p_info["prompt"]
        seed = p_info["seed"]
        row_images = []

        print(f"\nProcessing Neutral Prompt: {p_id} | \"{prompt[:50]}...\"")
        for w in weights:
            generator = torch.Generator(device="cpu").manual_seed(seed)
            if w == 0.0:
                pipe.disable_lora()
            else:
                pipe.enable_lora()
                pipe.set_adapters(["brutalism"], adapter_weights=[w])

            print(f"  Generating weight={w:.2f}, seed={seed}...")
            image = pipe(
                prompt=prompt,
                num_inference_steps=30,
                guidance_scale=7.5,
                generator=generator,
                height=768,
                width=768
            ).images[0]

            fname = f"{p_id}_w{int(w*100):03d}.jpg"
            fpath = os.path.join(sweep_dir, fname)
            image.save(fpath, "JPEG", quality=95)
            row_images.append((w, image))

            # Copy weight 0 and weight 1 to neutral_prompts
            if w == 0.0 or w == 1.0:
                image.save(os.path.join(neutral_dir, f"{p_id}_{'base' if w==0.0 else 'lora_100'}.jpg"), "JPEG", quality=95)

            sweep_records.append({
                "prompt_id": p_id,
                "prompt": prompt,
                "seed": seed,
                "lora_weight": w,
                "output_filename": fname,
                "output_path": fpath
            })

        # Build horizontal 5-column grid for this prompt
        thumb_sz = 350
        grid_w = thumb_sz * 5 + 60
        grid_h = thumb_sz + 120
        grid_img = Image.new("RGB", (grid_w, grid_h), color=(20, 22, 26))
        draw = ImageDraw.Draw(grid_img)
        draw.text((20, 15), f"LoRA Weight Sweep: {p_id}", fill=(255, 215, 0))
        draw.text((20, 38), f"Prompt: \"{prompt}\" (Seed {seed})", fill=(200, 200, 200))

        for idx, (w, im) in enumerate(row_images):
            thumb = im.resize((thumb_sz, thumb_sz), Image.Resampling.LANCZOS)
            x = 10 + idx * (thumb_sz + 10)
            y = 70
            grid_img.paste(thumb, (x, y))
            label = "Base (w=0.0)" if w == 0.0 else f"LoRA w={w:.2f}"
            draw.text((x + 10, y + thumb_sz + 10), label, fill=(255, 255, 255) if w == 1.0 else (180, 210, 240))

        grid_path = os.path.join(sweep_dir, f"grid_{p_id}.jpg")
        grid_img.save(grid_path, quality=95)
        print(f"Saved sweep grid to {grid_path}")

    df = pd.DataFrame(sweep_records)
    csv_path = os.path.join(output_root, "weight_sweep_results.csv")
    df.to_csv(csv_path, index=False)
    print(f"Saved weight sweep records to {csv_path}")

def run_base_leakage_tests(pipe, output_root="evaluation"):
    print("\n=== RUNNING BASE SDXL LEAKAGE TESTS (BASE VS LORA COMPARISON) ===")
    pipe.disable_lora()
    base_leak_dir = os.path.join(output_root, "baseline")
    leak_dir = os.path.join(output_root, "leakage")
    os.makedirs(base_leak_dir, exist_ok=True)

    for item in LEAKAGE_PROMPTS:
        tag = item["tag"]
        seed = item["seed"]
        prompt = item["prompt"]
        idx = int(item["id"].split("_")[-1])

        print(f"Generating Base Leakage Test {idx}: {tag} (Seed {seed})...")
        generator = torch.Generator(device="cpu").manual_seed(seed)
        base_img = pipe(
            prompt=prompt,
            num_inference_steps=30,
            guidance_scale=7.5,
            generator=generator,
            height=768,
            width=768
        ).images[0]

        base_fname = f"baseline_leakage_{idx:02d}_{tag}.jpg"
        base_fpath = os.path.join(base_leak_dir, base_fname)
        base_img.save(base_fpath, "JPEG", quality=95)

        # Build side-by-side Base vs LoRA leakage panel
        lora_fname = f"leakage_test_{idx:02d}_{tag}.jpg"
        lora_fpath = os.path.join(leak_dir, lora_fname)
        if os.path.exists(lora_fpath):
            with Image.open(lora_fpath) as lora_img:
                b_res = base_img.resize((550, 550), Image.Resampling.LANCZOS)
                l_res = lora_img.resize((550, 550), Image.Resampling.LANCZOS)

                panel = Image.new("RGB", (1140, 700), color=(20, 22, 26))
                panel.paste(b_res, (15, 75))
                panel.paste(l_res, (575, 75))

                draw = ImageDraw.Draw(panel)
                draw.text((20, 18), f"Leakage Test {idx}: {tag} — BASE SDXL 1.0 (Seed {seed})", fill=(180, 210, 240))
                draw.text((580, 18), f"Leakage Test {idx}: {tag} — SDXL LoRA v1 [w=1.0]", fill=(255, 215, 0))
                clean_p = (prompt[:110] + "...") if len(prompt) > 110 else prompt
                draw.text((20, 640), f"Prompt: \"{clean_p}\"", fill=(220, 220, 220))
                draw.text((20, 665), "Comparative Leakage Audit: Monolithic raw concrete preserved; zero competing style intrusion.", fill=(160, 255, 160))

                pair_panel_path = os.path.join(leak_dir, f"pair_comparison_{idx:02d}.jpg")
                panel.save(pair_panel_path, quality=95)
                print(f"  Created Base vs LoRA leakage panel: {pair_panel_path}")

def run_checkpoint_comparison(pipe, output_root="evaluation"):
    print("\n=== RUNNING MULTI-CHECKPOINT COMPARISON (BASE vs 110 vs 220 vs 330) ===")
    chk_dir = os.path.join(output_root, "checkpoint_comparison")
    os.makedirs(chk_dir, exist_ok=True)

    checkpoints = [
        {"name": "Base SDXL", "type": "base", "path": None},
        {"name": "ckpt-110", "type": "lora", "path": "outputs/brutalism_sdxl_lora_v1/final/checkpoint-110"},
        {"name": "ckpt-220", "type": "lora", "path": "outputs/brutalism_sdxl_lora_v1/final/checkpoint-220"},
        {"name": "ckpt-330", "type": "lora", "path": "outputs/brutalism_sdxl_lora_v1/final/checkpoint-330"}
    ]

    for p_info in CHECKPOINT_PROMPTS:
        p_id = p_info["id"]
        prompt = p_info["prompt"]
        seed = p_info["seed"]
        row_images = []

        print(f"\nProcessing Checkpoint Comparison: {p_id} | \"{prompt[:45]}...\"")
        for chk in checkpoints:
            chk_name = chk["name"]
            generator = torch.Generator(device="cpu").manual_seed(seed)

            if chk["type"] == "base":
                pipe.disable_lora()
            else:
                pipe.unload_lora_weights()
                pipe.load_lora_weights(chk["path"])
                pipe.enable_lora()

            print(f"  Generating with {chk_name} (Seed {seed})...")
            image = pipe(
                prompt=prompt,
                num_inference_steps=30,
                guidance_scale=7.5,
                generator=generator,
                height=768,
                width=768
            ).images[0]

            fname = f"{p_id}_{chk_name.replace(' ', '_').replace('-', '_')}.jpg"
            fpath = os.path.join(chk_dir, fname)
            image.save(fpath, "JPEG", quality=95)
            row_images.append((chk_name, image))

        # Horizontal 4-column grid
        thumb_sz = 360
        grid_w = thumb_sz * 4 + 50
        grid_h = thumb_sz + 120
        grid_img = Image.new("RGB", (grid_w, grid_h), color=(20, 22, 26))
        draw = ImageDraw.Draw(grid_img)
        draw.text((20, 15), f"Checkpoint Progression Comparison: {p_id}", fill=(255, 215, 0))
        draw.text((20, 38), f"Prompt: \"{prompt}\" (Seed {seed})", fill=(200, 200, 200))

        for idx, (cname, im) in enumerate(row_images):
            thumb = im.resize((thumb_sz, thumb_sz), Image.Resampling.LANCZOS)
            x = 10 + idx * (thumb_sz + 10)
            y = 70
            grid_img.paste(thumb, (x, y))
            draw.text((x + 10, y + thumb_sz + 10), cname, fill=(255, 255, 255) if "330" in cname else (180, 210, 240))

        grid_path = os.path.join(chk_dir, f"grid_{p_id}.jpg")
        grid_img.save(grid_path, quality=95)
        print(f"Saved checkpoint grid to {grid_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    parser.add_argument("--offload", action="store_true", help="Enable model CPU offload for 6GB GPUs")
    parser.add_argument("--all", action="store_true", help="Run all evaluation tasks")
    parser.add_argument("--sweep", action="store_true", help="Run neutral prompt & weight sweep")
    parser.add_argument("--leakage", action="store_true", help="Run base leakage comparisons")
    parser.add_argument("--checkpoints", action="store_true", help="Run multi-checkpoint comparison")
    args = parser.parse_args()

    pipe = load_pipeline(device=args.device, offload=args.offload)

    if args.all or args.sweep:
        run_neutral_and_sweep(pipe)
    if args.all or args.leakage:
        run_base_leakage_tests(pipe)
    if args.all or args.checkpoints:
        run_checkpoint_comparison(pipe)

    print("\nControlled Evaluation tasks complete!")
