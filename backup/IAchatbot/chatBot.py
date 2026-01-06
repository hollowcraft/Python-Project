import requests
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.style import Style

# Configuration de l'API Ollama
OLLAMA_API_URL = "http://localhost:11434/api/generate"  # URL de l'API Ollama
MODEL_NAME = "benevolentjoker/nsfwvanessa"  # Nom du modèle uniquement

# Initialisation de la console Rich
console = Console()

def get_ai_response(prompt):
    """Fonction pour interagir avec l'API Ollama et récupérer la réponse du modèle d'IA."""
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False  # Vous pouvez activer le streaming si vous voulez des réponses en temps réel
    }
    
    try:
        response = requests.post(OLLAMA_API_URL, json=payload)
        response.raise_for_status()
        return response.json()["response"]
    except requests.exceptions.RequestException as e:
        console.print(f"[red]Erreur lors de la requête à l'API Ollama: {e}[/red]")
        return None

def display_response(prompt, response):
    """Fonction pour afficher la réponse du modèle d'IA de manière stylisée."""
    # Style pour le prompt
    prompt_style = Style(color="blue", bold=True)
    
    # Style pour la réponse
    response_style = Style(color="green", italic=True)
    
    # Affichage du prompt
    console.print(Panel(Text(prompt, style=prompt_style), title="[bold]Prompt[/bold]", border_style="blue"))
    
    # Affichage de la réponse
    console.print(Panel(Text(response, style=response_style), title="[bold]Réponse de l'IA[/bold]", border_style="green"))

def main():
    """Fonction principale pour interagir avec l'utilisateur et afficher les réponses."""
    console.print("[bold]Bienvenue dans l'interface de chat avec l'IA Ollama![/bold]")
    
    while True:
        prompt = console.input("[bold cyan]Vous: [/bold cyan]")
        if prompt.lower() in ["exit", "quit"]:
            console.print("[bold]Au revoir![/bold]")
            break
        
        response = get_ai_response(prompt)
        if response:
            display_response(prompt, response)

if __name__ == "__main__":
    main()