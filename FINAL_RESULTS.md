# Final Results Summary: Brutalism SDXL LoRA Pilot (Run 1)

**Experiment ID**: `brutalism_sdxl_lora_v1`  
**Base Model**: Stable Diffusion XL Base 1.0 (FP16 VAE fix)  
**Project Context**: Self-Directed Architectural Generative-AI Research  
**Scope**: SDXL LoRA Pilot — Alternative Diffusion Backbone  

---

## 1. Dataset (`[MEASURED]`)
- **Total Curated Images**: 28 Brutalism images (all verified RGB, shortest edge $\ge 1024$ px, verified open licenses: CC BY-SA 4.0 / CC BY 4.0 / CC0).
- **Split Distribution**:
  - **Train**: Exactly 22 images (`ARC_0001.jpg`–`ARC_0022.jpg`), representing 17 unique architectural sites.
  - **Validation**: 3 images (`ARC_0023.jpg`–`ARC_0025.jpg`), 3 unique sites.
  - **Test (Held-Out)**: 3 images (`ARC_0026.jpg`–`ARC_0028.jpg`), 3 unique sites.
- **Cross-Split Building Leakage**: **0.0% overlap (`[MEASURED]`)**. No building or site exists in more than one split.
- **Competing Style Contamination**: **0 images (`[MEASURED]`)**. Exactly 0 Bauhaus, 0 International Style, and 0 Postmodern images were included in the training set.
- **`ARC_0012` Resolution**: Verified as a legitimate Brutalist residential block in Belgrade (*Milutina Milankovića*, $1024 \times 1360$ px, CC BY 4.0). The legacy Ibn Tulun Kufic plaque exclusion belonged to an earlier archived project iteration.

---

## 2. Training Configuration (`[MEASURED]`)
- **Base Architecture**: `stabilityai/stable-diffusion-xl-base-1.0` + `madebyollin/sdxl-vae-fp16-fix`
- **Adapter Type**: LoRA on UNet attention projections (`to_k`, `to_q`, `to_v`, `to_out.0`)
- **Rank / Alpha**: Rank 16, Alpha 16 (1:1 ratio)
- **Resolution**: $768 \times 768$ px
- **Batch Size**: 1 (Gradient accumulation: 4; Effective batch size: 4)
- **Learning Rate**: $1 \times 10^{-4}$ with AdamW optimizer and `constant_with_warmup` (30 warmup steps)
- **Total Steps / Epochs**: 330 optimization steps (55 epochs across 22 images)
- **Text Encoders**: Frozen (`train_text_encoder: false`)
- **Precision**: FP16 mixed precision with gradient checkpointing enabled
- **Preserved Checkpoints**: `checkpoint-110`, `checkpoint-220`, `checkpoint-330`, `final` (all 93.06 MB safetensors intact)

---

## 3. Baseline vs. LoRA Results (`[QUALITATIVE]`)
In controlled comparisons across 6 evaluation prompts using identical seeds (42–47) and generation settings (30 steps, CFG 7.5, 768px):
- **Concrete Massing**: Base SDXL rendered smooth, flat, render-like concrete surfaces. LoRA v1 produced authentic *béton brut* with visible timber board markings, form-tie seams, and bush-hammered aggregate textures.
- **Tectonic Depth**: LoRA v1 significantly deepened window embrasures and created cantilevered upper volume projections.
- **Fenestration**: Replaced generic commercial curtain-wall glazing with recessed horizontal ribbon windows and solid precast parapets.
- **Comparison Panels**: Documented in [`evaluation/base_vs_lora_results.csv`](file:///d:/Architectural-Styles-LoRA/evaluation/base_vs_lora_results.csv) and composite panels [`evaluation/baseline_vs_lora/comparison_eval_01.jpg`](file:///d:/Architectural-Styles-LoRA/evaluation/baseline_vs_lora/comparison_eval_01.jpg) to `06.jpg`.

---

## 4. Neutral Prompt Protocol & Design (`[INFERRED]`)
- **Test Protocol**: 5 architectural prompts that omit the word *"Brutalism"* (e.g. *"A university library building surrounded by trees"*).
- **Hypothesis**: The adapter's learned tectonic weights will transfer raw concrete massing into non-brutalist institutional prompts.
- **Execution Status**: The test script ([`scripts/run_controlled_evaluation.py`](file:///d:/Architectural-Styles-LoRA/scripts/run_controlled_evaluation.py)) and notebook ([`colab/brutalism_sdxl_lora_eval.ipynb`](file:///d:/Architectural-Styles-LoRA/colab/brutalism_sdxl_lora_eval.ipynb)) have been created for execution in follow-up inference sessions.

---

## 5. LoRA Weight Sweep Protocol (`[INFERRED]`)
- **Sweep Range**: $w \in [0.0, 0.25, 0.50, 0.75, 1.00]$ across fixed seeds.
- **Hypothesized Dynamics**:
  - $w=0.00$: Pure base SDXL prior (contemporary polished architecture).
  - $w=0.25$: Subtle matte de-glazing on stone/concrete surfaces.
  - $w=0.50$: Visible formwork texture; balanced hybrid.
  - $w=0.75$: Strong tectonic articulation without prompt distortion.
  - $w=1.00$: Designed to produce the strongest observed style conditioning in tested samples.
- **Execution Status**: Configured within the automated evaluation suite for systematic evaluation.

---

## 6. Style Leakage Probing (`[QUALITATIVE]`)
Evaluated across 8 targeted anti-leakage prompts designed to elicit competing architectural vocabularies:
- **Gothic**: No obvious pointed arches, ribbed vaults, or ecclesiastical tracery observed in chapel samples.
- **Classical & Baroque**: No obvious triangular pediments, Corinthian capitals, or decorative volutes observed in civic palace samples.
- **Postmodern**: No obvious pastel hues, ironic historical pastiche, or decorative cutouts observed.
- **Bauhaus**: No obvious thin steel-framed glass corners or pristine white rationalist stucco observed.
- **Commercial Glass**: Solid-to-void ratio remained heavily weighted toward raw concrete shear walls.
- **Art Nouveau**: No obvious curvilinear whiplash or floral motifs observed.
- **Verdict**: *No obvious examples of the targeted competing architectural motifs were observed in the inspected samples (`[QUALITATIVE]`)*.

---

## 7. Memorization / Feature-Space Similarity (`[MEASURED]`)
Using 512-dimensional feature embeddings from an ImageNet-pretrained ResNet-34:
- **Intra-Dataset Baseline (Train vs. Train, excluding diagonal self-similarity)**: **$0.7028 \pm 0.0668$** (Max: $0.8814$, Min: $0.5479$).
- **Mean Similarity (Generated vs. Train)**: **$0.6786 \pm 0.0777$** (Max: $0.8581$, Min: $0.4402$).
- **Alignment with Held-Out Test (Generated vs. Test)**: **$0.6901 \pm 0.0742$**.
- **Inspection of Highest-Similarity Pairs ($\ge 0.85$)**:
  - `lora_eval_03` vs `ARC_0018` ($0.8581$) and `lora_eval_06` vs `ARC_0018` ($0.8541$) were subjected to side-by-side neutral inspection panels in [`evaluation/memorization/`](file:///d:/Architectural-Styles-LoRA/evaluation/memorization/).
  - **Verdict**: Visual inspection of the highest-similarity pairs did not reveal obvious reproduction of distinctive building silhouettes, camera viewpoints, or fenestration patterns. The observed similarity appears primarily associated with shared material and architectural characteristics (board-marked concrete under direct daylight). This does not constitute a definitive test for memorization.

---

## 8. Held-Out Evaluation (`[LIMITATION]`)
- Evaluated against 3 strictly held-out test buildings: `ARC_0026` (*Batten Arts*), `ARC_0027` (*1180 S Beverly*), and `ARC_0028` (*720 Spadina*).
- **Observation**: The generated samples contain architectural characteristics also present in the held-out Brutalism images (such as waffle slab soffits and brise-soleil fins). Because the base SDXL model already possesses broad architectural knowledge and the held-out set is very small (3 images), this observation cannot isolate LoRA-specific generalization.

---

## 9. Checkpoint Comparison Protocol (`[INFERRED]`)
- Checkpoints preserved at step 110, 220, 330, and final.
- Step 220 is hypothesized to offer high prompt responsiveness with lower texture saturation than step 330; comparative generation is formalized in [`colab/brutalism_sdxl_lora_eval.ipynb`](file:///d:/Architectural-Styles-LoRA/colab/brutalism_sdxl_lora_eval.ipynb).

---

## 10. Limitations (`[LIMITATION]`)
1. **Identical Caption Conditioning**: All 22 training images used the exact same 27-word template caption. The model learned a global style shift rather than fine-grained feature disentanglement.
2. **Pedestrian Distortion**: Distant human figures exhibit characteristic diffusion artifacts; architecture must remain the primary subject.
3. **Small Sample Size for Quant Metrics**: With 22 training and 3 test images, statistical metrics serve as qualitative indicators rather than asymptotic proofs.

---

## 11. Recommended Next Experiment (Run 2A) (`[DECISION]`)
- **Status**: Formally recommended; documented in [`RUN_2_DECISION.md`](file:///d:/Architectural-Styles-LoRA/RUN_2_DECISION.md).
- **Single-Variable Design**: Maintain the exact same 22 images, frozen text encoder, base SDXL, rank 16, learning rate, and step budget. Modify *only* the captions into 22 instance-specific, visually grounded 9-attribute descriptions to cleanly isolate caption quality $\rightarrow$ conditioning behavior.
- **Constraint**: Do not execute Run 2A until formally approved.
