import trafilatura
import requests
import logging
from urllib.parse import urljoin, urlparse
import time

class WebScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def extract_content(self, url):
        """Extract main text content from a URL"""
        try:
            # Download the webpage
            downloaded = trafilatura.fetch_url(url)
            if not downloaded:
                return None
            
            # Extract the main text content
            text = trafilatura.extract(downloaded)
            
            if text and len(text.strip()) > 50:
                return text.strip()
            
            return None
            
        except Exception as e:
            logging.error(f"Content extraction error for {url}: {str(e)}")
            return None

    def extract_with_metadata(self, url):
        """Extract content with metadata"""
        try:
            downloaded = trafilatura.fetch_url(url)
            if not downloaded:
                return None
            
            # Extract with metadata
            result = trafilatura.extract(
                downloaded, 
                include_comments=False,
                include_tables=True,
                include_links=True,
                with_metadata=True
            )
            
            if result:
                return {
                    'content': result,
                    'url': url,
                    'extracted_at': time.time()
                }
            
            return None
            
        except Exception as e:
            logging.error(f"Metadata extraction error for {url}: {str(e)}")
            return None

    def batch_extract(self, urls, max_concurrent=5):
        """Extract content from multiple URLs"""
        results = []
        
        for i, url in enumerate(urls):
            try:
                content = self.extract_content(url)
                if content:
                    results.append({
                        'url': url,
                        'content': content,
                        'index': i
                    })
                
                # Small delay to be respectful
                if i > 0 and i % max_concurrent == 0:
                    time.sleep(1)
                    
            except Exception as e:
                logging.error(f"Batch extraction error for {url}: {str(e)}")
        
        return results

    def is_valid_url(self, url):
        """Check if URL is valid and accessible"""
        try:
            parsed = urlparse(url)
            return bool(parsed.netloc) and parsed.scheme in ['http', 'https']
        except:
            return False

    def get_domain(self, url):
        """Extract domain from URL"""
        try:
            return urlparse(url).netloc
        except:
            return None
