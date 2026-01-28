"""
Módulo para geração automática de formulários baseados nos campos do template.
"""
import streamlit as st
from typing import Dict, Any, List
from datetime import datetime


_TRANSLATIONS = {
    "name": "Nome",
    "nome": "Nome",
    "email": "E-mail",
    "phone": "Telefone",
    "telefone": "Telefone",
    "date": "Data",
    "data": "Data",
    "cpf": "CPF",
    "cnpj": "CNPJ",
    "address": "Endereço",
    "endereco": "Endereço",
    "city": "Cidade",
    "cidade": "Cidade",
    "state": "Estado",
    "estado": "Estado",
    "zip": "CEP",
    "cep": "CEP",
    "description": "Descrição",
    "descricao": "Descrição",
    "value": "Valor",
    "valor": "Valor",
    "price": "Preço",
    "preco": "Preço",
    "total": "Total",
    "quantity": "Quantidade",
    "quantidade": "Quantidade",
    "qtd": "Quantidade",
    "qty": "Quantidade",
    "client": "Cliente",
    "cliente": "Cliente",
    "customer": "Cliente",
    "service": "Serviço",
    "servico": "Serviço",
    "contract": "Contrato",
    "contrato": "Contrato",
    "note": "Observação",
    "observacao": "Observação",
    "observation": "Observação",
    "detail": "Detalhe",
    "detalhe": "Detalhe",
    "text": "Texto",
    "texto": "Texto",
    "comment": "Comentário",
    "comentario": "Comentário",
    "justification": "Justificativa",
    "justificativa": "Justificativa",
}


def _translate_field_name(field_name: str) -> str:
    """
    Traduz o nome do campo para português.
    Se o campo contém underscores, traduz cada parte separadamente.
    """
    parts = field_name.lower().split('_')
    translated_parts = []
    
    for part in parts:
        # Remove espaços e caracteres especiais
        clean_part = part.strip()
        if clean_part in _TRANSLATIONS:
            translated_parts.append(_TRANSLATIONS[clean_part])
        else:
            # Se não encontrar tradução, capitaliza a primeira letra
            translated_parts.append(clean_part.capitalize())
    
    return " ".join(translated_parts)


def _render_text_input(label: str, field: str, *, key: str, help_text: str | None = None) -> Any:
    """
    Renderiza o campo de texto adequado para permitir quebras de linha quando necessário.
    Por padrão usa text_area para permitir tópicos e múltiplas linhas.
    """
    multiline_keywords = ["descricao", "observacao", "detalhe", "texto", "nota", "coment", "justificativa"]
    if any(keyword in field.lower() for keyword in multiline_keywords):
        return st.text_area(label, key=key, help=help_text, height=130)
    return st.text_area(label, key=key, help=help_text, height=70)


def generate_form_from_fields(fields: List[str], template_info: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Gera um formulário Streamlit baseado nos campos do template.
    
    Returns:
        Dict com os valores preenchidos no formulário.
    """
    form_data = {}
    
    if template_info:
        st.subheader(f"{template_info.get('filename', 'Template')}")
        if template_info.get('description'):
            st.caption(template_info['description'])
        st.divider()
    
    # Agrupa campos relacionados (ex: cliente_nome, cliente_cpf)
    grouped_fields = {}
    simple_fields = []
    
    for field in fields:
        if '_' in field:
            prefix = field.split('_')[0]
            if prefix not in grouped_fields:
                grouped_fields[prefix] = []
            grouped_fields[prefix].append(field)
        else:
            simple_fields.append(field)
    
    # Campos simples primeiro
    if simple_fields:
        st.markdown("### Informações Gerais")
        cols = st.columns(2)
        
        for idx, field in enumerate(simple_fields):
            col = cols[idx % 2]
            with col:
                label = _translate_field_name(field)
                
                if 'email' in field.lower():
                    form_data[field] = st.text_input(label, key=f"field_{field}")
                elif 'data' in field.lower() or 'date' in field.lower():
                    form_data[field] = st.date_input(label, key=f"field_{field}")
                elif 'telefone' in field.lower() or 'phone' in field.lower() or 'fone' in field.lower():
                    form_data[field] = st.text_input(label, key=f"field_{field}", help="Formato: (XX) XXXXX-XXXX")
                elif 'cpf' in field.lower() or 'cnpj' in field.lower():
                    form_data[field] = st.text_input(label, key=f"field_{field}", help="Apenas números")
                elif 'valor' in field.lower() or 'preco' in field.lower() or 'total' in field.lower() or 'price' in field.lower():
                    form_data[field] = st.number_input(label, min_value=0.0, step=0.01, key=f"field_{field}", format="%.2f")
                elif 'quantidade' in field.lower() or 'qtd' in field.lower() or 'quantidade' in field.lower():
                    form_data[field] = st.number_input(label, min_value=0, step=1, key=f"field_{field}")
                else:
                    form_data[field] = _render_text_input(label, field, key=f"field_{field}")
    
    # Campos agrupados
    for prefix, prefix_fields in grouped_fields.items():
        if len(prefix_fields) > 1:
            st.markdown(f"### {_translate_field_name(prefix)}")
            cols = st.columns(2)
            
            for idx, field in enumerate(prefix_fields):
                col = cols[idx % 2]
                with col:
                    # Remove o prefixo do campo para criar o label
                    field_without_prefix = field.replace(f"{prefix}_", "", 1)
                    label = _translate_field_name(field_without_prefix)
                    if not label or label.lower() == prefix.lower():
                        label = _translate_field_name(field)
                    
                    if 'email' in field.lower():
                        form_data[field] = st.text_input(label, key=f"field_{field}")
                    elif 'data' in field.lower() or 'date' in field.lower():
                        form_data[field] = st.date_input(label, key=f"field_{field}")
                    elif 'telefone' in field.lower() or 'phone' in field.lower() or 'fone' in field.lower():
                        form_data[field] = st.text_input(label, key=f"field_{field}", help="Formato: (XX) XXXXX-XXXX")
                    elif 'cpf' in field.lower() or 'cnpj' in field.lower():
                        form_data[field] = st.text_input(label, key=f"field_{field}", help="Apenas números")
                    elif 'valor' in field.lower() or 'preco' in field.lower() or 'total' in field.lower():
                        form_data[field] = st.number_input(label, min_value=0.0, step=0.01, key=f"field_{field}", format="%.2f")
                    elif 'quantidade' in field.lower() or 'qtd' in field.lower():
                        form_data[field] = st.number_input(label, min_value=0, step=1, key=f"field_{field}")
                    else:
                        form_data[field] = _render_text_input(label, field, key=f"field_{field}")
        else:
            # Se só tem um campo no grupo, trata como simples
            field = prefix_fields[0]
            label = _translate_field_name(field)
            form_data[field] = _render_text_input(label, field, key=f"field_{field}")
    
    return form_data


def format_field_value(value: Any) -> Any:
    """Formata valores para o contexto do template."""
    if isinstance(value, datetime):
        return value.strftime('%d/%m/%Y')
    return value

