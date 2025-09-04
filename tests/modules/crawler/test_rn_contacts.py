

def test_extract_basic_email_and_name():
    from aurora_platform.modules.crawler.rn_contacts.extract import extract_from_text

    html = "Secretária: Maria Lima — contato: compras@prefeitura.rn.gov.br"
    results = list(extract_from_text("https://prefeitura.rn.gov.br/x", "Compras", html))
    assert len(results) >= 1
    r = results[0]
    assert "email" in r and r["email"].endswith("@prefeitura.rn.gov.br")
    assert "name" in r and "Maria" in r["name"]


def test_official_domain():
    from aurora_platform.modules.crawler.rn_contacts.extract import is_official

    assert is_official("user@secretaria.rn.gov.br")
    assert is_official("foo@org.gov.br")
    assert not is_official("joe@gmail.com")
