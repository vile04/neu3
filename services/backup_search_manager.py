"""
Gerenciador de Busca com Sistema de Backup
Implementa múltiplas alternativas gratuitas para pesquisa de mercado
GARANTIA: Sempre obter dados reais, nunca simulados
"""
import logging
import time
import requests
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import json
import urllib.parse

logger = logging.getLogger(__name__)

@dataclass
class SearchResult:
    """Resultado individual de busca"""
    title: str
    url: str
    snippet: str
    source: str
    relevance_score: float = 0.0

@dataclass
class SearchResponse:
    """Resposta completa de busca"""
    results: List[SearchResult]
    total_found: int
    search_time: float
    service_used: str
    query: str
    success: bool = True

class BackupSearchManager:
    """
    Gerenciador inteligente de busca com múltiplas alternativas gratuitas
    Prioriza APIs gratuitas e implementa fallbacks automáticos
    """
    
    def __init__(self):
        self.search_engines = self._setup_search_engines()
        self.current_engine = 0
        self.max_retries = 3
        self.cache = {}  # Cache simples para evitar buscas duplicadas
        
    def _setup_search_engines(self) -> List[Dict[str, Any]]:
        """Configura múltiplos motores de busca em ordem de prioridade"""
        return [
            {
                'name': 'DuckDuckGo',
                'handler': self._search_duckduckgo,
                'is_free': True,
                'rate_limit': 1.0,  # segundos entre requisições
                'max_results': 20
            },
            {
                'name': 'Bing Search Free',
                'handler': self._search_bing_free,
                'is_free': True,
                'rate_limit': 2.0,
                'max_results': 15
            },
            {
                'name': 'SerpAPI Free',
                'handler': self._search_serpapi_free,
                'is_free': True,  # plano gratuito
                'rate_limit': 3.0,
                'max_results': 10,
                'requires_key': True
            },
            {
                'name': 'Google Custom Search',
                'handler': self._search_google_custom,
                'is_free': False,  # plano limitado
                'rate_limit': 1.0,
                'max_results': 10,
                'requires_key': True
            }
        ]
    
    def search_with_backup(self, query: str, num_results: int = 10) -> SearchResponse:
        """
        Executa busca com sistema de backup automático
        Tenta múltiplos motores até obter resultados válidos
        """
        start_time = time.time()
        
        # Verificar cache primeiro
        cache_key = f"{query}_{num_results}"
        if cache_key in self.cache:
            cached_result = self.cache[cache_key]
            if time.time() - cached_result['timestamp'] < 3600:  # 1 hora de cache
                logger.info(f"Resultado obtido do cache para: {query}")
                return cached_result['response']
        
        logger.info(f"Iniciando busca com backup para: '{query}'")
        
        # Tentar cada motor de busca em ordem
        for i, engine in enumerate(self.search_engines):
            try:
                logger.info(f"Tentando {engine['name']} (tentativa {i+1}/{len(self.search_engines)})")
                
                # Verificar se tem chave necessária
                if engine.get('requires_key') and not self._has_required_key(engine['name']):
                    logger.warning(f"Chave não disponível para {engine['name']}, pulando...")
                    continue
                
                # Aplicar rate limiting
                if engine.get('rate_limit'):
                    time.sleep(engine['rate_limit'])
                
                # Executar busca
                results = engine['handler'](query, min(num_results, engine['max_results']))
                
                if results and len(results) >= 3:  # Mínimo de 3 resultados válidos
                    search_time = time.time() - start_time
                    
                    response = SearchResponse(
                        results=results,
                        total_found=len(results),
                        search_time=search_time,
                        service_used=engine['name'],
                        query=query,
                        success=True
                    )
                    
                    # Salvar no cache
                    self.cache[cache_key] = {
                        'response': response,
                        'timestamp': time.time()
                    }
                    
                    logger.info(f"✓ Busca concluída com {engine['name']}: {len(results)} resultados")
                    return response
                else:
                    logger.warning(f"Resultados insuficientes de {engine['name']}: {len(results) if results else 0}")
                    
            except Exception as e:
                logger.warning(f"Erro em {engine['name']}: {str(e)}")
                continue
        
        # Se chegou aqui, todos os motores falharam
        search_time = time.time() - start_time
        logger.error("Todos os motores de busca falharam")
        
        return SearchResponse(
            results=[],
            total_found=0,
            search_time=search_time,
            service_used='none',
            query=query,
            success=False
        )
    
    def _search_duckduckgo(self, query: str, num_results: int) -> List[SearchResult]:
        """
        DuckDuckGo Search - Completamente gratuito
        Motor principal para buscas devido à ausência de rate limits rigorosos
        """
        try:
            from duckduckgo_search import DDGS
            
            results = []
            with DDGS() as ddgs:
                search_results = ddgs.text(
                    query,
                    max_results=num_results,
                    region='br-pt',  # Foco no Brasil
                    safesearch='moderate'
                )
                
                for result in search_results:
                    results.append(SearchResult(
                        title=result.get('title', ''),
                        url=result.get('href', ''),
                        snippet=result.get('body', ''),
                        source='DuckDuckGo',
                        relevance_score=self._calculate_relevance(query, result.get('title', '') + ' ' + result.get('body', ''))
                    ))
            
            # Ordenar por relevância
            results.sort(key=lambda x: x.relevance_score, reverse=True)
            return results[:num_results]
            
        except Exception as e:
            logger.error(f"Erro no DuckDuckGo: {e}")
            return []
    
    def _search_bing_free(self, query: str, num_results: int) -> List[SearchResult]:
        """
        Bing Search via scraping - Gratuito
        Alternativa quando DuckDuckGo falha
        """
        try:
            import urllib.parse
            import re
            
            # Construir URL de busca do Bing
            encoded_query = urllib.parse.quote_plus(query + " site:*.br OR site:*.com.br")
            url = f"https://www.bing.com/search?q={encoded_query}&count={num_results}&mkt=pt-BR"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            html = response.text
            results = []
            
            # Regex para extrair resultados (simplificado)
            title_pattern = r'<h2><a href="([^"]*)"[^>]*>([^<]*)</a></h2>'
            snippet_pattern = r'<p[^>]*>([^<]*)</p>'
            
            titles_urls = re.findall(title_pattern, html)
            snippets = re.findall(snippet_pattern, html)
            
            for i, (url, title) in enumerate(titles_urls[:num_results]):
                snippet = snippets[i] if i < len(snippets) else ""
                
                results.append(SearchResult(
                    title=title.strip(),
                    url=url.strip(),
                    snippet=snippet.strip(),
                    source='Bing Free',
                    relevance_score=self._calculate_relevance(query, title + ' ' + snippet)
                ))
            
            return results[:num_results]
            
        except Exception as e:
            logger.error(f"Erro no Bing Free: {e}")
            return []
    
    def _search_serpapi_free(self, query: str, num_results: int) -> List[SearchResult]:
        """
        SerpAPI com plano gratuito - 100 buscas/mês
        Usar apenas quando DuckDuckGo e Bing falham
        """
        try:
            import os
            
            api_key = os.environ.get('SERPAPI_KEY')
            if not api_key:
                logger.warning("SERPAPI_KEY não configurada")
                return []
            
            url = "https://serpapi.com/search"
            params = {
                'engine': 'google',
                'q': query + ' brazil',
                'api_key': api_key,
                'num': num_results,
                'hl': 'pt-br',
                'gl': 'br'
            }
            
            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            for item in data.get('organic_results', []):
                results.append(SearchResult(
                    title=item.get('title', ''),
                    url=item.get('link', ''),
                    snippet=item.get('snippet', ''),
                    source='SerpAPI',
                    relevance_score=self._calculate_relevance(query, item.get('title', '') + ' ' + item.get('snippet', ''))
                ))
            
            return results[:num_results]
            
        except Exception as e:
            logger.error(f"Erro no SerpAPI: {e}")
            return []
    
    def _search_google_custom(self, query: str, num_results: int) -> List[SearchResult]:
        """
        Google Custom Search - 100 buscas/dia grátis
        Fallback final com melhor qualidade
        """
        try:
            import os
            
            api_key = os.environ.get('GOOGLE_API_KEY')
            cse_id = os.environ.get('GOOGLE_CSE_ID')
            
            if not api_key or not cse_id:
                logger.warning("Google API keys não configuradas")
                return []
            
            url = "https://www.googleapis.com/customsearch/v1"
            params = {
                'key': api_key,
                'cx': cse_id,
                'q': query,
                'num': min(num_results, 10),  # Google limita a 10
                'lr': 'lang_pt',
                'gl': 'br'
            }
            
            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            for item in data.get('items', []):
                results.append(SearchResult(
                    title=item.get('title', ''),
                    url=item.get('link', ''),
                    snippet=item.get('snippet', ''),
                    source='Google Custom Search',
                    relevance_score=self._calculate_relevance(query, item.get('title', '') + ' ' + item.get('snippet', ''))
                ))
            
            return results[:num_results]
            
        except Exception as e:
            logger.error(f"Erro no Google Custom Search: {e}")
            return []
    
    def _has_required_key(self, engine_name: str) -> bool:
        """Verifica se as chaves necessárias estão disponíveis"""
        import os
        
        key_mapping = {
            'SerpAPI Free': 'SERPAPI_KEY',
            'Google Custom Search': ['GOOGLE_API_KEY', 'GOOGLE_CSE_ID']
        }
        
        required_keys = key_mapping.get(engine_name, [])
        if isinstance(required_keys, str):
            required_keys = [required_keys]
        
        for key in required_keys:
            if not os.environ.get(key):
                return False
        
        return True
    
    def _calculate_relevance(self, query: str, text: str) -> float:
        """
        Calcula score de relevância simples baseado em correspondências de palavras
        """
        if not text:
            return 0.0
        
        query_words = set(query.lower().split())
        text_words = set(text.lower().split())
        
        # Calcular interseção
        intersection = query_words.intersection(text_words)
        if not query_words:
            return 0.0
        
        # Score baseado na proporção de palavras encontradas
        base_score = len(intersection) / len(query_words)
        
        # Bonus por título vs snippet
        if 'title' in locals():  # Se for título, dar peso extra
            base_score *= 1.2
        
        # Penalizar textos muito curtos
        if len(text) < 50:
            base_score *= 0.7
        
        return min(1.0, base_score)
    
    def search_multiple_queries(self, queries: List[str], results_per_query: int = 5) -> Dict[str, SearchResponse]:
        """
        Executa múltiplas buscas de forma eficiente
        Útil para coletar dados abrangentes sobre um tópico
        """
        results = {}
        
        for i, query in enumerate(queries):
            logger.info(f"Executando busca {i+1}/{len(queries)}: {query}")
            
            try:
                response = self.search_with_backup(query, results_per_query)
                results[query] = response
                
                # Rate limiting entre buscas
                if i < len(queries) - 1:
                    time.sleep(2)
                    
            except Exception as e:
                logger.error(f"Erro na busca '{query}': {e}")
                results[query] = SearchResponse(
                    results=[],
                    total_found=0,
                    search_time=0,
                    service_used='error',
                    query=query,
                    success=False
                )
        
        return results
    
    def get_search_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas de uso dos motores de busca"""
        stats = {
            'cache_size': len(self.cache),
            'engines_available': len(self.search_engines),
            'free_engines': len([e for e in self.search_engines if e['is_free']]),
            'engines_with_keys': len([e for e in self.search_engines if e.get('requires_key') and self._has_required_key(e['name'])])
        }
        
        return stats
    
    def clear_cache(self):
        """Limpa o cache de resultados"""
        self.cache.clear()
        logger.info("Cache de busca limpo")
    
    def validate_search_results(self, results: List[SearchResult]) -> List[SearchResult]:
        """
        Valida e filtra resultados de busca
        Remove resultados com conteúdo insuficiente ou suspeito
        """
        validated_results = []
        
        for result in results:
            # Verificações básicas
            if not result.title or not result.snippet or not result.url:
                continue
            
            # Verificar se não é spam ou conteúdo de baixa qualidade
            if len(result.snippet) < 30:
                continue
            
            # Verificar se URL é válida
            if not result.url.startswith('http'):
                continue
            
            # Filtrar domínios suspeitos ou irrelevantes
            suspicious_domains = ['spam', 'ads', 'click', 'fake']
            if any(domain in result.url.lower() for domain in suspicious_domains):
                continue
            
            validated_results.append(result)
        
        logger.info(f"Validação: {len(results)} → {len(validated_results)} resultados válidos")
        return validated_results