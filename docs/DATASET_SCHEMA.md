# Architectural-Styles-LoRA Dataset Schema & Provenance Guide

This document establishes the schema definitions, provenance tracking rules, and curation/selection criteria for the Architectural-Styles-LoRA dataset, tracked in [`metadata/dataset_master.csv`](file:///d:/Architectural-Styles-LoRA/metadata/dataset_master.csv).

---

## 1. Schema Definition

The master table uses the following 21 columns in exact order:

```csv
image_id,source,source_id,source_url,license,creator,country,city,architectural_period,building_type,spatial_type,architectural_elements,materials,geometric_pattern,lighting,interior_exterior,quality_score,relevance_score,keep,removal_reason,caption
```

| Field Name | Type | Description & Format |
|---|---|---|
| `image_id` | string | Unique primary key formatted by source prefix (e.g. `MNA_0001`, `WKM_0001`, `TRH_0001`). |
| `source` | string | Origin repository: `manar`, `wikimedia`, or `turath`. |
| `source_id` | string | Unique identifier, accession number, or filename in the source repository. |
| `source_url` | string | Canonical web link to the source page or image record. |
| `license` | string | Usage license (e.g. `CC-BY-4.0`, `CC-BY-SA-4.0`, `Public Domain`, `Academic/Research Use`). |
| `creator` | string | Photographer, author, or archival collection attributed by the source. |
| `country` | string | ISO country name of the structure location (e.g., `Egypt`, `Morocco`, `Syria`). |
| `city` | string | City or locality (e.g., `Cairo`, `Fez`, `Damascus`, `Cordoba`). |
| `architectural_period` | string | Historical or stylistic epoch (e.g., `Mamluk`, `Fatimid`, `Umayyad`, `Ottoman`, `Andalusian`, `Contemporary`). |
| `building_type` | string | Typology of the building (e.g., `mosque`, `madrasa`, `palace`, `residential`, `caravanserai`, `pavilion`). |
| `spatial_type` | string | Specific architectural space or viewpoint (e.g., `courtyard`, `iwan`, `facade`, `entrance portal`, `hypostyle hall`, `loggia`). |
| `architectural_elements` | string | Semicolon-delimited key elements (e.g., `mashrabiya; horseshoe arch; muqarnas; crenellation`). |
| `materials` | string | Semicolon-delimited construction materials (e.g., `limestone; carved wood; glazed ceramic tile; marble; concrete`). |
| `geometric_pattern` | string | Geometric taxonomy (e.g., `8-pointed star rosette; interlaced strapwork; girih; geometric tracery; none`). |
| `lighting` | string | Character of light (e.g., `filtered daylight; dappled sun; direct sunlight; dramatic shadow; diffused ambient`). |
| `interior_exterior` | string | Space classification: `interior`, `exterior`, or `transitional`. |
| `quality_score` | integer | Photographic and visual fidelity score (1 to 5). |
| `relevance_score` | integer | Domain relevance to Modern and Classical architectural vocabulary (1 to 5). |
| `keep` | boolean | Final inclusion flag: `TRUE` or `FALSE`. |
| `removal_reason` | string | Mandatory rationale if `keep == FALSE` (e.g., `synthetic_or_render`, `low_resolution`, `people_occlusion`). |
| `caption` | string | Structured descriptive caption. *(Deferred: populated during captioning stage).* |

---

## 2. Provenance Standards

Every candidate image entered into [`metadata/dataset_master.csv`](file:///d:/Architectural-Styles-LoRA/metadata/dataset_master.csv) must carry full provenance before selection decisions:

### Source ID Conventions
- **Manar al-Athar (`manar`)**: Use the Manar photo accession number (e.g., `MNA_0001` mapping to source ID e.g., `WA_EGY_CAI_0123`).
- **Wikimedia Commons (`wikimedia`)**: Use the Wikimedia file title or page ID (e.g., `WKM_0001` mapping to `File:Al-Azhar_Mosque_Courtyard.jpg`).
- **Turath-150K (`turath`)**: Use the Turath dataset sample index or hash (e.g., `TRH_0001`).

### Target Dataset Distribution
Per [`docs/PROJECT_SPEC.md`](file:///d:/Architectural-Styles-LoRA/docs/PROJECT_SPEC.md):
- **Manar al-Athar**: ~60 curated images
- **Wikimedia Commons**: ~25 curated images
- **Turath-150K**: ~15 curated images
- **Total Kept**: ~100 curated images

---

## 3. Selection & Curation Rubrics

### 3.1 Quality Score (1–5)
- **5 (Master)**: High resolution ($\ge 1024\times 1024$ native), exceptional sharpness, balanced dynamic range, zero watermarks/artifacts.
- **4 (Good)**: Clean resolution ($\ge 768\times 768$), sharp subject focus, minimal noise or non-intrusive lens distortion.
- **3 (Borderline)**: Moderate resolution, slight softness or sensor noise, requires careful center crop.
- **2 (Sub-par)**: Heavy JPEG compression artifacts, motion blur, low native resolution ($< 768$ px).
- **1 (Unusable)**: Extreme blur, pixelation, or destructive watermarks.

### 3.2 Relevance Score (1–5)
- **5 (Core Domain)**: Prime exemplar of target visual vocabulary (mashrabiya screens, geometric courtyards, muqarnas transitions, Distinctive architectural spatial composition with filtered light).
- **4 (Strong Domain)**: Clear architectural feature (pointed/horseshoe arches, carved stone/stucco facades, traditional Islamic geometric patterns).
- **3 (Moderate Domain)**: Contextual Architectural styles, but lacking distinctive decorative or spatial articulation.
- **2 (Peripheral)**: Scene dominated by modern utilitarian elements, tourists, or peripheral clutter.
- **1 (Off Domain)**: Generic non-architectural scenes, unrelated styles, or non-Architectural/Islamic contexts.

### 3.3 Selection Decision Rules
- **Rule 1 (Real Photography Only)**: Any synthetic, 3D render, AI-generated image, or architectural drawing must be assigned `keep = FALSE` and `removal_reason = synthetic_or_render`.
- **Rule 2 (Acceptance Threshold)**: A record is marked `keep = TRUE` only if `quality_score >= 4` AND `relevance_score >= 4` AND no exclusion criteria are met.
- **Rule 3 (Rejection Reasons)**: If `keep = FALSE`, `removal_reason` must be chosen from the standardized taxonomy:
  - `synthetic_or_render`
  - `low_resolution`
  - `blurry_or_distorted`
  - `watermark_or_overlay`
  - `people_occlusion`
  - `off_domain`
  - `duplicate_view`
  - `license_incompatible`

---

## 4. Controlled Architectural Vocabulary

To ensure consistency across annotators and models, fields should adhere to these conventions:

- **`architectural_period`**: `Umayyad`, `Abbasid`, `Fatimid`, `Ayyubid`, `Mamluk`, `Andalusian`, `Ottoman`, `Traditional/Vernacular`, `Modern/Contemporary`.
- **`spatial_type`**: `courtyard`, `iwan`, `facade`, `entrance portal`, `hypostyle hall`, `arcade`, `minaret view`, `dome exterior`, `dome interior`, `loggia`.
- **`architectural_elements`**: Semicolon-separated list: `mashrabiya`, `horseshoe arch`, `pointed arch`, `multifoil arch`, `muqarnas`, `qamariya` (stained glass stucco window), `minaret`, `dome`, `crenellation`, `sahn` (courtyard fountain/basin), `carved stucco band`.
- **`materials`**: Semicolon-separated list: `limestone`, `sandstone`, `carved wood`, `marble`, `glazed ceramic tile`, `stucco`, `brick`, `concrete`, `wrought iron`, `glass`.
- **`geometric_pattern`**: `girih`, `8-pointed star rosette`, `10-pointed star rosette`, `12-pointed star rosette`, `interlaced strapwork`, `geometric lattice`, `geometric tracery`, `calligraphic frieze`, `none`.
- **`lighting`**: `filtered daylight`, `dappled sun through mashrabiya`, `direct sunlight`, `diffused ambient`, `deep shadow`, `golden hour exterior`.
- **`interior_exterior`**: `interior`, `exterior`, `transitional` (e.g. open courtyards, porticos, iwans).

---

## 5. Captioning Staging Notice

> [!IMPORTANT]
> The `caption` field is intentionally left blank during initial metadata collection.
> Captions will be systematically authored following provenance verification and curation filtering (`keep == TRUE`).
