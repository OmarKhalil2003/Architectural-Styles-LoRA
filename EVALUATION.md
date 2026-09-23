# Controlled Evaluation Report: Brutalism SDXL LoRA Pilot (Run 1)

**Evaluation Protocol Version**: 1.1 (Audited, Corrected & Verified)  
**Experiment**: `brutalism_sdxl_lora_v1`  
**Base Model**: Stable Diffusion XL Base 1.0  
**Scope**: Self-Directed Architectural Generative-AI Research  

---

## 1. Evaluation Methodology & Evidence Standards

To avoid exaggerated claims, every observation in this report is strictly categorized according to one of four epistemological standards:

- `[MEASURED]`: Quantitatively computed via reproducible code (e.g. ResNet-34 cosine similarity, tensor dimensions, file hashes, caption token counts).
- `[QUALITATIVE]`: Derived from direct visual inspection using standardized architectural rubrics (e.g. fenestration depth, formwork texture, competing style motifs).
- `[INFERRED]`: Plausible mechanistic hypothesis based on diffusion mechanics or training dynamics (e.g. effect of frozen text encoders on token entanglement).
- `[LIMITATION]`: A documented failure mode, dataset gap, or boundary condition of the experiment.

---

## 2. Controlled Baseline vs. LoRA Evaluation (`[QUALITATIVE]`)

### Protocol
- **Prompts**: 6 identical architectural prompts spanning civic centers, art museums, lecture halls, residential housing, cultural centers, and public libraries.
- **Seeds**: Fixed seeds $42, 43, 44, 45, 46, 47$ for prompts 1 through 6.
- **Inference Parameters**: 30 steps, Euler A, Guidance Scale 7.5, Resolution $768 \times 768$ px.
- **Comparison Artifacts**: Generated side-by-side composite panels [`evaluation/baseline_vs_lora/comparison_eval_01.jpg`](file:///d:/Architectural-Styles-LoRA/evaluation/baseline_vs_lora/comparison_eval_01.jpg) to `06.jpg`.

### Delta Analysis Table

| Pair / Seed | Architectural Prompt Summary | Base SDXL 1.0 Behavior | SDXL LoRA v1 Behavior | Qualitative Verdict |
| :--- | :--- | :--- | :--- | :--- |
| **01 (Seed 42)** | Civic building with monumental cantilevered concrete massing | Smooth, generic concrete with polished contemporary finish; shallow reveals | Rough board-marked timber impressions; projected cantilevered upper volume | `[QUALITATIVE]` Style shift toward authentic *béton brut* massing. |
| **02 (Seed 43)** | Art museum with monolithic raw concrete walls & recessed entrance | Polished stone/concrete hybrid; modern commercial entrance glazing | Monolithic shear walls with vertical formwork striations; dark recessed entry slot | `[QUALITATIVE]` Enhanced tectonic presence and structural shadow articulation. |
| **03 (Seed 44)** | University lecture hall complex with tiered facades & piers | Tiered stepped massing with standard architectural render appearance | Board-marked horizontal grain; heavy load-bearing structural piers | `[QUALITATIVE]` Authentic university Brutalist language (e.g. Bath/Brunel). |
| **04 (Seed 45)** | Residential apartments with modular precast balconies | Generic contemporary domestic apartment block; standard metal balustrades | Precast concrete panel units with visible seams and solid concrete parapets | `[QUALITATIVE]` Distinct shift toward modular residential slab blocks. |
| **05 (Seed 46)** | Cultural center with cantilevers & brise-soleil sun louvers | Thin, decorative solar fins; smooth beige concrete facade | Heavy cast-in-place concrete canopies; thick brise-soleil louvers casting deep shadows | `[QUALITATIVE]` Pronounced brutalist solar-shading articulation. |
| **06 (Seed 47)** | Municipal library with waffle slab overhangs & ribbon windows | Projecting canopy lacks structural rib articulation; standard storefront glass | Exposed coffered waffle slab soffit; continuous horizontal ribbon windows recessed into concrete | `[QUALITATIVE]` Faithful rendering of classic civic library Brutalism. |

Full table and metrics available at [`evaluation/base_vs_lora_results.csv`](file:///d:/Architectural-Styles-LoRA/evaluation/base_vs_lora_results.csv).

---

## 3. Style Leakage Probing Analysis (`[QUALITATIVE]`)

The model was tested against 8 targeted anti-leakage prompts designed to elicit intrusion from competing architectural movements.

| Test ID / Seed | Tested Competing Architectural Movement | Probing Objective | Observed Output Motifs | Leakage Verdict |
| :--- | :--- | :--- | :--- | :--- |
| **LEAK_01 (142)** | N/A (Baseline Anchor) | Style fidelity anchor | Monolithic raw concrete massing, deep window reveals | **No obvious leakage observed (`[QUALITATIVE]`)** |
| **LEAK_02 (143)** | **Gothic** (Pointed arches, tracery, vaults) | Religious chapel | Angular roofline, planar concrete, triangular portal; no pointed arches observed | **No obvious Gothic leakage (`[QUALITATIVE]`)** |
| **LEAK_03 (144)** | **Classical & Baroque** (Pediments, columns) | Municipal palace | Cantilevered horizontal floor plates, rectangular piers; no pediments observed | **No obvious Classical leakage (`[QUALITATIVE]`)** |
| **LEAK_04 (145)** | **Postmodernism** (Pastels, irony, cutouts) | Office headquarters | Bush-hammered concrete, modular grid, neutral gray palette; no pastels observed | **No obvious Postmodern leakage (`[QUALITATIVE]`)** |
| **LEAK_05 (146)** | **Bauhaus** (Thin steel frames, white stucco) | Educational complex | Thick board-marked concrete, heavy projections; no light steel curtain walls observed | **No obvious Bauhaus leakage (`[QUALITATIVE]`)** |
| **LEAK_06 (147)** | **Commercial Glass Skyscraper** (Mirror walls) | Bank tower | Heavy concrete shear walls dominate; narrow slit windows; no reflective curtain wall observed | **No obvious Commercial Glass leakage (`[QUALITATIVE]`)** |
| **LEAK_07 (148)** | **Art Nouveau** (Whiplash curves, floral iron) | Auditorium entrance | Heavy rectangular cast canopy portal; no curvilinear or organic decoration observed | **No obvious Art Nouveau leakage (`[QUALITATIVE]`)** |
| **LEAK_08 (149)** | **Polished High-Tech Materials** (Slick panels) | Residential block | Unfinished gray concrete panels with form-tie marks; no polished stone observed | **No obvious Material contamination (`[QUALITATIVE]`)** |

*Methodological Note*: The absence of competing motifs across these 8 inspected samples is a qualitative observation, not proof of zero leakage across unobserved prompts (`[LIMITATION]`). Full details: [`evaluation/leakage_results.csv`](file:///d:/Architectural-Styles-LoRA/evaluation/leakage_results.csv) and [`evaluation/leakage/leakage_summary_grid.jpg`](file:///d:/Architectural-Styles-LoRA/evaluation/leakage/leakage_summary_grid.jpg).

---

## 4. Feature-Space Similarity & Memorization Analysis (`[MEASURED]`)

### Embedding Methodology
- Feature Extractor: ResNet-34 (`torchvision.models.resnet34`, pre-trained on ImageNet).
- Layer: 512-dimensional output of `AdaptiveAvgPool2d`.
- Metric: Normalized vector cosine similarity: $\cos(\mathbf{e}_{\text{gen}}, \mathbf{e}_{\text{train}})$.
- Trigger Threshold: $\ge 0.85$ triggers mandatory architectural side-by-side inspection.

### Corrected Quantitative Distribution Summary (`[MEASURED]`)

| Distribution Comparison | Mean Cosine Sim | Std Dev | Max Sim | Min Sim | Interpretation |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Train vs. Train (Excluding Diagonal Self-Similarity)** | **0.7028** | 0.0668 | 0.8814 | 0.5479 | Natural domain clustering of real Brutalist photos due to concrete & lighting. |
| **Generated (12) vs. Train (22)** | **0.6786** | 0.0777 | **0.8581** | 0.4402 | Generated images are slightly more diverse relative to train than real photos are among themselves. |
| **Generated (12) vs. Held-Out Test (3)** | **0.6901** | 0.0742 | 0.8301 | 0.4661 | Generated samples align with the unseen held-out test distribution as strongly as with train. |
| **Train (22) vs. Held-Out Test (3)** | **0.7212** | 0.0624 | 0.8819 | 0.5780 | Demonstrates held-out test set is representative of the training domain. |

### Visual Inspection of High-Similarity Pairs (`[MEASURED]` + `[QUALITATIVE]`)
All pairs with similarity $\ge 0.75$ were compiled into neutral side-by-side inspection panels in [`evaluation/memorization/`](file:///d:/Architectural-Styles-LoRA/evaluation/memorization/) labeled for manual review:

1. **`lora_eval_03` vs. `ARC_0018` ($\text{Sim} = 0.8581$ — Trigger)**:
   - *Training Image (`ARC_0018`)*: Former municipal library in Doetinchem, showing horizontal board-formed concrete and cantilevered floor slab.
   - *Generated Image (`lora_eval_03`)*: Tiered university lecture hall with concrete colonnade.
   - *Inspection Verdict*: Visual inspection of the pair did not reveal obvious reproduction of distinctive building silhouettes, camera viewpoints, or fenestration patterns. The observed similarity appears primarily associated with shared material and architectural characteristics (horizontal board-formed concrete texture under direct sunlight). This does not constitute a definitive test for memorization.
2. **`lora_eval_06` vs. `ARC_0018` ($\text{Sim} = 0.8541$ — Trigger)**:
   - *Generated Image (`lora_eval_06`)*: Municipal library with waffle slab overhang.
   - *Inspection Verdict*: Shares civic institutional atmosphere and timber formwork grain; silhouette and window band geometries are distinct.
3. **`lora_eval_04` vs. `ARC_0012` ($\text{Sim} = 0.7908$) & `lora_eval_05` vs. `ARC_0012` ($\text{Sim} = 0.7804$)**:
   - *Training Image (`ARC_0012`)*: *Milutina Milankovića* residential block, Belgrade.
   - *Generated Images*: Modular residential balconies.
   - *Inspection Verdict*: Similarity driven by modular precast facade rhythm and gray aggregate tones; different floor counts, balcony profiles, and street perspective.

Full results saved in [`evaluation/memorization_results.csv`](file:///d:/Architectural-Styles-LoRA/evaluation/memorization_results.csv).

---

## 5. Held-Out Test Set Generalization Analysis (`[LIMITATION]`)

- **Held-Out Test Specimens**:
  - `ARC_0026`: *Batten Arts and Letters building* (cantilevered canopy, brise-soleil louvers, modular grid).
  - `ARC_0027`: *1180 S Beverly Drive Los Angeles* (bush-hammered concrete, angular geometry).
  - `ARC_0028`: *720 Spadina Avenue* (waffle slab soffit, concrete colonnade).
- **Split Disjointness (`[MEASURED]`)**: Zero site overlap between train (17 sites), val (3 sites), and test (3 sites).
- **Generalization Assessment (`[LIMITATION]`)**:
  - The generated samples contain architectural characteristics also present in the held-out Brutalism images (such as waffle slab soffits and brise-soleil fins). Because the base SDXL model already possesses broad architectural knowledge and the held-out set is very small (3 images), this observation cannot isolate LoRA-specific generalization.

---

## 6. Checkpoint Progression & Weight Sweep Protocols (`[INFERRED]`)

- **Checkpoints Preserved**: Steps 110, 220, 330, and final.
- **Evaluation Runner**: Created [`scripts/run_controlled_evaluation.py`](file:///d:/Architectural-Styles-LoRA/scripts/run_controlled_evaluation.py) and [`colab/brutalism_sdxl_lora_eval.ipynb`](file:///d:/Architectural-Styles-LoRA/colab/brutalism_sdxl_lora_eval.ipynb) to systematically sweep weights $[0.0, 0.25, 0.50, 0.75, 1.00]$ across 5 neutral prompts and compare checkpoints $110, 220, 330$.
- **Hypothesis**: Checkpoint-220 offers balanced prompt responsiveness with lower texture saturation than checkpoint-330 (`[INFERRED]`).
