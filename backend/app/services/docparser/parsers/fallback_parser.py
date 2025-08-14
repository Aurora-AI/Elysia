def parse_with_fallback(content: bytes) -> dict:
    """
    Parser fallback usando PyMuPDF e OCR simulado.
    TODO: Implementar OCR real com PaddleOCR.
    """
    return {
        "texto_markdown": "# Documento\n\nConteúdo extraído via fallback (simulado).",
        "tabelas": [],
        "imagens": []
    }
