# Architectural AI Case Study: Curating, Fine-Tuning & Auditing a Diffusion LoRA for Brutalist Architecture

**Project Type**: Self-Directed Generative-AI / Architectural Machine Learning Research  
**Focus Area**: Dataset Curation, Style Conditioning, Diffusion Fine-Tuning & Empirical Model Auditing  
**Diffusion Backbone**: Stable Diffusion XL Base 1.0 (Alternative Diffusion Backbone)  
**Deliverables**: Audited Dataset (28 Images), UNet LoRA Adapter, Multi-Stage Evaluation Package  

---

## 1. Project Background & Objective
Modern text-to-image foundation models frequently fail to represent nuanced architectural movements with tectonic authenticity. When prompted for *"Brutalist architecture"*, base models often default to generic gray concrete boxes, slick commercial glass, or inaccurate historical pastiche.

This self-directed project investigates whether a **parameter-efficient low-rank adapter (LoRA)** fine-tuned on a small, highly curated architectural dataset can reliably steer an open diffusion model (**SDXL 1.0**) to generate authentic Brutalist architectural tectonics—characterized by monolithic raw concrete (*béton brut*), timber board formwork impressions, heavy cantilevers, and deep-set window embrasures—while rigorously probing for style leakage, spatial memorization, and conditioning limitations.

```text
Curate & Audit 28 Images
  (Provenance, Site-Disjoint Splits, Verified Licenses)
                   │
                   ▼
SDXL LoRA Fine-Tuning (Rank 16, Alpha 16, 330 Steps)
                   │
                   ▼
Controlled Baseline Evaluation (Identical Seeds 42–47)
                   │
                   ▼
Style Leakage & Feature-Space Similarity Audits (ResNet-34)
                   │
                   ▼
Caption Bottleneck Discovery & Run 2A Controlled Protocol
```

---

## 2. Dataset Engineering & Provenance Auditing
Fine-tuning on small datasets requires rigorous data curation:

1. **Source Curation**: Sourced 112 modern architectural photographs across four distinct movements (Brutalism, Bauhaus, International Style, Postmodernism) with verified open licenses (CC BY-SA 4.0 / CC BY 4.0 / CC0).
2. **Quality & Spatial Auditing**: Audited and excluded architectural blueprints, elevations, tourist-crowded scenes, and close-up decorative plaques lacking structural massing. Every retained image was verified in 24-bit sRGB with a shortest edge $\ge 1024$ px.
3. **Site-Disjoint Dataset Partitioning**:
   - **Train (22 images)**: 17 unique architectural sites.
   - **Validation (3 images)**: 3 unique architectural sites.
   - **Held-Out Test (3 images)**: 3 unique architectural sites.
   - **Zero Leakage**: Programmatically verified 0.0% building or site overlap across splits.
4. **Discrepancy Resolution (`ARC_0012`)**: Resolved an apparent contradiction from an earlier archival iteration, verifying that in the active dataset, `ARC_0012` is a legitimate Belgrade Brutalist residential block (*Milutina Milankovića*), not an excluded decorative Kufic plaque.

---

## 3. LoRA Fine-Tuning Architecture
- **Diffusion Backbone**: `stabilityai/stable-diffusion-xl-base-1.0` + `madebyollin/sdxl-vae-fp16-fix`
- **Adapter Configuration**: Low-Rank Adaptation (LoRA) applied to all UNet cross-attention and self-attention projections (`to_k`, `to_q`, `to_v`, `to_out.0`) with rank $r=16$ and alpha $\alpha=16$.
- **Training Constraints**: Both OpenCLIP text encoders remained frozen to preserve foundation language priors. Training was conducted at $768 \times 768$ px using AdamW ($1 \times 10^{-4}$) for 330 steps (55 epochs) with gradient accumulation (effective batch size 4) and FP16 mixed precision.
- **Checkpoints**: Preserved at step 110, 220, 330, and final.

---

## 4. Controlled Empirical Evaluation

### 4.1 Controlled Baseline vs. LoRA Comparison
Using identical prompts, seeds (42–47), CFG (7.5), and steps (30):
- **Material Fidelity**: While base SDXL produced flat, smooth concrete finishes, the LoRA consistently synthesized tactile board-marked timber impressions, formwork seams, and aggregate textures.
- **Tectonic Articulation**: The adapter introduced cantilevered upper volumes, structural piers, and deeply recessed embrasures, replacing unwanted contemporary curtain-wall glazing with solid parapets and ribbon strips.

### 4.2 Anti-Leakage Probing (8 Competing Movements)
The adapter was tested against 8 adversarial prompts designed to elicit intrusion from competing architectural styles (Gothic, Classical, Baroque, Postmodern, Bauhaus, Commercial Glass, Art Nouveau).
- **Result**: No obvious examples of the targeted competing motifs (such as pointed arches, classical pediments, pastel pastiche, or thin steel curtain walls) were observed in the inspected samples. The raw concrete tectonic expression dominated across all tests.

### 4.3 Feature-Space Similarity & Memorization Analysis
To evaluate whether the model was reproducing training images, 512-dimensional feature embeddings were extracted using an ImageNet-pretrained ResNet-34:
- **Intra-Dataset Baseline (Train vs. Train, excluding self-similarity)**: Real training images exhibited an intra-split similarity of **$0.7028 \pm 0.0668$** (Max: $0.8814$, Min: $0.5479$).
- **Generated vs. Train**: Mean cosine similarity was **$0.6786 \pm 0.0777$** (Max: $0.8581$, Min: $0.4402$).
- **Alignment with Held-Out Test**: Generated images aligned with the unseen held-out test distribution at **$0.6901 \pm 0.0742$**.
- **Inspection of Highest-Similarity Pairs**: Visual inspection of the highest-similarity pairs (e.g. `lora_eval_03` vs `ARC_0018` at $0.8581$) did not reveal obvious reproduction of distinctive building silhouettes, camera viewpoints, or fenestration patterns. The observed similarity appears primarily associated with shared material and architectural characteristics (board-formed concrete texture under direct sunlight). This does not constitute a definitive test for memorization.

### 4.4 Held-Out Generalization Context
The generated samples contain architectural characteristics also present in the held-out Brutalism images (such as waffle slab soffits and brise-soleil fins). Because the base SDXL model already possesses broad architectural knowledge and the held-out set is very small (3 images), this observation cannot isolate LoRA-specific generalization.

---

## 5. Critical Technical Finding: The Caption Bottleneck
A thorough audit of training metadata revealed that **all 22 training images were paired with an identical 27-word template caption**.
- **Diagnostic Finding**: The UNet LoRA learned a monolithic global style shift rather than fine-grained token-to-feature disentanglement (e.g. distinguishing waffle slabs from brise-soleil).
- **Controlled Follow-Up Proposal (Run 2A)**: Rather than simply increasing training steps or changing multiple variables simultaneously, a second run is warranted as a clean single-variable experiment. Run 2A will maintain the exact same 22 images, frozen text encoder, base SDXL, rank 16, learning rate, and step budget, modifying *only* the captions into 22 instance-specific, visually grounded 9-attribute descriptions to isolate caption quality $\rightarrow$ conditioning behavior.

---

## 6. Key Competencies Demonstrated
1. **Curatorial Rigor**: Site-disjoint dataset engineering, license tracking, and resolution auditing.
2. **Diffusion Fine-Tuning**: Practical mastery of SDXL LoRA parameter-efficient adaptation, VRAM optimization, and checkpoint preservation.
3. **Controlled Scientific Evaluation**: Deterministic seed-matched baseline comparisons, multi-style leakage probing, and quantitative feature-space similarity distributions.
4. **Technical Integrity**: Formulating empirical hypotheses, diagnosing conditioning bottlenecks, and withholding re-training until fully justified by data.
