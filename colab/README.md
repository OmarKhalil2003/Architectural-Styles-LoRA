# Google Colab Execution Guide: Brutalism SDXL LoRA Pilot

This guide explains step-by-step how to execute the **Brutalism Architecture SDXL LoRA** pilot experiment on Google Colab using the provided notebook: [`colab/brutalism_sdxl_lora.ipynb`](file:///d:/Architectural-Styles-LoRA/colab/brutalism_sdxl_lora.ipynb).

---

## 1. Where to Place the Project on Google Drive

1. Compress or upload the `Architectural-Styles-LoRA` folder to your personal **Google Drive** at the path:
   ```text
   My Drive/
   └── Architectural-Styles-LoRA/
       ├── colab/
       │   ├── brutalism_sdxl_lora.ipynb
       │   └── README.md
       ├── configs/
       │   └── brutalism_lora.yaml
       ├── data/
       │   └── clean/
       │       ├── images/
       │       │   └── brutalism/       (28 JPEGs: ARC_0001.jpg - ARC_0028.jpg)
       │       └── metadata/
       │           ├── train.csv        (22 Brutalism training records)
       │           ├── val.csv          (3 Brutalism validation records)
       │           └── test.csv         (3 Brutalism test records)
       ├── evaluation/
       │   ├── brutalism_prompts.txt    (12 Generalization prompts)
       │   ├── style_leakage_prompts.txt (8 Anti-leakage prompts)
       │   └── evaluation_protocol.md
       └── outputs/
   ```
2. The default path in the notebook is:
   ```python
   PROJECT_ROOT = "/content/drive/MyDrive/Architectural-Styles-LoRA"
   ```
   If your folder is in a different location, change only this single variable in **Cell 2**.

---

## 2. How to Open the Notebook & Enable GPU

1. Go to [Google Colab](https://colab.research.google.com/).
2. Select **File → Upload notebook** and upload `colab/brutalism_sdxl_lora.ipynb`.
3. Enable GPU acceleration:
   - Click **Runtime → Change runtime type**.
   - Under **Hardware accelerator**, select **T4 GPU** (standard free/pro tier), **L4 GPU** (preferred), or **A100 GPU**.
   - Click **Save**.
4. The notebook includes a hardware guardrail in **Cell 3** that checks your GPU VRAM:
   - Minimum required VRAM: **11.0 GB**.
   - Recommended: **NVIDIA T4 (16 GB)** or **L4 (24 GB)**.
   - If a CPU runtime is accidentally selected, execution will halt with a clear error prompt.

---

## 3. Step-by-Step Execution Sequence

Execute the cells sequentially from top to bottom:

| Step | Cell Title / Action | Description |
| :---: | :--- | :--- |
| **1** | **Mount Google Drive** | Prompts for Google Drive authorization to access `/content/drive/MyDrive/`. |
| **2** | **Configuration & Paths** | Sets up `PROJECT_ROOT`, hyperparameter constants, and output subdirectories. |
| **3** | **GPU Verification** | Verifies CUDA availability, GPU name, and VRAM capacity ($\ge 11$ GB). |
| **4** | **Install Dependencies** | Installs pinned versions of `diffusers`, `transformers`, `accelerate`, `peft`, `bitsandbytes`. |
| **5** | **Verify Dependencies** | Confirms package imports and versions. |
| **6** | **Dataset Verification** | Checks physical presence of all 28 Brutalism images (22 train, 3 val, 3 test) on Google Drive. |
| **7** | **Load Base Model** | Loads base `stabilityai/stable-diffusion-xl-base-1.0` and FP16-safe VAE `madebyollin/sdxl-vae-fp16-fix`. |
| **8** | **Generate Baseline Images** | Generates pre-LoRA benchmark images using `evaluation/brutalism_prompts.txt` and saves them to `outputs/brutalism_lora_v1/baseline/`. |
| **9** | **>>> START TRAINING HERE <<<** | **Launches LoRA Fine-Tuning** (see details below). |
| **10** | **Inspect Checkpoints** | Verifies saved `pytorch_lora_weights.safetensors` in `outputs/brutalism_lora_v1/final/`. |
| **11** | **Generate LoRA Images** | Loads the trained LoRA and generates post-training evaluation images with identical seeds. |
| **12** | **Style Leakage Tests** | Tests 8 anti-leakage prompts (Gothic, Classical, Postmodern, Bauhaus probes). |
| **13** | **Memorization Check** | Computes ResNet-34 cosine similarity against all 22 training images to detect replication vs. generalization. |
| **14** | **Package Results** | Creates a self-contained `.zip` archive on Google Drive for 1-click download. |

---

## 4. The Training Cell (`START TRAINING HERE`)

> [!IMPORTANT]
> The training cell is **Section 9**:
> ```text
> # >>> 9. START TRAINING HERE <<<
> ```
> This cell unloads the baseline pipeline from GPU memory to reclaim VRAM, downloads the official Diffusers SDXL LoRA trainer, formats `metadata.csv`, and launches:
> ```bash
> accelerate launch --mixed_precision="fp16" train_text_to_image_lora_sdxl.py ...
> ```
> - **Total Steps**: 330 steps (15 epochs $\times$ 22 images with gradient accumulation of 4).
> - **Expected Runtime**: **15 to 20 minutes** on Colab T4 (or ~8 minutes on L4 / A100).
> - **Dry Run Option**: To run a 2-minute test first, set `MAX_TRAIN_STEPS = 50` in Cell 2.

---

## 5. Where Results Are Saved & How to Download

All outputs are automatically saved directly to your Google Drive under:
```text
outputs/brutalism_sdxl_lora_v1/
├── baseline/              # Pre-training base SDXL images
├── lora/                  # Post-training SDXL + Brutalism LoRA images
├── leakage_tests/         # Anti-leakage probe generations
├── final/                 # Trained LoRA weights (pytorch_lora_weights.safetensors)
├── baseline_results.csv   # Prompts, seeds, and image mappings
├── evaluation_results.csv # LoRA prompt outputs
├── leakage_results.csv    # Style leakage test log
└── memorization_results.csv # ResNet similarity to training specimens
```

### How to Download the Trained LoRA Weights:
1. **Directly from Google Drive**: Navigate in your Google Drive UI to `Architectural-Styles-LoRA/outputs/brutalism_sdxl_lora_v1/final/` and download `pytorch_lora_weights.safetensors` (~45–90 MB).
2. **Via Packaged Archive**: Cell 14 automatically creates:
   ```text
   /content/drive/MyDrive/Architectural-Styles-LoRA/brutalism_sdxl_lora_v1_results.zip
   ```
   Download this single file to your local computer to inspect all images, weights, and evaluation CSVs.
