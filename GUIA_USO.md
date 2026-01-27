# Guia Completo de Uso - Plataforma de Geração de Documentos

## Iniciando a Plataforma

### 1. Instalação Inicial

Abra o terminal/PowerShell na pasta do projeto e execute:

```bash
# Criar ambiente virtual (se ainda não criou)
python -m venv .venv

# Ativar ambiente virtual
# Windows PowerShell:
.venv\Scripts\activate

# Windows CMD:
.venv\Scripts\activate.bat

# Linux/Mac:
source .venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### 2. Iniciar a Aplicação

```bash
streamlit run app.py
```

A aplicação abrirá automaticamente no navegador em `http://localhost:8501`

---

## Passo a Passo Completo

### PASSO 1: Criar um Template DOCX

Antes de usar a plataforma, você precisa criar um template DOCX com placeholders.

#### Exemplo de Template Simples:

1. Abra o Microsoft Word ou LibreOffice Writer
2. Digite o conteúdo do documento usando placeholders:

```
CONTRATO DE SERVIÇO

Cliente: {{nome_cliente}}
CPF: {{cpf_cliente}}
Email: {{email_cliente}}
Telefone: {{telefone_cliente}}

Data do Contrato: {{data_contrato}}

Descrição: {{descricao_servico}}

Valor Total: R$ {{valor_total}}

Data: {{data}}
```

3. Salve como arquivo `.docx` (ex: `contrato_template.docx`)

**Importante:** Use `{{nome_do_campo}}` para criar placeholders que serão substituídos pelos dados do formulário.

---

### PASSO 2: Adicionar Template na Plataforma

1. **Na barra lateral**, clique em **"Adicionar Template"**

2. **Clique em "Browse files"** ou arraste um arquivo `.docx` para a área de upload

3. **Preencha a descrição** (opcional):
   - Exemplo: "Template de contrato de prestação de serviços"

4. **Clique em "Adicionar Template"**

5. O sistema irá:
   - Analisar o template automaticamente
   - Extrair todos os campos encontrados
   - Mostrar quais campos foram detectados

**Resultado esperado:**
```
Template 'contrato_template.docx' adicionado com sucesso!

Campos encontrados: ['cpf_cliente', 'data', 'data_contrato', 'descricao_servico', 'email_cliente', 'nome_cliente', 'telefone_cliente', 'valor_total']
Total de campos: 8
```

---

### PASSO 3: Usar o Template para Gerar um Documento

1. **Na barra lateral**, clique em **"Meus Templates"**

2. **Selecione um template** no dropdown:
   - Você verá o nome do arquivo e a descrição

3. **Visualize as informações do template:**
   - Nome do arquivo
   - Descrição
   - Lista de campos necessários

4. **Preencha o formulário** que aparece automaticamente:
   - O sistema cria campos baseados nos nomes detectados
   - Campos de email, data, telefone, CPF são detectados automaticamente
   - Campos relacionados são agrupados (ex: `cliente_nome`, `cliente_cpf`)

5. **Digite o nome do arquivo de saída** (ex: `contrato_joao_silva.docx`)

6. **Clique em "Gerar Documento"**

7. **Resultado:**
   - Mensagem de sucesso
   - Informação sobre onde a cópia interna foi salva
   - Botão para baixar o documento

8. **Clique em "Baixar Documento"** para salvar em seu computador

---

### PASSO 4: Acessar Histórico de Documentos

1. **Na barra lateral**, clique em **"Documentos Gerados"**

2. **Visualize todos os documentos gerados:**
   - Nome do arquivo
   - Template usado
   - Data de geração
   - Dados utilizados

3. **Use os filtros:**
   - Filtre por template específico usando o dropdown

4. **Ações disponíveis:**
   - **Baixar**: Baixar o documento novamente
   - **Remover**: Excluir o documento do histórico

---

## Dicas e Truques

### Tipos de Campos Detectados Automaticamente

O sistema detecta automaticamente o tipo de campo pelo nome:

| Nome do Campo | Tipo Detectado | Exemplo |
|--------------|----------------|---------|
| `email`, `email_cliente` | Campo de email | `{{email}}` |
| `data`, `data_contrato`, `date` | Seletor de data | `{{data}}` |
| `telefone`, `phone`, `fone` | Campo de telefone | `{{telefone}}` |
| `cpf`, `cnpj` | Campo de CPF/CNPJ | `{{cpf}}` |
| `valor`, `preco`, `total`, `price` | Campo numérico (R$) | `{{valor_total}}` |
| `quantidade`, `qtd`, `qty` | Campo numérico (inteiro) | `{{quantidade}}` |
| Outros | Campo de texto | `{{nome}}` |

### Criando Listas Dinâmicas (Loops)

Para criar listas que se repetem, use a sintaxe Jinja2:

**No template DOCX:**
```
Itens do Pedido:

{% for item in itens %}
- {{item.descricao}} - Quantidade: {{item.quantidade}} - Preço: R$ {{item.preco}}
{% endfor %}

Total: R$ {{total}}
```

**No formulário**, você precisará preencher manualmente os dados em formato JSON (funcionalidade avançada).

### Campos Agrupados

Se você usar nomes como `cliente_nome`, `cliente_cpf`, `cliente_email`, o sistema agrupa automaticamente em uma seção "Cliente".

---

## Exemplo Prático Completo

### Cenário: Criar um Contrato de Serviço

**1. Criar o Template (`contrato.docx`):**
```
CONTRATO DE PRESTAÇÃO DE SERVIÇOS

Contratante: {{nome_cliente}}
CPF: {{cpf_cliente}}
Email: {{email_cliente}}
Telefone: {{telefone_cliente}}

Data do Contrato: {{data_contrato}}

OBJETO DO CONTRATO

O prestador se compromete a realizar o seguinte serviço:
{{descricao_servico}}

VALOR

O valor total do serviço é de R$ {{valor_total}}.

São Paulo, {{data}}

_________________________
Assinatura do Contratante
```

**2. Adicionar na Plataforma:**
- Upload do arquivo `contrato.docx`
- Descrição: "Contrato padrão de prestação de serviços"

**3. Gerar Documento:**
- Selecionar o template "contrato.docx"
- Preencher:
  - Nome Cliente: João Silva
  - CPF Cliente: 123.456.789-00
  - Email Cliente: joao@email.com
  - Telefone Cliente: (11) 98765-4321
  - Data Contrato: 15/01/2024
  - Descrição Servico: Desenvolvimento de site institucional
  - Valor Total: 5000.00
  - Data: 15/01/2024
- Nome do arquivo: `contrato_joao_silva.docx`
- Clicar em "Gerar Documento"
- Baixar o arquivo

**4. Resultado:**
- Documento gerado com todos os dados preenchidos
- Cópia salva internamente em `generated_docs/internal/`
- Disponível para download e no histórico

---

## ❓ Perguntas Frequentes

### Como remover um template?
- Vá em "Meus Templates"
- Selecione o template
- Clique em "Remover Template"

### Onde ficam salvos os documentos gerados?
- Cópias internas: `generated_docs/internal/`
- Você pode baixar uma cópia para seu computador

### Posso usar o mesmo template várias vezes?
- Sim! Você pode gerar quantos documentos quiser com o mesmo template

### Como editar um template?
- Atualmente, você precisa remover o template antigo e adicionar uma nova versão
- Ou edite o arquivo DOCX diretamente e faça upload novamente com o mesmo nome

### Os documentos ficam salvos permanentemente?
- Sim, até você removê-los manualmente
- Todos ficam em `generated_docs/internal/`

---

## Solução de Problemas

### Erro: "Template não encontrado"
- Verifique se o arquivo é um `.docx` válido
- Tente abrir o arquivo no Word para verificar se não está corrompido

### Erro: "Campos não detectados"
- Verifique se os placeholders estão no formato correto: `{{campo}}`
- Não use espaços dentro das chaves: `{{ campo }}` (incorreto) → `{{campo}}` (correto)

### Erro ao gerar documento
- Verifique se preencheu todos os campos obrigatórios
- Certifique-se de que os tipos de dados estão corretos (números para valores, etc.)

### Aplicação não inicia
- Verifique se ativou o ambiente virtual
- Verifique se instalou todas as dependências: `pip install -r requirements.txt`

---

## Próximos Passos

1. Crie seu primeiro template
2. Adicione na plataforma
3. Gere seu primeiro documento
4. Explore o histórico de documentos

Boa sorte!

