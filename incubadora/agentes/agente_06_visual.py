import os
import time
import json
import requests
from rich.console import Console

console = Console()

class Agente06Visual:
    def __init__(self):
        self._load_env()
        self.api_key = os.getenv("GOOGLE_API_KEY_IMAGE")
        
        # Validar que pelo menos uma API está configurada
        comfyui_url = os.getenv("COMFYUI_URL")
        if not self.api_key and not comfyui_url:
            raise ValueError(
                "ERRO CRÍTICO: Nenhuma API de imagem configurada!\n"
                "Configure pelo menos uma das opções:\n"
                "  - GOOGLE_API_KEY_IMAGE (Imagen 4.0)\n"
                "  - COMFYUI_URL (ComfyUI local/remoto)\n"
                "Adicione as credenciais no arquivo .env"
            )
        
        # Endpoint para Imagen via Generative Language API (Beta)
        self.api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro-vision:generateContent" 
        self.output_dir = os.path.join(os.getcwd(), "output", "images")
        
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def _load_env(self):
        """Carrega variáveis do .env manualmente."""
        env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
        if os.path.exists(env_path):
            with open(env_path, "r") as f:
                for line in f:
                    if "=" in line and not line.startswith("#"):
                        key, value = line.strip().split("=", 1)
                        os.environ[key] = value

    def gerar_visuais(self, roteiro, config={}):
        """
        Gera imagens para cada bloco do roteiro.
        """
        provider = config.get("provider_imagens", "Google Imagen")
        console.print(f"[bold yellow]AGENTE 06: Iniciando Geracao Visual ({provider})...[/bold yellow]")
        
        imagens_geradas = []

        for i, bloco in enumerate(roteiro if isinstance(roteiro, list) else roteiro.get("blocos", [])):
            descricao_visual = bloco.get("visual", "")
            if not descricao_visual:
                continue

            # Engenharia de Prompt para Estilo Pixar
            prompt_final = self._otimizar_prompt(descricao_visual)
            
            console.print(f"   [cyan]Bloco {i+1}:[/cyan] \"{descricao_visual[:30]}...\"")
            console.print(f"      -> [dim]Prompt: {prompt_final[:50]}...[/dim]")
            
            # Decisão de Provider
            caminho_imagem = None
            if "ComfyUI" in provider:
                caminho_imagem = self._chamar_comfyui(prompt_final, i)
            else:
                caminho_imagem = self._chamar_api_imagem(prompt_final, i)
            
            if caminho_imagem:
                console.print(f"      -> [green]Imagem Salva:[/green] {os.path.basename(caminho_imagem)}")
                imagens_geradas.append({
                    "bloco_id": i,
                    "prompt": prompt_final,
                    "arquivo": caminho_imagem
                })
            else:
                # ERRO FATAL - Sem fallback para mock
                console.print(f"      -> [bold red]ERRO FATAL: Falha na geração da imagem![/bold red]")
                console.print(f"      -> [yellow]Bloco {i+1}: \"{descricao_visual[:50]}...\"[/yellow]")
                console.print(f"      -> [yellow]Verifique suas credenciais de API ou configure ComfyUI[/yellow]")
                console.print(f"      -> [dim]APIs disponíveis:[/dim]")
                if self.api_key:
                    console.print(f"         - Google Imagen 4.0 (configurada)")
                if os.getenv("COMFYUI_URL"):
                    console.print(f"         - ComfyUI em {os.getenv('COMFYUI_URL')}")
                
                raise RuntimeError(
                    f"Imagem do bloco {i} não pôde ser gerada.\n"
                    f"Prompt: {prompt_final}\n"
                    f"Verifique configuração no .env:\n"
                    f"  - GOOGLE_API_KEY_IMAGE\n"
                    f"  - COMFYUI_URL"
                )
            
            time.sleep(2) 

        return imagens_geradas

    def gerar_thumbnail(self, packaging):
        """
        Gera a thumbnail do vídeo seguindo as regras do Top 100.
        """
        console.print(f"[bold yellow]AGENTE 06: Gerando Thumbnail (Top 100 Strategy)...[/bold yellow]")
        
        titulo = packaging.get('titulo_hook', '')
        conceito = packaging.get('thumbnail_concept', '')
        
        # Engenharia de Prompt Específica para Thumbnails (Arquivo 11)
        prompt_thumb = self._otimizar_prompt_thumbnail(conceito, titulo)
        
        console.print(f"      -> [dim]Prompt Thumb: {prompt_thumb[:50]}...[/dim]")
        
        # Usa o mesmo provider configurado
        # Se estiver usando ComfyUI, usa ele também para a thumb
        if "ComfyUI" in self.config.get("provider_imagens", ""):
            caminho_thumb = self._chamar_comfyui(prompt_thumb, 999)
        else:
            caminho_thumb = self._chamar_api_imagem(prompt_thumb, 999)
        
        if not caminho_thumb:
            # ERRO FATAL - Sem fallback
            raise RuntimeError(
                "Thumbnail não pôde ser gerada.\n"
                f"Conceito: {conceito}\n"
                "Verifique configuração das APIs de imagem no .env"
            )
             
        console.print(f"      -> [green]Thumbnail Salva:[/green] {os.path.basename(caminho_thumb)}")
        return caminho_thumb

    def _otimizar_prompt_thumbnail(self, conceito, titulo):
        """
        Aplica as Regras de Ouro de Thumbnails (Cores, Rostos, Contraste).
        """
        # Regras do Arquivo 11 (Top 100 Analysis)
        estilo_thumb = (
            "YouTube Thumbnail style, 8k resolution, high contrast, "
            "hyper-realistic face close-up (90% rule), "
            "vibrant colors (Red, White, Black/Dark Gray background), "
            "expressive emotion, 'Show don't tell' visual storytelling, "
            "clean composition, rule of thirds"
        )
        
        # Se o conceito não mencionar rosto, forçamos (91.3% dos virais têm rosto)
        if "rosto" not in conceito.lower() and "face" not in conceito.lower():
            estilo_thumb += ", with a shocked or intrigued human face in foreground"
            
        return f"{estilo_thumb}, {conceito}, text overlay: '{titulo}'"

    def _otimizar_prompt(self, descricao_base):
        """
        Adiciona modificadores de estilo Pixar/Disney 3D.
        """
        estilo = "Pixar style, 3d render, disney animation style, 8k, vibrant lighting, cute, expressive characters, high detail, unreal engine 5 render"
        return f"{estilo}, {descricao_base}"

    def _chamar_comfyui(self, prompt, index):
        """
        Chama a API do ComfyUI (Local ou Remoto).
        """
        # URL do ComfyUI (Pode ser parametrizado no .env)
        comfy_url = os.getenv("COMFYUI_URL", "http://127.0.0.1:8188")
        
        console.print(f"      -> [yellow]Enviando para ComfyUI ({comfy_url})... Aguarde.[/yellow]")
        
        try:
            # 1. Solicitar Geração (Queue Prompt)
            # Payload simplificado para Text-to-Image (SDXL)
            # Em produção, carregaria um workflow.json completo
            prompt_id = self._queue_prompt(comfy_url, prompt)
            
            if not prompt_id:
                console.print(f"      -> [red]Erro: ComfyUI não retornou imagem[/red]")
                return None

            # 2. Aguardar e Baixar Imagem
            image_data = self._get_image(comfy_url, prompt_id)
            
            if image_data:
                filename = f"scene_{index:03d}.png"
                filepath = os.path.join(self.output_dir, filename)
                with open(filepath, "wb") as f:
                    f.write(image_data)
                return filepath
            else:
                console.print(f"      -> [red]Erro: ComfyUI não retornou imagem[/red]")
                return None

        except Exception as e:
            console.print(f"      -> [red]Erro Conexão ComfyUI: {e}[/red]")
            return None

    def _queue_prompt(self, url, prompt_text):
        """Envia o workflow para a fila do ComfyUI."""
        try:
            # Carregar workflow template
            workflow_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "workflow_api.json")
            with open(workflow_path, "r", encoding="utf-8") as f:
                workflow = json.load(f)

            # Injetar Prompt (Node 6 é o Positive Prompt no padrão SD1.5)
            # Se o workflow mudar, esse ID precisa ser atualizado
            if "6" in workflow and "inputs" in workflow["6"]:
                workflow["6"]["inputs"]["text"] = prompt_text
            
            # Seed Aleatória
            if "3" in workflow and "inputs" in workflow["3"]:
                import random
                workflow["3"]["inputs"]["seed"] = random.randint(1, 9999999999)

            # Enviar para API
            p = {"prompt": workflow}
            data = json.dumps(p).encode('utf-8')
            
            # Ajuste URL para endpoint de prompt
            if url.endswith("/"):
                api_url = f"{url}prompt"
            else:
                api_url = f"{url}/prompt"

            import urllib.request
            req = urllib.request.Request(api_url, data=data)
            with urllib.request.urlopen(req) as response:
                return json.loads(response.read())

        except Exception as e:
            console.print(f"[red]Erro ao enfileirar no ComfyUI: {e}[/red]")
            return None

    def _get_image(self, url, prompt_response):
        """Aguarda e baixa a imagem gerada."""
        try:
            prompt_id = prompt_response['prompt_id']
            
            # Polling do histórico
            if url.endswith("/"):
                history_url = f"{url}history/{prompt_id}"
            else:
                history_url = f"{url}/history/{prompt_id}"

            import urllib.request
            import time

            console.print(f"      -> [yellow]Aguardando renderização (ID: {prompt_id})...[/yellow]")
            
            # Tenta por 10 minutos (CPU é lenta)
            for _ in range(60): 
                with urllib.request.urlopen(history_url) as response:
                    history = json.loads(response.read())
                
                if prompt_id in history:
                    # Sucesso! Pegar nome do arquivo
                    outputs = history[prompt_id]['outputs']
                    for node_id in outputs:
                        node_output = outputs[node_id]
                        if 'images' in node_output:
                            image_info = node_output['images'][0]
                            filename = image_info['filename']
                            subfolder = image_info['subfolder']
                            folder_type = image_info['type']
                            
                            # Baixar Imagem
                            data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
                            url_values = urllib.parse.urlencode(data)
                            
                            if url.endswith("/"):
                                view_url = f"{url}view?{url_values}"
                            else:
                                view_url = f"{url}/view?{url_values}"
                                
                            with urllib.request.urlopen(view_url) as img_response:
                                return img_response.read()
                
                time.sleep(10) # Espera 10s entre checks
            
            return None

        except Exception as e:
            console.print(f"[red]Erro ao baixar imagem: {e}[/red]")
            return None

    def _chamar_api_imagem(self, prompt, index):
        """
        Tenta chamar a API do Google (Imagen 3 via Generative Language API).
        """
        if not self.api_key:
            return None

        allow_premium = True

        # Endpoint para Imagen 4.0 (Preview)
        url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-4.0-generate-preview-06-06:predict?key={self.api_key}"
        
        headers = {
            "Content-Type": "application/json"
        }
        
        payload = {
            "instances": [
                {
                    "prompt": prompt
                }
            ],
            "parameters": {
                "sampleCount": 1,
                "aspectRatio": "16:9"
            }
        }

        try:
            response = requests.post(url, headers=headers, json=payload)
            
            if response.status_code == 200:
                data = response.json()
                if "predictions" in data and len(data["predictions"]) > 0:
                    b64_image = data["predictions"][0].get("bytesBase64Encoded")
                    if b64_image:
                        import base64
                        image_data = base64.b64decode(b64_image)
                        
                        filename = f"scene_{index:03d}.png"
                        filepath = os.path.join(self.output_dir, filename)
                        
                        with open(filepath, "wb") as f:
                            f.write(image_data)
                        
                        return filepath
            
            console.print(f"      -> [dim]Erro API Google ({response.status_code}): {response.text[:100]}...[/dim]")
            return None

        except Exception as e:
            console.print(f"      -> [red]Erro Conexão Google: {e}[/red]")
            return None


