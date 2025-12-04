"""
Gerenciador de APIs com sistema de fallback robusto.
"""

)

# Carrega env vars
load_dotenv()
console = Console()

class APIManager:
    """
    Gerencia chamadas de API com fallback em 2 níveis:
    1. Entre chaves do mesmo provider (ex: múltiplas contas Google)
    2. Entre providers diferentes (ex: Gemini -> Groq -> Claude)
    """
    
    def __init__(self):
        self.config_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "config",
            "api_priorities.json"
        )
        self.config = self._load_config()
        self.stats = {
            "chamadas_total": 0,
            "sucessos": 0,
            "falhas": 0,
            "uso_por_provider": {}
        }
        
    def _load_config(self) -> Dict:
        """Carrega configuração de prioridades."""
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Config não encontrada: {self.config_path}")
            
        with open(self.config_path, "r", encoding="utf-8") as f:
            return json.load(f)
            
    def _get_api_key(self, key_name: str) -> str:
        """Recupera chave do .env."""
        key = os.getenv(key_name)
        if not key:
            # Não levanta erro aqui, apenas retorna None para pular esta chave
            return None
        return key

    def chamar_com_fallback(self, tipo_servico: str, func_execucao, *args, **kwargs) -> Any:
        """
        Método principal de execução com fallback.
        
        Args:
            tipo_servico: 'llm_roteiro', 'imagem', 'audio_tts'
            func_execucao: Função que faz a chamada real (recebe api_key e modelo)
            *args, **kwargs: Argumentos para func_execucao
            
        Returns:
            Resultado da chamada
            
        Raises:
            AllAPIsFailed: Se todas tentativas falharem
        """
        if tipo_servico not in self.config:
            raise ValueError(f"Tipo de serviço desconhecido: {tipo_servico}")
            
        providers = sorted(
            self.config[tipo_servico]["providers"], 
            key=lambda x: x["prioridade"]
        )
        
        erros_acumulados = []
        
        for provider in providers:
            provider_tipo = provider["tipo"]
            modelos = provider["modelos"]
            keys = provider["keys"]
            
            # Tenta cada chave disponível para este provider
            for key_name in keys:
                api_key = self._get_api_key(key_name)
                if not api_key:
                    continue
                    
                # Tenta cada modelo (se houver lista)
                modelo_atual = modelos[0] # Por enquanto pega o primeiro, poderia iterar
                
                try:
                    console.print(f"[dim]Tentando {provider_tipo} ({modelo_atual}) com key {key_name}...[/dim]")
                    
                    # Executa a função passada
                    resultado = func_execucao(
                        api_key=api_key,
                        modelo=modelo_atual,
                        *args, 
                        **kwargs
                    )
                    
                    # Sucesso!
                    self._registrar_sucesso(provider_tipo, modelo_atual)
                    return resultado
                    
                except Exception as e:
                    erro_msg = str(e)
                    console.print(f"[yellow]⚠ Falha em {provider_tipo}/{key_name}: {erro_msg}[/yellow]")
                    erros_acumulados.append(f"{provider_tipo}/{key_name}: {erro_msg}")
                    self._registrar_falha(provider_tipo)
                    
                    # Se for erro de cota (429), continua para próxima key
                    if "429" in erro_msg or "quota" in erro_msg.lower():
                        continue
                    # Se for erro de auth, continua
                    if "401" in erro_msg or "403" in erro_msg:
                        continue
                        
        # Se chegou aqui, tudo falhou
        raise AllAPIsFailed(f"Todas APIs falharam. Erros: {'; '.join(erros_acumulados)}")

    def _registrar_sucesso(self, provider: str, modelo: str):
        """Registra estatísticas de sucesso."""
        self.stats["chamadas_total"] += 1
        self.stats["sucessos"] += 1
        
        key = f"{provider}:{modelo}"
        if key not in self.stats["uso_por_provider"]:
            self.stats["uso_por_provider"][key] = 0
        self.stats["uso_por_provider"][key] += 1

    def _registrar_falha(self, provider: str):
        """Registra estatísticas de falha."""
        self.stats["falhas"] += 1

    def gerar_relatorio(self):
        """Imprime relatório de uso."""
        console.print(Panel.fit(
            json.dumps(self.stats, indent=2),
            title="Relatório de Uso de APIs"
        ))
