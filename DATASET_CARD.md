# Dataset Card: Curated Architectural Styles Dataset (Brutalism Pilot Split)

## 1. Dataset Summary
The **Curated Architectural Styles Dataset (Brutalism Split)** is a specialized, audited computer vision dataset curated for fine-tuning text-to-image diffusion models (SDXL 1.0) on authentic Brutalist architectural visual vocabulary. The complete curated repository contains 112 images balanced across four major 20th-century architectural movements (Brutalism, Bauhaus, International Style, Postmodernism). 

This pilot focuses strictly on the **28 curated Brutalism images**, partitioned into site-disjoint splits: **22 training, 3 validation, and 3 test** exemplars.

---

## 2. Dataset Curation & Provenance

### Primary Sources
- **Source Repository**: `axel-riben/arcdataset-brutalism-extension` (curated from Wikimedia Commons and architectural photographic archives).
- **Licensing**: All 28 images carry verified open licenses permitting AI research, derivative works, and redistribution:
  - **CC BY-SA 4.0 / CC BY-SA 3.0**: 19 images
  - **CC BY 4.0 / CC BY 2.0**: 6 images
  - **CC0 (Public Domain)**: 3 images (`ARC_0010`, `ARC_0020`, `ARC_0023`)

### Site-Disjoint Dataset Partitioning

| Split | Count | Unique Buildings / Sites | Shortest Edge | Purpose in Experiment |
| :--- | :--- | :--- | :--- | :--- |
| **Train** | 22 | 17 unique sites (5 multi-view Milutina Milankovića blocks) | $\ge 1024$ px | UNet LoRA parameter optimization |
| **Validation** | 3 | 3 unique sites (*Hotel Zlatibor*, *Ibn Tulun modern adjacent*, *Bordeaux hall*) | $\ge 1024$ px | In-training loss / sample monitoring |
| **Held-Out Test**| 3 | 3 unique sites (*Batten Arts*, *1180 S Beverly*, *720 Spadina*) | $\ge 1024$ px | Out-of-distribution architectural comparison |
| **Total** | **28** | **23 unique architectural sites** | $\ge 1024$ px | Zero train/val/test building leakage |

---

## 3. Image Integrity & Quality Audit
Every image was subjected to an automated programmatic verification:
1. **Dimensions**: All 28 images have short edge $\ge 1024$ px (exceeding the 768px minimum training threshold). Aspect ratios range from 0.75 (portrait) to 1.60 (landscape).
2. **Color Mode**: 100% 24-bit sRGB format (no CMYK, grayscale, or palette-indexed files).
3. **Artifact Elimination**:
   - Zero historical drawings, elevations, floor plans, or blueprints.
   - Zero extreme compression artifacts, watermarks, or intrusive tourist crowds.
   - Every photograph depicts the building massing with clear structural daylight articulation.

---

## 4. Discrepancy Clarification: The `ARC_0012` Resolution
In early project iterations, an Historical architectural dataset was scraped from Archnet, in which `ARC_0012` depicted a close-up Kufic foundation plaque from the Mosque of Ibn Tulun. That image was rejected during spatial auditing because it lacked structural/building massing context.

When the project pivoted to the 4-style 112-image modern architectural dataset, images were re-indexed sequentially starting from `ARC_0001`. In the active dataset:
- `ARC_0012.jpg` is an exterior photograph of *20241013 171550375 Milutina Milankovića*, a Brutalist residential block in Belgrade, Serbia ($1024 \times 1360$ px, CC BY 4.0).
- It is a legitimate, verified member of the 22-image training set.
- Detailed documentation: [`evaluation/ARC_0012_resolution.md`](file:///d:/Architectural-Styles-LoRA/evaluation/ARC_0012_resolution.md).

---

## 5. Caption Analysis & Critical Limitation

### Active Run 1 Caption
All 22 training images were paired with the identical 27-word template caption:
> *"Brutalist architecture, monolithic raw concrete facade with visible board-marked texture, massive geometric cantilevered volumes, deep-set rectangular window embrasures, bold structural piers, strong geometric shadow patterns, natural daylight, architectural photography"*

### Identified Limitations
1. **100% Redundancy**: The UNet LoRA learned an invariant global style shift rather than fine-grained token-to-feature alignments.
2. **Inaccurate Material Claims**: Exemplars with smooth precast panels (`ARC_0012`) or bush-hammered aggregate (`ARC_0010`) were erroneously labeled as "board-marked".
3. **Missing Typology Tokens**: Typologies (libraries, housing, stadium grandstands) were not conditioned.
4. **Run 2 Recommendation**: Replace with 22 instance-specific, 9-attribute visually grounded captions (documented in [`evaluation/caption_audit.md`](file:///d:/Architectural-Styles-LoRA/evaluation/caption_audit.md)).

---

## 6. Dataset Manifest
The complete machine-readable manifest is available at [`dataset_manifest.csv`](file:///d:/Architectural-Styles-LoRA/dataset_manifest.csv).
