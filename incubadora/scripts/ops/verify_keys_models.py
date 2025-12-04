import os
import requests
from rich.console import Console
from rich.table import Table

console = Console()

def load_keys():
    keys = {}
    env_path = os.path.join(os.getcwd(), ".env")
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                if "=" in line and not line.startswith("#"):
                    key, value = line.strip().split("=", 1)
                    if key.startswith("GOOGLE_API_KEY"):
                        keys[key] = value
    return keys

def list_models_for_key(key_name, api_key):
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            models = [m['name'].replace('models/', '') for m in data.get('models', [])]
            return True, models
        else:
            return False, f"Error {response.status_code}"
    except Exception as e:
        return False, str(e)

def test_generation(key_name, api_key, model):
    # Simple text generation test
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    payload = {
        "contents": [{"parts": [{"text": "Hello"}]}]
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return True
        else:
            return False
    except:
        return False

def verify_all():
    keys = load_keys()
    
    table = Table(title="Google API Key Verification")
    table.add_column("Key Name", style="cyan")
    table.add_column("Status", style="magenta")
    table.add_column("Available Models (Top 5)", style="green")
    table.add_column("Test Gen", style="yellow")

    for key_name, api_key in keys.items():
        console.print(f"Checking {key_name}...")
        success, result = list_models_for_key(key_name, api_key)
        
        if success:
            models = result
            # Filter relevant models
            relevant_models = [m for m in models if 'gemini' in m or 'imagen' in m]
            display_models = ", ".join(relevant_models[:5]) + ("..." if len(relevant_models) > 5 else "")
            
            # Test generation with a Gemini model if available
            test_model = next((m for m in relevant_models if 'gemini-1.5-flash' in m or 'gemini-pro' in m), None)
            if not test_model and relevant_models: test_model = relevant_models[0]
            
            can_generate = "N/A"
            if test_model and 'imagen' not in test_model: # Skip image gen test for now in this simple loop
                if test_generation(key_name, api_key, test_model):
                    can_generate = f"✅ ({test_model})"
                else:
                    can_generate = f"❌ ({test_model})"
            
            table.add_row(key_name, "✅ Valid", display_models, can_generate)
        else:
            table.add_row(key_name, f"❌ Invalid ({result})", "-", "-")

    console.print(table)

if __name__ == "__main__":
    verify_all()
