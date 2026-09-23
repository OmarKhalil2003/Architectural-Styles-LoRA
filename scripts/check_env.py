import sys
import os
import torch

print(f"Python version: {sys.version.split()[0]}")
print(f"PyTorch version: {torch.__version__}")
print(f"CUDA availability: {torch.cuda.is_available()}")

if torch.cuda.is_available():
    print(f"GPU name: {torch.cuda.get_device_name(0)}")
    props = torch.cuda.get_device_properties(0)
    print(f"GPU VRAM: {props.total_memory / (1024**3):.2f} GB")
    print(f"CUDA Device Capability: {torch.cuda.get_device_capability(0)}")
else:
    print("GPU name: None (CPU only)")
    print("GPU VRAM: 0 GB")

packages = ["diffusers", "transformers", "peft", "bitsandbytes", "accelerate", "safetensors", "xformers"]
for pkg in packages:
    try:
        mod = __import__(pkg)
        ver = getattr(mod, "__version__", "available")
        print(f"{pkg} version: {ver}")
    except ImportError:
        print(f"{pkg} version: NOT installed")
