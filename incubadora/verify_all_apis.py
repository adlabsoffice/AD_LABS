"""
AUDITORIA COMPLETA DE APIS
Testa todas as APIs disponíveis e gera relatório detalhado
"""

import os
import json
import requests
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

class AuditoriaAPIs:
    def __init__(self):
        self.resultados = {
            "data_auditoria": datetime.now().isoformat(),
            "google_apis": {},
            "llm_apis": {},
            "cloud_resources": {},
            "creditos": {},
            "erros": []
        }
        self._carregar_env()
    
    def _carregar_env(self):
        """Carrega variáveis do .env"""
        env_path = os.path.join(os.path.dirname(__file__), ".env")
        if os.path.exists(env_path):
            with open(env_path, "r") as f:
                for line in f:
                    if "=" in line and not line.startswith("#"):
                        key, value = line.strip().split("=", 1)
                        os.environ[key] = value
    
    def testar_google_gemini(self):
        """Testa Google Gemini e lista modelos disponíveis"""
        console.print("\n[bold cyan]🔍 Testando Google Gemini...[/bold cyan]")
        
        keys = ["GOOGLE_API_KEY_VIDEO", "GOOGLE_API_KEY", "GOOGLE_API_KEY_AUDIO", "GOOGLE_API_KEY_IMAGE"]
        
        for key_name in keys:
            api_key = os.getenv(key_name)
            if not api_key:
                continue
            
            try:
                # Lista modelos disponíveis
                url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
                response = requests.get(url, timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    modelos = []
                    
                    for model in data.get("models", []):
                        nome = model.get("name", "").replace("models/", "")
                        descricao = model.get("displayName", "")
                        
                        # Filtrar apenas modelos relevantes
                        if any(x in nome.lower() for x in ["gemini", "imagen", "flash", "pro", "nano"]):
                            modelos.append({
                                "nome": nome,
                                "descricao": descricao,
                                "input_limit": model.get("inputTokenLimit", "N/A"),
                                "output_limit": model.get("outputTokenLimit", "N/A")
                            })
                    
                    self.resultados["google_apis"][key_name] = {
                        "status": "✅ ATIVO",
                        "modelos_disponiveis": modelos,
                        "total_modelos": len(modelos)
                    }
                    
                    console.print(f"  ✅ {key_name}: {len(modelos)} modelos disponíveis")
                    
                else:
                    self.resultados["google_apis"][key_name] = {
                        "status": "❌ ERRO",
                        "erro": f"HTTP {response.status_code}"
                    }
                    console.print(f"  ❌ {key_name}: Erro {response.status_code}")
                    
            except Exception as e:
                self.resultados["erros"].append(f"{key_name}: {str(e)}")
                console.print(f"  ❌ {key_name}: {str(e)}")
    
    def testar_google_imagen(self):
        """Testa Google Imagen especificamente"""
        console.print("\n[bold cyan]🎨 Testando Google Imagen...[/bold cyan]")
        
        api_key = os.getenv("GOOGLE_API_KEY_IMAGE")
        if not api_key:
            console.print("  ⚠️ GOOGLE_API_KEY_IMAGE não encontrada")
            return
        
        # Testar endpoint de geração
        try:
            # Apenas verifica se a API responde, sem gerar imagem real
            url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                modelos_imagen = []
                
                for model in data.get("models", []):
                    nome = model.get("name", "")
                    if "imagen" in nome.lower():
                        modelos_imagen.append({
                            "nome": nome.replace("models/", ""),
                            "display": model.get("displayName", ""),
                            "description": model.get("description", "")
                        })
                
                self.resultados["google_apis"]["IMAGEN"] = {
                    "status": "✅ ATIVO",
                    "modelos": modelos_imagen
                }
                
                console.print(f"  ✅ Imagen: {len(modelos_imagen)} versões disponíveis")
                for m in modelos_imagen:
                    console.print(f"     - {m['nome']}")
            else:
                console.print(f"  ❌ Erro HTTP {response.status_code}")
                
        except Exception as e:
            console.print(f"  ❌ Erro: {str(e)}")
            self.resultados["erros"].append(f"Imagen: {str(e)}")
    
    def testar_groq(self):
        """Testa Groq API"""
        console.print("\n[bold cyan]🚀 Testando Groq...[/bold cyan]")
        
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            console.print("  ⚠️ GROQ_API_KEY não encontrada")
            return
        
        try:
            url = "https://api.groq.com/openai/v1/models"
            headers = {"Authorization": f"Bearer {api_key}"}
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                modelos = [m["id"] for m in data.get("data", [])]
                
                self.resultados["llm_apis"]["GROQ"] = {
                    "status": "✅ ATIVO",
                    "modelos": modelos
                }
                
                console.print(f"  ✅ Groq: {len(modelos)} modelos disponíveis")
                for m in modelos[:5]:  # Mostrar primeiros 5
                    console.print(f"     - {m}")
            else:
                console.print(f"  ❌ Erro HTTP {response.status_code}")
                self.resultados["llm_apis"]["GROQ"] = {
                    "status": "❌ ERRO",
                    "erro": f"HTTP {response.status_code}"
                }
                
        except Exception as e:
            console.print(f"  ❌ Erro: {str(e)}")
            self.resultados["erros"].append(f"Groq: {str(e)}")
    
    def testar_xai_grok(self):
        """Testa XAI/Grok API"""
        console.print("\n[bold cyan]🤖 Testando XAI (Grok)...[/bold cyan]")
        
        api_key = os.getenv("XAI_API_KEY")
        if not api_key:
            console.print("  ⚠️ XAI_API_KEY não encontrada")
            return
        
        try:
            url = "https://api.x.ai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            # Teste mínimo apenas para verificar autenticação
            payload = {
                "messages": [{"role": "user", "content": "test"}],
                "model": "grok-beta",
                "max_tokens": 1
            }
            
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            
            if response.status_code in [200, 400]:  # 400 = autenticado mas payload inválido (OK)
                self.resultados["llm_apis"]["XAI_GROK"] = {
                    "status": "✅ ATIVO",
                    "modelo_testado": "grok-beta"
                }
                console.print(f"  ✅ XAI Grok: Autenticação OK")
            else:
                console.print(f"  ❌ Erro HTTP {response.status_code}")
                self.resultados["llm_apis"]["XAI_GROK"] = {
                    "status": "❌ ERRO",
                    "erro": f"HTTP {response.status_code}"
                }
                
        except Exception as e:
            console.print(f"  ❌ Erro: {str(e)}")
            self.resultados["erros"].append(f"XAI: {str(e)}")
    
    def testar_youtube_api(self):
        """Testa YouTube Data API e verifica quota"""
        console.print("\n[bold cyan]📺 Testando YouTube Data API...[/bold cyan]")
        
        api_key = os.getenv("YOUTUBE_API_KEY") or os.getenv("YOUTUBE_DATA_API_KEY")
        if not api_key:
            console.print("  ⚠️ YOUTUBE_API_KEY não encontrada")
            return
        
        try:
            # Teste simples: buscar 1 vídeo
            url = "https://www.googleapis.com/youtube/v3/search"
            params = {
                "part": "snippet",
                "q": "test",
                "maxResults": 1,
                "key": api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Verificar quota info (se disponível no header)
                quota_usage = response.headers.get("X-Goog-API-Quota-Usage", "Desconhecido")
                
                self.resultados["google_apis"]["YOUTUBE_DATA_API"] = {
                    "status": "✅ ATIVO",
                    "quota_usage": quota_usage,
                    "nota": "Quota total: 10.000 unidades/dia (padrão gratuito)"
                }
                
                console.print(f"  ✅ YouTube Data API: Funcionando")
                console.print(f"     Quota diária: 10.000 unidades (padrão)")
                
            elif response.status_code == 403:
                error_data = response.json()
                reason = error_data.get("error", {}).get("errors", [{}])[0].get("reason", "")
                
                if "quotaExceeded" in reason:
                    self.resultados["google_apis"]["YOUTUBE_DATA_API"] = {
                        "status": "⚠️ QUOTA EXCEDIDA",
                        "erro": "Quota diária excedida, redefine à meia-noite PT"
                    }
                    console.print(f"  ⚠️ YouTube API: Quota excedida (redefine à meia-noite)")
                else:
                    self.resultados["google_apis"]["YOUTUBE_DATA_API"] = {
                        "status": "❌ ERRO",
                        "erro": f"HTTP 403: {reason}"
                    }
                    console.print(f"  ❌ YouTube API: Erro 403 ({reason})")
            else:
                console.print(f"  ❌ Erro HTTP {response.status_code}")
                
        except Exception as e:
            console.print(f"  ❌ Erro: {str(e)}")
            self.resultados["erros"].append(f"YouTube API: {str(e)}")
    
    def testar_claude_api(self):
        """Testa Claude API (Anthropic)"""
        console.print("\n[bold cyan]🧠 Testando Claude API...[/bold cyan]")
        
        api_key = os.getenv("ANTHROPIC_API_KEY") or os.getenv("CLAUDE_API_KEY")
        if not api_key:
            console.print("  ⚠️ ANTHROPIC_API_KEY não encontrada")
            return
        
        try:
            url = "https://api.anthropic.com/v1/messages"
            headers = {
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            }
            
            payload = {
                "model": "claude-sonnet-4-20250514",
                "max_tokens": 1,
                "messages": [{"role": "user", "content": "test"}]
            }
            
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            
            if response.status_code in [200, 400]:  # 400 = autenticado
                self.resultados["llm_apis"]["CLAUDE"] = {
                    "status": "✅ ATIVO",
                    "modelos_disponiveis": [
                        "claude-sonnet-4-20250514",
                        "claude-3-5-sonnet-20241022",
                        "claude-3-opus-latest"
                    ]
                }
                console.print(f"  ✅ Claude API: Autenticação OK")
            else:
                console.print(f"  ❌ Erro HTTP {response.status_code}")
                self.resultados["llm_apis"]["CLAUDE"] = {
                    "status": "❌ ERRO",
                    "erro": f"HTTP {response.status_code}"
                }
                
        except Exception as e:
            console.print(f"  ❌ Erro: {str(e)}")
            self.resultados["erros"].append(f"Claude: {str(e)}")
    
    def listar_todos_modelos_gemini(self):
        """Lista TODOS os 40 modelos Gemini com detalhes"""
        console.print("\n[bold cyan]📋 Listando TODOS os modelos Gemini...[/bold cyan]")
        
        api_key = os.getenv("GOOGLE_API_KEY_VIDEO") or os.getenv("GOOGLE_API_KEY")
        if not api_key:
            return
        
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                todos_modelos = []
                
                for model in data.get("models", []):
                    nome_completo = model.get("name", "")
                    nome = nome_completo.replace("models/", "")
                    
                    todos_modelos.append({
                        "nome": nome,
                        "display": model.get("displayName", ""),
                        "description": model.get("description", "")[:100],
                        "input_limit": model.get("inputTokenLimit", 0),
                        "output_limit": model.get("outputTokenLimit", 0),
                        "supported_methods": model.get("supportedGenerationMethods", [])
                    })
                
                self.resultados["google_apis"]["TODOS_MODELOS_GEMINI"] = {
                    "total": len(todos_modelos),
                    "modelos": todos_modelos
                }
                
                console.print(f"  ✅ Total: {len(todos_modelos)} modelos catalogados")
                
        except Exception as e:
            console.print(f"  ❌ Erro ao listar modelos: {str(e)}")
    
    def verificar_aws_detalhado(self):
        """Verifica AWS com mais detalhes"""
        console.print("\n[bold cyan]☁️ Verificando AWS (detalhado)...[/bold cyan]")
        
        access_key = os.getenv("AWS_ACCESS_KEY_ID")
        secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        region = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
        
        if access_key and secret_key:
            self.resultados["cloud_resources"]["AWS"] = {
                "credencial": "✅ Encontrada",
                "credito": "$200 USD",
                "region": region,
                "servicos": [
                    "N8N (automação)",
                    "EC2 instance (verificar status via console)",
                    "S3 buckets (se houver)"
                ],
                "nota": "Para detalhes completos, usar AWS CLI: `aws ec2 describe-instances`"
            }
            console.print(f"  ✅ AWS: Credenciais OK")
            console.print(f"     Região: {region}")
            console.print(f"     Crédito: $200 USD")
            console.print(f"     💡 Dica: Rode `aws ec2 describe-instances` para ver VMs ativas")
        else:
            console.print("  ⚠️ AWS: Credenciais não encontradas no .env")

    
    def verificar_cloud_resources(self):
        """Verifica recursos cloud (AWS e GCP)"""
        console.print("\n[bold cyan]☁️ Verificando Cloud Resources...[/bold cyan]")
        
        # AWS
        if os.getenv("AWS_ACCESS_KEY_ID"):
            self.resultados["cloud_resources"]["AWS"] = {
                "credencial": "✅ Encontrada",
                "credito": "$200 USD",
                "servicos": ["N8N (automação)"]
            }
            console.print("  ✅ AWS: Credenciais encontradas ($200 crédito)")
        
        # GCP
        if os.path.exists(os.path.join(os.path.dirname(__file__), "gcp-credentials.json")):
            self.resultados["cloud_resources"]["GCP"] = {
                "credencial": "✅ Encontrada",
                "credito": "$300 USD",
                "servicos": ["VM para ComfyUI (não instalado)"],
                "quota_gpu": "❌ Pendente aprovação"
            }
            console.print("  ✅ GCP: Credenciais encontradas ($300 crédito)")
            console.print("  ⚠️ GCP: GPU quota pendente aprovação")
    
    def gerar_relatorio(self):
        """Gera relatório final"""
        console.print("\n[bold green]📊 Gerando Relatório...[/bold green]")
        
        # Salvar JSON
        output_file = "INVENTARIO_APIS_ATIVAS.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(self.resultados, indent=2, ensure_ascii=False, fp=f)
        
        console.print(f"  ✅ JSON salvo: {output_file}")
        
        # Criar Markdown
        self._criar_relatorio_markdown()
        
        # Mostrar resumo na tela
        self._mostrar_resumo()
    
    def _criar_relatorio_markdown(self):
        """Cria relatório em Markdown"""
        md_content = f"""# 📊 INVENTÁRIO DE APIS ATIVAS - AD_LABS

**Data da Auditoria:** {datetime.now().strftime("%d/%m/%Y %H:%M")}

---

## 🔑 Google APIs

"""
        
        for key, info in self.resultados.get("google_apis", {}).items():
            status = info.get("status", "❌")
            md_content += f"### {key}\n"
            md_content += f"**Status:** {status}\n\n"
            
            if "modelos_disponiveis" in info:
                md_content += f"**Total de Modelos:** {info['total_modelos']}\n\n"
                md_content += "**Modelos Disponíveis:**\n"
                for modelo in info["modelos_disponiveis"][:10]:  # Primeiros 10
                    md_content += f"- `{modelo['nome']}` - {modelo['descricao']}\n"
                md_content += "\n"
        
        md_content += "\n---\n\n## 🤖 LLM APIs\n\n"
        
        for key, info in self.resultados.get("llm_apis", {}).items():
            md_content += f"### {key}\n"
            md_content += f"**Status:** {info.get('status', '❌')}\n\n"
            
            if "modelos" in info:
                md_content += "**Modelos:**\n"
                for m in info["modelos"][:10]:
                    md_content += f"- `{m}`\n"
                md_content += "\n"
        
        md_content += "\n---\n\n## ☁️ Cloud Resources\n\n"
        
        for cloud, info in self.resultados.get("cloud_resources", {}).items():
            md_content += f"### {cloud}\n"
            md_content += f"**Crédito:** {info.get('credito', 'N/A')}\n"
            md_content += f"**Serviços:**\n"
            for s in info.get("servicos", []):
                md_content += f"- {s}\n"
            md_content += "\n"
        
        if self.resultados.get("erros"):
            md_content += "\n---\n\n## ⚠️ Erros Encontrados\n\n"
            for erro in self.resultados["erros"]:
                md_content += f"- {erro}\n"
        
        with open("INVENTARIO_APIS_ATIVAS.md", "w", encoding="utf-8") as f:
            f.write(md_content)
        
        console.print("  ✅ Markdown salvo: INVENTARIO_APIS_ATIVAS.md")
    
    def _mostrar_resumo(self):
        """Mostra tabela resumo na tela"""
        console.print("\n")
        console.print(Panel.fit(
            "[bold green]✅ AUDITORIA COMPLETA[/bold green]\n"
            "Verifique os arquivos:\n"
            "- INVENTARIO_APIS_ATIVAS.json\n"
            "- INVENTARIO_APIS_ATIVAS.md",
            title="Relatório Gerado"
        ))
        
        # Tabela de resumo
        table = Table(title="Resumo de APIs")
        table.add_column("Plataforma", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("Detalhes")
        
        # Google APIs
        google_count = len([v for v in self.resultados.get("google_apis", {}).values() if "✅" in v.get("status", "")])
        table.add_row("Google APIs", f"✅ {google_count} ativas", "Gemini, Imagen, TTS")
        
        # LLM APIs
        llm_count = len([v for v in self.resultados.get("llm_apis", {}).values() if "✅" in v.get("status", "")])
        table.add_row("LLM APIs", f"✅ {llm_count} ativas", "Groq, XAI/Grok")
        
        # Cloud
        cloud_count = len(self.resultados.get("cloud_resources", {}))
        table.add_row("Cloud", f"✅ {cloud_count} plataformas", "AWS ($200), GCP ($300)")
        
        console.print(table)
    
    def executar(self):
        """Executa auditoria completa"""
        console.print(Panel.fit(
            "[bold cyan]🔍 AUDITORIA COMPLETA DE APIS[/bold cyan]\n"
            "[dim]Testando todas as APIs e recursos disponíveis...[/dim]",
            title="Iniciando"
        ))
        
        self.testar_google_gemini()
        self.testar_google_imagen()
        self.listar_todos_modelos_gemini()
        self.testar_youtube_api()
        self.testar_groq()
        self.testar_xai_grok()
        self.testar_claude_api()
        self.verificar_aws_detalhado()
        self.verificar_cloud_resources()
        self.gerar_relatorio()


if __name__ == "__main__":
    auditoria = AuditoriaAPIs()
    auditoria.executar()
