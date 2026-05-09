"""
Testes automatizados para validação de prompts.
"""
import pytest
import yaml
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils import validate_prompt_structure

def load_prompts(file_path: str):
    """Carrega prompts do arquivo YAML."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

class TestPrompts:
    @classmethod
    def setup_class(cls):
        cls.prompt_file = Path(__file__).parent.parent / "prompts" / "bug_to_user_story_v2.yml"
        cls.prompt_data = load_prompts(str(cls.prompt_file))

    def test_prompt_has_system_prompt(self):
        """Verifica se o campo 'system_prompt' existe e não está vazio."""
        assert "system_prompt" in self.prompt_data, "Campo 'system_prompt' ausente."
        assert isinstance(self.prompt_data["system_prompt"], str)
        assert len(self.prompt_data["system_prompt"].strip()) > 0

    def test_prompt_has_role_definition(self):
        """Verifica se o prompt define uma persona (ex: "Você é um Product Manager")."""
        system_prompt = self.prompt_data.get("system_prompt", "").lower()
        assert "você é" in system_prompt or "atue como" in system_prompt, "Definição de persona não encontrada."

    def test_prompt_mentions_format(self):
        """Verifica se o prompt exige formato Markdown ou User Story padrão."""
        system_prompt = self.prompt_data.get("system_prompt", "").lower()
        has_format = "como um" in system_prompt and "para que" in system_prompt
        assert has_format, "O formato padrão de User Story (Como um... para que...) não foi exigido."

    def test_prompt_has_few_shot_examples(self):
        """Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot)."""
        system_prompt = self.prompt_data.get("system_prompt", "").lower()
        assert "exemplo" in system_prompt and "entrada" in system_prompt and "saída" in system_prompt, "Exemplos Few-Shot não encontrados."

    def test_prompt_no_todos(self):
        """Garante que você não esqueceu nenhum `[TODO]` no texto."""
        system_prompt = self.prompt_data.get("system_prompt", "")
        assert "TODO" not in system_prompt, "Foram encontrados placeholders TODO no texto."

    def test_minimum_techniques(self):
        """Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas."""
        techniques = self.prompt_data.get("techniques_applied", [])
        assert isinstance(techniques, list) and len(techniques) >= 2, "Devem ser listadas no mínimo 2 técnicas."

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])