import nbformat as nbf

nb = nbf.v4.new_notebook()
cells = []

# Title
cells.append(nbf.v4.new_markdown_cell("""# Brutalism SDXL LoRA — Controlled Evaluation Suite
This notebook performs the controlled evaluation suite for the **Brutalism SDXL LoRA Pilot (Run 1)**:
1. **Neutral Prompt & LoRA Weight Sweep**: Tests style induction when Brutalism is not explicitly prompted across weights [0.0, 0.25, 0.50, 0.75, 1.00].
2. **Base vs. LoRA Style Leakage Testing**: Generates Base SDXL versions of the 8 anti-leakage prompts and constructs side-by-side comparison panels.
3. **Multi-Checkpoint Comparison**: Directly compares Base SDXL vs Checkpoint-110 vs Checkpoint-220 vs Checkpoint-330 on identical prompts/seeds.
"""))

# Mount Drive
cells.append(nbf.v4.new_markdown_cell("## 1. Mount Google Drive"))
cells.append(nbf.v4.new_code_cell("""from google.colab import drive
import os
drive.mount('/content/drive')
PROJECT_ROOT = '/content/drive/MyDrive/Architectural-Styles-LoRA'
os.chdir(PROJECT_ROOT)
print(f'Working directory: {os.getcwd()}')
"""))

# Dependencies
cells.append(nbf.v4.new_markdown_cell("## 2. Install Pinned Dependencies"))
cells.append(nbf.v4.new_code_cell("""!pip install -q \\
    "torch>=2.1.0" \\
    "torchvision>=0.16.0" \\
    "diffusers>=0.30.0" \\
    "transformers>=4.44.0" \\
    "accelerate>=0.33.0" \\
    "peft>=0.12.0" \\
    "safetensors>=0.4.0" \\
    "pandas" "pillow"
"""))

# Run evaluation suite
cells.append(nbf.v4.new_markdown_cell("## 3. Execute Controlled Evaluation Suite"))
cells.append(nbf.v4.new_code_cell("""!python scripts/run_controlled_evaluation.py --all
"""))

# Visualize
cells.append(nbf.v4.new_markdown_cell("## 4. Visualize Generated Grids"))
cells.append(nbf.v4.new_code_cell("""from PIL import Image
import matplotlib.pyplot as plt
import glob

grids = sorted(glob.glob('evaluation/weight_sweep/grid_*.jpg') + glob.glob('evaluation/checkpoint_comparison/grid_*.jpg'))
for g in grids:
    print(f'Showing {g}:')
    img = Image.open(g)
    plt.figure(figsize=(16, 5))
    plt.imshow(img)
    plt.axis('off')
    plt.show()
"""))

nb['cells'] = cells
with open('colab/brutalism_sdxl_lora_eval.ipynb', 'w', encoding='utf-8') as f:
    nbf.write(nb, f)
print('Successfully created colab/brutalism_sdxl_lora_eval.ipynb')
