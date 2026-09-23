# Architectural LoRA Evaluation Protocol: Brutalism Pilot

This document establishes the standardized qualitative and empirical evaluation protocol for testing the **Brutalism Architecture SDXL LoRA** against base SDXL 1.0. Rather than arbitrary subjective numbers, evaluations must record concrete descriptive observations across seven rigorous dimensions.

---

## Evaluation Dimensions

### A. Style Adherence
- **Objective**: Determine whether the generated building accurately exhibits the primary morphological characteristics of Brutalist architecture.
- **Key Indicators to Inspect**:
  - *Massing*: Heavy, monolithic, sculptural, or volumetric masses.
  - *Structural Expression*: Exposed load-bearing piers, pilotis, shear walls, cantilevered beams, or waffle slab soffits.
  - *Fenestration*: Deep-set punched rectangular windows, continuous horizontal ribbon openings with deep reveals, or narrow vertical slit embrasures.
  - *Surface Treatment*: Raw unpainted concrete, visible wooden formwork impressions (board-marked *béton brut*), bush-hammered textures, or coarse exposed aggregate.
- **Descriptive Outcome Categories**:
  - `STRONG_ADHERENCE`: Clear, dominant Brutalist massing and raw concrete materiality.
  - `MODERATE_ADHERENCE`: Recognizable Brutalist cues, but partially diluted by generic modernist traits.
  - `NON_ADHERENT`: Building does not exhibit identifiable Brutalist vocabulary.

---

### B. Architectural Coherence
- **Objective**: Assess the overall composition, proportion, and unity of the building's exterior.
- **Key Indicators to Inspect**:
  - Logical spatial relationships between base, middle floors, roofline, and entryways.
  - Consistent geometric grid or module across the facade.
  - Absence of floating, detached, or physically impossible floating geometric fragments.
- **Descriptive Outcome Categories**:
  - `COHERENT`: Well-proportioned architectural elevation with unified rhythm.
  - `MINOR_INCOHERENCE`: Minor local discrepancies (e.g., misaligned window mullions or uneven sill heights) that do not break the overall building composition.
  - `INCOHERENT`: Severe architectural hallucinations, detached roofs, or broken perspectives.

---

### C. Structural Plausibility
- **Objective**: Evaluate whether the depicted structure obeys real-world structural engineering and load-path logic.
- **Key Indicators to Inspect**:
  - Adequate load-bearing support for large cantilevered upper stories.
  - Realistic column-to-beam connections and ground piers.
  - Gravity logic: Cantilevers must visually show structural depth or counterbalancing geometry rather than hovering unrealistically.
- **Descriptive Outcome Categories**:
  - `STRUCTURALLY_PLAUSIBLE`: Structural members, cantilevers, and spans appear capable of supporting real-world loads.
  - `QUESTIONABLE`: Unusually thin supports or extreme spans that appear dubious without specialized tension engineering.
  - `IMPLAUSIBLE`: Clear violation of gravity logic (e.g., massive solid concrete block resting on fragile glass without columns).

---

### D. Material Consistency
- **Objective**: Check surface textures, tactile rendering, and realistic weathering.
- **Key Indicators to Inspect**:
  - Authentic representation of board-marked concrete grain, tie-rod holes, aggregate specks, and slight rainwater staining.
  - Proper reflectivity: Matte, low-specular finish for raw concrete; appropriate reflection on glass panes.
  - Avoidance of plastic, overly smooth, or airbrushed textures.
- **Descriptive Outcome Categories**:
  - `AUTHENTIC_TEXTURE`: Convincing concrete surface tactile realism with natural lighting response.
  - `ARTIFICIAL_TEXTURE`: Concrete appears painted, plasticky, or excessively blurred.
  - `INCORRECT_MATERIAL`: Concrete replaced by steel panels, plaster, or stucco.

---

### E. Prompt Adherence
- **Objective**: Verify that the generated image faithfully incorporates all specific conditions defined in the evaluation prompt (e.g., building typology, lighting condition, viewpoint).
- **Key Indicators to Inspect**:
  - Did the prompt ask for a *library*, *museum*, or *plaza*? Is the functional character conveyed?
  - Did the prompt specify *direct daylight* vs. *overcast diffuse light*?
  - Did the prompt specify *street level* vs. *courtyard* perspective?
- **Descriptive Outcome Categories**:
  - `FULL_COMPLIANCE`: All prompt elements faithfully represented.
  - `PARTIAL_COMPLIANCE`: General style captured, but specific context (e.g., courtyard or overcast light) omitted.
  - `NON_COMPLIANT`: Generation fails to reflect key prompt constraints.

---

### F. Style Leakage (Cross-Contamination)
- **Objective**: Identify unexpected intrusion of decorative or formal elements belonging to non-Brutalist movements.
- **Checklist of Specific Leakage Artifacts**:
  1. *Gothic*: Pointed lancet arches, traceried stone windows, ribbed vaults, pinnacles.
  2. *Classical / Baroque*: Fluted columns, pediments, ornate capitals, entablatures, decorative moldings.
  3. *Postmodern*: Ironic broken pediments, pastel color accents, playful geometric pop-art elements.
  4. *Bauhaus / Early Modern*: Delicate thin steel sash frames, smooth pure white render, tubular ship-railings.
  5. *Commercial High-Tech*: All-glass curtain wall boxes, mirror-glass reflections, thin metal mullions.
- **Descriptive Outcome Categories**:
  - `ZERO_LEAKAGE`: Purely Brutalist vocabulary; no foreign stylistic artifacts.
  - `MINOR_LEAKAGE`: Trace element present (e.g., slightly decorative metal railing or non-standard color accent).
  - `SEVERE_LEAKAGE`: Prominent non-Brutalist architectural forms dominate the image.

---

### G. Memorization vs. Generalization
- **Objective**: Confirm that the fine-tuned model has learned an *architectural visual vocabulary* rather than simply replicating training photographs.
- **Protocol**:
  1. For every generated evaluation sample, compare against all 22 Brutalism training images (`ARC_0001` through `ARC_0022`).
  2. Specifically cross-reference against landmark training specimens:
     - *Milutina Milankovića Residential Complex, Belgrade* (`ARC_0011`–`ARC_0015`)
     - *Former Public Library, Doetinchem* (`ARC_0017`, `ARC_0018`)
     - *Arnulfsplatz Regensburg* (`ARC_0001`)
     - *Biurowiec ZREMB, Wrocław* (`ARC_0002`)
     - *Bank of Finland, Helsinki* (`ARC_0010`)
  3. Verify whether the generation reproduces identical facade arrangements, window counts, unique background urban context, or photographic angles of any training image.
- **Descriptive Outcome Categories**:
  - `NOVEL_COMPOSITION`: Distinct, novel architectural design sharing stylistic vocabulary without copying specific training buildings.
  - `PARTIAL_DERIVATIVE`: Notable structural motif strongly reminiscent of a specific training building, but in a modified composition.
  - `MEMORIZED_REPLICA`: High structural and photographic correspondence to an existing training photograph.

---

## Evaluation Workflow Summary

```text
Prompt (from brutalism_prompts.txt or style_leakage_prompts.txt)
                     │
                     ▼
       Generate with Base SDXL 1.0 (Fixed Seed, 30 steps)
       Generate with SDXL + Brutalism LoRA (Same Seed, 30 steps)
                     │
                     ▼
           Side-by-Side Comparison
                     │
       ┌─────────────┴─────────────┐
       ▼                           ▼
Vocabulary Gain Check       Style Leakage Check
(Concrete texture, massing) (Gothic, Classical, Postmodern)
       │                           │
       └─────────────┬─────────────┘
                     ▼
          Memorization Comparison
       (Against 22 Training Images)
                     │
                     ▼
       Complete Evaluation Record Entry
```
