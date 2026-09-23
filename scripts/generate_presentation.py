import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    # 16:9 widescreen dimensions
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Theme colors
    COLOR_BG = RGBColor(20, 23, 28)
    COLOR_CARD = RGBColor(30, 34, 42)
    COLOR_CARD_BORDER = RGBColor(50, 58, 72)
    COLOR_GOLD = RGBColor(225, 185, 110)
    COLOR_CYAN = RGBColor(115, 195, 235)
    COLOR_GREEN = RGBColor(135, 215, 155)
    COLOR_WHITE = RGBColor(245, 247, 250)
    COLOR_MUTED = RGBColor(170, 178, 192)
    COLOR_LIGHT_MUTED = RGBColor(130, 138, 150)

    def set_slide_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = COLOR_BG
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, category_text="ARCHITECTURAL STYLES LORA PILOT"):
        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(1.1))
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        p_cat = tf.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = COLOR_GOLD

        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.size = Pt(24)
        p_title.font.bold = True
        p_title.font.color.rgb = COLOR_WHITE

    def add_card(slide, left, top, width, height, title=None, title_color=COLOR_GOLD):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = COLOR_CARD
        card.line.color.rgb = COLOR_CARD_BORDER
        card.line.width = Pt(1)

        if title:
            tb = slide.shapes.add_textbox(left + Inches(0.25), top + Inches(0.2), width - Inches(0.5), Inches(0.5))
            tf = tb.text_frame
            tf.word_wrap = True
            tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
            p = tf.paragraphs[0]
            p.text = title
            p.font.size = Pt(15)
            p.font.bold = True
            p.font.color.rgb = title_color
        return card

    # =========================================================================
    # SLIDE 0: TITLE & METADATA
    # =========================================================================
    slide0 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide0)

    title_box = slide0.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.3), Inches(3.2))
    tf0 = title_box.text_frame
    tf0.word_wrap = True

    p0_sub = tf0.paragraphs[0]
    p0_sub.text = "ARCHITECTURAL GENERATIVE-AI RESEARCH PILOT"
    p0_sub.font.size = Pt(13)
    p0_sub.font.bold = True
    p0_sub.font.color.rgb = COLOR_GOLD

    p0_title = tf0.add_paragraph()
    p0_title.text = "Architectural Styles LoRA: Diffusion Fine-Tuning Pilot"
    p0_title.font.size = Pt(32)
    p0_title.font.bold = True
    p0_title.font.color.rgb = COLOR_WHITE
    p0_title.space_before = Pt(8)

    p0_desc = tf0.add_paragraph()
    p0_desc.text = "Curating, Fine-Tuning, and Auditing an SDXL 1.0 Low-Rank Adapter for Authentic Brutalist Tectonics"
    p0_desc.font.size = Pt(18)
    p0_desc.font.color.rgb = COLOR_CYAN
    p0_desc.space_before = Pt(10)

    # Author metadata card
    add_card(slide0, Inches(1.0), Inches(5.1), Inches(11.333), Inches(1.6))
    meta_box = slide0.shapes.add_textbox(Inches(1.3), Inches(5.3), Inches(10.7), Inches(1.2))
    tf_meta = meta_box.text_frame
    tf_meta.word_wrap = True

    p_a1 = tf_meta.paragraphs[0]
    p_a1.text = "Author: Omar Khalil"
    p_a1.font.size = Pt(15)
    p_a1.font.bold = True
    p_a1.font.color.rgb = COLOR_WHITE

    p_a2 = tf_meta.add_paragraph()
    p_a2.text = "GitHub Repository: https://github.com/OmarKhalil2003/Architectural-Styles-LoRA"
    p_a2.font.size = Pt(13)
    p_a2.font.color.rgb = COLOR_GOLD
    p_a2.space_before = Pt(4)

    p_a3 = tf_meta.add_paragraph()
    p_a3.text = "Contact: omarkhalil.contact@gmail.com  |  Self-Directed Research Pilot"
    p_a3.font.size = Pt(13)
    p_a3.font.color.rgb = COLOR_MUTED
    p_a3.space_before = Pt(4)

    # =========================================================================
    # SLIDE 1: PROBLEM
    # =========================================================================
    slide1 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide1)
    add_header(slide1, "The Problem: Tectonic Hallucination in Foundation Models", "01. RESEARCH MOTIVATION")

    add_card(slide1, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "Foundation Model Limitations", COLOR_GOLD)
    tb1_1 = slide1.shapes.add_textbox(Inches(1.05), Inches(2.5), Inches(5.1), Inches(4.0))
    tf1_1 = tb1_1.text_frame
    tf1_1.word_wrap = True
    bullets_1 = [
        ("Generic Concrete Geometry: ", "Pretrained models (SDXL 1.0) collapse Brutalism into flat, smooth gray boxes lacking material depth."),
        ("Commercial Style Drift: ", "Prompts frequently inject modern polished curtain-wall glazing and aluminum composite cladding into historical styles."),
        ("Lack of Tectonic Specificity: ", "Models fail to differentiate board-marked timber formwork, bush-hammered aggregate, and cast-in-place concrete joints."),
        ("Superficial Pastiche: ", "Architectural prompts often yield pastiche combinations rather than structurally coherent monolithic massing.")
    ]
    for idx, (b_title, b_desc) in enumerate(bullets_1):
        p = tf1_1.paragraphs[0] if idx == 0 else tf1_1.add_paragraph()
        p.space_before = Pt(10)
        run1 = p.add_run()
        run1.text = b_title
        run1.font.bold = True
        run1.font.size = Pt(13)
        run1.font.color.rgb = COLOR_WHITE
        run2 = p.add_run()
        run2.text = b_desc
        run2.font.size = Pt(13)
        run2.font.color.rgb = COLOR_MUTED

    add_card(slide1, Inches(6.9), Inches(1.8), Inches(5.6), Inches(5.0), "Experimental Research Objective", COLOR_CYAN)
    tb1_2 = slide1.shapes.add_textbox(Inches(7.15), Inches(2.5), Inches(5.1), Inches(4.0))
    tf1_2 = tb1_2.text_frame
    tf1_2.word_wrap = True
    bullets_2 = [
        ("Parameter-Efficient Fine-Tuning: ", "Train a Low-Rank Adapter (LoRA) on SDXL 1.0 using a small, rigorously curated dataset."),
        ("Tectonic Vocabulary Induction: ", "Teach the model authentic béton brut, massive cantilevered volumes, deep window embrasures, and structural piers."),
        ("Anti-Leakage Verification: ", "Verify that the adapter does not leak competing styles (Gothic, Classical, Baroque, Postmodern, Bauhaus)."),
        ("Memorization vs. Generalization: ", "Establish quantitative feature-space similarity bounds (ResNet-34) to verify genuine visual generalization.")
    ]
    for idx, (b_title, b_desc) in enumerate(bullets_2):
        p = tf1_2.paragraphs[0] if idx == 0 else tf1_2.add_paragraph()
        p.space_before = Pt(10)
        run1 = p.add_run()
        run1.text = b_title
        run1.font.bold = True
        run1.font.size = Pt(13)
        run1.font.color.rgb = COLOR_WHITE
        run2 = p.add_run()
        run2.text = b_desc
        run2.font.size = Pt(13)
        run2.font.color.rgb = COLOR_MUTED

    # =========================================================================
    # SLIDE 2: DATASET OVERVIEW
    # =========================================================================
    slide2 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide2)
    add_header(slide2, "Dataset Architecture: Multi-Style Corpus & Pilot Partitioning", "02. DATASET SPECIFICATION")

    # 3 Stat Cards across top
    stats = [
        ("112 IMAGES", "Balanced Multi-Style Dataset", "28 Brutalism, 28 Bauhaus, 28 International, 28 Postmodern", COLOR_GOLD),
        ("28 BRUTALISM", "Pilot Dataset Focus", "100% verified 24-bit sRGB, short edge >= 1024 px", COLOR_CYAN),
        ("0.0% LEAKAGE", "Site-Disjoint Splits", "22 Train (17 sites), 3 Val (3 sites), 3 Held-Out Test (3 sites)", COLOR_GREEN)
    ]
    for idx, (val, title, desc, col) in enumerate(stats):
        x = Inches(0.8 + idx * 4.0)
        add_card(slide2, x, Inches(1.8), Inches(3.7), Inches(1.6))
        tb = slide2.shapes.add_textbox(x + Inches(0.2), Inches(1.95), Inches(3.3), Inches(1.3))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = val
        p1.font.size = Pt(22)
        p1.font.bold = True
        p1.font.color.rgb = col
        p2 = tf.add_paragraph()
        p2.text = title
        p2.font.size = Pt(13)
        p2.font.bold = True
        p2.font.color.rgb = COLOR_WHITE
        p2.space_before = Pt(2)
        p3 = tf.add_paragraph()
        p3.text = desc
        p3.font.size = Pt(11)
        p3.font.color.rgb = COLOR_MUTED

    # Split details card
    add_card(slide2, Inches(0.8), Inches(3.7), Inches(11.733), Inches(3.1), "Site-Disjoint Split Integrity & Licensing", COLOR_WHITE)
    tb2_main = slide2.shapes.add_textbox(Inches(1.05), Inches(4.3), Inches(11.2), Inches(2.3))
    tf2_main = tb2_main.text_frame
    tf2_main.word_wrap = True
    split_lines = [
        ("Training Set (22 Images): ", "Spans 17 unique architectural sites across Europe and North America (libraries, grandstands, housing blocks, research centers)."),
        ("Validation Set (3 Images): ", "3 completely separate sites (Hotel Zlatibor, modern pavilion, Bordeaux educational hall) used for monitoring."),
        ("Held-Out Test Set (3 Images): ", "3 strictly isolated sites (Batten Arts, 1180 S Beverly, 720 Spadina) reserved for out-of-distribution evaluation."),
        ("License Transparency: ", "100% open licenses permitting machine learning research (CC BY-SA 4.0, CC BY 4.0, CC BY 2.0, and CC0 Public Domain). Complete per-image URLs and attribution in dataset_manifest.csv.")
    ]
    for idx, (b_title, b_desc) in enumerate(split_lines):
        p = tf2_main.paragraphs[0] if idx == 0 else tf2_main.add_paragraph()
        p.space_before = Pt(8)
        r1 = p.add_run()
        r1.text = b_title
        r1.font.bold = True
        r1.font.size = Pt(13)
        r1.font.color.rgb = COLOR_GOLD if "Train" in b_title else (COLOR_CYAN if "Test" in b_title else COLOR_WHITE)
        r2 = p.add_run()
        r2.text = b_desc
        r2.font.size = Pt(13)
        r2.font.color.rgb = COLOR_MUTED

    # =========================================================================
    # SLIDE 3: DATASET CURATION & AUDITING
    # =========================================================================
    slide3 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide3)
    add_header(slide3, "Curatorial Auditing: Provenance, Filters & Discrepancy Resolution", "03. DATASET ENGINEERING")

    add_card(slide3, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "Spatial Quality Curation Filters", COLOR_GOLD)
    tb3_1 = slide3.shapes.add_textbox(Inches(1.05), Inches(2.5), Inches(5.1), Inches(4.0))
    tf3_1 = tb3_1.text_frame
    tf3_1.word_wrap = True
    cur_bullets = [
        ("Resolution Standard: ", "Every image audited for short edge >= 1024 px (well above the 768px training resolution) to eliminate compression noise."),
        ("Elimination of Non-Spatial Assets: ", "Filtered out floor plans, blueprints, structural section drawings, and construction diagrams."),
        ("Photographic Cleanliness: ", "Excluded tourist-crowded perspectives, extreme raking distortion, and prominent commercial signage."),
        ("Lighting & Daylight Quality: ", "Selected exterior views capturing direct sunlight or diffuse daylight to reveal genuine surface formwork textures.")
    ]
    for idx, (b_title, b_desc) in enumerate(cur_bullets):
        p = tf3_1.paragraphs[0] if idx == 0 else tf3_1.add_paragraph()
        p.space_before = Pt(10)
        r1 = p.add_run()
        r1.text = b_title
        r1.font.bold = True
        r1.font.size = Pt(13)
        r1.font.color.rgb = COLOR_WHITE
        r2 = p.add_run()
        r2.text = b_desc
        r2.font.size = Pt(13)
        r2.font.color.rgb = COLOR_MUTED

    add_card(slide3, Inches(6.9), Inches(1.8), Inches(5.6), Inches(5.0), "Case Study: The ARC_0012 Discrepancy", COLOR_CYAN)
    tb3_2 = slide3.shapes.add_textbox(Inches(7.15), Inches(2.5), Inches(5.1), Inches(4.0))
    tf3_2 = tb3_2.text_frame
    tf3_2.word_wrap = True
    case_bullets = [
        ("The Initial Inconsistency: ", "Prior notes indicated ARC_0012 was rejected as a close-up Kufic foundation plaque from Mosque of Ibn Tulun."),
        ("Root-Cause Audit: ", "That exclusion belonged to an earlier, archived historical dataset. When pivoting to the 4-style 112-image modern dataset, filenames were sequentially re-indexed from ARC_0001."),
        ("Active Image Verification: ", "ARC_0012 in the clean dataset is a 1024x1360 RGB exterior photograph of a Brutalist residential block in Belgrade (Milutina Milankovica, CC BY 4.0)."),
        ("Conclusion: ", "ARC_0012 legitimately belongs to the 22 training images. Zero dataset corruption exists. Formally documented in evaluation/ARC_0012_resolution.md.")
    ]
    for idx, (b_title, b_desc) in enumerate(case_bullets):
        p = tf3_2.paragraphs[0] if idx == 0 else tf3_2.add_paragraph()
        p.space_before = Pt(10)
        r1 = p.add_run()
        r1.text = b_title
        r1.font.bold = True
        r1.font.size = Pt(13)
        r1.font.color.rgb = COLOR_WHITE
        r2 = p.add_run()
        r2.text = b_desc
        r2.font.size = Pt(13)
        r2.font.color.rgb = COLOR_MUTED

    # =========================================================================
    # SLIDE 4: TRAINING CONFIGURATION
    # =========================================================================
    slide4 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide4)
    add_header(slide4, "Diffusion LoRA Training Configuration & Dynamics", "04. MODEL & HYPERPARAMETERS")

    add_card(slide4, Inches(0.8), Inches(1.8), Inches(11.733), Inches(5.0), "Stable Diffusion XL 1.0 Parameter-Efficient Adaptation", COLOR_GOLD)
    tb4 = slide4.shapes.add_textbox(Inches(1.05), Inches(2.5), Inches(11.2), Inches(4.0))
    tf4 = tb4.text_frame
    tf4.word_wrap = True

    params = [
        ("Base Model & VAE", "stabilityai/stable-diffusion-xl-base-1.0  +  madebyollin/sdxl-vae-fp16-fix (FP16 numerical stability)", "Foundation Diffusion Backbone"),
        ("Adapter Architecture", "Low-Rank Adaptation (LoRA) on UNet attention projections (to_k, to_q, to_v, to_out.0)", "Parameter-efficient rank 16"),
        ("LoRA Rank & Alpha", "Rank r = 16, Alpha a = 16 (1:1 scaling ratio to prevent over-saturation)", "Prevents geometric memorization"),
        ("Text Encoders", "FROZEN (OpenCLIP ViT-bigG/14 and CLIP ViT-L/14)", "Preserves language prior"),
        ("Resolution & Batch", "768 x 768 px | Batch Size 1, Gradient Accumulation 4 (Effective Batch = 4)", "Stable gradient estimation"),
        ("Optimization", "AdamW (lr = 1e-4, beta1=0.9, beta2=0.999, wd=0.01) | constant_with_warmup (30 steps)", "Smooth convergence"),
        ("Training Budget", "330 optimization steps (55 epochs across 22 images) | Checkpoints @ 110, 220, 330", "Preserved all checkpoints"),
        ("Hardware & Precision", "NVIDIA Tesla T4 (14.56 GB VRAM) | FP16 mixed precision + Gradient Checkpointing", "Clean execution under 14 GB")
    ]
    for idx, (p_name, p_val, p_note) in enumerate(params):
        p = tf4.paragraphs[0] if idx == 0 else tf4.add_paragraph()
        p.space_before = Pt(6)
        r1 = p.add_run()
        r1.text = f"{p_name:22}: "
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = COLOR_CYAN
        r2 = p.add_run()
        r2.text = f"{p_val}  "
        r2.font.size = Pt(12)
        r2.font.color.rgb = COLOR_WHITE
        r3 = p.add_run()
        r3.text = f"[{p_note}]"
        r3.font.size = Pt(11)
        r3.font.color.rgb = COLOR_MUTED

    # =========================================================================
    # SLIDE 5: BASE VS LORA COMPARISON
    # =========================================================================
    slide5 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide5)
    add_header(slide5, "Controlled Evaluation: Base SDXL vs. SDXL LoRA v1", "05. BASELINE COMPARATIVE ANALYSIS")

    add_card(slide5, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "Base SDXL 1.0 (Pretrained)", COLOR_MUTED)
    tb5_1 = slide5.shapes.add_textbox(Inches(1.05), Inches(2.5), Inches(5.1), Inches(4.0))
    tf5_1 = tb5_1.text_frame
    tf5_1.word_wrap = True
    base_points = [
        ("Surface Finish: ", "Smooth, flat, render-like concrete surfaces lacking authentic timber formwork texture."),
        ("Glazing & Fenestration: ", "Defaults to contemporary commercial glass storefronts and standard domestic metal balcony railings."),
        ("Structural Shadowing: ", "Shallow window embrasures with weak, diffuse shadows that fail to articulate tectonic depth."),
        ("Massing Articulation: ", "Tendency toward conventional rectilinear blocks rather than aggressive, sculptural cantilevered projections.")
    ]
    for idx, (b_title, b_desc) in enumerate(base_points):
        p = tf5_1.paragraphs[0] if idx == 0 else tf5_1.add_paragraph()
        p.space_before = Pt(10)
        r1 = p.add_run()
        r1.text = b_title
        r1.font.bold = True
        r1.font.size = Pt(13)
        r1.font.color.rgb = COLOR_WHITE
        r2 = p.add_run()
        r2.text = b_desc
        r2.font.size = Pt(13)
        r2.font.color.rgb = COLOR_MUTED

    add_card(slide5, Inches(6.9), Inches(1.8), Inches(5.6), Inches(5.0), "SDXL LoRA v1 (Trained Adapter)", COLOR_GOLD)
    tb5_2 = slide5.shapes.add_textbox(Inches(7.15), Inches(2.5), Inches(5.1), Inches(4.0))
    tf5_2 = tb5_2.text_frame
    tf5_2.word_wrap = True
    lora_points = [
        ("Authentic Beton Brut: ", "Synthesizes tactile board-marked timber grain, visible form-tie seams, and bush-hammered aggregate textures."),
        ("Modular Fenestration: ", "Substitutes commercial glass with deeply recessed horizontal ribbon windows, solid precast parapets, and concrete louvers."),
        ("Monumental Shadows: ", "Deep embrasures create crisp, high-contrast geometric cast shadows under raking daylight."),
        ("Cantilevered Tectonics: ", "Aggressively projects heavy upper floor plates and exposed waffle slab soffits without geometric collapse.")
    ]
    for idx, (b_title, b_desc) in enumerate(lora_points):
        p = tf5_2.paragraphs[0] if idx == 0 else tf5_2.add_paragraph()
        p.space_before = Pt(10)
        r1 = p.add_run()
        r1.text = b_title
        r1.font.bold = True
        r1.font.size = Pt(13)
        r1.font.color.rgb = COLOR_GOLD
        r2 = p.add_run()
        r2.text = b_desc
        r2.font.size = Pt(13)
        r2.font.color.rgb = COLOR_WHITE

    # =========================================================================
    # SLIDE 6: STYLE LEAKAGE PROBING
    # =========================================================================
    slide6 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide6)
    add_header(slide6, "Anti-Leakage Probing: Testing Competing Architectural Styles", "06. STYLE ISOLATION AUDIT")

    add_card(slide6, Inches(0.8), Inches(1.8), Inches(11.733), Inches(5.0), "Qualitative Audit Across 8 Competing Movements", COLOR_CYAN)
    tb6 = slide6.shapes.add_textbox(Inches(1.05), Inches(2.5), Inches(11.2), Inches(4.0))
    tf6 = tb6.text_frame
    tf6.word_wrap = True

    leak_table = [
        ("Gothic", "Pointed arches, ribbed vaults, church tracery", "Stark angular roofline, planar concrete; no pointed arches observed", "No obvious leakage"),
        ("Classical & Baroque", "Triangular pediments, Corinthian columns, volutes", "Cantilevered horizontal plates, rectangular piers; no pediments observed", "No obvious leakage"),
        ("Postmodernism", "Pastel cladding, ironic pastiche, split pediments", "Bush-hammered concrete, modular grid, gray palette; no pastels observed", "No obvious leakage"),
        ("Bauhaus / Early Modern", "Thin steel frames, pristine white stucco, light corners", "Thick textured cast-in-place concrete; no thin steel curtain walls observed", "No obvious leakage"),
        ("Commercial Glass", "Continuous reflective curtain walls, mirror glass", "Heavy shear walls dominate; narrow slit windows; no glass towers observed", "No obvious leakage"),
        ("Art Nouveau", "Curvilinear whiplash arches, floral wrought iron", "Heavy rectangular cast concrete canopy portal; no organic curves observed", "No obvious leakage"),
        ("High-Tech Cladding", "Polished marble, slick composite metal panels", "Unfinished gray concrete panels with form-tie holes; no slick finishes observed", "No obvious leakage")
    ]
    for idx, (style, target, obs, verdict) in enumerate(leak_table):
        p = tf6.paragraphs[0] if idx == 0 else tf6.add_paragraph()
        p.space_before = Pt(6)
        r1 = p.add_run()
        r1.text = f"{style:22}: "
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = COLOR_WHITE
        r2 = p.add_run()
        r2.text = f"{obs}  "
        r2.font.size = Pt(12)
        r2.font.color.rgb = COLOR_MUTED
        r3 = p.add_run()
        r3.text = f"[{verdict}]"
        r3.font.bold = True
        r3.font.size = Pt(11)
        r3.font.color.rgb = COLOR_GREEN

    # =========================================================================
    # SLIDE 7: MEMORIZATION & GENERALIZATION
    # =========================================================================
    slide7 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide7)
    add_header(slide7, "Feature-Space Similarity Analysis: Memorization vs. Generalization", "07. RESNET-34 EMBEDDING AUDIT")

    metrics = [
        ("0.7028 ± 0.07", "Train vs. Train Baseline", "Excluding self-similarity diagonal", COLOR_MUTED),
        ("0.6786 ± 0.08", "Generated vs. Train", "Generated samples are more diverse", COLOR_GOLD),
        ("0.6901 ± 0.07", "Generated vs. Held-Out", "Strong alignment with test domain", COLOR_CYAN),
        ("0.8581", "Highest Similarity Trigger", "ARC_0018: novel composition", COLOR_GREEN)
    ]
    for idx, (val, title, desc, col) in enumerate(metrics):
        x = Inches(0.8 + idx * 3.0)
        add_card(slide7, x, Inches(1.8), Inches(2.7), Inches(1.6))
        tb = slide7.shapes.add_textbox(x + Inches(0.15), Inches(1.95), Inches(2.4), Inches(1.3))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = val
        p1.font.size = Pt(20)
        p1.font.bold = True
        p1.font.color.rgb = col
        p2 = tf.add_paragraph()
        p2.text = title
        p2.font.size = Pt(12)
        p2.font.bold = True
        p2.font.color.rgb = COLOR_WHITE
        p2.space_before = Pt(2)
        p3 = tf.add_paragraph()
        p3.text = desc
        p3.font.size = Pt(10)
        p3.font.color.rgb = COLOR_MUTED

    add_card(slide7, Inches(0.8), Inches(3.7), Inches(11.733), Inches(3.1), "Visual Inspection Findings & Generalization Boundaries", COLOR_WHITE)
    tb7 = slide7.shapes.add_textbox(Inches(1.05), Inches(4.3), Inches(11.2), Inches(2.3))
    tf7 = tb7.text_frame
    tf7.word_wrap = True
    mem_findings = [
        ("Corrected Baseline Methodology: ", "Earlier diagonal inclusion inflated baseline to 0.7163; corrected off-diagonal baseline is 0.7028. Generated-to-train similarity (0.6786) is slightly lower, showing healthy diversity."),
        ("Visual Inspection of High-Similarity Pairs: ", "Visual inspection of pairs >= 0.75 (such as lora_eval_03 vs ARC_0018 at 0.8581) did not reveal obvious reproduction of distinctive silhouettes, camera viewpoints, or fenestration patterns. Similarity is driven by shared material and lighting properties. This does not constitute a definitive test for memorization."),
        ("Held-Out Generalization Boundary: ", "The generated samples contain architectural characteristics also present in the held-out Brutalism images (waffle slab soffits, brise-soleil fins). Because base SDXL already possesses broad architectural knowledge and the test set is small (3 images), this observation cannot isolate LoRA-specific generalization.")
    ]
    for idx, (b_title, b_desc) in enumerate(mem_findings):
        p = tf7.paragraphs[0] if idx == 0 else tf7.add_paragraph()
        p.space_before = Pt(8)
        r1 = p.add_run()
        r1.text = b_title
        r1.font.bold = True
        r1.font.size = Pt(13)
        r1.font.color.rgb = COLOR_GOLD if "Inspection" in b_title else COLOR_WHITE
        r2 = p.add_run()
        r2.text = b_desc
        r2.font.size = Pt(13)
        r2.font.color.rgb = COLOR_MUTED

    # =========================================================================
    # SLIDE 8: KEY LIMITATION: CAPTIONS
    # =========================================================================
    slide8 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide8)
    add_header(slide8, "Diagnostic Finding: The Identical Template Caption Bottleneck", "08. CONDITIONING LIMITATION AUDIT")

    add_card(slide8, Inches(0.8), Inches(1.8), Inches(11.733), Inches(5.0), "100% Caption Redundancy Across Training Set", COLOR_GOLD)
    tb8 = slide8.shapes.add_textbox(Inches(1.05), Inches(2.4), Inches(11.2), Inches(4.2))
    tf8 = tb8.text_frame
    tf8.word_wrap = True

    p8_callout = tf8.paragraphs[0]
    p8_callout.text = "THE RUN 1 CAPTION (APPLIED IDENTICALLY TO ALL 22 IMAGES):"
    p8_callout.font.size = Pt(12)
    p8_callout.font.bold = True
    p8_callout.font.color.rgb = COLOR_CYAN

    p8_quote = tf8.add_paragraph()
    p8_quote.text = "\"Brutalist architecture, monolithic raw concrete facade with visible board-marked texture, massive geometric cantilevered volumes, deep-set rectangular window embrasures, bold structural piers, strong geometric shadow patterns, natural daylight, architectural photography\""
    p8_quote.font.size = Pt(13)
    p8_quote.font.italic = True
    p8_quote.font.color.rgb = COLOR_GOLD
    p8_quote.space_before = Pt(4)

    limit_bullets = [
        ("Monolithic Style Collapse: ", "Because text encoders were frozen and all 22 captions were identical, the UNet received an invariant conditioning embedding at every step. It learned a single global style vector rather than individual token-to-feature alignments."),
        ("Token Disentanglement Failure: ", "The model cannot distinguish 'waffle slab' from 'cantilever' or 'brise-soleil'. Prompting for specific tectonic features relies heavily on base SDXL's spatial prior rather than the adapter."),
        ("Factual Material Contradictions: ", "The template claims 'board-marked texture' for smooth precast panel blocks (ARC_0012) and 'window embrasures' for open-air stadium grandstands with no windows (ARC_0008)."),
        ("Key Experimental Insight: ", "Identified the primary conditioning bottleneck through data auditing rather than blindly increasing training steps.")
    ]
    for b_title, b_desc in limit_bullets:
        p = tf8.add_paragraph()
        p.space_before = Pt(8)
        r1 = p.add_run()
        r1.text = b_title
        r1.font.bold = True
        r1.font.size = Pt(13)
        r1.font.color.rgb = COLOR_WHITE
        r2 = p.add_run()
        r2.text = b_desc
        r2.font.size = Pt(13)
        r2.font.color.rgb = COLOR_MUTED

    # =========================================================================
    # SLIDE 9: RUN 2 PROPOSAL (FUTURE WORK / ENHANCEMENT)
    # =========================================================================
    slide9 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide9)
    add_header(slide9, "Future Work & Enhancement: Run 2A Controlled Experiment", "09. HYPOTHESIS-DRIVEN REFINEMENT")

    add_card(slide9, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "Single-Variable Experimental Design", COLOR_GREEN)
    tb9_1 = slide9.shapes.add_textbox(Inches(1.05), Inches(2.5), Inches(5.1), Inches(4.0))
    tf9_1 = tb9_1.text_frame
    tf9_1.word_wrap = True
    exp_bullets = [
        ("The Single-Variable Hypothesis: ", "Holding dataset images, base model, rank, learning rate, and step budget constant, modifying only captions into instance-specific descriptions will improve attribute conditioning."),
        ("Strict Controls Maintained: ", "Same 22 Brutalism images, same SDXL 1.0 + FP16 VAE, same Rank 16 / Alpha 16, same LR (1e-4), same 330 step budget."),
        ("No Confounding Variables: ", "Avoid simultaneously changing text encoder training or trigger tokens; cleanly isolate caption quality as the experimental variable."),
        ("Evaluation Plan: ", "Systematically compare Run 1 vs. Run 2A on attribute disentanglement (waffle slabs, sun louvers, modular balconies).")
    ]
    for idx, (b_title, b_desc) in enumerate(exp_bullets):
        p = tf9_1.paragraphs[0] if idx == 0 else tf9_1.add_paragraph()
        p.space_before = Pt(10)
        r1 = p.add_run()
        r1.text = b_title
        r1.font.bold = True
        r1.font.size = Pt(13)
        r1.font.color.rgb = COLOR_WHITE
        r2 = p.add_run()
        r2.text = b_desc
        r2.font.size = Pt(13)
        r2.font.color.rgb = COLOR_MUTED

    add_card(slide9, Inches(6.9), Inches(1.8), Inches(5.6), Inches(5.0), "9-Attribute Grounded Caption Framework", COLOR_GOLD)
    tb9_2 = slide9.shapes.add_textbox(Inches(7.15), Inches(2.5), Inches(5.1), Inches(4.0))
    tf9_2 = tb9_2.text_frame
    tf9_2.word_wrap = True
    p9_formula = tf9_2.paragraphs[0]
    p9_formula.text = "CAPTION FRAMEWORK DIMENSIONS:"
    p9_formula.font.size = Pt(12)
    p9_formula.font.bold = True
    p9_formula.font.color.rgb = COLOR_CYAN

    dims = [
        "1. Building Typology (Library, Housing Block, Stadium)",
        "2. Primary Massing (Stepped, Monolithic, Tiered)",
        "3. Structural System (Cantilever, Colonnade, Shear Wall)",
        "4. Specific Finish (Board-Marked, Bush-Hammered, Precast)",
        "5. Fenestration (Horizontal Ribbon, Recessed Embrasures)",
        "6. Circulation/Tectonics (Elevated Walkway, Stair Tower)",
        "7. Lighting & Weather (Direct Sunlight, Overcast Diffuse)",
        "8. Viewpoint & Scale (Eye-Level, Low-Angle Street View)",
        "9. Style Anchor (Brutalist Architecture)"
    ]
    for d in dims:
        p = tf9_2.add_paragraph()
        p.space_before = Pt(5)
        p.text = d
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_WHITE

    # =========================================================================
    # SLIDE 10: REPOSITORY & REPRODUCIBILITY
    # =========================================================================
    slide10 = prs.slides.add_slide(blank_layout)
    set_slide_background(slide10)
    add_header(slide10, "Repository & Reproducibility Package", "10. OPEN SCIENCE & DOCUMENTATION")

    add_card(slide10, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0), "Complete Documentation Suite", COLOR_CYAN)
    tb10_1 = slide10.shapes.add_textbox(Inches(1.05), Inches(2.5), Inches(5.1), Inches(4.0))
    tf10_1 = tb10_1.text_frame
    tf10_1.word_wrap = True
    docs = [
        ("PORTFOLIO_CASE_STUDY.md: ", "1–2 page executive project summary."),
        ("README.md: ", "Repository manual indexing every file and quickstart."),
        ("DATASET_CARD.md: ", "Provenance, licenses, exclusions, and splits."),
        ("MODEL_CARD.md: ", "SDXL LoRA adapter card, hyperparameters, limits."),
        ("EVALUATION.md: ", "Complete empirical findings with evidence labels."),
        ("RUN_2_DECISION.md: ", "Decision record and Run 2A experimental design."),
        ("evaluation/caption_audit.md: ", "Conditioning limitation report.")
    ]
    for idx, (b_title, b_desc) in enumerate(docs):
        p = tf10_1.paragraphs[0] if idx == 0 else tf10_1.add_paragraph()
        p.space_before = Pt(8)
        r1 = p.add_run()
        r1.text = b_title
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = COLOR_WHITE
        r2 = p.add_run()
        r2.text = b_desc
        r2.font.size = Pt(12)
        r2.font.color.rgb = COLOR_MUTED

    add_card(slide10, Inches(6.9), Inches(1.8), Inches(5.6), Inches(5.0), "Reproducibility & Execution Artifacts", COLOR_GOLD)
    tb10_2 = slide10.shapes.add_textbox(Inches(7.15), Inches(2.5), Inches(5.1), Inches(4.0))
    tf10_2 = tb10_2.text_frame
    tf10_2.word_wrap = True
    repro = [
        ("requirements.txt & environment.txt: ", "Pinned dependencies and runtime specs."),
        ("training_config.json: ", "Exact training parameters from hparams.yml."),
        ("dataset_manifest.csv: ", "Complete metadata for all 28 Brutalism images."),
        ("scripts/run_memorization_audit.py: ", "Automated ResNet-34 similarity calculator."),
        ("scripts/generate_base_vs_lora_panels.py: ", "Side-by-side comparison generator."),
        ("scripts/run_controlled_evaluation.py: ", "Automated sweep and checkpoint runner."),
        ("colab/brutalism_sdxl_lora_eval.ipynb: ", "1-click Colab evaluation runner.")
    ]
    for idx, (b_title, b_desc) in enumerate(repro):
        p = tf10_2.paragraphs[0] if idx == 0 else tf10_2.add_paragraph()
        p.space_before = Pt(8)
        r1 = p.add_run()
        r1.text = b_title
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = COLOR_WHITE
        r2 = p.add_run()
        r2.text = b_desc
        r2.font.size = Pt(12)
        r2.font.color.rgb = COLOR_MUTED

    out_pptx = "Architectural_Styles_LoRA_Presentation.pptx"
    prs.save(out_pptx)
    print(f"Successfully generated presentation deck: {out_pptx} (11 slides)")

if __name__ == "__main__":
    create_deck()
