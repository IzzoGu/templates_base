"""
Módulo de autenticação simples para área administrativa.
"""
import streamlit as st
import hashlib


# Senha padrão do admin (pode ser alterada via variável de ambiente)
DEFAULT_ADMIN_PASSWORD = "admin123"  # Mude isso em produção!


def hash_password(password: str) -> str:
    """Gera hash da senha."""
    return hashlib.sha256(password.encode()).hexdigest()


def check_admin_password(password: str) -> bool:
    """Verifica se a senha está correta."""
    # Em produção, use variável de ambiente ou arquivo de configuração seguro
    import os
    admin_password = os.getenv('ADMIN_PASSWORD', DEFAULT_ADMIN_PASSWORD)
    return password == admin_password


def is_admin() -> bool:
    """Verifica se o usuário atual é admin."""
    return st.session_state.get('is_admin', False)


def login_admin(password: str) -> bool:
    """Realiza login do admin."""
    if check_admin_password(password):
        st.session_state.is_admin = True
        return True
    return False


def logout_admin():
    """Realiza logout do admin."""
    st.session_state.is_admin = False


def require_admin():
    """Decorador/função para proteger páginas admin."""
    if not is_admin():
        st.error("Acesso negado. Faça login como administrador.")
        st.stop()
