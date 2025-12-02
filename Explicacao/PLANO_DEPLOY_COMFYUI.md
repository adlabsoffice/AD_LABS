# 🎮 Plano de Deploy: "O Músculo" (ComfyUI na AWS)

Este é o plano para criar a máquina potente que vai gerar as imagens.
**Você pediu para ver o código antes, então aqui está a lógica do script `deploy_muscle.py`.**

## 1. O que eu tenho de senhas?
Atualmente, no arquivo `.env`, eu tenho:
*   ✅ **AWS:** Suas chaves de acesso (para criar as máquinas).
*   ✅ **Google:** Suas chaves de IA (Gemini, Voz).
*   ❌ **Instagram:** **NÃO TENHO.** Lá está escrito `seu_usuario` e `sua_senha`. Você precisará editar o arquivo `.env` e colocar os verdadeiros quando formos ligar o agente.

---

## 2. O Script de Instalação (`deploy_muscle.py`)

Este script vai fazer o seguinte:
1.  Criar uma máquina **g4dn.xlarge** (NVIDIA T4) na AWS.
2.  Instalar os Drivers da NVIDIA (chatíssimo de fazer na mão).
3.  Instalar o **ComfyUI**.
4.  Configurar para ele ligar e desligar via comando (para economizar).

### 📜 Rascunho do Código (Preview)

```python
# ... imports ...

def launch_muscle_server():
    print("🚀 Criando servidor GPU (g4dn.xlarge)...")
    
    # Script que roda assim que a máquina liga (User Data)
    setup_script = '''#!/bin/bash
    # 1. Instalar Drivers NVIDIA
    sudo apt-get update
    sudo apt-get install -y nvidia-driver-470 cuda-drivers
    
    # 2. Instalar Python e Git
    sudo apt-get install -y python3-pip git

    # 3. Baixar ComfyUI
    git clone https://github.com/comfyanonymous/ComfyUI
    cd ComfyUI
    pip3 install -r requirements.txt
    
    # 4. Baixar Modelos (Checkpoints)
    # (Aqui vamos colocar os links dos modelos Realistas/Pixar que você gosta)
    wget -O models/checkpoints/juggernaut.safetensors https://civitai.com/...
    
    # 5. Iniciar ComfyUI
    python3 main.py --listen 0.0.0.0 --port 8188
    '''

    # Comando para criar a máquina na AWS
    ec2.create_instances(
        InstanceType='g4dn.xlarge', # Custa $0.50/hora
        ImageId='ami-0... (Ubuntu Deep Learning)',
        UserData=setup_script,
        # ...
    )
    print("✅ Máquina Criada! IP: x.x.x.x")
```

## 3. Custo e Segurança
*   **Custo:** Essa máquina gasta os seus créditos. Se ficar ligada 24h, come $12 por dia.
*   **Segurança:** O script vai instalar um "Auto-Shutdown". Se ela ficar 30 minutos sem fazer nada, ela se desliga sozinha.

## 4. Aprovação
Posso transformar esse rascunho no script real `deploy_muscle.py` e executar?
