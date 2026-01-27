import json
from pathlib import Path

import streamlit as st


DEFAULT_ADMIN_PASSWORD = "admin123"
ADMIN_CONFIG_FILE = Path("admin_config.json")
USERS_CONFIG_FILE = Path("users_config.json")


def _load_admin_config() -> dict:
    if ADMIN_CONFIG_FILE.exists():
        try:
            with open(ADMIN_CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def _save_admin_config(config: dict) -> None:
    with open(ADMIN_CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def get_admin_password() -> str:
    config = _load_admin_config()
    if "password" in config and config["password"]:
        return config["password"]
    return DEFAULT_ADMIN_PASSWORD


def set_admin_password(new_password: str) -> None:
    config = _load_admin_config()
    config["password"] = new_password
    _save_admin_config(config)


def check_admin_password(password: str) -> bool:
    return password == get_admin_password()


def is_admin() -> bool:
    return st.session_state.get("is_admin", False)


def login_admin(password: str) -> bool:
    if check_admin_password(password):
        st.session_state.is_admin = True
        return True
    return False


def logout_admin() -> None:
    st.session_state.is_admin = False


def require_admin() -> None:
    if not is_admin():
        st.error("Acesso negado. Faça login como administrador.")
        st.stop()


def _load_users() -> dict:
    if USERS_CONFIG_FILE.exists():
        try:
            with open(USERS_CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    return data
        except Exception:
            return {}
    return {}


def _save_users(users: dict) -> None:
    with open(USERS_CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2, ensure_ascii=False)


def list_users() -> list[str]:
    users = _load_users()
    return sorted(users.keys())


def create_user(username: str, password: str) -> bool:
    username = username.strip()
    if not username or not password:
        return False

    users = _load_users()
    if username in users:
        return False

    users[username] = {"password": password}
    _save_users(users)
    return True


def authenticate_user(username: str, password: str) -> bool:
    users = _load_users()
    info = users.get(username)
    if not info:
        return False
    return info.get("password") == password


def login_user(username: str, password: str) -> bool:
    if authenticate_user(username, password):
        st.session_state.user = username
        return True
    return False


def logout_user() -> None:
    st.session_state.user = None


def get_current_user() -> str | None:
    return st.session_state.get("user")


def is_user_logged_in() -> bool:
    return get_current_user() is not None
