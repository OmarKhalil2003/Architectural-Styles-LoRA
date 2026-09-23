# Architectural-Styles-LoRA

### *Learning Historical Architectural Vocabulary Across Historical and Contemporary Architecture*

---

## 1. Project Objective & Core Research Question

Investigate whether a rigorously curated photographic dataset spanning historical, traditional, modern, and contemporary Architectural/Islamic architecture—paired with structured architectural captioning—can teach an image-generation model (SDXL LoRA) to preserve core architectural vocabulary while legitimately adapting it to contemporary structural contexts.

### Central Research Question
> **Can a curated dataset spanning historical and contemporary Architectural/Islamic architecture teach an image-generation model to preserve architectural vocabulary while adapting it to contemporary architectural contexts, without regressing to generic historical pastiche or incoherent hallucinations?**

---

## 2. Target Visual Domain & Architectural Continuum

The dataset models a coherent evolutionary continuum rather than isolated historical monuments:

```
HISTORICAL (Fatimid, Mamluk, Umayyad, Ayyubid)
   │
   ▼
TRADITIONAL (Vernacular Architectural, Ottoman-period domestic, Hijazi coral stone & rawshan)
   │
   ▼
MODERN (20th-century Architectural regionalism, Hassan Fathy, early civic reinventions)
   │
   ▼
CONTEMPORARY (Aga Khan Award projects, contemporary screens, concrete/timber lattices, cultural centers)
```

### Core Architectural Vocabulary
- **Geometric Architectural Screens**: Traditional turned-wood *mashrabiya* / *rawshan*, pierced stone *qamariya*, modern ultra-high-performance concrete (UHPC) and engineered timber shading screens.
- **Arches & Portals**: Pointed arches, horseshoe arches, keel arches, and contemporary structural parabolic/catenary spans.
- **Spatial Composition**: Open-air *sahn* (courtyards) with central basins/fountains, transitional *iwans*, arcaded galleries, and overhead lightwells/oculi.
- **Materials**: Ashlar limestone, coral stone, brick, marble polychromy (*ablaq*), teak/cedar timber, modern fair-faced concrete, steel, and structural glass.
- **Filtered Daylight**: Deep shadows, dappled daylight through geometric perforations, and passive solar climate responsiveness.

---

## 3. Geographic Scope

To prevent architectural incoherence, the geographic scope is strictly controlled across four interconnected Historical cultural zones:
1. **Egypt** (Cairo historic cores & contemporary cultural adaptations)
2. **Levant** (Syria, Jordan, Palestine, Lebanon)
3. **Architecturalian Peninsula** (Jeddah Hijazi historic district, Najd/Diriyah vernacular, Gulf contemporary)
4. **North Africa / Maghreb** (Morocco, Tunisia)

---

## 4. Primary Dataset Source: Archnet

The dataset is consolidated around **Archnet** (Aga Khan Documentation Center at MIT & Aga Khan Trust for Culture), supplemented by our vetted pilot references:
- **Unified Ecosystem**: Consistent architectural terminology, scholarly site documentation, and institutional provenance.
- **Temporal Span**: Documents historic monuments alongside contemporary Aga Khan Award for Architecture (AKAA) projects.
- **Rigorous Rights Management**: Explicit tracking of individual image rights, photographer credit, institution, and fair academic use.

### Target Dataset Distribution (60 Images Total)

| Architectural Category | Target Count | Architectural Focus |
|---|:---:|---|
| **Historical Islamic Architecture** | 20 | Fatimid, Mamluk, and Umayyad stone facades, monumental portals, and grand courtyards |
| **Traditional Architectural Architecture** | 10 | Ottoman-period residences, vernacular Hijazi *rawshan*, domestic courtyards (*Bayt al-Suhaymi*) |
| **Modern Islamic/Architectural Architecture** | 15 | 20th-century Architectural modernism, indigenous earth/brick adaptations, modern civic mosques |
| **Contemporary Architecture (Islamic Vocabulary)** | 15 | Aga Khan Award winners, contemporary geometric screen envelopes, modern cultural centers |
| **Total** | **60** | **Balanced across the temporal and spatial continuum** |

---

## 5. Controlled Evaluation Framework

### Comparative Benchmark
**Base SDXL 1.0** vs. **Architectural-Styles-LoRA (Fine-Tuned)**

### Benchmark Evaluation Prompts
- **Prompt 1 (Historical)**:
  `"Cairo Islamic courtyard with carved limestone, pointed arches, traditional wooden screens and geometric ornament, authentic natural lighting."`
- **Prompt 2 (Contemporary)**:
  `"Contemporary cultural center in Cairo using geometric stone screens, modern concrete structure and filtered daylight, architectural photography."`
- **Prompt 3 (Cross-Era Synthesis)**:
  `"Contemporary Architectural cultural center inspired by traditional Cairo mashrabiya, using modern concrete, glass and engineered timber, dappled natural light, high architectural realism."`

### Evaluation Criteria
1. **Architectural Vocabulary Fidelity**: Accurate geometric screens, genuine arch typologies, coherent spatial transitions.
2. **Material Consistency**: Plausible textures (limestone, cedar, fair-faced concrete, architectural glass).
3. **Geometric Integrity**: Intricate, non-warped star rosettes and lattice screens.
4. **Style Leakage Reduction**: Contemporary prompts generate genuine contemporary buildings rather than historical pastiche with modern windows.
5. **Structural Plausibility**: Coherent engineering and load-bearing logic.