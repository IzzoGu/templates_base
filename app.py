import io
import tempfile
import shutil
from pathlib import Path
import streamlit as st
import mammoth
from docxtpl import DocxTemplate
import streamlit.components.v1 as components

from auth import (
    is_admin,
    login_admin,
    logout_admin,
    require_admin,
    set_admin_password,
    check_admin_password,
    login_user,
    logout_user,
    get_current_user,
    create_user,
    list_users,
    is_user_logged_in,
)
from template_manager import (
    add_template, list_templates, get_template, delete_template,
    update_template_publication
)
from form_generator import generate_form_from_fields, format_field_value
from document_storage import (
    save_generated_document, list_generated_documents, get_document, delete_document
)


st.set_page_config(
    page_title="Gerador de Documentos",
    layout="wide",
    initial_sidebar_state="expanded"
)

if 'current_template_id' not in st.session_state:
    st.session_state.current_template_id = None
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False


def main():
    admin_logged = is_admin()
    current_user = get_current_user()

    st.sidebar.title("Gerador de Documentos")
    if admin_logged:
        st.sidebar.success("Modo Administrador")
        if st.sidebar.button("Sair", type="secondary"):
            logout_admin()
            st.rerun()
    else:
        if current_user:
            st.sidebar.success(f"Usuário: {current_user}")
            if st.sidebar.button("Sair usuário", type="secondary"):
                logout_user()
                st.rerun()
        else:
            st.sidebar.info("Modo Público")

    st.sidebar.markdown("---")
    
    if admin_logged:
        page = st.sidebar.radio(
            "Navegação Admin",
            [
                "Dashboard Admin",
                "Adicionar Template",
                "Gerenciar Templates",
                "Gerenciar Usuários",
                "Documentos Gerados",
                "Limpar Base",
                "Configurações",
            ],
        )
    else:
        # Usuário comum: se não estiver logado, só pode acessar telas de login
        if is_user_logged_in():
            page = st.sidebar.radio(
                "Navegação",
                ["Início", "Templates Disponíveis", "Login Usuário", "Login Admin"],
            )
        else:
            page = st.sidebar.radio(
                "Navegação",
                ["Login Usuário", "Login Admin"],
            )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Sobre")
    if admin_logged:
        st.sidebar.info(
            "Área administrativa para gerenciar templates e documentos. "
            "Você pode adicionar templates, publicá-los e acessar todos os documentos gerados."
        )
    else:
        st.sidebar.info(
            "Plataforma para criar documentos a partir de templates DOCX. "
            "Selecione um template publicado, preencha o formulário e gere seu documento."
        )
    st.sidebar.caption("Desenvolvido por Gustavo Izzo")

    if admin_logged:
        if page == "Dashboard Admin":
            show_admin_dashboard()
        elif page == "Adicionar Template":
            require_admin()
            show_add_template_page()
        elif page == "Gerenciar Templates":
            require_admin()
            show_manage_templates_page()
        elif page == "Gerenciar Usuários":
            require_admin()
            show_admin_users_page()
        elif page == "Documentos Gerados":
            require_admin()
            show_documents_page()
        elif page == "Limpar Base":
            require_admin()
            show_clear_base_page()
        elif page == "Configurações":
            require_admin()
            show_admin_settings_page()
    else:
        if page == "Início":
            show_home_page()
        elif page == "Templates Disponíveis":
            show_public_templates_page()
        elif page == "Login Usuário":
            show_user_login_page()
        elif page == "Login Admin":
            show_login_page()


def show_login_page():
    st.title("Login Administrativo")
    st.markdown("---")
    
    st.info("Acesso restrito para administradores da plataforma.")
    
    password = st.text_input(
        "Senha de Administrador",
        type="password",
        help="Digite a senha para acessar a área administrativa"
    )
    
    if st.button("Entrar", type="primary"):
        if login_admin(password):
            st.success("Login realizado com sucesso!")
            st.rerun()
        else:
            st.error("Senha incorreta. Tente novamente.")


def show_user_login_page():
    st.title("Login de Usuário")
    st.markdown("---")

    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")

    if st.button("Entrar", type="primary"):
        if login_user(username, password):
            st.success("Login realizado com sucesso.")
            st.rerun()
        else:
            st.error("Usuário ou senha inválidos.")


def show_home_page():
    st.title("Bem-vindo ao Gerador de Documentos")
    st.markdown("---")
    
    published_templates = list_templates(only_published=True)
    all_documents = list_generated_documents()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Templates Disponíveis", len(published_templates))
    
    with col2:
        st.metric("Documentos Gerados", len(all_documents))
    
    with col3:
        recent_docs = list_generated_documents(limit=5)
        st.metric("Últimos 7 dias", len([d for d in recent_docs if d.get('generated_at')]))
    
    st.markdown("---")
    
    st.subheader("Como usar")
    
    steps = [
        "1. **Selecione um Template**: Vá para 'Templates Disponíveis' e escolha um template publicado",
        "2. **Preencha o Formulário**: Um formulário será gerado automaticamente com base nos campos do template",
        "3. **Gere o Documento**: Clique em 'Gerar Documento' e baixe sua cópia",
        "4. **Acesso Admin**: Administradores podem adicionar novos templates e gerenciar a plataforma"
    ]
    
    for step in steps:
        st.markdown(step)


def show_public_templates_page():
    st.title("Templates Disponíveis")
    st.markdown("---")

    if not is_user_logged_in():
        st.info("Para utilizar os templates, faça login como usuário na opção 'Login Usuário'.")
        return

    templates = list_templates(only_published=True)
    
    if not templates:
        st.info("Nenhum template publicado disponível no momento. Entre em contato com o administrador.")
        return
    
    # Seleção de template
    template_options = {f"{t['filename']} - {t.get('description', 'Sem descrição')}": t['id'] 
                       for t in templates}
    
    selected_option = st.selectbox(
        "Selecione um template para usar:",
        options=list(template_options.keys())
    )
    
    selected_template_id = template_options[selected_option]
    template_info = get_template(selected_template_id)
    
    if template_info:
        st.markdown("---")
        
        st.subheader(f"{template_info['filename']}")
        if template_info.get('description'):
            st.caption(template_info['description'])
        
        st.markdown("**Campos necessários:**")
        st.info(", ".join(template_info['fields']) if template_info['fields'] else "Nenhum campo encontrado")
        
        st.markdown("---")
        
        # Formulário de preenchimento
        st.subheader("Preencha os dados")
        
        col_form, col_preview = st.columns([1.05, 0.95])

        with col_form:
            form_data = generate_form_from_fields(template_info['fields'], template_info)

            output_filename = st.text_input(
                "Nome do arquivo de saída",
                value=f"{template_info['filename'].replace('.docx', '')}_gerado.docx"
            )

            generate_btn = st.button("Gerar Documento", type="primary")

            if generate_btn:
                missing_fields = [field for field in template_info['fields']
                                  if not form_data.get(field) or str(form_data[field]).strip() == '']

                if missing_fields:
                    st.warning(f"Preencha os seguintes campos: {', '.join(missing_fields)}")
                else:
                    try:
                        template_path = Path(template_info['path'])
                        doc = DocxTemplate(str(template_path))

                        context = {}
                        for key, value in form_data.items():
                            context[key] = format_field_value(value) if value not in (None, "") else "—"

                        doc.render(context)

                        buffer = io.BytesIO()
                        doc.save(buffer)
                        buffer.seek(0)
                        document_bytes = buffer.read()

                        doc_info = save_generated_document(
                            document_bytes,
                            selected_template_id,
                            template_info['filename'],
                            output_filename or f"{template_info['filename']}_gerado.docx",
                            context
                        )

                        st.success("Documento gerado com sucesso.")
                        st.info(f"Cópia interna salva em: `{doc_info['internal_path']}`")

                        st.download_button(
                            "Baixar Documento",
                            data=document_bytes,
                            file_name=output_filename or f"{template_info['filename']}_gerado.docx",
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                            type="primary"
                        )

                    except Exception as e:
                        st.error(f"Erro ao gerar documento: {str(e)}")

        with col_preview:
            st.subheader("Pré-visualização em tempo real")
            st.caption("A visualização é apenas para referência. A geração final usa o DOCX original sem alterar a formatação.")
            try:
                preview_html = render_preview_html(
                    Path(template_info['path']),
                    {
                        field: format_field_value(form_data.get(field)) if form_data.get(field) else "..."
                        for field in template_info['fields']
                    }
                )
                components.html(preview_html, height=780, scrolling=True)
            except Exception as e:
                st.warning(f"Não foi possível gerar a pré-visualização: {e}")


def show_admin_dashboard():
    """Dashboard administrativo."""
    require_admin()
    
    st.title("Dashboard Administrativo")
    st.markdown("---")
    
    all_templates = list_templates()
    published_templates = list_templates(only_published=True)
    all_documents = list_generated_documents()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total de Templates", len(all_templates))
    
    with col2:
        st.metric("Templates Publicados", len(published_templates))
    
    with col3:
        st.metric("Templates Rascunho", len(all_templates) - len(published_templates))
    
    with col4:
        st.metric("Documentos Gerados", len(all_documents))
    
    st.markdown("---")
    
    st.subheader("Ações Rápidas")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Adicionar Template", use_container_width=True):
            st.switch_page("pages/add_template.py") if hasattr(st, 'switch_page') else None
    
    with col2:
        if st.button("Gerenciar Templates", use_container_width=True):
            st.switch_page("pages/manage_templates.py") if hasattr(st, 'switch_page') else None
    
    with col3:
        if st.button("Ver Documentos", use_container_width=True):
            st.switch_page("pages/documents.py") if hasattr(st, 'switch_page') else None
    
    st.markdown("---")
    
    st.subheader("Templates Recentes")
    if all_templates:
        for template in all_templates[:5]:
            status = "Publicado" if template.get('published', False) else "Rascunho"
            st.markdown(f"- **{template['filename']}** - {status}")
    else:
        st.info("Nenhum template cadastrado ainda.")


def show_add_template_page():
    """Página para adicionar novos templates (admin)."""
    require_admin()
    
    st.title("Adicionar Novo Template")
    st.markdown("---")
    
    uploaded_file = st.file_uploader(
        "Selecione um arquivo DOCX",
        type=["docx"],
        help="O arquivo deve conter placeholders Jinja2 como {{campo}}"
    )
    
    description = st.text_area(
        "Descrição do Template (opcional)",
        help="Descreva para que serve este template",
        height=100
    )
    
    published = st.checkbox(
        "Publicar imediatamente",
        help="Se marcado, o template ficará disponível para usuários públicos",
        value=False
    )
    
    if uploaded_file is not None:
        st.info(f"Arquivo selecionado: **{uploaded_file.name}**")
        
        if st.button("Adicionar Template", type="primary"):
            try:
                template_bytes = uploaded_file.read()
                
                with st.spinner("Analisando template e extraindo campos..."):
                    template_info = add_template(
                        template_bytes,
                        uploaded_file.name,
                        description,
                        published=published
                    )
                
                status_msg = "publicado" if published else "adicionado como rascunho"
                st.success(f"Template '{template_info['filename']}' {status_msg} com sucesso.")
                st.json({
                    "Campos encontrados": template_info['fields'],
                    "Total de campos": template_info['field_count'],
                    "Status": "Publicado" if published else "Rascunho"
                })
                
            except Exception as e:
                st.error(f"Erro ao adicionar template: {str(e)}")


def show_manage_templates_page():
    """Página para gerenciar templates (admin)."""
    require_admin()
    
    st.title("Gerenciar Templates")
    st.markdown("---")
    
    templates = list_templates()
    
    if not templates:
        st.info("Nenhum template cadastrado. Adicione um template na página 'Adicionar Template'.")
        return
    
    st.metric("Total de Templates", len(templates))
    st.markdown("---")
    
    # Lista de templates com ações
    for template in templates:
        published_status = template.get('published', False)
        status_badge = "Publicado" if published_status else "Rascunho"
        
        with st.expander(f"{template['filename']} - {status_badge}"):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.write(f"**Descrição:** {template.get('description', 'Sem descrição')}")
                st.write(f"**Campos:** {', '.join(template.get('fields', []))}")
                st.write(f"**Total de campos:** {template.get('field_count', 0)}")
                st.write(f"**Adicionado em:** {template.get('uploaded_at', 'N/A')[:10]}")
            
            with col2:
                # Botão de publicar/despublicar
                if published_status:
                    if st.button("Despublicar", key=f"unpublish_{template['id']}"):
                        if update_template_publication(template['id'], False):
                            st.success("Template despublicado!")
                            st.rerun()
                else:
                    if st.button("Publicar", key=f"publish_{template['id']}"):
                        if update_template_publication(template['id'], True):
                            st.success("Template publicado!")
                            st.rerun()
                
                # Botão de remover
                if st.button("Remover", key=f"delete_{template['id']}", type="secondary"):
                    if delete_template(template['id']):
                        st.success("Template removido!")
                        st.rerun()


def show_documents_page():
    """Página para listar documentos gerados (admin)."""
    require_admin()
    
    st.title("Documentos Gerados")
    st.markdown("---")
    
    documents = list_generated_documents()
    
    if not documents:
        st.info("Nenhum documento gerado ainda.")
        return
    
    st.metric("Total de Documentos", len(documents))
    st.markdown("---")
    
    # Filtros
    col1, col2 = st.columns(2)
    with col1:
        template_filter = st.selectbox(
            "Filtrar por template:",
            options=["Todos"] + list(set([d['template_name'] for d in documents]))
        )
    
    filtered_docs = documents
    if template_filter != "Todos":
        filtered_docs = [d for d in documents if d['template_name'] == template_filter]
    
    # Lista de documentos
    for doc in filtered_docs:
        with st.expander(f"{doc['filename']} - {doc.get('generated_at', '')[:10]}"):
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.write(f"**Template:** {doc['template_name']}")
                st.write(f"**Gerado em:** {doc.get('generated_at', 'N/A')}")
                if doc.get('form_data'):
                    st.write("**Dados utilizados:**")
                    st.json(doc['form_data'])
            
            with col2:
                doc_data = get_document(doc['id'])
                if doc_data and 'bytes' in doc_data:
                    st.download_button(
                        "Baixar",
                        data=doc_data['bytes'],
                        file_name=doc['filename'],
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        key=f"download_{doc['id']}"
                    )
            
            with col3:
                if st.button("Remover", key=f"delete_{doc['id']}"):
                    if delete_document(doc['id']):
                        st.success("Documento removido!")
                        st.rerun()


def show_clear_base_page():
    require_admin()
    
    st.title("Limpar Base de Dados")
    st.markdown("---")
    
    st.warning("ATENÇÃO: Esta ação irá remover TODOS os templates e documentos gerados. Esta ação não pode ser desfeita!")
    
    col1, col2 = st.columns(2)
    
    templates_count = len(list_templates())
    documents_count = len(list_generated_documents())
    
    with col1:
        st.metric("Templates a serem removidos", templates_count)
    
    with col2:
        st.metric("Documentos a serem removidos", documents_count)
    
    st.markdown("---")
    
    if templates_count == 0 and documents_count == 0:
        st.info("A base de dados já está vazia.")
        return
    
    st.subheader("Confirmação")
    
    confirm_text = st.text_input(
        "Digite 'LIMPAR' para confirmar:",
        help="Digite exatamente 'LIMPAR' para confirmar a exclusão"
    )
    
    col1, col2 = st.columns([1, 4])
    
    with col1:
        clear_btn = st.button(
            "Limpar Tudo",
            type="primary",
            disabled=(confirm_text != "LIMPAR")
        )
    
    if clear_btn and confirm_text == "LIMPAR":
        try:
            # Remove templates
            templates_dir = Path('templates')
            if templates_dir.exists():
                for file in templates_dir.glob('*.docx'):
                    file.unlink()
                
                metadata_file = templates_dir / 'metadata.json'
                if metadata_file.exists():
                    metadata_file.unlink()
            
            # Remove documentos gerados
            generated_docs_dir = Path('generated_docs')
            if generated_docs_dir.exists():
                internal_dir = generated_docs_dir / 'internal'
                if internal_dir.exists():
                    for file in internal_dir.glob('*.docx'):
                        file.unlink()
                
                metadata_file = generated_docs_dir / 'metadata.json'
                if metadata_file.exists():
                    metadata_file.unlink()
            
            # Remove arquivos temporários
            temp_dir = Path('temp')
            if temp_dir.exists():
                shutil.rmtree(temp_dir)
            
            st.success("Base de dados limpa com sucesso!")
            st.info("Todos os templates e documentos foram removidos.")
            st.rerun()
            
        except Exception as e:
            st.error(f"Erro ao limpar base de dados: {str(e)}")


def show_admin_settings_page():
    st.title("Configurações da Área Administrativa")
    st.markdown("---")

    st.subheader("Alterar senha do administrador")

    col1, col2 = st.columns(2)

    with col1:
        current_password = st.text_input(
            "Senha atual",
            type="password",
        )
        new_password = st.text_input(
            "Nova senha",
            type="password",
        )
        confirm_password = st.text_input(
            "Confirmar nova senha",
            type="password",
        )

        if st.button("Salvar nova senha", type="primary"):
            if not current_password or not new_password or not confirm_password:
                st.error("Preencha todos os campos de senha.")
            elif not check_admin_password(current_password):
                st.error("Senha atual incorreta.")
            elif new_password != confirm_password:
                st.error("A confirmação da nova senha não confere.")
            else:
                set_admin_password(new_password)
                st.success("Senha do administrador atualizada com sucesso.")

    with col2:
        st.info(
            "A senha é usada apenas para acesso à área administrativa desta "
            "plataforma. Guarde-a em local seguro."
        )


def show_admin_users_page():
    st.title("Gerenciar Usuários")
    st.markdown("---")

    st.subheader("Usuários cadastrados")
    users = list_users()
    if users:
        st.write(", ".join(users))
    else:
        st.info("Nenhum usuário cadastrado até o momento.")

    st.markdown("---")
    st.subheader("Criar novo usuário")

    col1, col2 = st.columns(2)

    with col1:
        username = st.text_input("Nome de usuário")
        password = st.text_input("Senha", type="password")
        confirm_password = st.text_input("Confirmar senha", type="password")

        if st.button("Criar usuário", type="primary"):
            if not username or not password or not confirm_password:
                st.error("Preencha todos os campos.")
            elif password != confirm_password:
                st.error("A confirmação da senha não confere.")
            else:
                created = create_user(username, password)
                if not created:
                    st.error("Não foi possível criar o usuário. Verifique se o nome já existe ou se os dados são válidos.")
                else:
                    st.success("Usuário criado com sucesso.")
                    st.rerun()

    with col2:
        st.info(
            "Usuários cadastrados aqui poderão fazer login na opção "
            "'Login Usuário' e utilizar os templates publicados."
        )

def render_preview_html(template_path: Path, context: dict) -> str:
    """
    Gera HTML de pré-visualização renderizando o DOCX e convertendo para HTML.
    """
    temp_dir = Path(tempfile.mkdtemp())
    temp_docx = temp_dir / "preview.docx"

    doc = DocxTemplate(str(template_path))
    doc.render(context)
    doc.save(str(temp_docx))

    with open(temp_docx, "rb") as f:
        result = mammoth.convert_to_html(f)
        return f"""
        <style>
            body {{
                background: #f6f6f6;
                margin: 0;
                padding: 16px;
                font-family: 'Segoe UI', sans-serif;
            }}
            .preview {{
                background: white;
                padding: 32px;
                border-radius: 8px;
                box-shadow: 0 4px 24px rgba(0,0,0,0.08);
                max-width: 900px;
                margin: auto;
            }}
        </style>
        <div class="preview">{result.value}</div>
        """


if __name__ == "__main__":
    main()
