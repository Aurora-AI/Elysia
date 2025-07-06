# src/aurora_platform/services/deep_dive_scraper_service.py
import asyncio
import os
import hashlib
from firecrawl import FirecrawlApp
from src.aurora_platform.core.config import settings

async def scrape_url(url: str) -> list:
    """Realiza scraping de uma URL usando Firecrawl e retorna os dados extraídos."""
    try:
        # Inicializa o cliente Firecrawl com a chave de API
        app = FirecrawlApp(api_key=settings.FIRECRAWL_API_KEY.get_secret_value())
        
        # Realiza o scraping da URL
        result = app.scrape_url(url=url)
        
        # Retorna os dados extraídos
        return [result] if result else []
        
    except Exception as e:
        print(f"Erro durante o scraping da URL {url}: {e}")
        return []

async def scrape_and_save_url(url: str, output_dir: str) -> str:
    """Realiza scraping de uma URL e salva o conteúdo em arquivo de texto."""
    try:
        # Cria o diretório se não existir
        os.makedirs(output_dir, exist_ok=True)
        
        # Inicializa o cliente Firecrawl
        app = FirecrawlApp(api_key=settings.FIRECRAWL_API_KEY.get_secret_value())
        
        # Realiza o scraping
        result = app.scrape_url(url=url)
        
        if result and 'content' in result:
            # Gera nome do arquivo baseado na URL
            url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
            filename = f"scraped_{url_hash}.txt"
            filepath = os.path.join(output_dir, filename)
            
            # Salva o conteúdo em arquivo
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(result['content'])
            
            return filepath
        else:
            raise Exception("Nenhum conteúdo foi extraído da URL")
            
    except Exception as e:
        print(f"Erro durante o scraping e salvamento da URL {url}: {e}")
        raise

if __name__ == '__main__':
    from dotenv import load_dotenv
    load_dotenv()
    
    # Exemplo de uso
    example_url = "https://docs.firecrawl.dev/"
    result = asyncio.run(scrape_url(example_url))
    print(f"Resultado do scraping: {result}")