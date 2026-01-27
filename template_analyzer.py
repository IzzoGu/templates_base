"""
Módulo para análise de templates DOCX e extração de campos/variáveis.
"""
import re
from collections import OrderedDict
from typing import Dict, List, Any
from pathlib import Path
from docx import Document


def extract_jinja_variables(text: str) -> List[str]:
    """
    Extrai variáveis Jinja2 de um texto.
    Retorna uma lista mantendo a ordem de aparecimento no template.
    """
    ordered_vars: "OrderedDict[str, None]" = OrderedDict()
    
    # Padrão para {{ variavel }} ou {{ variavel.atributo }}
    pattern = r'\{\{\s*([a-zA-Z_][a-zA-Z0-9_.]*)\s*\}\}'
    for match in re.finditer(pattern, text):
        # Remove atributos para pegar apenas a variável base
        var_name = match.group(1).split('.')[0]
        ordered_vars.setdefault(var_name, None)
    
    # Padrão para loops {% for item in items %}
    loop_pattern = r'\{\%\s*for\s+(\w+)\s+in\s+(\w+)\s*\%\}'
    for match in re.finditer(loop_pattern, text):
        list_var = match.group(2)
        ordered_vars.setdefault(list_var, None)
    
    return list(ordered_vars.keys())


def analyze_template(template_path: Path) -> Dict[str, Any]:
    """
    Analisa um template DOCX e retorna informações sobre os campos necessários.
    
    Returns:
        Dict com informações do template incluindo:
        - name: nome do arquivo
        - fields: lista de campos encontrados
        - has_loops: se tem loops
    """
    try:
        doc = Document(str(template_path))
        all_text = []
        
        # Extrai texto de todos os parágrafos
        for paragraph in doc.paragraphs:
            all_text.append(paragraph.text)
        
        # Extrai texto de tabelas
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    all_text.append(cell.text)
        
        full_text = '\n'.join(all_text)
        
        # Extrai variáveis
        variables = extract_jinja_variables(full_text)
        
        # Identifica loops
        has_loops = bool(re.search(r'\{\%\s*for\s+', full_text))
        
        return {
            'name': template_path.name,
            'path': str(template_path),
            'fields': variables,
            'has_loops': has_loops,
            'field_count': len(variables)
        }
    except Exception as e:
        raise ValueError(f"Erro ao analisar template: {e}")


def analyze_template_from_bytes(template_bytes: bytes, filename: str) -> Dict[str, Any]:
    """
    Analisa um template DOCX a partir de bytes em memória.
    """
    # Salva temporariamente para análise
    temp_path = Path('temp') / filename
    temp_path.parent.mkdir(exist_ok=True)
    
    try:
        with open(temp_path, 'wb') as f:
            f.write(template_bytes)
        
        result = analyze_template(temp_path)
        return result
    finally:
        # Remove arquivo temporário
        if temp_path.exists():
            temp_path.unlink()

