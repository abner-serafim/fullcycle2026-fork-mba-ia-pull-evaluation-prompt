"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull dos prompts do Hub
3. Salva localmente em prompts/bug_to_user_story_v1.yml

SIMPLIFICADO: Usa serialização nativa do LangChain para extrair prompts.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from langchain import hub
from utils import save_yaml, check_env_vars, print_section_header

load_dotenv()


def pull_prompts_from_langsmith():
    """
    Faz o pull do prompt leonanluppi/bug_to_user_story_v1
    e salva em prompts/bug_to_user_story_v1.yml
    """
    print_section_header("Iniciando Pull do Prompt V1")
    
    prompt_name = "leonanluppi/bug_to_user_story_v1"
    output_path = "prompts/bug_to_user_story_v1.yml"
    
    try:
        from langchain_core.load import dumpd
        print(f"Fazendo pull do prompt: {prompt_name} ...")
        prompt = hub.pull(prompt_name)
        
        # Extrai os dados do prompt usando a serialização nativa
        prompt_data = dumpd(prompt)
        
        if save_yaml(prompt_data, output_path):
            print(f"✅ Prompt salvo com sucesso em: {output_path}")
        else:
            print("❌ Falha ao salvar o prompt.")
    except Exception as e:
        print(f"❌ Erro ao fazer pull do prompt: {e}")


def main():
    """Função principal"""
    # Verifica variáveis de ambiente necessárias
    if not check_env_vars(['LANGSMITH_API_KEY']):
        return 1
        
    pull_prompts_from_langsmith()
    return 0


if __name__ == "__main__":
    sys.exit(main())
