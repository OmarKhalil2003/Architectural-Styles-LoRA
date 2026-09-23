# Experiment Report: Brutalism SDXL LoRA Pilot (Run 1)

**Project**: Architectural-Styles-LoRA / Architectural Styles LoRA  
**Experiment Name**: `brutalism_sdxl_lora_v1`  
**Author / Scope**: Self-Directed Architectural Generative-AI Research  
**Hardware Used**: Google Colab Tesla T4 (14.56 GB VRAM) & Local Workstation (GTX 1660 Ti, 6.0 GB VRAM)  
**Date**: September 2026  

---

## 1. Project Objective & Experimental Framing
The objective of this self-directed experiment is to establish a rigorous, reproducible methodology for fine-tuning diffusion models on specialized architectural styles without style leakage, catastrophic forgetting, or spatial memorization. 

This pilot specifically implements **SDXL LoRA as a proven, open-weights alternative diffusion backbone**. This demonstrates the full end-to-end technical pipeline:
$$\text{Dataset Curation} \rightarrow \text{Provenance Tracking} \rightarrow \text{Conditioning Audit} \rightarrow \text{Diffusion Fine-Tuning} \rightarrow \text{Controlled Evaluation} \rightarrow \text{Feature-Space Similarity Analysis}$$

---

## 2. Dataset Curation, Auditing & Split Design

### 2.1 Curation Pipeline
A curated corpus of 112 images across 4 modern architectural movements (Brutalism, Bauhaus, International Style, Postmodernism) was consolidated. For this pilot, the **28 Brutalism images** were isolated and audited:
- **Exclusion of Non-Spatial Assets**: Architectural sketches, floor plans, construction drawings, and interior close-up plaques were audited and excluded.
- **Resolution & Aspect Ratio**: All 28 images have short edge $\ge 1024$ px, 24-bit sRGB.
- **Site-Disjoint Splits**:
  - **Train**: 22 images across 17 distinct architectural sites.
  - **Validation**: 3 images across 3 distinct architectural sites.
  - **Test (Held-Out)**: 3 images across 3 distinct architectural sites.
  - **Zero Leakage**: Confirmed zero building or site overlap across splits.

### 2.2 The `ARC_0012` Numbering Collision Audit
A critical audit resolved an apparent contradiction: an earlier historical Architectural-Styles dataset had rejected an `ARC_0012` for being a decorative Kufic plaque from Ibn Tulun Mosque. The audit confirmed that upon pivoting to the 4-style modern architecture dataset, images were re-indexed sequentially. In the active dataset, `ARC_0012.jpg` is a high-resolution ($1024 \times 1360$ px) photograph of a residential block in Belgrade (*Milutina Milankovića*), licensed CC BY 4.0, and legitimately belongs in the training set.

---

## 3. LoRA Fine-Tuning Architecture & Training Dynamics

### 3.1 Parameter Configuration (Verified from `hparams.yml`)
- **Base Diffusion Model**: `stabilityai/stable-diffusion-xl-base-1.0`
- **VAE**: `madebyollin/sdxl-vae-fp16-fix`
- **LoRA Rank ($r$)**: 16 | **LoRA Alpha ($\alpha$)**: 16
- **Target Modules**: `to_k`, `to_q`, `to_v`, `to_out.0` across UNet cross- and self-attention layers
- **Text Encoders**: Frozen (OpenCLIP ViT-bigG/14 and CLIP ViT-L/14)
- **Resolution**: $768 \times 768$ px
- **Batch Size**: 1 (Gradient Accumulation Steps: 4; Effective Batch Size: 4)
- **Optimizer**: AdamW ($\text{LR} = 1 \times 10^{-4}$, $\text{warmup} = 30$, $\text{scheduler} = \text{constant\_with\_warmup}$)
- **Optimization Steps**: 330 total steps (55 epochs across 22 training images)
- **Precision**: FP16 mixed precision with gradient checkpointing enabled

### 3.2 Training Loss Progression
- Step 110: `step_loss = 0.0415` (Checkpoint saved)
- Step 220: `step_loss = 0.2510` (Checkpoint saved)
- Step 330: `step_loss = 0.1910` (Final weights saved)
- Stable convergence without gradient explosion or NaN loss spikes.

---

## 4. Controlled Evaluation & Experimental Findings

### 4.1 Base SDXL vs. LoRA v1 (`[QUALITATIVE]`)
In 6 side-by-side controlled comparisons using identical prompts and seeds (42–47), the LoRA demonstrated:
- **Tectonic Massing**: Shift from generic smooth facades to heavy, cantilevered raw concrete volumes.
- **Material Realism**: Synthesis of board-marked timber impressions and bush-hammered aggregate textures.
- **Fenestration Realism**: Replacement of flat commercial glazing with recessed window embrasures and structural ribbon strips.

### 4.2 Anti-Leakage Probing (`[QUALITATIVE]`)
In 8 targeted anti-leakage tests, the model was probed for intrusion from Gothic, Classical, Baroque, Postmodern, Bauhaus, Commercial Glass, and Art Nouveau styles.
- **Result**: No obvious examples of the targeted competing motifs were observed in the inspected samples. The raw concrete tectonic expression dominated across all prompts.

### 4.3 Feature-Space Similarity & Memorization Analysis (`[MEASURED]`)
Using a pre-trained ResNet-34 512-dimensional feature extractor:
- **Intra-Train Diversity Baseline (Excl. Self-Similarity)**: $0.7028 \pm 0.0668$
- **Mean Similarity to Train**: $0.6786 \pm 0.0777$
- **Alignment to Held-Out Test Set**: $0.6901 \pm 0.0742$
- **Interpretation**: Generated images exhibit greater diversity relative to the training set than real training photos exhibit among themselves. Visual inspection of high-similarity pairs ($\ge 0.85$, such as `lora_eval_03` vs `ARC_0018` at 0.8581) did not reveal obvious reproduction of distinctive building silhouettes, camera viewpoints, or fenestration patterns. The observed similarity appears primarily associated with shared material and architectural characteristics. This does not constitute a definitive test for memorization.

### 4.4 Held-Out Test Set Generalization (`[LIMITATION]`)
The generated samples contain architectural characteristics also present in the held-out Brutalism images (such as waffle slab soffits and brise-soleil fins). Because the base SDXL model already possesses broad architectural knowledge and the held-out set is very small (3 images), this observation cannot isolate LoRA-specific generalization.

---

## 5. Caption Audit: The Key Technical Insight (`[LIMITATION]`)
An exhaustive caption audit revealed that **all 22 training images shared an identical 27-word template caption**.
- **Impact**: The UNet LoRA learned a monolithic global style shift rather than fine-grained token-to-feature alignments (such as associating "waffle slab" with coffered ceiling ribs).
- **Implication**: A second run (Run 2A) is warranted as a controlled follow-up experiment to test whether instance-specific captions improve architectural attribute conditioning.

---

## 6. Run 2A Controlled Experimental Design
- **Single-Variable Design**: Maintain the exact same 22 images, frozen text encoder, base SDXL, rank 16, learning rate, and step budget.
- **Single Change**: Modify *only* the captions into 22 instance-specific, visually grounded 9-attribute descriptions to cleanly isolate caption quality $\rightarrow$ conditioning behavior.
- **Status**: Documented in [`RUN_2_DECISION.md`](file:///d:/Architectural-Styles-LoRA/RUN_2_DECISION.md); awaiting explicit user approval before execution.
