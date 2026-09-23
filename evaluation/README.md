# Controlled Evaluation Package: Brutalism SDXL LoRA Pilot (Run 1)

This directory contains the complete evaluation suite, quantitative results, and qualitative comparison panels for the **Brutalism SDXL LoRA Pilot (`brutalism_sdxl_lora_v1`)**.

---

## Directory Organization

```text
evaluation/
├── baseline/                  # 6 Base SDXL 1.0 generations (Seeds 42–47) & base leakage tests
├── lora/                      # 12 SDXL LoRA v1 generations (Seeds 42–53, weight 1.0)
├── baseline_vs_lora/          # Side-by-side composite comparison panels (Base SDXL vs LoRA v1)
│   ├── comparison_eval_01.jpg
│   ├── ...
│   └── comparison_eval_06.jpg
├── leakage/                   # 8 Anti-Leakage test generations & composite evaluation grid
│   ├── leakage_test_01_1. Baseline Test.jpg
│   ├── ...
│   ├── leakage_test_08_8. Material Contrast Test.jpg
│   └── leakage_summary_grid.jpg
├── memorization/              # ResNet-34 feature similarity inspection panels (similarity >= 0.75)
│   ├── panel_lora_eval_01_vs_ARC_0020.jpg
│   ├── panel_lora_eval_03_vs_ARC_0018.jpg  (Trigger: 0.8581)
│   ├── panel_lora_eval_04_vs_ARC_0012.jpg  (Discrepancy audit: 0.7908)
│   ├── panel_lora_eval_06_vs_ARC_0018.jpg  (Trigger: 0.8541)
│   └── ... (10 total panels)
├── heldout/                   # 3 Held-out test exemplars (ARC_0026, ARC_0027, ARC_0028)
├── neutral_prompts/           # Outputs for neutral architectural prompts
├── weight_sweep/              # LoRA adapter weight sweep [0.0, 0.25, 0.50, 0.75, 1.00]
├── checkpoint_comparison/     # Multi-checkpoint comparison (Base vs 110 vs 220 vs 330)
│
├── base_vs_lora_results.csv   # Detailed delta analysis for controlled Base vs LoRA comparisons
├── evaluation_results.csv     # Full generation log for 12 LoRA evaluation prompts
├── leakage_results.csv        # Multi-style leakage audit findings (8 competing architectural styles)
├── memorization_results.csv   # ResNet-34 cosine similarity, top-3 neighbors, & inspection tags
├── caption_audit.md           # Critical conditioning audit of the 22 training captions
├── ARC_0012_resolution.md      # Provenance and numbering collision resolution report
└── README.md                  # This index document
```

---

## Evaluation Summary Table

| Evaluation Phase | Methodology | Key Finding | Status |
| :--- | :--- | :--- | :--- |
| **Dataset Verification** | File inspection & checksum audit | Exactly 22 Brutalism images in train; 0 competing styles. | **Verified (`MEASURED`)** |
| **`ARC_0012` Resolution** | Historical vs active dataset mapping | Legitimate Belgrade residential block (CC BY 4.0), not legacy Kufic plaque. | **Resolved (`MEASURED`)** |
| **Base vs. LoRA** | Identical prompts/seeds (42–47) | Visibly textured board-marked concrete, deep embrasures, reduced glazing. | **Demonstrated (`QUALITATIVE`)** |
| **Style Leakage** | 8 Competing-style anti-prompts | Zero Gothic, Classical, Baroque, Postmodern, or Bauhaus motifs observed. | **Contained (`QUALITATIVE`)** |
| **Feature Similarity** | ResNet-34 512-dim cosine sim | Mean sim $0.6786$; aligns with held-out test ($0.6901$); no geometric memorization. | **Generalizing (`MEASURED`)** |
| **Caption Audit** | Lexical & token diversity analysis | 100% boilerplate redundancy; monolithic style vector learned. | **Identified (`LIMITATION`)** |
| **Run 2 Justification** | Empirical gap analysis | Justified to introduce grounded 9-attribute captions and checkpoint selection. | **Recommended (`DECISION`)** |
