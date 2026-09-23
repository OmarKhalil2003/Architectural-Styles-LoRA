# Model Card: Brutalism SDXL LoRA Adapter (v1 Pilot)

## 1. Model Overview
The **Brutalism SDXL LoRA Adapter (`brutalism_sdxl_lora_v1`)** is a low-rank parameter-efficient adapter fine-tuned on top of **Stable Diffusion XL Base 1.0** to generate authentic Brutalist architectural forms. Fine-tuned as part of a self-directed architectural AI experiment, the model injects raw concrete textures (*béton brut*), board-marked timber impressions, heavy cantilevered massing, and deep rectangular window embrasures.

- **Base Diffusion Model**: `stabilityai/stable-diffusion-xl-base-1.0`
- **VAE**: `madebyollin/sdxl-vae-fp16-fix` (FP16 numerical stability fix)
- **Adapter Architecture**: Low-Rank Adaptation (LoRA) on UNet cross-attention & self-attention projections
- **Framework**: Hugging Face Diffusers (`0.40.0`), PEFT (`0.20.0`), PyTorch (`2.11.0` / `2.6.0`)

---

## 2. Technical Hyperparameters

| Hyperparameter | Configuration Value | Technical Rationale |
| :--- | :--- | :--- |
| **LoRA Rank ($r$)** | 16 | Conservative rank to avoid spatial memorization on small 22-image dataset |
| **LoRA Alpha ($\alpha$)** | 16 | 1:1 rank-to-alpha ratio for linear parameter scaling |
| **Target Modules** | `to_k`, `to_q`, `to_v`, `to_out.0` | Injects style into all 4 attention projection layers across down/mid/up blocks |
| **Text Encoder Fine-Tuning** | **False (Frozen)** | Freezing both OpenCLIP text encoders prevents semantic catastrophic forgetting |
| **Training Resolution** | $768 \times 768$ px | Optimal balance between VRAM efficiency, training stability, and texture detail |
| **Batch Size / Accumulation** | $1 \times 4$ | Effective batch size of 4 with gradient accumulation |
| **Learning Rate** | $1 \times 10^{-4}$ ($0.0001$) | Standard UNet LoRA convergence rate |
| **LR Scheduler** | `constant_with_warmup` (30 steps) | Smooth initial gradient trajectory |
| **Total Steps / Epochs** | 330 steps / 55 epochs | 15–60 effective passes over 22 images |
| **Optimizer** | AdamW ($\beta_1=0.9, \beta_2=0.999, \epsilon=10^{-8}, \text{wd}=0.01$) | Standard decoupled weight decay |
| **Precision** | FP16 mixed precision | Half-precision parameter representation |
| **Gradient Checkpointing** | Enabled | Preserves VRAM headroom under 14 GB on Tesla T4 |

---

## 3. Training Checkpoints
Checkpoints were preserved every 110 steps:
- `checkpoint-110`: Initial style induction; subtle concrete texture shift.
- `checkpoint-220`: Balanced tectonic articulation; strong massing with high prompt flexibility.
- `checkpoint-330` / `final`: Full material saturation; prominent board-formed textures and deep cast shadows.

All checkpoints contain intact `pytorch_lora_weights.safetensors` (93,065,304 bytes).

---

## 4. Intended Use & Capabilities
- **Primary Use Case**: Conceptual architectural exploration, tectonic studies, facade texture synthesis, and stylistic conditioning studies.
- **Recommended Inference Settings**:
  - Sampler: Euler A / DPM++ 2M Karras
  - Steps: 30–40 steps
  - CFG Guidance Scale: 7.0–8.0
  - Resolution: $768 \times 768$ px or $1024 \times 1024$ px
  - Adapter Weight: $0.75$–$1.00$ for strong brutalist features; $0.50$ for subtle textural enhancement.

---

## 5. Limitations & Known Failure Modes

1. **Monolithic Style Conditioning (Caption Limitation)**:
   - Due to the use of identical training captions in Run 1, the model cannot reliably disentangle fine-grained structural components (e.g. asking for *"waffle slab soffit"* may still produce generic cantilevered balconies).
2. **Pedestrian Distortion**:
   - Background pedestrian figures rendered at distant scale may exhibit characteristic diffusion limb artifacts; architectural prompts should focus on building exteriors and facade tectonics.
3. **Overcast Bias**:
   - The training set contains many overcast or neutral daylight European architectural photographs, which occasionally induces a gray, desaturated atmosphere in sunny prompts.
4. **Not Client/Commercial Work**:
   - This model is a self-directed experimental research artifact and is not certified for structural engineering or construction documentation.
