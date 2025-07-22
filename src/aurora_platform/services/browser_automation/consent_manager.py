import logging
from playwright.async_api import Page, TimeoutError

logger = logging.getLogger(__name__)


class ConsentManager:
    """
    Gerencia o aceite de pop-ups de consentimento (cookies, LGPD, etc.)
    de forma genérica em páginas web.
    """

    def __init__(self):
        # Lista de seletores CSS/texto para botões de aceite comuns
        self.selectors = [
            "button:has-text('Aceitar todos')",
            "button:has-text('Aceitar')",
            "button:has-text('Accept All')",
            "button:has-text('Accept')",
            "button:has-text('Concordo')",
            "button:has-text('OK')",
            "button:has-text('Continuar')",
            "button#onetrust-accept-btn-handler",  # Seletor comum de plataformas de consentimento
        ]

    async def handle_consent(self, page: Page):
        """
        Tenta encontrar e clicar em um dos botões de consentimento conhecidos.
        """
        for selector in self.selectors:
            try:
                # Tenta encontrar o botão com um timeout curto para não atrasar a navegação
                button = page.locator(selector).first
                if await button.is_visible(timeout=2000):
                    await button.click()
                    logger.info(f"Consentimento aceito com o seletor: '{selector}'")
                    # Uma vez que um botão é clicado, podemos parar de procurar
                    return True
            except TimeoutError:
                logger.debug(
                    f"Seletor de consentimento não encontrado ou visível: '{selector}'"
                )
            except Exception as e:
                logger.warning(
                    f"Erro ao tentar clicar no consentimento com o seletor '{selector}': {e}"
                )
        return False
