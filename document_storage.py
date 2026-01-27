"""
Módulo para gerenciamento de documentos gerados (armazenamento interno e download).
"""
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
import io


INTERNAL_DIR = Path('generated_docs/internal')
METADATA_FILE = Path('generated_docs/metadata.json')


def ensure_directories():
    """Garante que os diretórios necessários existem."""
    INTERNAL_DIR.mkdir(parents=True, exist_ok=True)


def load_documents_metadata() -> Dict[str, Any]:
    """Carrega metadados dos documentos gerados."""
    ensure_directories()
    if METADATA_FILE.exists():
        try:
            with open(METADATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}


def save_documents_metadata(metadata: Dict[str, Any]):
    """Salva metadados dos documentos gerados."""
    ensure_directories()
    with open(METADATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)


def save_generated_document(
    document_bytes: bytes,
    template_id: str,
    template_name: str,
    filename: str,
    form_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Salva um documento gerado internamente e retorna informações sobre ele.
    
    Returns:
        Dict com informações do documento salvo incluindo caminho interno.
    """
    ensure_directories()
    
    # Cria nome único baseado em timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    safe_filename = filename.replace('.docx', '')
    internal_filename = f"{timestamp}_{safe_filename}.docx"
    internal_path = INTERNAL_DIR / internal_filename
    
    # Salva arquivo interno
    with open(internal_path, 'wb') as f:
        f.write(document_bytes)
    
    # Carrega metadados
    metadata = load_documents_metadata()
    
    # Adiciona informações do documento
    doc_id = f"{timestamp}_{template_id}"
    metadata[doc_id] = {
        'template_id': template_id,
        'template_name': template_name,
        'filename': filename,
        'internal_filename': internal_filename,
        'internal_path': str(internal_path),
        'generated_at': datetime.now().isoformat(),
        'form_data': form_data
    }
    
    save_documents_metadata(metadata)
    
    return {
        'id': doc_id,
        'filename': filename,
        'internal_path': str(internal_path),
        'generated_at': metadata[doc_id]['generated_at']
    }


def list_generated_documents(limit: int = 50) -> List[Dict[str, Any]]:
    """Lista documentos gerados recentemente."""
    metadata = load_documents_metadata()
    documents = []
    
    for doc_id, info in metadata.items():
        internal_path = Path(info['internal_path'])
        if internal_path.exists():
            documents.append({
                'id': doc_id,
                **info
            })
    
    # Ordena por data de geração (mais recentes primeiro)
    documents.sort(key=lambda x: x.get('generated_at', ''), reverse=True)
    
    return documents[:limit]


def get_document(doc_id: str) -> Optional[Dict[str, Any]]:
    """Obtém informações e bytes de um documento gerado."""
    metadata = load_documents_metadata()
    
    if doc_id not in metadata:
        return None
    
    info = metadata[doc_id].copy()
    internal_path = Path(info['internal_path'])
    
    if not internal_path.exists():
        return None
    
    # Lê bytes do arquivo
    with open(internal_path, 'rb') as f:
        info['bytes'] = f.read()
    
    return info


def delete_document(doc_id: str) -> bool:
    """Remove um documento gerado."""
    metadata = load_documents_metadata()
    
    if doc_id not in metadata:
        return False
    
    # Remove arquivo
    internal_path = Path(metadata[doc_id]['internal_path'])
    if internal_path.exists():
        internal_path.unlink()
    
    # Remove dos metadados
    del metadata[doc_id]
    save_documents_metadata(metadata)
    
    return True

