Isaac mateus - 01707297
Allyson Cesário - 01703538

# MemoMind AI

Projeto de IA de lembretes e anotações usando:
- Python
- Streamlit
- Ollama
- SQLite
- Kaggle

## Como executar

### Instalar dependências
pip install -r requirements.txt

### Baixar modelo
ollama pull llama3

### Rodar sistema
streamlit run app.py
# MemoMind AI

MemoMind AI é um assistente de lembretes e anotações feito em Python com interface em Streamlit. O projeto salva lembretes em um banco SQLite, permite definir data e hora para cada lembrete, consulta um modelo local via Ollama e pode exibir notificações no Windows quando um lembrete vence.

## Recursos

- Cadastro de lembretes com mensagem, data e hora.
- Histórico dos lembretes salvos.
- Status de lembrete pendente ou notificado.
- Banco de dados local com SQLite.
- Integração com Ollama usando o modelo `llama3`.
- Notificações locais com `plyer`.
- Atualização automática da tela com `streamlit-autorefresh`.
- Dataset de exemplo para lembretes e produtividade.

## Tecnologias

- Python
- Streamlit
- Ollama
- SQLite
- Pandas
- Plyer
- Streamlit Autorefresh

## Pré-requisitos

Antes de executar o projeto, instale:

- Python 3.10 ou superior
- Ollama
- Modelo `llama3` no Ollama

Para baixar o modelo:

```bash
ollama pull llama3
```

## Instalação

Clone ou extraia este projeto e entre na pasta:

```bash
cd memomind-ai
```

Crie um ambiente virtual:

```bash
python -m venv .venv
```

Ative o ambiente virtual no Windows:

```bash
.venv\Scripts\activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

## Como Executar

Inicie o aplicativo com:

```bash
streamlit run app.py
```

Depois, acesse o endereço mostrado pelo Streamlit no navegador.

## Como Usar

1. Digite o texto do lembrete.
2. Escolha a data do lembrete.
3. Escolha a hora do lembrete.
4. Clique em **Enviar**.
5. Veja o lembrete salvo no histórico.

Quando a data e a hora do lembrete forem atingidas, o sistema marca o item como notificado e tenta mostrar uma notificação local.

## Estrutura do Projeto

```text
.
+-- app.py
+-- database.py
+-- prompts.py
+-- requirements.txt
+-- memomind.db
+-- dataset/
|   +-- reminders_dataset.csv
+-- docs/
    +-- agente.md
    +-- dados.md
    +-- metricas.md
    +-- prompts.md
```

## Arquivos Principais

- `app.py`: aplicativo principal em Streamlit.
- `database.py`: criação e atualização da tabela de lembretes.
- `prompts.py`: prompt base do assistente.
- `requirements.txt`: lista de dependências do projeto.
- `memomind.db`: banco SQLite local.
- `dataset/reminders_dataset.csv`: dataset de exemplo.
- `docs/`: documentação auxiliar do projeto.

## Banco de Dados

O projeto usa SQLite e cria a tabela `reminders` com os campos:

- `id`: identificador do lembrete.
- `message`: texto do lembrete.
- `created_at`: data e hora em que o lembrete foi criado.
- `remind_at`: data e hora em que o lembrete deve avisar.
- `notified`: status de notificação.

## Observações

- O Ollama precisa estar instalado e em execução para que a resposta da IA funcione.
- Se o Ollama ou o modelo `llama3` não estiver disponível, o lembrete ainda será salvo, mas a resposta da IA poderá ser substituída por uma mensagem padrão.
- As notificações dependem da biblioteca `plyer` e do suporte do sistema operacional.
- O aplicativo verifica lembretes vencidos automaticamente a cada 30 segundos quando `streamlit-autorefresh` está instalado.

## Próximas Melhorias

- Permitir edição e exclusão de lembretes.
- Adicionar filtros por status, data ou categoria.
- Usar o prompt de `prompts.py` diretamente na chamada ao modelo.
- Criar testes automatizados para banco de dados e fluxo principal.
- Melhorar o tratamento de erros da integração com Ollama.
