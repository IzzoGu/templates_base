"""
Módulo para gerenciamento de templates (upload, listagem, remoção).
"""
import json
import shutil
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
from template_analyzer import analyze_template


TEMPLATES_DIR = Path('templates')
METADATA_FILE = TEMPLATES_DIR / 'metadata.json'


def ensure_directories():
    """Garante que os diretórios necessários existem."""
    TEMPLATES_DIR.mkdir(exist_ok=True)
    Path('generated_docs').mkdir(exist_ok=True)
    Path('generated_docs/internal').mkdir(exist_ok=True)


def load_metadata() -> Dict[str, Any]:
    """Carrega metadados dos templates."""
    ensure_directories()
    if METADATA_FILE.exists():
        try:
            with open(METADATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}


def save_metadata(metadata: Dict[str, Any]):
    """Salva metadados dos templates."""
    ensure_directories()
    with open(METADATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)


def add_template(template_bytes: bytes, filename: str, description: str = "", published: bool = False) -> Dict[str, Any]:
    """
    Adiciona um novo template ao sistema.
    
    Args:
        template_bytes: Bytes do arquivo template
        filename: Nome do arquivo
        description: Descrição do template
        published: Se o template deve ser publicado (visível para usuários)
    
    Returns:
        Dict com informações do template adicionado.
    """
    ensure_directories()
    
    # Salva o arquivo
    template_path = TEMPLATES_DIR / filename
    with open(template_path, 'wb') as f:
        f.write(template_bytes)
    
    # Analisa o template
    try:
        analysis = analyze_template(template_path)
    except Exception as e:
        # Remove arquivo se análise falhar
        template_path.unlink()
        raise ValueError(f"Erro ao analisar template: {e}")
    
    # Carrega metadados existentes
    metadata = load_metadata()
    
    # Adiciona informações do template
    template_id = filename.replace('.docx', '').replace(' ', '_').lower()
    metadata[template_id] = {
        'filename': filename,
        'description': description,
        'uploaded_at': datetime.now().isoformat(),
        'fields': analysis['fields'],
        'field_count': analysis['field_count'],
        'has_loops': analysis['has_loops'],
        'published': published
    }
    
    save_metadata(metadata)
    
    return {
        'id': template_id,
        'filename': filename,
        'description': description,
        'fields': analysis['fields'],
        'field_count': analysis['field_count'],
        'published': published
    }


def list_templates(only_published: bool = False) -> List[Dict[str, Any]]:
    """
    Lista templates disponíveis.
    
    Args:
        only_published: Se True, retorna apenas templates publicados
    """
    metadata = load_metadata()
    templates = []
    
    for template_id, info in metadata.items():
        template_path = TEMPLATES_DIR / info['filename']
        if template_path.exists():
            # Verifica se deve filtrar apenas publicados
            if only_published:
                if info.get('published', False):
                    templates.append({
                        'id': template_id,
                        **info
                    })
            else:
                templates.append({
                    'id': template_id,
                    **info
                })
    
    return sorted(templates, key=lambda x: x.get('uploaded_at', ''), reverse=True)


def get_template(template_id: str) -> Optional[Dict[str, Any]]:
    """Obtém informações de um template específico."""
    metadata = load_metadata()
    if template_id in metadata:
        info = metadata[template_id].copy()
        info['id'] = template_id
        template_path = TEMPLATES_DIR / info['filename']
        if template_path.exists():
            info['path'] = str(template_path)
            return info
    return None


def delete_template(template_id: str) -> bool:
    """Remove um template do sistema."""
    metadata = load_metadata()
    
    if template_id not in metadata:
        return False
    
    # Remove arquivo
    filename = metadata[template_id]['filename']
    template_path = TEMPLATES_DIR / filename
    if template_path.exists():
        template_path.unlink()
    
    # Remove dos metadados
    del metadata[template_id]
    save_metadata(metadata)
    
    return True


def toggle_template_publication(template_id: str) -> bool:
    """Alterna o status de publicação de um template."""
    metadata = load_metadata()
    
    if template_id not in metadata:
        return False
    
    # Alterna status de publicação
    current_status = metadata[template_id].get('published', False)
    metadata[template_id]['published'] = not current_status
    save_metadata(metadata)
    
    return True


def update_template_publication(template_id: str, published: bool) -> bool:
    """Atualiza o status de publicação de um template."""
    metadata = load_metadata()
    
    if template_id not in metadata:
        return False
    
    metadata[template_id]['published'] = published
    save_metadata(metadata)
    
    return True

