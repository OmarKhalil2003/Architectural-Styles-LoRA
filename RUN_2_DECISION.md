# Architectural AI Experiment: Run 2 Decision Record & Experimental Design

**Project**: Brutalism SDXL LoRA Pilot  
**Role/Scope**: Self-Directed Architectural Generative-AI Research  
**Document**: Technical Decision Record (Run 1 Audit $\rightarrow$ Run 2A Proposal)  
**Status**: Recommendation Documented — Awaiting Explicit Approval Before Retraining  

---

## 1. Executive Summary & Recommendation

| Field | Evaluation / Assessment |
| :--- | :--- |
| **Current Pilot Status** | `brutalism_sdxl_lora_v1` successfully trained and audited across 20 phases. |
| **Model Health** | Stable, zero NaN loss spikes, strong raw concrete material fidelity, no severe mode collapse, no obvious competing style leakage. |
| **Primary Limitation** | **100% caption redundancy** (22 identical template captions) resulting in a monolithic global style shift without fine-grained architectural token disentanglement. |
| **Formal Decision** | **A second run (Run 2A) is warranted as a controlled follow-up experiment** to test whether instance-specific captions improve architectural attribute conditioning. |
| **Execution Constraint** | **Do NOT start Run 2A immediately.** Complete all baseline and evaluation documentation first. |

---

## 2. Empirical Evidence from Run 1 Audit

The recommendation to proceed to a second training run is grounded strictly in empirical findings from the Phase 1–13 audit:

1. **Dataset Integrity Verified (`[MEASURED]`)**:
   - Exactly 22 Brutalism training images (`ARC_0001`–`ARC_0022`), verified short edge $\ge 1024$ px, RGB format, clean licensing (CC BY 4.0 / CC BY-SA 4.0 / CC0).
   - Zero contamination from Bauhaus, International Style, or Postmodern sets.
   - Zero building overlap between train and test/validation splits.
2. **Material Style Induction Demonstrated (`[QUALITATIVE]`)**:
   - Controlled baseline comparisons (prompts 1–6, seeds 42–47) confirm that the LoRA successfully injects board-marked concrete impressions, deeper window reveals, and cantilevered silhouettes compared to base SDXL 1.0.
3. **Feature-Space Distribution (`[MEASURED]` + `[QUALITATIVE]`)**:
   - Mean feature-space similarity (ResNet-34) between generated samples and training images is $0.6786 \pm 0.0777$, compared to the natural off-diagonal intra-dataset baseline similarity of $0.7028 \pm 0.0668$.
   - Alignment with held-out test distribution is $0.6901 \pm 0.0742$.
   - Visual inspection of the highest-similarity pairs (e.g. `ARC_0018` at 0.8581) did not reveal obvious reproduction of distinctive building silhouettes, camera viewpoints, or fenestration patterns. The observed similarity appears primarily associated with shared material and architectural characteristics. This does not constitute a definitive test for memorization.
4. **Style Leakage Contained (`[QUALITATIVE]`)**:
   - No obvious examples of the targeted competing motifs (Gothic pointed arches, Classical pediments, Postmodern pastel cladding, Bauhaus steel/glass lightness, or commercial curtain walls) were observed in the 8 anti-leakage test samples.
5. **The Critical Bottleneck — Caption Redundancy (`[MEASURED]` & `[LIMITATION]`)**:
   - The caption audit revealed that all 22 training images received the exact same 27-word boilerplate caption.
   - Consequently, the UNet attention layers were trained with an invariant text embedding. Tokens like `"waffle slab"`, `"brise-soleil"`, and `"pilotis"` were never associated with their respective physical forms.

---

## 3. Problems Identified in Run 1

| Problem ID | Problem Description | Root Cause | Impact on Generation |
| :--- | :--- | :--- | :--- |
| **P-01** | **Monolithic Style Entanglement** | 22 identical boilerplate captions | The adapter treats all Brutalism tokens as a single uniform texture trigger rather than modular architectural elements. |
| **P-02** | **Inability to Condition on Building Typology** | Captions never specify building type (library, stadium, housing, clinic) | The model defaults to base SDXL's spatial prior when generating specific functional typologies. |
| **P-03** | **Checkpoints Not Evaluated During Training** | Training executed to step 330 without evaluating intermediate checkpoints | Step 330 was adopted by default; intermediate steps (e.g. step 220) may offer better prompt adherence with less texture saturation. |

---

## 4. Controlled Experimental Design for Run 2A

To maintain strict scientific validity, **Run 2A will change only one experimental variable at a time**. Combining caption rewriting, trigger tokens, and text encoder training simultaneously would confound the experiment, making it impossible to determine which factor caused any observed changes.

### The Single-Variable Hypothesis
> *Holding the base model, dataset images, LoRA rank, learning rate, and step budget constant, replacing identical boilerplate captions with instance-specific, visually grounded captions will improve attribute-level architectural conditioning without degrading style fidelity.*

### Run 2A Configuration Table

| Parameter | Run 1 (Pilot) | Run 2A (Proposed Controlled Follow-Up) | Experimental Control Status |
| :--- | :--- | :--- | :--- |
| **Training Images** | 22 Brutalism images | Same 22 Brutalism images (`ARC_0001`–`ARC_0022`) | **CONSTANT** |
| **Captions** | 1 identical 27-word template | **22 instance-specific, 9-attribute grounded captions** | **ISOLATED VARIABLE** |
| **Base Model** | SDXL Base 1.0 + FP16 VAE | SDXL Base 1.0 + FP16 VAE | **CONSTANT** |
| **LoRA Rank ($r$)** | 16 | 16 | **CONSTANT** |
| **LoRA Alpha ($\alpha$)**| 16 | 16 | **CONSTANT** |
| **Text Encoder** | Frozen (`train_text_encoder: false`) | Frozen (`train_text_encoder: false`) | **CONSTANT** |
| **Target Modules** | `to_k`, `to_q`, `to_v`, `to_out.0` | `to_k`, `to_q`, `to_v`, `to_out.0` | **CONSTANT** |
| **Resolution** | $768 \times 768$ px | $768 \times 768$ px | **CONSTANT** |
| **Learning Rate** | $1 \times 10^{-4}$ | $1 \times 10^{-4}$ | **CONSTANT** |
| **Scheduler** | `constant_with_warmup` (30 steps) | `constant_with_warmup` (30 steps) | **CONSTANT** |
| **Step Budget** | 330 steps (checkpointing @ 110, 220, 330) | 330 steps (checkpointing @ 110, 220, 330) | **CONSTANT** |
| **Trigger Token** | None (standard natural text) | None (standard natural text) | **CONSTANT** |

---

## 5. Grounded 9-Attribute Caption Framework for Run 2A

Each of the 22 images will be described along 9 visible architectural dimensions:
$$\text{Caption} = [\text{Typology}] + [\text{Primary Massing}] + [\text{Structural System}] + [\text{Specific Surface Finish}] + [\text{Fenestration/Embrasures}] + [\text{Circulation/Tectonics}] + [\text{Lighting/Atmosphere}] + [\text{Viewpoint}] + [\text{Style Anchor}]$$

### Example Grounded Captions for Run 2A

1. **`ARC_0012` (*Milutina Milankovića Residential Block, Belgrade*)**:
   > *"Brutalist residential apartment building, prefabricated modular concrete panel facade, repetitive geometric window grid with recessed loggias and integrated brise-soleil sun louvers, heavy street-level entrance canopy, weathered gray aggregate surface, low-angle eye-level street photography, overcast diffuse daylight"*
2. **`ARC_0008` (*Tribune Koning Boudewijnstadion, Belgium*)**:
   > *"Brutalist athletic stadium grandstand, cast-in-place raw concrete stepped seating tiers, massive diagonal structural rake beams, open-air canopy overhang without glazing, heavy concrete retaining walls, direct afternoon sunlight casting raking structural shadows, wide-angle architectural exterior view"*
3. **`ARC_0018` (*Former Library, Doetinchem*)**:
   > *"Brutalist municipal library building, deeply articulated board-formed raw concrete facade with prominent horizontal wood grain texture, dramatically cantilevered upper floor volume, narrow horizontal ribbon strip windows, solid corner stair tower, bright daylight, architectural photography"*

---

## 6. Expected Effects & Evaluation Criteria

### Success Criteria for Run 2A vs. Run 1
1. **Attribute Disentanglement**: Prompting for *"waffle slab soffit"* produces coffered ceiling grids without forcing residential balcony forms.
2. **Typology Adherence**: Prompting for *"civic library"* vs *"residential tower"* produces distinct functional silhouettes.
3. **Preserved Anti-Leakage**: Competing styles (Gothic, Classical, Bauhaus, etc.) remain absent.
4. **Generalization**: Feature similarity distribution relative to held-out test set remains healthy ($\approx 0.68$–$0.72$).

---

## 7. Formal Recommendation & Constraints

1. **Do not retrain today.**
2. Complete all Run 1 evaluation reports, comparison panels, and cards.
3. Prepare the revised `data/clean/metadata/train_run2.csv` containing the 22 grounded captions.
4. Launch Run 2A only when formally approved.
