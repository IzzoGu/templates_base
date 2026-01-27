# Plataforma de Geração de Documentos

Sistema completo para criação de documentos a partir de templates DOCX com interface web intuitiva. A plataforma permite gerenciar templates, gerar formulários automaticamente e armazenar documentos gerados.

## Funcionalidades

- **Sistema de Admin**: Área administrativa protegida por senha para gerenciar templates e documentos
- **Área Pública**: Usuários podem acessar apenas templates publicados para preenchimento
- **Gerenciamento de Templates**: Adicione, visualize, publique/despublique e remova templates DOCX
- **Análise Automática**: Extração automática de campos dos templates usando placeholders Jinja2
- **Formulários Dinâmicos**: Geração automática de formulários baseados nos campos encontrados no template
- **Armazenamento Interno**: Todos os documentos gerados são salvos internamente para histórico
- **Download**: Download imediato dos documentos gerados
- **Histórico**: Acesso completo ao histórico de documentos gerados com filtros

## Instalação

### Requisitos
- Python 3.10+
- pip

### Passos

1. Clone ou baixe este repositório

2. Crie um ambiente virtual (recomendado):
```bash
python -m venv .venv
```

3. Ative o ambiente virtual:
```bash
# Windows (PowerShell)
.venv\Scripts\activate

# Windows (CMD)
.venv\Scripts\activate.bat

# Linux/Mac
source .venv/bin/activate
```

4. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Como Usar

### Iniciar a aplicação

```bash
streamlit run app.py
```

A aplicação será aberta automaticamente no navegador em `http://localhost:8501`

### Fluxo de Trabalho

#### Para Administradores

1. **Login Admin**
   - Vá para "Login Admin" na área pública
   - Digite a senha de administrador (padrão: `admin123`)
   - Acesse a área administrativa

2. **Adicionar Template**
   - Vá para "Adicionar Template"
   - Faça upload de um arquivo `.docx` com placeholders Jinja2
   - Adicione uma descrição (opcional)
   - Marque "Publicar imediatamente" se quiser que o template fique disponível para usuários
   - O sistema analisará automaticamente e extrairá os campos necessários

3. **Gerenciar Templates**
   - Vá para "Gerenciar Templates"
   - Visualize todos os templates (publicados e rascunhos)
   - Publique ou despublique templates conforme necessário
   - Remova templates que não são mais necessários

4. **Acessar Documentos Gerados**
   - Vá para "Documentos Gerados"
   - Visualize todos os documentos gerados por todos os usuários
   - Filtre por template
   - Baixe ou remova documentos

#### Para Usuários Públicos

1. **Acessar Templates Disponíveis**
   - Vá para "Templates Disponíveis"
   - Veja apenas os templates publicados pelo administrador
   - Selecione um template da lista

2. **Preencher e Gerar Documento**
   - Preencha o formulário gerado automaticamente
   - Clique em "Gerar Documento"
   - Baixe sua cópia do documento

### Configuração da Senha Admin

Por padrão, a senha de administrador é `admin123`. Para alterar:

1. Edite o arquivo `auth.py`
2. Altere a variável `DEFAULT_ADMIN_PASSWORD`
3. Ou defina a variável de ambiente `ADMIN_PASSWORD` antes de executar a aplicação

**IMPORTANTE**: Em produção, sempre altere a senha padrão e use variáveis de ambiente para maior segurança!

## Criando Templates

### Sintaxe Jinja2

Use placeholders Jinja2 no seu documento Word:

```
Olá {{nome}},

Seu CPF é {{cpf}} e seu email é {{email}}.

Data: {{data}}
```

### Campos Simples

```docx
Nome: {{nome}}
CPF: {{cpf}}
Email: {{email}}
```

### Loops (Listas)

Para criar listas dinâmicas:

```
Itens do pedido:
{% for item in itens %}
- {{item.descricao}}: R$ {{item.preco}}
{% endfor %}

Total: R$ {{total}}
```

### Campos Agrupados

O sistema detecta automaticamente campos relacionados:

```
Cliente: {{cliente_nome}}
CPF: {{cliente_cpf}}
Email: {{cliente_email}}
```

## 📁 Estrutura de Diretórios

```
templates_base/
├── app.py                      # Aplicação principal Streamlit
├── auth.py                     # Sistema de autenticação admin
├── template_analyzer.py        # Análise de templates e extração de campos
├── template_manager.py         # Gerenciamento de templates
├── form_generator.py           # Geração de formulários dinâmicos
├── document_storage.py         # Armazenamento de documentos gerados
├── requirements.txt            # Dependências Python
├── README.md                   # Este arquivo
├── templates/                 # Templates DOCX armazenados
│   └── metadata.json          # Metadados dos templates (inclui status de publicação)
└── generated_docs/            # Documentos gerados
    ├── internal/              # Cópias internas dos documentos
    └── metadata.json          # Metadados dos documentos gerados
```

## 🔧 Dependências

- **streamlit**: Interface web
- **docxtpl**: Renderização de templates DOCX com Jinja2
- **python-docx**: Análise de documentos DOCX

## Recursos Avançados

### Tipos de Campos Detectados Automaticamente

O sistema detecta automaticamente o tipo de campo pelo nome:

- **Email**: Campos com "email" no nome
- **Data**: Campos com "data" ou "date" no nome
- **Telefone**: Campos com "telefone", "phone" ou "fone" no nome
- **CPF/CNPJ**: Campos com "cpf" ou "cnpj" no nome
- **Valores**: Campos com "valor", "preco", "total" ou "price" no nome
- **Quantidades**: Campos com "quantidade", "qtd" ou "qty" no nome

### Armazenamento

- Todos os templates são armazenados em `templates/`
- Todos os documentos gerados são salvos em `generated_docs/internal/`
- Metadados são armazenados em arquivos JSON para persistência
- Status de publicação dos templates é armazenado nos metadados

### Sistema de Publicação

- Templates podem ser adicionados como **rascunho** ou **publicados**
- Apenas templates publicados aparecem na área pública
- Administradores podem publicar/despublicar templates a qualquer momento
- Templates antigos (sem campo `published`) são tratados como não publicados por padrão

## Solução de Problemas

### Erro ao analisar template
- Verifique se o arquivo é um DOCX válido
- Certifique-se de que os placeholders estão na sintaxe correta: `{{campo}}`

### Campos não detectados
- Verifique a sintaxe dos placeholders (deve ser `{{campo}}` e não `{campo}`)
- Certifique-se de que não há espaços extras dentro das chaves

### Erro ao gerar documento
- Verifique se todos os campos obrigatórios foram preenchidos
- Certifique-se de que os tipos de dados estão corretos (números, datas, etc.)

## Licença

Este projeto é fornecido como está, para uso interno.

## Contribuindo

Para melhorias ou correções, sinta-se à vontade para fazer alterações e testar localmente.
