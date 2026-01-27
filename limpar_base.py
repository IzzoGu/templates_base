"""
Script para limpar toda a base de dados da plataforma.
Remove todos os templates, documentos gerados e metadados.
"""
import shutil
from pathlib import Path


def limpar_base():
    """Remove todos os dados da plataforma."""
    
    print("Iniciando limpeza da base de dados...")
    
    # Diretórios e arquivos a limpar
    templates_dir = Path('templates')
    generated_docs_dir = Path('generated_docs')
    temp_dir = Path('temp')
    
    # Remove templates (exceto o diretório)
    if templates_dir.exists():
        print("Removendo templates...")
        for file in templates_dir.glob('*.docx'):
            file.unlink()
            print(f"  - Removido: {file.name}")
        
        metadata_file = templates_dir / 'metadata.json'
        if metadata_file.exists():
            metadata_file.unlink()
            print("  - Removido: metadata.json")
    
    # Remove documentos gerados
    if generated_docs_dir.exists():
        print("\nRemovendo documentos gerados...")
        internal_dir = generated_docs_dir / 'internal'
        if internal_dir.exists():
            for file in internal_dir.glob('*.docx'):
                file.unlink()
                print(f"  - Removido: {file.name}")
        
        metadata_file = generated_docs_dir / 'metadata.json'
        if metadata_file.exists():
            metadata_file.unlink()
            print("  - Removido: metadata.json")
    
    # Remove arquivos temporários
    if temp_dir.exists():
        print("\nRemovendo arquivos temporários...")
        shutil.rmtree(temp_dir)
        print("  - Diretório temp removido")
    
    print("\n" + "="*50)
    print("Limpeza concluída com sucesso!")
    print("="*50)
    print("\nA base de dados foi completamente zerada.")
    print("Os diretórios foram mantidos para uso futuro.")


if __name__ == "__main__":
    resposta = input("Tem certeza que deseja limpar TODA a base de dados? (sim/não): ")
    
    if resposta.lower() in ['sim', 's', 'yes', 'y']:
        limpar_base()
    else:
        print("Operação cancelada.")

