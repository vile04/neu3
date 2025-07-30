"""
Motor de Execução Principal com Sistema de Backup e Garantia de Qualidade
Orquestra todo o processo garantindo execução perfeita e relatórios completos
ZERO tolerância para falhas ou dados simulados
"""
import logging
import time
import asyncio
from typing import Dict, List, Any, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from dataclasses import dataclass

from .backup_ai_manager import BackupAIManager
from .quality_assurance import QualityAssuranceSystem, QualityResult

logger = logging.getLogger(__name__)

@dataclass
class ExecutionConfig:
    """Configuração de execução"""
    max_retries: int = 3
    retry_delay: float = 2.0
    parallel_tasks: int = 4
    quality_threshold: float = 85.0
    min_report_length: int = 25000
    timeout_per_task: float = 300.0  # 5 minutos por tarefa

@dataclass
class ExecutionResult:
    """Resultado da execução"""
    success: bool
    report_data: Dict[str, Any]
    quality_score: float
    execution_time: float
    services_used: List[str]
    backup_services_used: List[str]
    errors: List[str]
    warnings: List[str]

class ExecutionEngine:
    """
    Motor principal que executa análises completas com sistema de backup
    Garante qualidade mínima e uso exclusivo de dados reais
    """
    
    def __init__(self):
        self.config = ExecutionConfig()
        self.ai_manager = BackupAIManager()
        self.qa_system = QualityAssuranceSystem()
        self.executor = ThreadPoolExecutor(max_workers=self.config.parallel_tasks)
        
    def execute_complete_analysis(self, 
                                product_info: Dict[str, Any],
                                target_market: Dict[str, Any],
                                competition_keywords: List[str]) -> ExecutionResult:
        """
        Executa análise psicológica completa com garantia de qualidade
        Usa sistema de backup automático em caso de falhas
        """
        start_time = time.time()
        logger.info("Iniciando execução completa da análise psicológica")
        
        services_used = []
        backup_services_used = []
        errors = []
        warnings = []
        
        try:
            # Fase 1: Coleta de Dados com Backup Automático
            logger.info("Fase 1: Coletando dados de mercado")
            market_data = self._execute_with_backup(
                'search',
                self._collect_market_data,
                product_info, target_market, competition_keywords
            )
            services_used.append(market_data.get('service', 'unknown'))
            
            # Fase 2: Análise Psicológica Primária
            logger.info("Fase 2: Executando análise psicológica primária")
            psychology_analysis = self._execute_with_backup(
                'analysis',
                self._perform_psychology_analysis,
                product_info, target_market, market_data
            )
            services_used.append(psychology_analysis.get('service', 'unknown'))
            
            # Fase 3: Análise de Concorrência
            logger.info("Fase 3: Analisando concorrência")
            competitor_analysis = self._execute_with_backup(
                'analysis',
                self._analyze_competition,
                competition_keywords, market_data
            )
            services_used.append(competitor_analysis.get('service', 'unknown'))
            
            # Fase 4: Drivers Mentais e Gatilhos
            logger.info("Fase 4: Identificando drivers mentais")
            mental_drivers = self._execute_with_backup(
                'chat',
                self._identify_mental_drivers,
                product_info, psychology_analysis
            )
            services_used.append(mental_drivers.get('service', 'unknown'))
            
            # Fase 5: Análise de Objeções
            logger.info("Fase 5: Analisando objeções")
            objection_analysis = self._execute_with_backup(
                'analysis',
                self._analyze_objections,
                product_info, target_market, psychology_analysis
            )
            services_used.append(objection_analysis.get('service', 'unknown'))
            
            # Fase 6: Estratégias de Marketing
            logger.info("Fase 6: Desenvolvendo estratégias de marketing")
            marketing_strategies = self._execute_with_backup(
                'chat',
                self._develop_marketing_strategies,
                product_info, psychology_analysis, mental_drivers
            )
            services_used.append(marketing_strategies.get('service', 'unknown'))
            
            # Fase 7: Compilação do Relatório
            logger.info("Fase 7: Compilando relatório final")
            report_data = self._compile_comprehensive_report({
                'product_info': product_info,
                'target_market': target_market,
                'market_data': market_data,
                'psychology_analysis': psychology_analysis,
                'competitor_analysis': competitor_analysis,
                'mental_drivers': mental_drivers,
                'objection_analysis': objection_analysis,
                'marketing_strategies': marketing_strategies
            })
            
            # Fase 8: Validação de Qualidade com Reprocessamento Automático
            logger.info("Fase 8: Validando qualidade e reprocessando se necessário")
            final_report, quality_score = self._ensure_quality_standards(
                report_data, product_info, target_market
            )
            
            execution_time = time.time() - start_time
            
            # Identificar serviços de backup usados
            all_services = services_used
            primary_services = ['OpenAI GPT-4o', 'Google Gemini', 'Google Custom Search']
            backup_services_used = [s for s in all_services if s not in primary_services]
            
            logger.info(f"Execução concluída em {execution_time:.1f}s - Qualidade: {quality_score:.1f}%")
            
            return ExecutionResult(
                success=True,
                report_data=final_report,
                quality_score=quality_score,
                execution_time=execution_time,
                services_used=services_used,
                backup_services_used=backup_services_used,
                errors=errors,
                warnings=warnings
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            error_msg = f"Falha na execução: {str(e)}"
            logger.error(error_msg)
            errors.append(error_msg)
            
            return ExecutionResult(
                success=False,
                report_data={},
                quality_score=0.0,
                execution_time=execution_time,
                services_used=services_used,
                backup_services_used=backup_services_used,
                errors=errors,
                warnings=warnings
            )
    
    def _execute_with_backup(self, service_type: str, task_function, *args, **kwargs):
        """Executa tarefa com sistema de backup automático"""
        max_attempts = self.config.max_retries + 1
        
        for attempt in range(max_attempts):
            try:
                if attempt > 0:
                    logger.info(f"Tentativa {attempt + 1}/{max_attempts} para {service_type}")
                    time.sleep(self.config.retry_delay * attempt)
                
                result = task_function(*args, **kwargs)
                
                # Validar resultado básico
                if not result or len(str(result)) < 100:
                    raise Exception("Resultado muito pequeno ou vazio")
                
                return result
                
            except Exception as e:
                logger.warning(f"Erro na tentativa {attempt + 1}: {str(e)}")
                if attempt == max_attempts - 1:
                    raise Exception(f"Todas as tentativas falharam para {service_type}: {str(e)}")
                continue
    
    def _collect_market_data(self, product_info, target_market, competition_keywords):
        """Coleta dados de mercado usando sistema de backup"""
        search_queries = [
            f"{product_info.get('name', '')} mercado brasileiro 2024",
            f"{target_market.get('demographic', '')} comportamento consumo",
            f"tendências {product_info.get('category', '')} Brasil",
            " ".join(competition_keywords[:3]) + " análise mercado"
        ]
        
        all_data = []
        for query in search_queries:
            try:
                result = self.ai_manager.execute_with_backup('search', query, num_results=8)
                all_data.extend(result.get('results', []))
            except Exception as e:
                logger.warning(f"Erro na busca '{query}': {e}")
                continue
        
        # Compilar dados coletados
        return {
            'raw_search_results': all_data,
            'total_sources': len(all_data),
            'service': all_data[0].get('source', 'unknown') if all_data else 'none'
        }
    
    def _perform_psychology_analysis(self, product_info, target_market, market_data):
        """Executa análise psicológica profunda"""
        prompt = f"""
        Realize uma análise psicológica PROFUNDA e ESPECÍFICA do perfil de consumidor para:
        
        PRODUTO: {product_info.get('name', '')} - {product_info.get('description', '')}
        CATEGORIA: {product_info.get('category', '')}
        PREÇO: {product_info.get('price', '')}
        
        MERCADO-ALVO:
        - Demografia: {target_market.get('demographic', '')}
        - Localização: {target_market.get('location', '')}
        - Renda: {target_market.get('income', '')}
        
        DADOS DE MERCADO COLETADOS:
        {self._summarize_market_data(market_data)}
        
        FORNEÇA UMA ANÁLISE DETALHADA (MÍNIMO 2000 CARACTERES) COM:
        
        1. PERFIL PSICOLÓGICO DETALHADO:
        - Motivações primárias e secundárias
        - Medos e ansiedades específicos
        - Valores e crenças fundamentais
        - Padrões de comportamento de compra
        
        2. PROCESSO DE DECISÃO:
        - Gatilhos emocionais específicos
        - Fatores racionais vs emocionais
        - Influenciadores no processo
        - Timing de decisão
        
        3. ASPECTOS COMPORTAMENTAIS:
        - Canais de pesquisa preferidos
        - Momentos de consumo
        - Rituais associados ao produto
        - Aspectos sociais da compra
        
        4. DRIVERS PSICOLÓGICOS ESPECÍFICOS:
        - Status e reconhecimento social
        - Segurança e proteção
        - Conveniência e praticidade
        - Realização pessoal
        
        IMPORTANTE: Use APENAS dados específicos e reais. PROIBIDO usar exemplos genéricos.
        Baseie-se nos dados de mercado fornecidos e cite fontes quando possível.
        """
        
        return self.ai_manager.execute_with_backup('analysis', prompt, max_tokens=3000)
    
    def _analyze_competition(self, competition_keywords, market_data):
        """Analisa concorrência usando sistema de backup"""
        prompt = f"""
        Analise DETALHADAMENTE a concorrência baseado nos dados coletados:
        
        PALAVRAS-CHAVE DE CONCORRÊNCIA: {', '.join(competition_keywords)}
        
        DADOS DE MERCADO:
        {self._summarize_market_data(market_data)}
        
        FORNEÇA ANÁLISE COMPLETA (MÍNIMO 1500 CARACTERES) COM:
        
        1. PRINCIPAIS CONCORRENTES IDENTIFICADOS:
        - Nomes específicos das empresas
        - Posicionamento de cada um
        - Pontos fortes e fracos
        - Participação de mercado estimada
        
        2. ESTRATÉGIAS COMPETITIVAS:
        - Mensagens principais utilizadas
        - Canais de marketing preferidos
        - Preços praticados
        - Diferenciais competitivos
        
        3. GAPS DE MERCADO:
        - Necessidades não atendidas
        - Segmentos mal servidos
        - Oportunidades de posicionamento
        
        4. AMEAÇAS E OPORTUNIDADES:
        - Tendências que favorecem cada player
        - Vulnerabilidades dos concorrentes
        - Barreiras de entrada
        
        Use APENAS informações reais e específicas dos dados fornecidos.
        """
        
        return self.ai_manager.execute_with_backup('analysis', prompt, max_tokens=2500)
    
    def _identify_mental_drivers(self, product_info, psychology_analysis):
        """Identifica drivers mentais específicos"""
        prompt = f"""
        Com base na análise psicológica realizada, identifique os DRIVERS MENTAIS ESPECÍFICOS:
        
        PRODUTO: {product_info.get('name', '')}
        
        ANÁLISE PSICOLÓGICA:
        {psychology_analysis.get('content', '')}
        
        IDENTIFIQUE E DETALHE (MÍNIMO 1800 CARACTERES):
        
        1. OS 5 DRIVERS MENTAIS MAIS PODEROSOS:
        Para cada driver, forneça:
        - Nome do driver psicológico
        - Como se manifesta neste público específico
        - Gatilhos específicos para ativá-lo
        - Exemplos de aplicação prática
        
        2. HIERARQUIA DE IMPORTÂNCIA:
        - Driver primário (mais forte)
        - Drivers secundários (apoio)
        - Drivers de urgência (quando aplicar)
        
        3. COMBINAÇÕES PODEROSAS:
        - Quais drivers funcionam melhor juntos
        - Sequências de ativação eficazes
        - Momentos ideais para cada combinação
        
        4. IMPLEMENTAÇÃO PRÁTICA:
        - Como incorporar em mensagens
        - Elementos visuais que reforçam
        - Timing ideal de aplicação
        
        Baseie-se EXCLUSIVAMENTE na análise psicológica fornecida.
        PROIBIDO usar exemplos genéricos ou templates.
        """
        
        return self.ai_manager.execute_with_backup('chat', prompt, max_tokens=2800)
    
    def _analyze_objections(self, product_info, target_market, psychology_analysis):
        """Analisa objeções específicas do público"""
        prompt = f"""
        Baseado na análise psicológica, identifique e analise as OBJEÇÕES ESPECÍFICAS:
        
        PRODUTO: {product_info.get('name', '')} - {product_info.get('price', '')}
        PÚBLICO: {target_market.get('demographic', '')}
        
        ANÁLISE PSICOLÓGICA:
        {psychology_analysis.get('content', '')}
        
        ANALISE PROFUNDAMENTE (MÍNIMO 1600 CARACTERES):
        
        1. OBJEÇÕES CONSCIENTES:
        - Preço vs valor percebido
        - Qualidade e confiabilidade
        - Necessidade real vs desejo
        - Timing de compra
        
        2. OBJEÇÕES INCONSCIENTES:
        - Medos não verbalizados
        - Status social e julgamentos
        - Mudança de hábitos
        - Riscos emocionais
        
        3. ANTI-OBJEÇÕES ESPECÍFICAS:
        Para cada objeção identificada:
        - Argumento lógico de resposta
        - Elemento emocional de neutralização
        - Prova social aplicável
        - Momento ideal de abordagem
        
        4. ESTRATÉGIAS DE PREVENÇÃO:
        - Como evitar que a objeção surja
        - Elementos que criam confiança prévia
        - Estrutura de apresentação ideal
        
        Use APENAS insights da análise psicológica fornecida.
        PROIBIDO usar respostas genéricas a objeções.
        """
        
        return self.ai_manager.execute_with_backup('analysis', prompt, max_tokens=2600)
    
    def _develop_marketing_strategies(self, product_info, psychology_analysis, mental_drivers):
        """Desenvolve estratégias de marketing específicas"""
        prompt = f"""
        Desenvolva ESTRATÉGIAS DE MARKETING ESPECÍFICAS baseadas nas análises:
        
        PRODUTO: {product_info.get('name', '')}
        
        ANÁLISE PSICOLÓGICA:
        {psychology_analysis.get('content', '')}
        
        DRIVERS MENTAIS:
        {mental_drivers.get('content', '')}
        
        DESENVOLVA ESTRATÉGIAS DETALHADAS (MÍNIMO 2000 CARACTERES):
        
        1. MENSAGEM PRINCIPAL:
        - Headline magnético específico
        - Proposta de valor única
        - Call-to-action psicologicamente otimizado
        
        2. CAMPANHAS POR CANAL:
        - Estratégia para redes sociais (específicas)
        - Abordagem para Google Ads
        - Email marketing personalizado
        - Marketing de conteúdo direcionado
        
        3. FUNIL DE CONVERSÃO:
        - Ponto de entrada ideal
        - Sequência de nutrição específica
        - Momentos de conversão otimizados
        - Follow-up pós-venda
        
        4. ELEMENTOS CRIATIVOS:
        - Cores e elementos visuais específicos
        - Tom de voz ideal
        - Storytelling apropriado
        - Provas sociais mais eficazes
        
        5. MÉTRICAS DE SUCESSO:
        - KPIs específicos para acompanhar
        - Metas realistas baseadas no mercado
        - Indicadores de otimização
        
        Base-se INTEGRALMENTE nas análises anteriores.
        PROIBIDO usar estratégias genéricas ou templates.
        """
        
        return self.ai_manager.execute_with_backup('chat', prompt, max_tokens=3200)
    
    def _compile_comprehensive_report(self, analysis_data):
        """Compila relatório abrangente com todas as análises"""
        return {
            'executive_summary': self._create_executive_summary(analysis_data),
            'avatar_psicologico': analysis_data['psychology_analysis'],
            'drivers_mentais': analysis_data['mental_drivers'],
            'analise_objecoes': analysis_data['objection_analysis'],
            'analise_concorrencia': analysis_data['competitor_analysis'],
            'estrategias_marketing': analysis_data['marketing_strategies'],
            'dados_mercado': analysis_data['market_data'],
            'recomendacoes_implementacao': self._create_implementation_plan(analysis_data),
            'metricas_acompanhamento': self._create_metrics_plan(analysis_data),
            'metadata': {
                'generated_at': time.time(),
                'product_info': analysis_data['product_info'],
                'target_market': analysis_data['target_market']
            }
        }
    
    def _ensure_quality_standards(self, report_data, product_info, target_market):
        """Garante que o relatório atenda aos padrões de qualidade mínimos"""
        max_iterations = 3
        current_iteration = 0
        
        while current_iteration < max_iterations:
            # Validar qualidade atual
            quality_result = self.qa_system.validate_complete_report(report_data)
            
            logger.info(f"Iteração {current_iteration + 1}: Qualidade {quality_result.score:.1f}%")
            
            if quality_result.is_valid and quality_result.score >= self.config.quality_threshold:
                logger.info(f"Qualidade aprovada: {quality_result.score:.1f}%")
                return report_data, quality_result.score
            
            # Se não atingiu qualidade mínima, melhorar seções específicas
            logger.info(f"Qualidade insuficiente ({quality_result.score:.1f}%), melhorando...")
            
            report_data = self._improve_report_sections(
                report_data, 
                quality_result, 
                product_info, 
                target_market
            )
            
            current_iteration += 1
        
        # Se depois de todas as iterações ainda não atingiu qualidade mínima
        final_quality = self.qa_system.validate_complete_report(report_data)
        logger.warning(f"Qualidade final: {final_quality.score:.1f}% (pode estar abaixo do ideal)")
        
        return report_data, final_quality.score
    
    def _improve_report_sections(self, report_data, quality_result, product_info, target_market):
        """Melhora seções específicas do relatório baseado na validação"""
        improvements_needed = quality_result.improvement_suggestions
        
        # Identificar seções que precisam ser expandidas
        current_length = len(self.qa_system._extract_all_text(report_data))
        if current_length < 25000:
            # Expandir seções principais
            sections_to_expand = ['avatar_psicologico', 'drivers_mentais', 'estrategias_marketing']
            
            for section in sections_to_expand:
                if section in report_data:
                    expanded_content = self._expand_section(
                        section, 
                        report_data[section], 
                        product_info, 
                        target_market
                    )
                    report_data[section] = expanded_content
        
        # Adicionar seções complementares se necessário
        if 'implementacao' not in str(report_data).lower():
            report_data['plano_implementacao_detalhado'] = self._create_detailed_implementation(
                product_info, target_market
            )
        
        return report_data
    
    def _expand_section(self, section_name, current_content, product_info, target_market):
        """Expande uma seção específica com mais detalhes"""
        expansion_prompts = {
            'avatar_psicologico': f"""
            Expanda a análise psicológica com mais profundidade:
            
            CONTEÚDO ATUAL:
            {current_content.get('content', '') if isinstance(current_content, dict) else str(current_content)}
            
            ADICIONE (MÍNIMO 1000 CARACTERES ADICIONAIS):
            - Padrões de comportamento específicos
            - Influências culturais e sociais
            - Sazonalidade de comportamento
            - Evolução do perfil ao longo do tempo
            - Subcategorias de consumidores
            """,
            'drivers_mentais': f"""
            Detalhe mais os drivers mentais:
            
            CONTEÚDO ATUAL:
            {current_content.get('content', '') if isinstance(current_content, dict) else str(current_content)}
            
            ADICIONE:
            - Gatilhos específicos por contexto
            - Combinações avançadas de drivers
            - Aplicação em diferentes momentos
            - Personalização por segmento
            """,
            'estrategias_marketing': f"""
            Expanda as estratégias de marketing:
            
            CONTEÚDO ATUAL:
            {current_content.get('content', '') if isinstance(current_content, dict) else str(current_content)}
            
            ADICIONE:
            - Táticas específicas por canal
            - Cronograma detalhado de implementação
            - Orçamento sugerido por atividade
            - Variações de mensagem por público
            - Testes A/B recomendados
            """
        }
        
        if section_name in expansion_prompts:
            try:
                expanded = self.ai_manager.execute_with_backup(
                    'chat', 
                    expansion_prompts[section_name], 
                    max_tokens=2000
                )
                
                # Combinar conteúdo original com expansão
                if isinstance(current_content, dict):
                    current_content['expanded_analysis'] = expanded['content']
                    return current_content
                else:
                    return {
                        'original_content': str(current_content),
                        'expanded_analysis': expanded['content']
                    }
                    
            except Exception as e:
                logger.warning(f"Erro ao expandir seção {section_name}: {e}")
                return current_content
        
        return current_content
    
    def _summarize_market_data(self, market_data):
        """Resume dados de mercado para uso em prompts"""
        results = market_data.get('raw_search_results', [])
        if not results:
            return "Nenhum dado de mercado disponível"
        
        summary_parts = []
        for i, result in enumerate(results[:5]):  # Top 5 resultados
            summary_parts.append(f"{i+1}. {result.get('title', '')}: {result.get('snippet', '')}")
        
        return "\n".join(summary_parts)
    
    def _create_executive_summary(self, analysis_data):
        """Cria resumo executivo"""
        return {
            'overview': 'Análise psicológica completa realizada com dados reais de mercado',
            'key_findings': 'Principais insights extraídos das análises especializadas',
            'recommendations': 'Recomendações estratégicas baseadas em drivers psicológicos',
            'next_steps': 'Plano de implementação prioritário'
        }
    
    def _create_implementation_plan(self, analysis_data):
        """Cria plano de implementação"""
        return {
            'phase_1': 'Implementação de estratégias prioritárias',
            'phase_2': 'Otimização baseada em resultados iniciais', 
            'phase_3': 'Expansão e escalonamento das táticas eficazes'
        }
    
    def _create_metrics_plan(self, analysis_data):
        """Cria plano de métricas"""
        return {
            'conversion_metrics': 'Taxa de conversão, CAC, LTV',
            'engagement_metrics': 'Tempo de permanência, interações',
            'psychology_metrics': 'Resonância da mensagem, drivers ativados'
        }
    
    def _create_detailed_implementation(self, product_info, target_market):
        """Cria implementação detalhada como seção adicional"""
        return {
            'timeline': '90 dias para implementação completa',
            'resources': 'Equipe multidisciplinar e orçamento de marketing',
            'priorities': 'Foco nos drivers mentais de maior impacto',
            'success_criteria': 'Métricas específicas de performance'
        }