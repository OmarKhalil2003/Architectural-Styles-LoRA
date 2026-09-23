# ARC_0012 Discrepancy Resolution & Audit Report

## 1. Executive Summary
During the initial memorization and feature-similarity inspection of the Brutalism SDXL LoRA pilot (`brutalism_sdxl_lora_v1`), the analysis reported:
- `lora_eval_04.jpg` $\rightarrow$ `ARC_0012` (Cosine Similarity: 0.7908)
- `lora_eval_05.jpg` $\rightarrow$ `ARC_0012` (Cosine Similarity: 0.7804)

This prompted a critical integrity check because an earlier project audit noted that `ARC_0012` was removed for being a close-up decorative Kufic foundation plaque without sufficient architectural/spatial context. 

This document definitively clarifies the **provenance and numbering collision** between the legacy Architectural-Styles dataset and the active 4-style architectural dataset.

---

## 2. Legacy vs. Active Dataset Comparison

| Dimension | Legacy Architectural-Styles Dataset (Archived) | Active Pilot Dataset (`data/clean/images/brutalism/`) |
| :--- | :--- | :--- |
| **Dataset Scope** | Historical Historical Architecture | 4-Style Modern Architectural Styles (Curated) |
| **Primary Source** | Archnet / Aga Khan Documentation | Wikimedia Commons / Architectural Styles Dataset |
| **Subject of `ARC_0012`** | Detail of Kufic foundation inscription band, Mosque of Ibn Tulun, Cairo | Residential apartment block: *20241013 171550375 Milutina Milankovića*, Belgrade |
| **Image Type** | Close-up decorative plaque / bas-relief | Exterior architectural photograph showing massing |
| **Resolution** | Sub-standard / cropped archival plate | $1024 \times 1360$ px, 24-bit RGB JPEG |
| **Audit Status** | **REMOVED** during preliminary spatial audit | **RETAINED** as high-quality Brutalist exemplar |
| **Dataset Split** | Excluded | **Train** (`ARC_0012`, index 11 in 22-image split) |
| **License** | Institutional Educational Use | **CC BY 4.0** (Attribution 4.0 International) |
| **URL / Source** | `https://www.archnet.org/sites/1522` | [Wikimedia Commons File:20241013 171550375 Milutina Milankovića.jpg](https://upload.wikimedia.org/wikipedia/commons/a/aa/20241013_171550375_Milutina_Milankovi%C4%87a.jpg) |

---

## 3. Why the Discrepancy Occurred
1. **Re-indexing on Dataset Pivot**: When the project pivoted from the single-source Islamic dataset to the balanced 112-image modern architectural dataset (28 Brutalism, 28 Bauhaus, 28 International Style, 28 Postmodern), the image naming scheme was reset to sequential `ARC_0001` through `ARC_0028` within each style subfolder.
2. **Identifier Reuse**: The identifier `ARC_0012` was reassigned to the 12th curated Brutalism image (`20241013 171550375 Milutina Milankovića.jpg`).
3. **No Database Corruption**: The training scripts, Colab notebook, and memorization scripts operated exclusively on `data/clean/images/brutalism/ARC_0012.jpg`. The old Islamic plaque image does not exist anywhere in `data/clean/`.

---

## 4. Verification in the 22-Image Training Set
- `ARC_0012.jpg` exists on disk at `data/clean/images/brutalism/ARC_0012.jpg` ($1024 \times 1360$, RGB).
- Metadata row in `data/clean/metadata/train.csv`:
  - `image_id`: `ARC_0012`
  - `style`: `Brutalism architecture`
  - `building_name`: `20241013 171550375 Milutina Milankovića`
  - `architectural_elements`: `cantilevered canopy;brise-soleil louvers;modular grid`
  - `materials`: `concrete;aluminum`
  - `split`: `train`
- `lora_eval_04.jpg` was generated with the prompt:
  > *"Brutalist residential apartment building with modular precast concrete balconies and rhythmic geometric facade articulation, urban street view, architectural photography"*
- The high feature-space similarity (0.7908) between `lora_eval_04.jpg` and `ARC_0012` is technically logical: both depict modular residential concrete facades with rectangular window articulation.

## 5. Conclusion
There is **no dataset inconsistency, leak, or phantom file**. The model was trained on genuine Brutalist architecture, and `ARC_0012` is a verified, high-resolution training specimen.
