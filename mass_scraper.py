#!/usr/bin/env python3
"""Scraper massivo para teste de estresse - Rede Log RJ."""

import sys
import os
import requests
import time
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from collections import deque
import json

sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

class MassScraper:
    def __init__(self, base_url, max_pages=50):
        self.base_url = base_url
        self.domain = urlparse(base_url).netloc
        self.visited = set()
        self.to_visit = deque([base_url])
        self.max_pages = max_pages
        self.scraped_content = []
        
    def get_headers(self):
        return {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
            "Connection": "keep-alive"
        }
    
    def is_valid_url(self, url):
        parsed = urlparse(url)
        return (parsed.netloc == self.domain and 
                url not in self.visited and
                not url.endswith(('.pdf', '.jpg', '.png', '.gif', '.css', '.js')))
    
    def extract_links(self, soup, current_url):
        links = []
        for link in soup.find_all('a', href=True):
            full_url = urljoin(current_url, link['href'])
            if self.is_valid_url(full_url):
                links.append(full_url)
        return links
    
    def scrape_page(self, url):
        try:
            print(f"Scraping: {url}")
            response = requests.get(url, headers=self.get_headers(), timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove elementos desnecessários
            for element in soup(["script", "style", "nav", "footer", "header"]):
                element.decompose()
            
            # Extrair texto
            text = soup.get_text(separator='\n', strip=True)
            
            # Extrair links
            links = self.extract_links(soup, url)
            
            return text, links
            
        except Exception as e:
            print(f"Erro ao scraping {url}: {e}")
            return None, []
    
    def run(self):
        scraped_count = 0
        
        while self.to_visit and scraped_count < self.max_pages:
            url = self.to_visit.popleft()
            
            if url in self.visited:
                continue
                
            self.visited.add(url)
            text, links = self.scrape_page(url)
            
            if text:
                self.scraped_content.append({
                    'url': url,
                    'content': text[:5000],  # Limitar tamanho
                    'length': len(text)
                })
                scraped_count += 1
                
                # Adicionar novos links
                for link in links[:5]:  # Limitar links por página
                    if link not in self.visited:
                        self.to_visit.append(link)
            
            # Delay para não sobrecarregar
            time.sleep(2)
            
        print(f"\nScraping concluído: {scraped_count} páginas")
        return self.scraped_content

def ingest_to_api(content_list):
    """Ingere conteúdo via API."""
    api_url = "http://127.0.0.1:8000/api/v1/knowledge/ingest-from-web"
    
    success_count = 0
    for i, item in enumerate(content_list):
        try:
            print(f"Ingerindo {i+1}/{len(content_list)}: {item['url']}")
            
            response = requests.post(
                api_url,
                json={"url": item['url']},
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code in [200, 202]:
                success_count += 1
                print(f"[OK] Ingerido com sucesso")
            else:
                print(f"[ERRO] Status {response.status_code}")
                
            time.sleep(1)  # Delay entre ingestões
            
        except Exception as e:
            print(f"[ERRO] {e}")
    
    print(f"\nIngestão concluída: {success_count}/{len(content_list)} sucessos")

if __name__ == "__main__":
    print("[INICIO] TESTE DE ESTRESSE - REDE LOG RJ")
    
    # Scraping massivo
    scraper = MassScraper("https://redelog.rj.gov.br/redelog/", max_pages=20)
    content = scraper.run()
    
    # Salvar resultado
    with open("scraped_redelog.json", "w", encoding="utf-8") as f:
        json.dump(content, f, ensure_ascii=False, indent=2)
    
    print(f"\n[STATS] ESTATÍSTICAS:")
    print(f"- Páginas processadas: {len(content)}")
    print(f"- Total de caracteres: {sum(item['length'] for item in content)}")
    
    # Ingestão via API
    print("\n[API] INICIANDO INGESTÃO VIA API...")
    ingest_to_api(content[:10])  # Limitar a 10 para teste
    
    print("\n[OK] TESTE DE ESTRESSE CONCLUÍDO!")