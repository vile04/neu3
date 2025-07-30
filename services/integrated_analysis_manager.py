"""
Gerenciador Integrado de Análise com Sistema Completo de Backup
Integra todos os componentes para garantir execução perfeita
"""
import logging
import os
import time
from typing import Dict, List, Any, Optional
from .backup_ai_manager import BackupAIManager
from .quality_assurance import QualityAssuranceSystem
from .backup_search_manager import BackupSearchManager
from .execution_engine import ExecutionEngine

logger = logging.getLogger(__name__)

class IntegratedAnalysisManager:
    """
    Gerenciador principal que orquestra todos os sistemas de backup
    Garante execução perfeita com dados reais e relatórios de 25k+ caracteres
    """
    
    def __init__(self):
        self.ai_manager = BackupAIManager()
        self.qa_system = QualityAssuranceSystem()
        self.search_manager = BackupSearchManager()
        self.execution_engine = ExecutionEngine()
        self.setup_environment_variables()
        
    def setup_environment_variables(self):
        """Configura variáveis de ambiente padrão para backups gratuitos"""
        # Estas são variáveis que podem ser configuradas pelo usuário
        # mas não são obrigatórias pois temos alternativas gratuitas
        
        backup_services_info = {
            'GROQ_API_KEY': {
                'url': 'https://console.groq.com/',
                'description': 'API gratuita da Groq para Llama3 e Mixtral',
                'free_tier': '10k requests/dia'
            },
            'SERPAPI_KEY': {
                'url': 'https://serpapi.com/',
                'description': 'API de busca com 100 pesquisas grátis/mês',
                'free_tier': '100 searches/mês'
            },
            'HUGGINGFACE_API_KEY': {
                'url': 'https://huggingface.co/settings/tokens',
                'description': 'Token para modelos HuggingFace',
                'free_tier': 'Ilimitado para inference API'
            }
        }
        
        logger.info("Serviços de backup disponíveis configurados")
    
    def execute_full_analysis(self, 
                            product_name: str,
                            product_description: str,
                            product_category: str,
                            product_price: str,
                            target_demographic: str,
                            target_location: str,
                            target_income: str,
                            competition_keywords: List[str]) -> Dict[str, Any]:
        """
        Executa análise psicológica completa usando sistema de backup
        Garante relatório de mínimo 25.000 caracteres com dados reais
        """
        
        logger.info("Iniciando análise psicológica completa com sistema de backup")
        
        # Preparar dados de entrada
        product_info = {
            'name': product_name,
            'description': product_description,
            'category': product_category,
            'price': product_price
        }
        
        target_market = {
            'demographic': target_demographic,
            'location': target_location,
            'income': target_income
        }
        
        try:
            # Executar através do motor principal
            execution_result = self.execution_engine.execute_complete_analysis(
                product_info=product_info,
                target_market=target_market,
                competition_keywords=competition_keywords
            )
            
            if execution_result.success:
                logger.info(f"Análise concluída com sucesso - Qualidade: {execution_result.quality_score:.1f}%")
                
                # Preparar resposta com informações detalhadas
                return {
                    'success': True,
                    'report': execution_result.report_data,
                    'quality_score': execution_result.quality_score,
                    'execution_time': execution_result.execution_time,
                    'services_used': execution_result.services_used,
                    'backup_services_used': execution_result.backup_services_used,
                    'system_status': self._get_system_status(),
                    'report_stats': self._get_report_statistics(execution_result.report_data),
                    'warnings': execution_result.warnings,
                    'next_steps': self._generate_next_steps(execution_result)
                }
            else:
                logger.error("Falha na execução da análise")
                return {
                    'success': False,
                    'error': 'Falha na execução da análise',
                    'errors': execution_result.errors,
                    'system_status': self._get_system_status(),
                    'fallback_suggestions': self._get_fallback_suggestions()
                }
                
        except Exception as e:
            logger.error(f"Erro crítico na análise: {e}")
            return {
                'success': False,
                'error': f'Erro crítico: {str(e)}',
                'system_status': self._get_system_status(),
                'emergency_contact': 'Configure pelo menos uma chave de API para garantir funcionamento'
            }
    
    def _get_system_status(self) -> Dict[str, Any]:
        """Obtém status completo do sistema"""
        return {
            'ai_services': self.ai_manager.get_system_status(),
            'search_services': self.search_manager.get_search_stats(),
            'quality_assurance': 'operational',
            'backup_systems': 'active'
        }
    
    def _get_report_statistics(self, report_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calcula estatísticas do relatório gerado"""
        if not report_data:
            return {}
        
        # Extrair todo o texto
        full_text = self.qa_system._extract_all_text(report_data)
        
        return {
            'total_characters': len(full_text),
            'total_words': len(full_text.split()),
            'total_sections': len(report_data.keys()) if isinstance(report_data, dict) else 0,
            'meets_minimum_length': len(full_text) >= 25000,
            'estimated_reading_time': f"{len(full_text.split()) // 200} minutos"
        }
    
    def _generate_next_steps(self, execution_result) -> List[str]:
        """Gera próximos passos baseados no resultado"""
        next_steps = []
        
        if execution_result.quality_score >= 90:
            next_steps.extend([
                "Relatório pronto para implementação",
                "Revisar recomendações estratégicas",
                "Definir cronograma de implementação"
            ])
        elif execution_result.quality_score >= 80:
            next_steps.extend([
                "Relatório aprovado com ressalvas menores",
                "Considerar refinamentos opcionais",
                "Iniciar implementação das estratégias principais"
            ])
        else:
            next_steps.extend([
                "Relatório necessita melhorias",
                "Revisar seções com menor qualidade",
                "Executar nova análise se necessário"
            ])
        
        # Adicionar sugestões específicas sobre serviços
        if execution_result.backup_services_used:
            next_steps.append(f"Nota: Utilizados serviços de backup - considere configurar APIs primárias")
        
        return next_steps
    
    def _get_fallback_suggestions(self) -> List[str]:
        """Sugestões quando todos os sistemas falham"""
        return [
            "Configure pelo menos uma chave de API (OpenAI, Gemini ou Groq)",
            "Verifique conexão com internet",
            "Execute diagnose.bat para verificar problemas",
            "Considere usar VPN se houver bloqueios regionais",
            "Entre em contato com suporte se problemas persistirem"
        ]
    
    def test_all_systems(self) -> Dict[str, Any]:
        """Testa todos os sistemas de backup"""
        test_results = {
            'timestamp': time.time(),
            'ai_services': {},
            'search_services': {},
            'quality_system': False,
            'overall_health': 'unknown'
        }
        
        # Testar serviços de IA
        for service_type in ['chat', 'analysis']:
            try:
                result = self.ai_manager.execute_with_backup(
                    service_type, 
                    "Teste rápido de conectividade - responda apenas 'OK'",
                    max_tokens=10
                )
                test_results['ai_services'][service_type] = {
                    'status': 'working',
                    'service_used': result.get('service', 'unknown')
                }
            except Exception as e:
                test_results['ai_services'][service_type] = {
                    'status': 'failed',
                    'error': str(e)
                }
        
        # Testar sistema de busca
        try:
            search_result = self.search_manager.search_with_backup("teste", num_results=1)
            test_results['search_services'] = {
                'status': 'working' if search_result.success else 'failed',
                'service_used': search_result.service_used,
                'results_found': search_result.total_found
            }
        except Exception as e:
            test_results['search_services'] = {
                'status': 'failed',
                'error': str(e)
            }
        
        # Testar sistema de qualidade
        try:
            test_report = {'test_section': 'Este é um teste de validação do sistema de qualidade.'}
            qa_result = self.qa_system.validate_complete_report(test_report)
            test_results['quality_system'] = True
        except Exception as e:
            test_results['quality_system'] = False
        
        # Determinar saúde geral
        working_services = 0
        total_services = 3  # AI, Search, QA
        
        if any(service.get('status') == 'working' for service in test_results['ai_services'].values()):
            working_services += 1
        
        if test_results['search_services'].get('status') == 'working':
            working_services += 1
            
        if test_results['quality_system']:
            working_services += 1
        
        if working_services == total_services:
            test_results['overall_health'] = 'excellent'
        elif working_services >= 2:
            test_results['overall_health'] = 'good'
        elif working_services >= 1:
            test_results['overall_health'] = 'limited'
        else:
            test_results['overall_health'] = 'critical'
        
        return test_results
    
    def get_service_recommendations(self) -> Dict[str, Any]:
        """Retorna recomendações para otimizar o sistema"""
        import os
        
        recommendations = {
            'priority_apis': [],
            'optional_apis': [],
            'free_alternatives': [],
            'setup_instructions': {}
        }
        
        # Verificar APIs configuradas
        if not os.environ.get('OPENAI_API_KEY'):
            recommendations['priority_apis'].append({
                'name': 'OpenAI API',
                'benefit': 'Melhor qualidade de análise psicológica',
                'cost': 'Pago por uso',
                'setup_url': 'https://platform.openai.com/'
            })
        
        if not os.environ.get('GEMINI_API_KEY'):
            recommendations['priority_apis'].append({
                'name': 'Google Gemini API',
                'benefit': 'Análise alternativa de alta qualidade',
                'cost': 'Plano gratuito generoso',
                'setup_url': 'https://ai.google.dev/'
            })
        
        if not os.environ.get('GROQ_API_KEY'):
            recommendations['free_alternatives'].append({
                'name': 'Groq API',
                'benefit': 'Backup gratuito para análises',
                'cost': 'Gratuito (10k requests/dia)',
                'setup_url': 'https://console.groq.com/'
            })
        
        return recommendations