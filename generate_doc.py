import argparse
import json
from pathlib import Path

from docxtpl import DocxTemplate


def render_template(template_path: Path, context_path: Path, output_path: Path) -> None:
    if not template_path.exists():
        raise FileNotFoundError(f"Template não encontrado: {template_path}")
    if not context_path.exists():
        raise FileNotFoundError(f"Arquivo de contexto não encontrado: {context_path}")

    with context_path.open("r", encoding="utf-8") as fh:
        context = json.load(fh)

    doc = DocxTemplate(str(template_path))
    doc.render(context)
    doc.save(str(output_path))


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Preenche um template DOCX com dados JSON."
    )
    parser.add_argument(
        "--template",
        required=True,
        type=Path,
        help="Caminho do template DOCX (com placeholders Jinja).",
    )
    parser.add_argument(
        "--context",
        required=True,
        type=Path,
        help="Caminho do arquivo JSON com os dados a preencher.",
    )
    parser.add_argument(
        "--output",
        required=True,
        type=Path,
        help="Caminho de saída para o DOCX gerado.",
    )
    args = parser.parse_args()

    render_template(args.template, args.context, args.output)
    print(f"Documento gerado em: {args.output}")


if __name__ == "__main__":
    main()

