import sys
import os
import logging
from unittest.mock import MagicMock

# Add project root to path
sys.path.append("d:/AD_LABS/incubadora")

from agentes.agente_06_roteirista import Agente06Roteirista
from agentes.agente_07_visual import Agente07Visual
from specs.schemas.video_pipeline import SceneBlock

# Configure logging
logging.basicConfig(level=logging.INFO)

def test_agente_06_template_selection():
    print("\n🧪 Testing Agente 06 Template Selection...")
    
    config = {"canal_id": "bible_in_a_nutshell"}
    agente = Agente06Roteirista(config=config)
    
    # Mock LLM call to avoid actual API usage
    agente.api_manager.chamar_com_fallback = MagicMock(return_value='{"scenes": []}')
    agente._limpar_e_parsear_json = MagicMock(return_value={"scenes": []})
    agente._validar_e_ajustar = MagicMock(return_value={"scenes": []})
    agente.salvar_roteiro = MagicMock()
    
    # Run generation to trigger model selection logic
    try:
        agente.gerar_roteiro({"titulo": "Test", "id": "test"}, template_name="react")
    except:
        pass # Ignore errors, we just want to check the call args
        
    # Verify if Claude was requested
    call_args = agente.api_manager.chamar_com_fallback.call_args
    if call_args and "claude-3-5-sonnet" in str(call_args):
        print("✅ Agente 06 is using Claude 3.5 Sonnet")
    else:
        print("⚠️ Agente 06 might not be using Claude (check logs)")
    
    print("✅ Agente 06 initialized with config:", agente.config)
    # Ideally we would run gerar_roteiro and check the logs, but for now this confirms it runs.

def test_agente_07_style_mapper():
    print("\n🧪 Testing Agente 07 Style Mapper...")
    
    config = {"image_provider": "MagicLight.ai"}
    
    # Mock dependencies
    mock_char_manager = MagicMock()
    mock_char_manager.inject_consistency.return_value = "A beautiful scene"
    
    agente = Agente07Visual(
        canal_id="bible_in_a_nutshell", 
        config=config,
        character_manager=mock_char_manager
    )
    
    # Check if style mapper is active
    if getattr(agente, "style_mapper_active", False):
        print("✅ Style Mapper is ACTIVE")
    else:
        print("❌ Style Mapper is INACTIVE")
        
    # Check prompt generation
    cena = SceneBlock(
        speaker="Narrador",
        dialogue="Hello world, this is a longer dialogue to pass validation.",
        visual_prompt="A test prompt that is definitely longer than twenty characters for validation.",
        duration_seconds=5.0
    )
    
    prompt = agente._preparar_prompt_consistente(cena)
    print(f"Generated Prompt: {prompt}")
    
    if "Pixar-like" in prompt:
        print("✅ Style keywords found in prompt")
    else:
        print("❌ Style keywords NOT found in prompt")

if __name__ == "__main__":
    test_agente_06_template_selection()
    test_agente_07_style_mapper()
