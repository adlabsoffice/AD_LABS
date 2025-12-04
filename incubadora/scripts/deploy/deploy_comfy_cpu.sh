#!/bin/bash

# Deploy ComfyUI on Google Cloud VM (CPU Mode)
# Usage: bash deploy_comfy_cpu.sh

echo "🐢 INICIANDO SETUP DO COMFYUI (MODO CPU)..."

# 1. System Updates & Dependencies
echo "📦 Atualizando sistema e instalando dependências..."
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv git libgl1-mesa-glx

# 2. Clone ComfyUI
if [ ! -d "ComfyUI" ]; then
    echo "⬇️ Clonando ComfyUI..."
    git clone https://github.com/comfyanonymous/ComfyUI.git
else
    echo "✅ ComfyUI já existe."
fi

cd ComfyUI

# 3. Virtual Environment
if [ ! -d "venv" ]; then
    echo "🐍 Criando ambiente virtual..."
    python3 -m venv venv
fi

source venv/bin/activate

# 4. Install PyTorch (CPU Version)
echo "🔥 Instalando PyTorch (CPU)..."
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# 5. Install ComfyUI Requirements
echo "📦 Instalando requirements do ComfyUI..."
pip install -r requirements.txt

# 6. Install ComfyUI Manager (Optional but good)
cd custom_nodes
if [ ! -d "ComfyUI-Manager" ]; then
    git clone https://github.com/ltdrdata/ComfyUI-Manager.git
fi
cd ..

# 7. Start ComfyUI
echo "🚀 INICIANDO COMFYUI (CPU)..."
echo "⚠️  Atenção: A geração será lenta. Tenha paciência."
# Listen on 0.0.0.0 to allow external connections (requires Firewall rule)
# Or use SSH Tunneling (Recommended)
python main.py --cpu --listen 0.0.0.0 --port 8188
