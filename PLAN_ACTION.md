### Plano de Ação Passo a Passo

**Passo 1: Configuração do Ambiente e Chaves de API**
Antes de escrever código, precisamos deixar o ambiente pronto e autenticado.

1. Crie o ambiente virtual e instale as dependências:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

```


2. Crie o arquivo `.env` baseado no `.env.example`.
3. Gere suas chaves de API:
* **LangSmith:** Crie a API Key, pegue o endpoint padrão e descubra seu username publicando um prompt qualquer lá.
* **LLM:** Como você tem o ambiente configurado para o modelo `gemini-2.5-flash`, gere a sua chave no Google AI Studio e adicione em `GOOGLE_API_KEY`. Certifique-se de alterar as variáveis `LLM_PROVIDER` para `google` e preencher os campos `LLM_MODEL` e `EVAL_MODEL` com `gemini-2.5-flash`.



**Passo 2: Implementar o `src/pull_prompts.py`**
O esqueleto do arquivo já existe, mas está vazio.

* **O que fazer:** Usar a função `hub.pull("leonanluppi/bug_to_user_story_v1")` da biblioteca `langchain` para baixar o prompt original e salvá-lo localmente na pasta `prompts/` usando a função `save_yaml` do `utils.py`.
* **Objetivo:** Ter o arquivo base salvo localmente para análise.

**Passo 3: Criar o Prompt Otimizado (`bug_to_user_story_v2.yml`)**
Esta é a parte central da "Engenharia de Prompt". O arquivo `v1` é muito genérico.

* **O que fazer:** Criar o arquivo `prompts/bug_to_user_story_v2.yml` do zero.
* **Técnicas Obrigatórias:** Você *precisa* usar **Few-Shot Learning** (dar 2 a 3 exemplos de entrada de bug e saída de user story).
* **Técnicas Adicionais (escolher no mínimo mais uma):** Recomendo usar **Role Prompting** (ex: "Você é um Product Manager experiente...") somado a **Chain of Thought** (instruir o modelo a pensar passo a passo antes de formatar a User Story).
* **Estrutura:** Certifique-se de preencher os metadados corretos no YAML (versão, descrição, técnicas utilizadas).

**Passo 4: Implementar o `src/push_prompts.py`**
Depois de escrever o seu prompt V2 localmente, ele precisa ir para a nuvem.

* **O que fazer:** Implementar a lógica que lê o seu `bug_to_user_story_v2.yml` usando `load_yaml`, cria um objeto `ChatPromptTemplate` e usa `hub.push(f"{username}/bug_to_user_story_v2", prompt)` para enviá-lo ao LangSmith.
* **Importante:** Lembre-se de validar se o prompt contém as técnicas exigidas antes do push.

**Passo 5: Avaliação e Iteração (`src/evaluate.py`)**
O script de avaliação já está 100% pronto, você só precisa executá-lo.

* **O que fazer:** Rode `python src/evaluate.py`. Ele vai testar seu novo prompt V2 contra os 15 exemplos do arquivo `.jsonl`.
* **Iteração:** Dificilmente você conseguirá 0.9 logo de primeira em todas as métricas. Se tirar notas baixas (por exemplo, em *Completeness* ou *Clarity*), analise o log, altere o arquivo `v2.yml`, faça o push de novo (Passo 4) e rode a avaliação novamente. Repita até tudo ficar verde (>= 0.9).

**Passo 6: Implementar os Testes de Validação (`tests/test_prompts.py`)**
O projeto exige que você escreva 6 testes unitários usando `pytest` para garantir que a estrutura do seu prompt V2 está correta (se tem system_prompt, se tem persona, se tem exemplos few-shot, se não deixou a tag [TODO] para trás, etc.).

* **O que fazer:** Preencher as funções vazias no `test_prompts.py` lendo o arquivo YAML criado e validando suas chaves e conteúdos.

**Passo 7: Documentação e Entrega**
Com o código rodando e as métricas passando de 90%:

* **O que fazer:** Preencher o seu `README.md`. Ele precisa ter quais técnicas você aplicou na Fase 2 (e justificar o porquê), os resultados finais (com links públicos e prints do dashboard do LangSmith provando as notas) e as instruções de como executar.
