# src/aurora_platform/services/deep_dive_scraper_service.py
import asyncio
import os
import time
import hashlib
import logging
from firecrawl import FirecrawlApp
from typing import Dict, Any, List, cast
from src.aurora_platform.core.config import settings

# Configuração do logger
logger = logging.getLogger(__name__)

async def scrape_url(url: str) -> List[Dict[str, Any]]:
    """Realiza scraping de uma URL usando Firecrawl e retorna os dados extraídos."""
    try:
        # Inicializa o cliente Firecrawl com a chave de API
        app = FirecrawlApp(api_key=settings.FIRECRAWL_API_KEY.get_secret_value())
        
        # Realiza o scraping da URL
        result = app.scrape_url(url=url)
        
        # Converte para dicionário se necessário
        if hasattr(result, '__dict__'):
            result_dict = {
                'content': getattr(result, 'content', ''),
                'markdown': getattr(result, 'markdown', ''),
                'url': getattr(result, 'url', url),
                'metadata': getattr(result, 'metadata', {})
            }
        elif isinstance(result, dict):
            result_dict = result
        else:
            result_dict = {'content': str(result) if result else ''}
        
        return [result_dict] if result_dict else []
        
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
        
        # Extrai conteúdo de diferentes estruturas possíveis
        content = None
        if hasattr(result, 'content'):
            content = result.content
        elif hasattr(result, 'markdown'):
            content = result.markdown
        elif isinstance(result, dict):
            content = result.get('content') or result.get('markdown')
        
        if content:
            # Gera nome do arquivo baseado na URL
            url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
            filename = f"scraped_{url_hash}.txt"
            filepath = os.path.join(output_dir, filename)
            
            # Salva o conteúdo em arquivo
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(str(content))
            
            return filepath
        else:
            raise Exception("Nenhum conteúdo foi extraído da URL")
            
    except Exception as e:
        print(f"Erro durante o scraping e salvamento da URL {url}: {e}")
        raise

def crawl_and_save(url: str, output_dir: str = "data/crawled") -> str:
    """Realiza crawling assíncrono de uma URL e salva o conteúdo em arquivos Markdown."""
    try:
        # Cria o diretório se não existir
        os.makedirs(output_dir, exist_ok=True)
        
        # Lê a chave de API das configurações
        api_key = settings.FIRECRAWL_API_KEY.get_secret_value()
        
        # Inicializa o cliente Firecrawl
        logger.info(f"Usando chave Firecrawl: {api_key[:8]}...")
        app = FirecrawlApp(api_key=api_key)
        
        # Inicia o job de crawling
        logger.info(f"Iniciando crawling de: {url}")
        crawl_response = app.crawl_url(url)
        
        # Verifica se é resposta síncrona (já concluída) ou assíncrona (com job_id)
        status = getattr(crawl_response, 'status', None)
        
        if status == 'completed':
            # Resposta síncrona - dados já disponíveis
            logger.info("Crawling concluído diretamente (resposta síncrona)!")
            status_response = crawl_response
        else:
            # Resposta assíncrona - precisa fazer polling
            job_id = getattr(crawl_response, 'jobId', None) or getattr(crawl_response, 'job_id', None)
            
            if not job_id:
                raise Exception("Não foi possível obter job_id do Firecrawl")
            
            logger.info(f"Job ID: {job_id}")
            
            # Loop de polling para verificar status
            while True:
                status_response = app.check_crawl_status(job_id)
                status = getattr(status_response, 'status', None)
                
                logger.info(f"Status do job: {status}... aguardando...")
                
                if status == 'completed':
                    logger.info("Crawling concluído!")
                    break
                elif status == 'failed':
                    error_msg = getattr(status_response, 'error', 'Erro desconhecido')
                    raise Exception(f"Job de crawling falhou: {error_msg}")
                elif status in ['pending', 'scraping']:
                    time.sleep(10)  # Aguarda 10 segundos antes da próxima verificação
                else:
                    raise Exception(f"Status desconhecido: {status}")
        
        # Extrai os dados do resultado final
        data = getattr(status_response, 'data', [])
        if not data:
            raise Exception("Nenhum dado foi extraído do crawling")
        
        # Salva cada página em arquivo Markdown separado
        saved_files = []
        for i, page_data in enumerate(data):
            # Acessa atributos do objeto FirecrawlDocument
            content = getattr(page_data, 'markdown', '') or getattr(page_data, 'content', '')
            page_url = getattr(page_data, 'url', None)
            
            # Se não tem URL direta, tenta pegar dos metadados
            if not page_url:
                metadata = getattr(page_data, 'metadata', {})
                page_url = metadata.get('url', url) if isinstance(metadata, dict) else url
            
            # Gera nome do arquivo baseado na URL
            url_hash = hashlib.md5(str(page_url).encode()).hexdigest()[:8]
            filename = f"crawled_{url_hash}_{i}.md"
            filepath = os.path.join(output_dir, filename)
            
            # Obtém título dos metadados se disponível
            title = 'Página Extraída'
            metadata = getattr(page_data, 'metadata', {})
            if isinstance(metadata, dict) and 'title' in metadata:
                title = metadata['title']
            
            # Salva o conteúdo em formato Markdown
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"# {title}\n\n")
                f.write(f"**URL:** {page_url}\n\n")
                f.write(f"---\n\n")
                f.write(content)
            
            saved_files.append(filepath)
            logger.info(f"Salvo: {filepath}")
        
        success_msg = f"Crawling concluído. {len(saved_files)} arquivos salvos em {output_dir}"
        logger.info(success_msg)
        return success_msg
        
    except Exception as e:
        error_msg = f"Erro durante o crawling da URL {url}: {e}"
        logger.error(error_msg)
        raise Exception(error_msg)

if __name__ == '__main__':
    # Configuração básica do logging para teste
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Exemplo de uso do crawling com depuração
    example_url = "https://example.com"
    try:
        result = crawl_and_save(example_url)
        logger.info(f"Resultado: {result}")
    except Exception as e:
        logger.error(f"Erro: {e}")