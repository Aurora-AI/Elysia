# src/aurora_platform/services/deep_dive_scraper_service.py

import asyncio
import logging
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from async_lru import alru_cache

logger = logging.getLogger("DeepDiveScraperService")

class DeepDiveScraperService:
    """
    Serviço de scraping assíncrono e robusto, com encerramento de driver resiliente.
    """
    def __init__(self):
        pass

    def _blocking_scrape_logic(self, url: str) -> str:
        """
        Lógica de scraping síncrona que será executada em uma thread separada.
        """
        driver = None
        try:
            options = uc.ChromeOptions()
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            
            driver = uc.Chrome(options=options, use_subprocess=False)
            driver.get(url)
            
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            
            for tag in ['main', 'article', 'div[role="main"]', 'div[class*="content"]']:
                content = soup.select_one(tag)
                if content:
                    return content.get_text(separator='\n', strip=True)
            
            return soup.body.get_text(separator='\n', strip=True) if soup.body else ""
        finally:
            if driver:
                # --- CORREÇÃO DE ENCERRAMENTO RESILIENTE ---
                try:
                    driver.quit()
                except OSError as e:
                    # Ignora o erro WinError 6 que ocorre durante o shutdown
                    if "Identificador inválido" in str(e):
                        logger.debug("Ignorando erro de 'Identificador inválido' no encerramento do driver, pois o processo já foi finalizado.")
                    else:
                        logger.error(f"Erro inesperado ao encerrar o driver: {e}")
                # --- FIM DA CORREÇÃO ---


    def _validate_content_quality(self, text: str) -> bool:
        """Valida se o conteúdo extraído tem a qualidade mínima."""
        if len(text) < 200:
            logger.warning("Conteúdo descartado por ser muito curto.")
            return False
        return True

    @alru_cache(maxsize=128)
    @retry(
        stop=stop_after_attempt(3), 
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(Exception)
    )
    async def extract_text_from_url(self, url: str) -> str:
        """Orquestra a extração de forma assíncrona, com cache e retentativas."""
        logger.info(f"Iniciando extração assíncrona para: {url}")
        try:
            raw_text = await asyncio.to_thread(self._blocking_scrape_logic, url)
            
            if self._validate_content_quality(raw_text):
                logger.info(f"Conteúdo de qualidade validado para: {url}")
                return raw_text
            else:
                logger.warning(f"Conteúdo de baixa qualidade extraído de: {url}")
                return ""
                
        except Exception as e:
            logger.exception(f"Falha final ao extrair conteúdo de {url} após múltiplas tentativas. Erro: {e}")
            return ""