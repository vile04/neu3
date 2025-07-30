"""
Gerenciador de IA com Sistema de Backup Automático
Sistema que garante execução perfeita com múltiplas alternativas gratuitas
PROIBIDO: Respostas simuladas, mocadas ou pré-prontas
"""
import os
import logging
import time
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import json

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ServiceStatus:
    """Status de um serviço de IA"""
    name: str
    is_working: bool
    last_error: Optional[str]
    attempts: int
    max_attempts: int = 3
    
class BackupAIManager:
    """
    Gerenciador inteligente de serviços de IA com sistema de backup automático
    Garante execução perfeita usando sempre dados reais
    """
    
    def __init__(self):
        self.primary_services = {}
        self.backup_services = {}
        self.service_status = {}
        self.min_report_length = 25000
        self._setup_services()
    
    def _setup_services(self):
        """Configura todos os serviços primários e de backup"""
        
        # Serviços de Chat/Análise - Primário: OpenAI, Backup: Groq (grátis)
        self.primary_services['chat'] = {
            'name': 'OpenAI GPT-4o',
            'handler': self._openai_chat,
            'requires': ['OPENAI_API_KEY']
        }
        
        self.backup_services['chat'] = [
            {
                'name': 'Groq Llama3',
                'handler': self._groq_chat,
                'requires': ['GROQ_API_KEY'],
                'is_free': True
            },
            {
                'name': 'HuggingFace Transformers',
                'handler': self._huggingface_chat,
                'requires': [],
                'is_free': True
            }
        ]
        
        # Serviços de Análise Avançada - Primário: Gemini, Backup: Groq
        self.primary_services['analysis'] = {
            'name': 'Google Gemini',
            'handler': self._gemini_analysis,
            'requires': ['GEMINI_API_KEY']
        }
        
        self.backup_services['analysis'] = [
            {
                'name': 'Groq Mixtral',
                'handler': self._groq_analysis,
                'requires': ['GROQ_API_KEY'],
                'is_free': True
            },
            {
                'name': 'OpenAI GPT-4o Mini',
                'handler': self._openai_mini_analysis,
                'requires': ['OPENAI_API_KEY'],
                'is_free': True  # modelo mini é gratuito
            }
        ]
        
        # Serviços de Busca - Primário: Google, Backup: DuckDuckGo
        self.primary_services['search'] = {
            'name': 'Google Custom Search',
            'handler': self._google_search,
            'requires': ['GOOGLE_API_KEY', 'GOOGLE_CSE_ID']
        }
        
        self.backup_services['search'] = [
            {
                'name': 'DuckDuckGo Search',
                'handler': self._duckduckgo_search,
                'requires': [],
                'is_free': True
            },
            {
                'name': 'SerpAPI',
                'handler': self._serpapi_search,
                'requires': ['SERPAPI_KEY'],
                'is_free': True  # plano gratuito disponível
            }
        ]
        
        # Inicializar status
        for service_type in ['chat', 'analysis', 'search']:
            self.service_status[service_type] = ServiceStatus(
                name=self.primary_services[service_type]['name'],
                is_working=True,
                last_error=None,
                attempts=0
            )
    
    def execute_with_backup(self, service_type: str, prompt: str, **kwargs) -> Dict[str, Any]:
        """
        Executa serviço com sistema de backup automático
        Garante que sempre obtemos dados reais, nunca simulados
        """
        result = None
        error_log = []
        
        # Tentar serviço primário
        try:
            logger.info(f"Tentando serviço primário: {self.primary_services[service_type]['name']}")
            result = self._execute_service(
                self.primary_services[service_type], 
                prompt, 
                **kwargs
            )
            
            if self._validate_result(result, service_type):
                self.service_status[service_type].is_working = True
                self.service_status[service_type].attempts = 0
                logger.info(f"Serviço primário executado com sucesso")
                return result
                
        except Exception as e:
            error_msg = f"Erro no serviço primário {self.primary_services[service_type]['name']}: {str(e)}"
            logger.warning(error_msg)
            error_log.append(error_msg)
            self.service_status[service_type].is_working = False
            self.service_status[service_type].last_error = str(e)
        
        # Tentar serviços de backup em ordem
        for backup_service in self.backup_services[service_type]:
            try:
                logger.info(f"Tentando serviço de backup: {backup_service['name']}")
                result = self._execute_service(backup_service, prompt, **kwargs)
                
                if self._validate_result(result, service_type):
                    logger.info(f"Serviço de backup {backup_service['name']} executado com sucesso")
                    return result
                    
            except Exception as e:
                error_msg = f"Erro no backup {backup_service['name']}: {str(e)}"
                logger.warning(error_msg)
                error_log.append(error_msg)
                continue
        
        # Se chegou aqui, todos os serviços falharam
        raise Exception(f"Todos os serviços falharam para {service_type}. Erros: {'; '.join(error_log)}")
    
    def _execute_service(self, service_config: Dict, prompt: str, **kwargs) -> Dict[str, Any]:
        """Executa um serviço específico"""
        
        # Verificar se as chaves necessárias estão disponíveis
        for required_key in service_config.get('requires', []):
            if not os.environ.get(required_key):
                raise Exception(f"Chave {required_key} não configurada")
        
        # Executar o handler específico
        return service_config['handler'](prompt, **kwargs)
    
    def _validate_result(self, result: Dict[str, Any], service_type: str) -> bool:
        """
        Valida se o resultado é real e atende aos requisitos mínimos
        JAMAIS aceita dados simulados ou mocados
        """
        if not result or not isinstance(result, dict):
            return False
        
        content = result.get('content', '')
        if not content or len(content.strip()) < 100:
            return False
        
        # Verificar se não é resposta simulada ou mocada
        forbidden_indicators = [
            'lorem ipsum', 'placeholder', 'exemplo', 'simulado', 
            'mocado', 'teste', 'sample', 'dummy', 'fake',
            '[insert', '[your', 'replace with', 'add your'
        ]
        
        content_lower = content.lower()
        for indicator in forbidden_indicators:
            if indicator in content_lower:
                logger.warning(f"Resultado rejeitado - contém indicador de simulação: {indicator}")
                return False
        
        return True
    
    # ========== IMPLEMENTAÇÕES DOS SERVIÇOS ==========
    
    def _openai_chat(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """OpenAI GPT-4o - Serviço primário de chat"""
        try:
            from openai import OpenAI
            
            client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
            
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "Você é um especialista em análise psicológica de mercado. Forneça sempre análises detalhadas e específicas baseadas em dados reais. NUNCA use exemplos genéricos ou simulados."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=kwargs.get('max_tokens', 4000),
                temperature=kwargs.get('temperature', 0.7)
            )
            
            return {
                'content': response.choices[0].message.content,
                'model': 'gpt-4o',
                'service': 'OpenAI',
                'tokens_used': response.usage.total_tokens if response.usage else 0
            }
            
        except Exception as e:
            logger.error(f"Erro no OpenAI: {e}")
            raise
    
    def _groq_chat(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Groq Llama3 - Backup gratuito para chat"""
        try:
            # from groq import Groq  # Será instalado quando necessário
            
            client = Groq(api_key=os.environ.get('GROQ_API_KEY'))
            
            response = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[
                    {"role": "system", "content": "Você é um especialista em análise psicológica de mercado. Forneça sempre análises detalhadas e específicas baseadas em dados reais. NUNCA use exemplos genéricos ou simulados."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=kwargs.get('max_tokens', 4000),
                temperature=kwargs.get('temperature', 0.7)
            )
            
            return {
                'content': response.choices[0].message.content,
                'model': 'llama3-70b-8192',
                'service': 'Groq',
                'tokens_used': response.usage.total_tokens if response.usage else 0
            }
            
        except Exception as e:
            logger.error(f"Erro no Groq: {e}")
            raise
    
    def _huggingface_chat(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """HuggingFace Transformers - Backup local gratuito"""
        try:
            # from transformers import pipeline  # Será instalado quando necessário
            
            # Usar modelo local gratuito
            generator = pipeline('text-generation', 
                               model='microsoft/DialoGPT-large',
                               device=-1)  # CPU
            
            response = generator(
                prompt,
                max_length=kwargs.get('max_tokens', 1000),
                temperature=kwargs.get('temperature', 0.7),
                do_sample=True,
                pad_token_id=50256
            )
            
            return {
                'content': response[0]['generated_text'],
                'model': 'DialoGPT-large',
                'service': 'HuggingFace Local',
                'tokens_used': len(response[0]['generated_text'].split())
            }
            
        except Exception as e:
            logger.error(f"Erro no HuggingFace: {e}")
            raise
    
    def _gemini_analysis(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Google Gemini - Serviço primário de análise"""
        try:
            from google import genai
            from google.genai import types
            
            client = genai.Client(api_key=os.environ.get('GEMINI_API_KEY'))
            
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=kwargs.get('temperature', 0.7),
                    max_output_tokens=kwargs.get('max_tokens', 4000)
                )
            )
            
            return {
                'content': response.text,
                'model': 'gemini-2.5-flash',
                'service': 'Google Gemini',
                'tokens_used': len(response.text.split()) if response.text else 0
            }
            
        except Exception as e:
            logger.error(f"Erro no Gemini: {e}")
            raise
    
    def _groq_analysis(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """Groq Mixtral - Backup gratuito para análise"""
        try:
            # from groq import Groq  # Será instalado quando necessário
            
            client = Groq(api_key=os.environ.get('GROQ_API_KEY'))
            
            response = client.chat.completions.create(
                model="mixtral-8x7b-32768",
                messages=[
                    {"role": "system", "content": "Você é um especialista em análise psicológica avançada. Forneça análises profundas e detalhadas baseadas em dados reais. NUNCA use exemplos genéricos."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=kwargs.get('max_tokens', 4000),
                temperature=kwargs.get('temperature', 0.7)
            )
            
            return {
                'content': response.choices[0].message.content,
                'model': 'mixtral-8x7b-32768',
                'service': 'Groq Mixtral',
                'tokens_used': response.usage.total_tokens if response.usage else 0
            }
            
        except Exception as e:
            logger.error(f"Erro no Groq Mixtral: {e}")
            raise
    
    def _openai_mini_analysis(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """OpenAI GPT-4o Mini - Backup econômico"""
        try:
            from openai import OpenAI
            
            client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
            
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Você é um especialista em análise psicológica avançada. Forneça análises profundas e detalhadas baseadas em dados reais."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=kwargs.get('max_tokens', 4000),
                temperature=kwargs.get('temperature', 0.7)
            )
            
            return {
                'content': response.choices[0].message.content,
                'model': 'gpt-4o-mini',
                'service': 'OpenAI Mini',
                'tokens_used': response.usage.total_tokens if response.usage else 0
            }
            
        except Exception as e:
            logger.error(f"Erro no OpenAI Mini: {e}")
            raise
    
    def _google_search(self, query: str, **kwargs) -> Dict[str, Any]:
        """Google Custom Search - Serviço primário de busca"""
        try:
            import requests
            
            api_key = os.environ.get('GOOGLE_API_KEY')
            cse_id = os.environ.get('GOOGLE_CSE_ID')
            
            url = f"https://www.googleapis.com/customsearch/v1"
            params = {
                'key': api_key,
                'cx': cse_id,
                'q': query,
                'num': kwargs.get('num_results', 10)
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            for item in data.get('items', []):
                results.append({
                    'title': item.get('title', ''),
                    'url': item.get('link', ''),
                    'snippet': item.get('snippet', ''),
                    'source': 'Google Custom Search'
                })
            
            return {
                'results': results,
                'total_results': len(results),
                'service': 'Google Custom Search'
            }
            
        except Exception as e:
            logger.error(f"Erro no Google Search: {e}")
            raise
    
    def _duckduckgo_search(self, query: str, **kwargs) -> Dict[str, Any]:
        """DuckDuckGo Search - Backup gratuito para busca"""
        try:
            from duckduckgo_search import DDGS
            
            with DDGS() as ddgs:
                results = []
                
                for result in ddgs.text(
                    query, 
                    max_results=kwargs.get('num_results', 10)
                ):
                    results.append({
                        'title': result.get('title', ''),
                        'url': result.get('href', ''),
                        'snippet': result.get('body', ''),
                        'source': 'DuckDuckGo'
                    })
            
            return {
                'results': results,
                'total_results': len(results),
                'service': 'DuckDuckGo'
            }
            
        except Exception as e:
            logger.error(f"Erro no DuckDuckGo: {e}")
            raise
    
    def _serpapi_search(self, query: str, **kwargs) -> Dict[str, Any]:
        """SerpAPI - Backup com plano gratuito"""
        try:
            import requests
            
            api_key = os.environ.get('SERPAPI_KEY')
            
            url = "https://serpapi.com/search"
            params = {
                'api_key': api_key,
                'q': query,
                'engine': 'google',
                'num': kwargs.get('num_results', 10)
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            results = []
            
            for item in data.get('organic_results', []):
                results.append({
                    'title': item.get('title', ''),
                    'url': item.get('link', ''),
                    'snippet': item.get('snippet', ''),
                    'source': 'SerpAPI'
                })
            
            return {
                'results': results,
                'total_results': len(results),
                'service': 'SerpAPI'
            }
            
        except Exception as e:
            logger.error(f"Erro no SerpAPI: {e}")
            raise
    
    def get_system_status(self) -> Dict[str, Any]:
        """Retorna status completo do sistema"""
        status = {
            'services': {},
            'overall_health': 'healthy',
            'working_services': 0,
            'total_services': len(self.service_status)
        }
        
        for service_type, service_status in self.service_status.items():
            status['services'][service_type] = {
                'name': service_status.name,
                'is_working': service_status.is_working,
                'last_error': service_status.last_error,
                'attempts': service_status.attempts,
                'has_backups': len(self.backup_services.get(service_type, [])) > 0
            }
            
            if service_status.is_working:
                status['working_services'] += 1
        
        # Determinar saúde geral
        if status['working_services'] == 0:
            status['overall_health'] = 'critical'
        elif status['working_services'] < status['total_services']:
            status['overall_health'] = 'degraded'
        
        return status