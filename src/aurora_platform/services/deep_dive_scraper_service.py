from firecrawl import FirecrawlApp
from typing import List, Dict, Any
import os

async def scrape_url(url: str) -> List[Dict[str, Any]]:
    """
    Extrai conteúdo de uma URL usando FireCrawl.
    """
    try:
        app = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY", "fc-demo"))
        result = app.scrape_url(url, params={'formats': ['markdown']})
        
        if result and 'markdown' in result:
            return [{
                'markdown': result['markdown'],
                'metadata': result.get('metadata', {'sourceURL': url})
            }]
        return []
    except Exception as e:
        print(f"Erro ao fazer scraping da URL {url}: {e}")
        return []