"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script:
1. Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
2. Valida os prompts
3. Faz push PÚBLICO para o LangSmith Hub
4. Adiciona metadados (tags, descrição, técnicas utilizadas)

SIMPLIFICADO: Código mais limpo e direto ao ponto.
"""

"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.
"""

import os
import sys
from dotenv import load_dotenv
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate
from utils import load_yaml, check_env_vars, print_section_header, validate_prompt_structure

load_dotenv()


def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    """
    Faz push do prompt otimizado para o LangSmith Hub (PÚBLICO).
    """
    try:
        # Cria o template do LangChain usando os dados do YAML
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", prompt_data["system_prompt"]),
            ("user", prompt_data.get("user_prompt", "{bug_report}"))
        ])
        
        # Faz o push para o Hub
        print(f"Fazendo push do prompt para o Hub como: {prompt_name} ...")
        hub.push(prompt_name, prompt_template)
        print("✅ Push realizado com sucesso!")
        return True
    except Exception as e:
        print(f"❌ Erro ao fazer push do prompt: {e}")
        return False


def validate_prompt(prompt_data: dict) -> tuple[bool, list]:
    """
    Valida estrutura básica de um prompt.
    """
    return validate_prompt_structure(prompt_data)


def main():
    """Função principal"""
    print_section_header("Iniciando Push do Prompt V2")
    
    # Verifica variáveis de ambiente
    if not check_env_vars(['LANGSMITH_API_KEY', 'USERNAME_LANGSMITH_HUB']):
        return 1
        
    username = os.getenv("USERNAME_LANGSMITH_HUB")
    prompt_name = f"{username}/bug_to_user_story_v2"
    file_path = "prompts/bug_to_user_story_v2.yml"
    
    # Carrega o YAML
    prompt_data = load_yaml(file_path)
    if not prompt_data:
        return 1
        
    # Valida o YAML localmente
    is_valid, errors = validate_prompt(prompt_data)
    if not is_valid:
        print("❌ Validação do prompt falhou com os erros:")
        for error in errors:
            print(f"  - {error}")
        return 1
        
    print("✅ Validação estrutural do prompt V2 passou!")
    
    # Executa o push
    if push_prompt_to_langsmith(prompt_name, prompt_data):
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())