import os
import pandas as pd
from PIL import Image, ImageDraw

leak_dir = "evaluation/leakage"
df = pd.read_csv("outputs/brutalism_sdxl_lora_v1/leakage_results.csv")

audit_records = [
    {
        "test_tag": "1. Baseline Test",
        "target_competing_style": "N/A (Style Fidelity Anchor)",
        "observed_motifs": "Massive monolithic raw concrete volumes, deeply recessed rectangular windows, minimal decoration",
        "leakage_observed": "None",
        "qualitative_verdict": "Strong, authentic Brutalist expression without decorative intrusion."
    },
    {
        "test_tag": "2. Anti-Gothic Test",
        "target_competing_style": "Gothic (Pointed arches, ribbed vaults, tracery, buttresses)",
        "observed_motifs": "Sharp angular roofline, planar concrete slabs, stark triangular entrance slot; zero pointed arches or tracery",
        "leakage_observed": "None",
        "qualitative_verdict": "No obvious examples of Gothic pointed arches or ecclesiastic tracery were observed in the generated chapel sample."
    },
    {
        "test_tag": "3. Anti-Classical & Baroque Test",
        "target_competing_style": "Classical & Baroque (Triangular pediments, Corinthian columns, decorative cornices)",
        "observed_motifs": "Massive horizontal cantilevered floor plates, monolithic rectangular piers, deep geometric embrasures; zero pediments",
        "leakage_observed": "None",
        "qualitative_verdict": "No obvious classical pediments, fluted columns, or baroque volutes were observed in the civic palace sample."
    },
    {
        "test_tag": "4. Anti-Postmodern Test",
        "target_competing_style": "Postmodernism (Pastel colors, ornamental arches, ironic classical pastiche, split pediments)",
        "observed_motifs": "Rugged bush-hammered concrete surface, strictly modular rectangular structural grid, neutral gray palette; zero pastels or whimsical motifs",
        "leakage_observed": "None",
        "qualitative_verdict": "No obvious postmodern pastel hues, pediment cutouts, or decorative pastiche motifs were observed."
    },
    {
        "test_tag": "5. Anti-Bauhaus Test",
        "target_competing_style": "Bauhaus / Early Modern (Pristine smooth white stucco, thin steel-framed glass curtain corners)",
        "observed_motifs": "Thick heavy cast-in-place concrete walls with prominent horizontal formwork grain, structural concrete projections; zero light steel/glass lightness",
        "leakage_observed": "None",
        "qualitative_verdict": "No obvious thin-profile steel curtain walls or smooth white rationalist stucco were observed; tectonic mass dominates."
    },
    {
        "test_tag": "6. Anti-Commercial Glass Skyscraper Test",
        "target_competing_style": "Corporate Modernist Glass Curtain Wall (Continuous reflective mirror glazing)",
        "observed_motifs": "Monolithic shear walls dominate exterior facade; narrow vertical slit windows deeply recessed into concrete; zero reflective curtain wall",
        "leakage_observed": "None",
        "qualitative_verdict": "No obvious continuous glass curtain walls or mirror glazing were observed; solid-to-void ratio remains heavily weighted toward solid concrete."
    },
    {
        "test_tag": "7. Anti-Art Nouveau Test",
        "target_competing_style": "Art Nouveau (Curvilinear whiplash arches, floral wrought ironwork, organic asymmetry)",
        "observed_motifs": "Heavy cast concrete canopy forming a stark rectangular portal with sharp rectilinear geometries; zero curvilinear or organic ornamentation",
        "leakage_observed": "None",
        "qualitative_verdict": "No obvious organic or curvilinear whiplash ornamentation was observed in the portal entrance."
    },
    {
        "test_tag": "8. Material Contrast Test",
        "target_competing_style": "High-Tech / Polished Cladding (Composite metal panels, polished marble, painted surfaces)",
        "observed_motifs": "Unfinished matte gray concrete panels with form-tie holes and subtle weathering patina, deeply recessed unglazed openings",
        "leakage_observed": "None",
        "qualitative_verdict": "No obvious polished stone, slick metal cladding, or synthetic finishes were observed; raw concrete material integrity maintained."
    }
]

# Write updated leakage CSV
res_df = pd.DataFrame(audit_records)
res_df["prompt"] = df["prompt"]
res_df["seed"] = df["seed"]
res_df["output_path"] = df["output_path"]

out_csv = "evaluation/leakage_results.csv"
res_df.to_csv(out_csv, index=False)
print(f"Saved qualitative leakage evaluation to {out_csv}")

# Create visual grid: 4 columns x 2 rows (each 500x500)
cols, rows = 4, 2
thumb_w, thumb_h = 450, 450
grid_w = cols * thumb_w + (cols + 1) * 20
grid_h = rows * thumb_h + (rows + 1) * 60 + 50

grid = Image.new("RGB", (grid_w, grid_h), color=(22, 24, 28))
draw = ImageDraw.Draw(grid)
draw.text((20, 20), "SDXL Brutalism LoRA v1 — Style Leakage Probing Analysis (8 Anti-Contamination Tests)", fill=(255, 215, 0))
draw.text((20, 45), "Qualitative evaluation of competing architectural motifs: Gothic, Classical, Baroque, Postmodern, Bauhaus, Commercial Glass, Art Nouveau", fill=(180, 200, 220))

for idx, r in enumerate(audit_records):
    tag = r["test_tag"]
    fpath = os.path.join(leak_dir, f"leakage_test_{idx+1:02d}_{tag}.jpg")
    
    col = idx % cols
    row = idx // cols
    x = 20 + col * (thumb_w + 20)
    y = 80 + row * (thumb_h + 60)

    if os.path.exists(fpath):
        with Image.open(fpath) as im:
            thumb = im.convert("RGB").resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
            grid.paste(thumb, (x, y))

        draw.text((x, y + thumb_h + 5), f"{tag}", fill=(255, 255, 255))
        draw.text((x, y + thumb_h + 22), f"Target: {r['target_competing_style'][:38]}", fill=(255, 180, 180))
        draw.text((x, y + thumb_h + 38), f"Observed: {r['leakage_observed']} Leakage", fill=(160, 255, 160))

out_grid_path = os.path.join(leak_dir, "leakage_summary_grid.jpg")
grid.save(out_grid_path, quality=95)
print(f"Saved leakage summary grid to {out_grid_path}")
