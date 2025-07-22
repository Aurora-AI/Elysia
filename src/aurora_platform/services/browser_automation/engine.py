import logging
from playwright.async_api import async_playwright, Page
from .consent_manager import ConsentManager
from .local_llm_service import LocalLLMService

logger = logging.getLogger(__name__)


class BrowserEngine:
    """
    Motor de automação de navegador para navegação segura, extração
    e processamento de conteúdo.
    """

    def __init__(self):
        self.llm_service = LocalLLMService()
        self.consent_manager = ConsentManager()

    async def _extract_main_text(self, page: Page) -> str:
        """Usa JavaScript para extrair o texto principal, removendo ruído."""
        try:
            text = await page.evaluate(
                """() => {
                document.querySelectorAll('script, style, nav, header, footer, aside').forEach(el => el.remove());
                return document.body.innerText;
            }"""
            )
            return text.strip()
        except Exception as e:
            logger.error(f"Falha ao executar script de extração de texto: {e}")
            return ""

    async def fetch_and_summarize(self, url: str) -> dict:
        """
        Navega até a URL, lida com consentimento e sumariza o conteúdo principal.
        """
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True, args=["--disable-blink-features=AutomationControlled"]
            )
            page = await browser.new_page()
            try:
                logger.info(f"Navegando para: {url}")
                await page.goto(url, timeout=30000, wait_until="domcontentloaded")

                # Lida com pop-ups de consentimento
                await self.consent_manager.handle_consent(page)

                # Extrai o texto limpo
                text_content = await self._extract_main_text(page)

                if not text_content:
                    logger.warning(f"Nenhum conteúdo principal extraído de {url}")
                    return {
                        "url": url,
                        "summary": "Não foi possível extrair conteúdo textual da página.",
                        "raw_text_snippet": "",
                    }

                # Sumariza o conteúdo com o SLM local
                summary = self.llm_service.summarize(text_content)

                return {
                    "url": url,
                    "summary": summary,
                    "raw_text_snippet": text_content[:500]
                    + "...",  # Retorna um trecho para verificação
                }
            except Exception as e:
                logger.exception(
                    f"Erro durante o processo de fetch_and_summarize para {url}: {e}"
                )
                raise
            finally:
                await browser.close()
