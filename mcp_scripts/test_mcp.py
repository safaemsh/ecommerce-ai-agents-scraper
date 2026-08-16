"""
Script de test pour les fonctionnalités MCP
"""
import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BASE_DIR))

from mcp_server import handle_mcp_request
from generate_prompt import generate_daily_prompt


def test_generate_prompt():
    """Tester la génération de prompt"""
    print("=== Test génération de prompt ===")
    prompt = generate_daily_prompt()
    print(f"Prompt généré: {len(prompt)} caractères")
    print(prompt[:200] + "...")
    return prompt


def test_mcp_server():
    """Tester le serveur MCP"""
    print("\n=== Test serveur MCP ===")
    
    # Test run_scraping
    request = {"method": "run_scraping", "params": {}}
    response = handle_mcp_request(request)
    print(f"Run scraping: {response.get('status')}")
    
    # Test get_stats
    request = {"method": "get_stats", "params": {}}
    response = handle_mcp_request(request)
    print(f"Get stats: {response.get('status')}")
    if response.get('status') == 'success':
        print(f"Statistiques: {response.get('stats')}")
    
    # Test generate_prompt
    request = {"method": "generate_prompt", "params": {}}
    response = handle_mcp_request(request)
    print(f"Generate prompt: {response.get('status')}")
    if response.get('status') == 'success':
        print(f"Prompt généré: {len(response.get('prompt', ''))} caractères")


if __name__ == '__main__':
    test_generate_prompt()
    test_mcp_server()
    print("\n=== Tests terminés ===")

