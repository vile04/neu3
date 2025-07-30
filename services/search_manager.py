import os
import requests
import json
import logging
from .web_scraper import WebScraper
import time

class SearchManager:
    def __init__(self):
        self.google_api_key = os.environ.get("GOOGLE_SEARCH_KEY")
        self.google_cse_id = os.environ.get("GOOGLE_CSE_ID")
        self.serper_api_key = os.environ.get("SERPER_API_KEY")
        self.jina_api_key = os.environ.get("JINA_API_KEY")
        self.scrapingant_api_key = os.environ.get("SCRAPINGANT_API_KEY")
        self.web_scraper = WebScraper()

    def comprehensive_search(self, queries):
        """Perform comprehensive search using multiple engines"""
        all_results = []
        
        for query in queries:
            try:
                # Google Custom Search
                google_results = self._google_search(query)
                all_results.extend(google_results)
                
                # Serper API
                serper_results = self._serper_search(query)
                all_results.extend(serper_results)
                
                # Small delay to respect rate limits
                time.sleep(0.5)
                
            except Exception as e:
                logging.error(f"Search error for query '{query}': {str(e)}")
        
        # Remove duplicates and extract content
        unique_results = self._deduplicate_results(all_results)
        enriched_results = self._enrich_with_content(unique_results[:20])  # Limit to top 20
        
        return enriched_results

    def _google_search(self, query):
        """Search using Google Custom Search API"""
        try:
            if not self.google_api_key or not self.google_cse_id:
                return []
            
            url = "https://www.googleapis.com/customsearch/v1"
            params = {
                'key': self.google_api_key,
                'cx': self.google_cse_id,
                'q': query,
                'num': 10
            }
            
            response = requests.get(url, params=params)
            data = response.json()
            
            results = []
            if 'items' in data:
                for item in data['items']:
                    results.append({
                        'title': item.get('title', ''),
                        'url': item.get('link', ''),
                        'snippet': item.get('snippet', ''),
                        'source': 'google'
                    })
            
            return results
            
        except Exception as e:
            logging.error(f"Google search error: {str(e)}")
            return []

    def _serper_search(self, query):
        """Search using Serper API"""
        try:
            if not self.serper_api_key:
                return []
            
            url = "https://google.serper.dev/search"
            headers = {
                'X-API-KEY': self.serper_api_key,
                'Content-Type': 'application/json'
            }
            payload = json.dumps({
                "q": query,
                "num": 10
            })
            
            response = requests.post(url, headers=headers, data=payload)
            data = response.json()
            
            results = []
            if 'organic' in data:
                for item in data['organic']:
                    results.append({
                        'title': item.get('title', ''),
                        'url': item.get('link', ''),
                        'snippet': item.get('snippet', ''),
                        'source': 'serper'
                    })
            
            return results
            
        except Exception as e:
            logging.error(f"Serper search error: {str(e)}")
            return []

    def _deduplicate_results(self, results):
        """Remove duplicate URLs"""
        seen_urls = set()
        unique_results = []
        
        for result in results:
            url = result.get('url', '')
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_results.append(result)
        
        return unique_results

    def _enrich_with_content(self, results):
        """Extract full content from URLs"""
        enriched = []
        
        for result in results:
            try:
                url = result.get('url', '')
                if url:
                    # Extract content using web scraper
                    content = self.web_scraper.extract_content(url)
                    
                    if content and len(content.strip()) > 100:  # Only keep substantial content
                        result['content'] = content
                        result['content_length'] = len(content)
                        enriched.append(result)
                
            except Exception as e:
                logging.error(f"Content extraction error for {result.get('url', '')}: {str(e)}")
                # Keep result even if content extraction fails
                enriched.append(result)
        
        return enriched

    def search_specific_domain(self, query, domain):
        """Search within a specific domain"""
        domain_query = f"site:{domain} {query}"
        return self.comprehensive_search([domain_query])

    def search_by_type(self, query, content_type="news"):
        """Search for specific content types"""
        if content_type == "news":
            news_query = f"{query} news OR articles OR reports"
        elif content_type == "academic":
            news_query = f"{query} research OR study OR academic OR paper"
        elif content_type == "social":
            news_query = f"{query} twitter OR reddit OR forum OR discussion"
        else:
            news_query = query
        
        return self.comprehensive_search([news_query])
