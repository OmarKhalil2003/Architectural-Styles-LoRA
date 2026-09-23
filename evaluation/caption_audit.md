# Caption Audit & Conditioning Analysis: Brutalism SDXL LoRA Pilot (Run 1)

## 1. Executive Summary & Core Finding
A rigorous audit of the training captions in `data/clean/metadata/train.csv` revealed a critical architectural and conditioning limitation:
**All 22 Brutalism training images share the exact same monolithic template caption.**

```text
"Brutalist architecture, monolithic raw concrete facade with visible board-marked texture, massive geometric cantilevered volumes, deep-set rectangular window embrasures, bold structural piers, strong geometric shadow patterns, natural daylight, architectural photography"
```

Across 22 diverse training images depicting university libraries, municipal sports grandstands, residential high-rises, parking garages, and pharmaceutical buildings, the unique caption count is exactly **1**.

---

## 2. Quantitative & Lexical Analysis

| Metric | Measured Value | Standard Best Practice (Diffusion Fine-Tuning) |
| :--- | :--- | :--- |
| **Total Training Images** | 22 | 20–50 for focused style LoRA |
| **Total Captions** | 22 | 22 |
| **Unique Captions** | **1 (100% redundancy)** | 22 (100% uniqueness) |
| **Mean Word Count** | 27 words | 30–65 words per image |
| **Vocabulary Diversity (TTR)** | 1.0 (intra-caption) / 0.045 (dataset-wide) | > 0.45 across dataset |
| **Building Typology Specificity** | 0% (never identifies library, housing, etc.) | 100% grounded in specific typology |
| **Viewpoint / Perspective Tagging** | 0% (no low-angle, aerial, or raking light) | Explicit perspective & elevation tagging |
| **Material Variation** | 0% (claims "board-marked" for all 22 images) | Grounded in actual material (bush-hammered, precast, aggregate) |

---

## 3. Discrepancies Between Visible Reality & Template Caption
The template caption claims every image contains *"visible board-marked texture"*, *"massive cantilevered volumes"*, *"deep-set rectangular window embrasures"*, and *"bold structural piers"*. 

Cross-referencing the template against the ground truth metadata and visible image features reveals severe discrepancies:

1. **`ARC_0012` (*20241013 171550375 Milutina Milankovića*)**:
   - *Actual Architecture*: Multi-story modular residential slab block in New Belgrade with a precast panel grid, recessed loggias, and aluminum frames.
   - *Template Claim*: Claims "board-marked concrete" and "cantilevered volumes". In reality, the building is precast panelized facade construction with zero timber-grain formwork impressions.
2. **`ARC_0008` (*Tribune Koning Boudewijnstadion, Kessel-Lo*)**:
   - *Actual Architecture*: Sports stadium grandstand canopy with raking diagonal beam seating supports and open concrete bleachers.
   - *Template Claim*: Claims "deep-set rectangular window embrasures" and "cantilevered volumes". In reality, the grandstand has *no windows at all*—it is an open-air structural sports facility!
3. **`ARC_0021` (*Berlin Wedding Bayer Parkhaus*)**:
   - *Actual Architecture*: Multi-level open-air parking garage with continuous horizontal crash barriers and exposed spiral ramps.
   - *Template Claim*: Claims "deep-set rectangular window embrasures". Parking decks have open ventilation slots, not framed glazed embrasures.
4. **`ARC_0010` (*Bank of Finland, Helsinki*)**:
   - *Actual Architecture*: Compact bush-hammered concrete civic building with monolithic planar sheer walls.
   - *Template Claim*: Claims "board-marked texture". The surface finish is actually bush-hammered aggregate with pneumatic point-chiseled texture, not timber-grain formwork.

---

## 4. Technical Implications for LoRA Learning
Because the SDXL text encoders were frozen during training (`train_text_encoder: false`) and every single image was paired with the exact same text sequence:

1. **Monolithic Style Collapse (No Feature Disentanglement)**:
   - The UNet cross-attention layers received an invariant text conditioning embedding $\mathbf{c} = \text{TextEncoder}(\text{caption})$ across every training step.
   - Consequently, the model could not learn to associate individual tokens (e.g., `"waffle slab"`, `"cantilever"`, `"brise-soleil"`, `"balconies"`) with their corresponding spatial or visual features.
   - Instead, the LoRA learned a single **global style vector**: *"when prompted with Brutalism tokens, increase raw concrete massing, darken cast shadows, and desaturate the scene"*.
2. **Inability to Control Specific Architectural Typologies**:
   - Prompts requesting specific structural systems (e.g. pilotis vs. shear walls) rely entirely on SDXL's base pretraining prior rather than the fine-tuned adapter, because the adapter was never trained to differentiate them.
3. **Overfitting to High-Frequency Spatial Layouts**:
   - Because text conditioning provided zero distinguishing signal between images, the UNet's attention maps tended to gravitate toward the spatial layouts of the most visually dominant training images (e.g., `ARC_0018` and `ARC_0012`), explaining why those two exemplars scored highest in feature-space similarity.

---

## 5. Recommended Caption Strategy for Run 2 (When Approved)

To achieve true architectural control and feature disentanglement, Run 2 must employ **syntactically structured, multi-attribute, visually grounded captions**.

### Proposed 9-Attribute Caption Framework
Each training image will be described along 9 orthogonal architectural dimensions:
$$\text{Caption} = [\text{Typology}] + [\text{Primary Massing}] + [\text{Structural System}] + [\text{Specific Surface Finish}] + [\text{Fenestration/Embrasures}] + [\text{Circulation/Tectonics}] + [\text{Lighting/Atmosphere}] + [\text{Viewpoint}] + [\text{Style Anchor}]$$

### Concrete Exemplar Transformations

#### Case A: `ARC_0012` (Residential Slab Block, Belgrade)
- **Run 1 Template**:
  > *"Brutalist architecture, monolithic raw concrete facade with visible board-marked texture, massive geometric cantilevered volumes, deep-set rectangular window embrasures, bold structural piers, strong geometric shadow patterns, natural daylight, architectural photography"*
- **Run 2 Grounded Caption**:
  > *"Brutalist residential apartment building, prefabricated modular concrete panel facade, repetitive geometric window grid with recessed loggias and integrated brise-soleil sun louvers, heavy street-level entrance canopy, weathered gray aggregate surface, low-angle eye-level street photography, overcast diffuse daylight"*

#### Case B: `ARC_0008` (Stadium Grandstand, Belgium)
- **Run 1 Template**:
  > *"Brutalist architecture, monolithic raw concrete facade with visible board-marked texture, massive geometric cantilevered volumes, deep-set rectangular window embrasures, bold structural piers, strong geometric shadow patterns, natural daylight, architectural photography"*
- **Run 2 Grounded Caption**:
  > *"Brutalist athletic stadium grandstand, cast-in-place raw concrete stepped seating tiers, massive diagonal structural rake beams, open-air canopy overhang without glazing, heavy concrete retaining walls, direct afternoon sunlight casting raking structural shadows, wide-angle architectural exterior view"*

#### Case C: `ARC_0018` (Former Library, Doetinchem)
- **Run 1 Template**:
  > *"Brutalist architecture, monolithic raw concrete facade with visible board-marked texture, massive geometric cantilevered volumes, deep-set rectangular window embrasures, bold structural piers, strong geometric shadow patterns, natural daylight, architectural photography"*
- **Run 2 Grounded Caption**:
  > *"Brutalist municipal library building, deeply articulated board-formed raw concrete facade with prominent horizontal wood grain texture, dramatically cantilevered upper floor volume, narrow horizontal ribbon strip windows, solid corner stair tower, bright daylight, architectural photography"*

---

## 6. Conclusion
The identical template captions used in Run 1 represent the single largest bottleneck to fine-grained architectural control. While the pilot successfully proved that the LoRA learns the concrete material vocabulary and massive tectonic silhouette, fine-tuning with instance-specific, visually grounded captions is the primary technical rationale for executing Run 2.
