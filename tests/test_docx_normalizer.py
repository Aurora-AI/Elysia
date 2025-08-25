from scripts.docx_to_json import normalize_text_to_json


def test_normalize_heading_and_paragraph():
    text = "TITLE\n\nThis is a paragraph explaining the title.\n\nANOTHER HEADING\n\nMore details."
    obj = normalize_text_to_json(text)
    assert 'blocks' in obj
    types = [b['type'] for b in obj['blocks']]
    assert types == ['heading', 'paragraph', 'heading', 'paragraph']
