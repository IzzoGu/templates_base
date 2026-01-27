# Changelog - Sistema de Admin e Área Pública

## Novas Funcionalidades Implementadas

### Sistema de Autenticação
- Criado módulo `auth.py` com sistema de autenticação simples para administradores
- Login/logout funcional com controle de sessão

### Área Administrativa
- **Dashboard Admin**: Visão geral com métricas e ações rápidas
- **Adicionar Template**: Upload de templates com opção de publicação imediata
- **Gerenciar Templates**: 
  - Lista todos os templates (publicados e rascunhos)
  - Botões para publicar/despublicar templates
  - Remoção de templates
- **Documentos Gerados**: Acesso completo a todos os documentos gerados
- **Limpar Base**: Ferramenta administrativa para limpar toda a base de dados

### Área Pública
- **Início**: Página inicial com informações sobre a plataforma
- **Templates Disponíveis**: 
  - Lista apenas templates publicados
  - Formulário de preenchimento
  - Geração e download de documentos
- **Login Admin**: Acesso para administradores

### Sistema de Publicação
- Templates podem ser adicionados como **rascunho** ou **publicados**
- Campo `published` adicionado aos metadados dos templates
- Funções para publicar/despublicar templates
- Compatibilidade com templates antigos (tratados como não publicados por padrão)

## Arquivos Modificados

1. **app.py**: Refatorado completamente para separar área admin e pública
2. **template_manager.py**: 
   - Adicionado parâmetro `published` em `add_template()`
   - Adicionado parâmetro `only_published` em `list_templates()`
   - Criadas funções `toggle_template_publication()` e `update_template_publication()`
3. **auth.py**: Novo arquivo com sistema de autenticação
4. **README.md**: Atualizado com documentação do sistema de admin

## Como Usar

### Para Administradores
1. Acesse a aplicação
2. Vá para "Login Admin"
3. Informe a senha configurada para o administrador
4. Acesse a área administrativa

### Para Usuários Públicos
1. Acesse a aplicação
2. Vá para "Templates Disponíveis"
3. Selecione um template publicado
4. Preencha o formulário e gere o documento

## Segurança

**IMPORTANTE**: 
- Altere a senha padrão em produção
- Use variáveis de ambiente para senhas em produção
- O sistema atual é básico e adequado para uso interno

## Compatibilidade

- Templates antigos (sem campo `published`) continuam funcionando
- São tratados como não publicados por padrão
- Podem ser publicados através da interface admin
