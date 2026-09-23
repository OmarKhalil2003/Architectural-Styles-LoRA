# Architectural-Styles-LoRA: Architectural Style Diffusion Fine-Tuning Pilot

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![PyTorch 2.1+](https://img.shields.io/badge/PyTorch-2.1+-ee4c2c.svg)](https://pytorch.org/)
[![Diffusers 0.30+](https://img.shields.io/badge/Diffusers-0.30+-yellow.svg)](https://github.com/huggingface/diffusers)
[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC_BY--SA_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)

> [!TIP]
> ### 📊 Executive Presentation Deck Available
> A complete, professionally formatted 11-slide presentation deck is provided in the repository root:  
> 🔗 **[`Architectural_Styles_LoRA_Presentation.pptx`](Architectural_Styles_LoRA_Presentation.pptx)**  
> 
> *Slide Deck Overview*:
> - **Slide 0**: Author (Omar Khalil), GitHub Repository Link, and Contact Info
> - **Slide 1**: The Problem — Tectonic Hallucination in Foundation Models
> - **Slide 2**: Dataset Architecture — 112-Image Multi-Style Corpus & 28-Image Brutalism Partitioning
> - **Slide 3**: Curatorial Auditing — Spatial Quality Filters & the ARC_0012 Discrepancy Resolution
> - **Slide 4**: Diffusion LoRA Training Configuration — SDXL 1.0, Rank 16, 768px, 330 Steps
> - **Slide 5**: Controlled Baseline Evaluation — Base SDXL 1.0 vs. SDXL LoRA v1 (Matched Seeds)
> - **Slide 6**: Anti-Leakage Probing — Qualitative Audit Across 8 Competing Movements
> - **Slide 7**: Feature-Space Similarity Analysis — ResNet-34 Embeddings & Generalization Bounds
> - **Slide 8**: Key Diagnostic Limitation — The 100% Identical Template Caption Bottleneck
> - **Slide 9**: Future Work & Enhancement — Run 2A Single-Variable Controlled Experiment Proposal
> - **Slide 10**: Repository Manual & Reproducibility Package

---

## 1. Project Overview & Scope
This is a **self-directed architectural machine learning project** investigating how parameter-efficient low-rank adapters (LoRA) steer open diffusion foundation models toward authentic architectural visual vocabularies. 

The pilot focuses on **Brutalist Architecture**, characterized by *béton brut* (raw exposed concrete), timber board formwork impressions, heavy cantilevered massing, and deeply recessed window embrasures.

### Core Objectives & Principles
- **Curatorial Rigor**: Site-disjoint dataset curation (zero cross-split building overlap), verified open licensing (CC BY-SA 4.0, CC BY 4.0, CC0), and explicit resolution auditing.
- **Controlled Evaluation**: Deterministic seed-matched baseline comparisons (Base SDXL vs. LoRA v1), targeted anti-leakage testing across 8 competing movements, and feature-space similarity analysis (ResNet-34).
- **Scientific Honesty**: Explicitly distinguishing `[MEASURED]`, `[QUALITATIVE]`, `[INFERRED]`, and `[LIMITATION]` observations. Differentiating between completed pilot generations and planned evaluation protocols.
- **Root-Cause Analysis**: Diagnosing conditioning bottlenecks (uncovering 100% boilerplate caption redundancy) and formulating clean, hypothesis-driven future enhancements rather than blindly retraining.

---

## 2. Repository Manual & Documentation Map

This repository is thoroughly documented. Below is a comprehensive guide to every Markdown document in the project:

### Root Documentation Suite

| Document | Primary Focus & Summary |
| :--- | :--- |
| [`PORTFOLIO_CASE_STUDY.md`](PORTFOLIO_CASE_STUDY.md) | **1–2 Page Executive Summary**: A concise, application-ready portfolio narrative detailing the problem, dataset engineering, LoRA training configuration, baseline comparisons, feature similarity analysis, and the caption conditioning limitation. |
| [`FINAL_RESULTS.md`](FINAL_RESULTS.md) | **Concise Results Summary**: Structured technical summary organized into 11 sections covering dataset splits, training parameters, base vs. LoRA findings, anti-leakage results, ResNet-34 distributions, and limitations with strict epistemological labeling. |
| [`EXPERIMENT_REPORT.md`](EXPERIMENT_REPORT.md) | **Comprehensive Technical Report**: In-depth 20-phase audit documenting the full experimental lifecycle, training dynamics, loss progression, hardware profiles, and analytical methodology. |
| [`DATASET_CARD.md`](DATASET_CARD.md) | **Hugging Face / Model Card Format**: Complete dataset specification including source provenance (`axel-riben/arcdataset-brutalism-extension` / Wikimedia), licensing breakdown, spatial quality filters, site-disjoint split logic, and manifest references. |
| [`MODEL_CARD.md`](MODEL_CARD.md) | **Adapter Model Card**: Detailed architecture documentation of `brutalism_sdxl_lora_v1`, UNet attention target modules (`to_k`, `to_q`, `to_v`, `to_out.0`), rank/alpha parameters, intended use, and failure modes. |
| [`EVALUATION.md`](EVALUATION.md) | **Evaluation Protocol & Findings**: Detailed qualitative and quantitative evaluation documentation, delta analysis tables for Base vs. LoRA (seeds 42–47), anti-leakage audits, ResNet-34 cosine similarity metrics, and held-out test distribution analysis. |
| [`RUN_2_DECISION.md`](RUN_2_DECISION.md) | **Future Work / Enhancement Proposal**: Formal justification for a controlled follow-up experiment (Run 2A), isolating caption quality as the single variable by introducing 22 instance-specific, visually grounded captions while holding all other training parameters constant. |

### Specialized Evaluation Reports (`evaluation/`)

| Document | Primary Focus & Summary |
| :--- | :--- |
| [`evaluation/README.md`](evaluation/README.md) | **Evaluation Package Index**: Directory overview indexing baseline generations, LoRA outputs, comparison panels, anti-leakage montages, and CSV logs. |
| [`evaluation/caption_audit.md`](evaluation/caption_audit.md) | **Conditioning Limitation Audit**: Critical diagnostic report revealing that all 22 training images received the exact same 27-word template caption. Analyzes the resulting monolithic style collapse and defines the 9-attribute captioning framework for Run 2A. |
| [`evaluation/ARC_0012_resolution.md`](evaluation/ARC_0012_resolution.md) | **Discrepancy Resolution Report**: Clarifies the numbering collision between the legacy historical dataset (where an Ibn Tulun Kufic plaque was excluded) and the active modern dataset (where `ARC_0012` is a legitimate Belgrade Brutalist residential block, CC BY 4.0). |

### Colab & Notebook Guides (`colab/`)

| Document | Primary Focus & Summary |
| :--- | :--- |
| [`colab/README.md`](colab/README.md) | **Google Colab Execution Guide**: Step-by-step instructions for running training (`brutalism_sdxl_lora.ipynb`) and controlled evaluations (`brutalism_sdxl_lora_eval.ipynb`) on cloud GPUs (Tesla T4 / A100). |

---

## 3. Directory Layout

```text
Architectural-Styles-LoRA/
├── Architectural_Styles_LoRA_Presentation.pptx # 11-Slide Executive Visual Deck
├── data/
│   └── clean/
│       ├── images/
│       │   ├── brutalism/             # 28 Curated Brutalism images (ARC_0001–ARC_0028)
│       │   ├── bauhaus/               # 28 Bauhaus images
│       │   ├── international_style/   # 28 International Style images
│       │   └── postmodern/            # 28 Postmodern images
│       └── metadata/
│           ├── train.csv              # 88 train records (22 per style)
│           ├── val.csv                # 12 val records (3 per style)
│           └── test.csv               # 12 test records (3 per style)
├── evaluation/
│   ├── baseline/                      # 6 Base SDXL 1.0 generations (Seeds 42–47)
│   ├── lora/                          # 12 SDXL LoRA v1 generations (Seeds 42–53)
│   ├── baseline_vs_lora/              # 6 Side-by-side composite comparison panels
│   ├── leakage/                       # 8 Anti-leakage test outputs & montage grid
│   ├── memorization/                  # 10 ResNet-34 inspection panels (similarity >= 0.75)
│   ├── heldout/                       # 3 Held-out test specimens (ARC_0026, 0027, 0028)
│   ├── neutral_prompts/               # Test directory for neutral prompt evaluation
│   ├── weight_sweep/                  # Test directory for adapter weight sweep grids
│   ├── checkpoint_comparison/         # Test directory for multi-checkpoint comparison
│   ├── base_vs_lora_results.csv       # Side-by-side delta analysis
│   ├── evaluation_results.csv         # Full 12-prompt LoRA generation log
│   ├── leakage_results.csv            # Anti-leakage audit findings
│   ├── memorization_results.csv       # Corrected feature similarity & nearest training neighbors
│   ├── caption_audit.md               # Conditioning audit of training captions
│   ├── ARC_0012_resolution.md        # Legacy vs active dataset disambiguation
│   └── README.md                      # Evaluation package overview
├── colab/
│   ├── brutalism_sdxl_lora.ipynb      # Complete Colab training notebook
│   ├── brutalism_sdxl_lora_eval.ipynb # Colab controlled evaluation runner
│   └── README.md                      # Colab execution guide
├── scripts/
│   ├── train_text_to_image_lora_sdxl.py # Official Diffusers SDXL LoRA trainer
│   ├── generate_presentation.py       # Automated 11-slide presentation generator
│   ├── run_memorization_audit.py      # ResNet-34 feature extraction & panel builder
│   ├── generate_base_vs_lora_panels.py# Base vs LoRA side-by-side panel generator
│   ├── audit_leakage_tests.py         # Anti-leakage audit & montage generator
│   └── run_controlled_evaluation.py   # Full evaluation runner (sweep, base leakage, ckpt)
├── outputs/
│   └── brutalism_sdxl_lora_v1/        # Raw run outputs, tensorboard logs & checkpoints
│       └── final/                     # Checkpoint-110, 220, 330, and final safetensors
├── requirements.txt                   # Pinned Python package dependencies
├── environment.txt                    # Hardware & software environment specs
├── training_config.json               # Exact training parameters
├── evaluation_config.json             # Exact evaluation parameters & rubrics
├── dataset_manifest.csv               # Manifest of all 28 Brutalism images
├── DATASET_CARD.md                    # Curation, provenance, splits & limitations
├── MODEL_CARD.md                      # Model architecture, hyperparameters & usage
├── EVALUATION.md                      # Empirical evaluation report with evidence labels
├── EXPERIMENT_REPORT.md               # End-to-end 20-phase technical experiment report
├── FINAL_RESULTS.md                   # Concise results summary (Sections 1–11)
├── RUN_2_DECISION.md                  # Future Work: Run 2A single-variable proposal
└── PORTFOLIO_CASE_STUDY.md            # 1–2 page application-ready portfolio case study
```

---

## 4. Controlled Evaluation Summary (Run 1)

| Evaluation Dimension | Methodology & Scope | Key Empirical Finding | Evidence Level |
| :--- | :--- | :--- | :--- |
| **Dataset Verification** | Filesystem & checksum audit | Exactly 22 Brutalism images in train; 0 competing styles. Short edge $\ge 1024$ px. | `[MEASURED]` |
| **`ARC_0012` Resolution** | Historical vs. active provenance | Verified as Belgrade residential block (CC BY 4.0), not legacy Kufic plaque. | `[MEASURED]` |
| **Base vs. LoRA** | Matched seeds ($42$–$47$), CFG 7.5 | LoRA synthesizes rough board-marked concrete, deep embrasures, heavy cantilevers. | `[QUALITATIVE]` |
| **Style Leakage** | 8 Anti-leakage test prompts | No obvious examples of targeted competing motifs (Gothic, Classical, Bauhaus, etc.) observed. | `[QUALITATIVE]` |
| **Feature Similarity** | ResNet-34 cosine similarity (excl. self) | Train-vs-train baseline: $0.7028 \pm 0.0668$. Generated-vs-train: $0.6786 \pm 0.0777$. Aligns with held-out test ($0.6901$). | `[MEASURED]` |
| **Memorization Inspection** | Side-by-side inspection ($\ge 0.75$) | No obvious reproduction of distinctive silhouettes, camera angles, or window layouts. | `[QUALITATIVE]` |
| **Generalization Context** | 3 Held-out test images | Generated samples contain vocabulary present in held-out test; attribution to LoRA vs. SDXL prior remains unisolated. | `[LIMITATION]` |
| **Caption Audit** | Lexical & token diversity analysis | 22/22 captions are identical template boilerplate; model learned a monolithic style vector. | `[LIMITATION]` |
| **Future Work / Enhancement** | Controlled follow-up design | Run 2A proposed as a single-variable controlled experiment testing 22 instance-specific captions. | `[DECISION]` |

---

## 5. Future Work & Planned Enhancements (Run 2A)

The primary finding from the Run 1 audit is that the adapter's inability to disentangle fine-grained architectural features stems from **100% boilerplate caption redundancy**.

Rather than increasing training duration or modifying multiple variables simultaneously, the proposed **Run 2A** follow-up experiment maintains strict experimental controls:
- **Constants**: Same 22 Brutalism images, same SDXL 1.0 base model, same Rank 16 / Alpha 16, same frozen text encoder, same learning rate ($1 \times 10^{-4}$), and same 330-step budget.
- **Single Isolated Variable**: Replaces the single template caption with **22 unique, visually grounded 9-attribute captions** describing building typology, structural massing, specific surface finish, fenestration, and daylight.
- **Detailed Specification**: Documented in [`RUN_2_DECISION.md`](RUN_2_DECISION.md).

---

## 6. Quickstart & Reproducibility

### 1. Environment Setup
```bash
git clone https://github.com/OmarKhalil2003/Architectural-Styles-LoRA.git
cd Architectural-Styles-LoRA
pip install -r requirements.txt
```

### 2. Rerun Memorization & Feature-Space Similarity Audit
```bash
python scripts/run_memorization_audit.py
```
Outputs verified metrics and neutral side-by-side inspection panels to `evaluation/memorization/`.

### 3. Generate Base vs. LoRA Comparison Panels
```bash
python scripts/generate_base_vs_lora_panels.py
```
Builds 6 composite side-by-side panels in `evaluation/baseline_vs_lora/` and updates `evaluation/base_vs_lora_results.csv`.

### 4. Run Anti-Leakage Audit
```bash
python scripts/audit_leakage_tests.py
```
Audits all 8 leakage test images and generates `evaluation/leakage/leakage_summary_grid.jpg`.

### 5. Generate Presentation Deck
```bash
python scripts/generate_presentation.py
```
Builds the 11-slide widescreen presentation deck `Architectural_Styles_LoRA_Presentation.pptx`.

### 6. Execute Additional Evaluation Suite (Colab or Local)
To run the automated neutral-prompt weight sweep and multi-checkpoint comparisons:
- In Google Colab: open [`colab/brutalism_sdxl_lora_eval.ipynb`](colab/brutalism_sdxl_lora_eval.ipynb).
- Locally (requires GPU / CPU offload):
  ```bash
  python scripts/run_controlled_evaluation.py --all --offload
  ```

---

## 7. License & Attribution
- Architectural images curated from Wikimedia Commons under Creative Commons licenses (CC BY-SA 4.0, CC BY 4.0, CC0). Full per-image attribution and source URLs are documented in [`dataset_manifest.csv`](dataset_manifest.csv).
- Research code and technical documentation licensed under the MIT License.
