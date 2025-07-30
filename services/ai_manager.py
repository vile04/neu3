"""
Gerenciador de IA principal com sistema de backup integrado
Orquestra análises psicológicas complexas com múltiplos provedores
"""
import logging
import time
import os
from typing import Dict, List, Any, Optional
from .simple_backup_manager import SimpleBackupManager

logger = logging.getLogger(__name__)

class AIManager:
    """
    Gerenciador principal de IA com capacidades avançadas
    Integra com sistema de backup para garantir funcionamento contínuo
    """
    
    def __init__(self):
        self.backup_manager = SimpleBackupManager()
        self.analysis_modules = self._setup_analysis_modules()
        
    def _setup_analysis_modules(self) -> Dict[str, Any]:
        """Configura módulos especializados de análise"""
        return {
            'market_research': self._conduct_market_research,
            'avatar_psychology': self._analyze_avatar_psychology,
            'mental_drivers': self._create_mental_drivers,
            'objection_analysis': self._analyze_objections,
            'provi_system': self._create_provi_system,
            'prepitch_architecture': self._create_prepitch_architecture
        }
    
    def conduct_market_research(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Conduz pesquisa abrangente de mercado
        Coleta dados de múltiplas fontes para análise psicológica
        """
        logger.info("Iniciando pesquisa de mercado abrangente")
        
        product_name = input_data.get('product_name', '')
        target_market = input_data.get('target_market', '')
        competition_keywords = input_data.get('competition_keywords', [])
        
        try:
            # Usar sistema de backup para pesquisa
            search_queries = [
                f"{product_name} mercado brasileiro tendências 2024",
                f"{target_market} comportamento consumidor Brasil",
                f"análise concorrência {product_name}",
                " ".join(competition_keywords[:3]) + " market share Brasil",
                f"{product_name} preço médio mercado",
                f"{target_market} poder compra perfil"
            ]
            
            market_insights = []
            
            # Coletar dados usando sistema de backup
            if hasattr(self.backup_manager, 'services_available') and self.backup_manager.services_available.get('duckduckgo'):
                try:
                    from duckduckgo_search import DDGS
                    
                    with DDGS() as ddgs:
                        for query in search_queries:
                            try:
                                results = ddgs.text(query, max_results=5, region='br-pt')
                                for result in results:
                                    market_insights.append({
                                        'query': query,
                                        'title': result.get('title', ''),
                                        'snippet': result.get('body', ''),
                                        'url': result.get('href', ''),
                                        'relevance': self._calculate_relevance(query, result.get('body', ''))
                                    })
                            except Exception as e:
                                logger.warning(f"Erro na busca '{query}': {e}")
                                continue
                                
                except Exception as e:
                    logger.warning(f"Erro no DuckDuckGo: {e}")
            
            # Analisar insights coletados
            analysis_prompt = f"""
            Com base nos dados de mercado coletados, realize uma análise psicológica profunda:
            
            PRODUTO: {product_name}
            PÚBLICO-ALVO: {target_market}
            
            DADOS COLETADOS:
            {self._format_market_insights(market_insights[:10])}
            
            FORNEÇA ANÁLISE DETALHADA (MÍNIMO 1500 CARACTERES) COM:
            
            1. PERFIL PSICOLÓGICO DO MERCADO:
            - Motivações principais do público
            - Medos e ansiedades identificados
            - Padrões comportamentais observados
            - Influências culturais e sociais
            
            2. ANÁLISE COMPETITIVA PSICOLÓGICA:
            - Como concorrentes abordam emocionalmente o público
            - Gaps psicológicos no mercado
            - Oportunidades de posicionamento emocional
            
            3. TENDÊNCIAS COMPORTAMENTAIS:
            - Mudanças no comportamento do consumidor
            - Fatores que influenciam decisões de compra
            - Sazonalidade psicológica
            
            4. INSIGHTS ESTRATÉGICOS:
            - Pontos de dor não atendidos
            - Oportunidades de conexão emocional
            - Positioning psicológico recomendado
            
            Use APENAS dados reais dos insights coletados.
            """
            
            # Executar análise com backup
            analysis_result = self._execute_analysis_with_backup(analysis_prompt)
            
            return {
                'raw_data': market_insights,
                'analysis': analysis_result,
                'data_sources': len(market_insights),
                'coverage_score': min(100, len(market_insights) * 10),
                'timestamp': time.time()
            }
            
        except Exception as e:
            logger.error(f"Erro na pesquisa de mercado: {e}")
            return {
                'raw_data': [],
                'analysis': self._fallback_market_analysis(input_data),
                'data_sources': 0,
                'coverage_score': 30,
                'timestamp': time.time(),
                'fallback_used': True
            }
    
    def analyze_avatar_psychology(self, input_data: Dict[str, Any], 
                                 market_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Análise psicológica profunda do avatar do cliente
        Cria perfil psicológico detalhado baseado em dados reais
        """
        logger.info("Analisando psicologia do avatar")
        
        analysis_prompt = f"""
        Crie um PERFIL PSICOLÓGICO DETALHADO do avatar baseado em dados reais:
        
        PRODUTO: {input_data.get('product_name', '')}
        PÚBLICO: {input_data.get('target_market', '')}
        
        DADOS DE MERCADO:
        {self._extract_market_analysis(market_data)}
        
        CRIE PERFIL PSICOLÓGICO COMPLETO (MÍNIMO 2000 CARACTERES):
        
        1. DEMOGRAFIA PSICOLÓGICA:
        - Idade, gênero, localização com implicações psicológicas
        - Classe social e suas influências comportamentais
        - Educação e padrões de pensamento
        - Estrutura familiar e influências
        
        2. PSICOGRAFIA DETALHADA:
        - Valores fundamentais e crenças
        - Medos primários e secundários
        - Aspirações e sonhos específicos
        - Frustrações e dores cotidianas
        
        3. COMPORTAMENTO DE COMPRA:
        - Processo de tomada de decisão específico
        - Gatilhos emocionais que ativam compras
        - Influenciadores na decisão (pessoas, mídia, etc.)
        - Objeções típicas e suas origens psicológicas
        
        4. LINGUAGEM E COMUNICAÇÃO:
        - Tom de voz que ressoa
        - Palavras e expressões preferidas
        - Canais de comunicação favoritos
        - Formato de conteúdo mais eficaz
        
        5. DRIVERS MOTIVACIONAIS:
        - O que o move para ação
        - Como define sucesso
        - Que tipo de reconhecimento busca
        - Qual seu relacionamento com dinheiro
        
        Baseie-se EXCLUSIVAMENTE nos dados de mercado fornecidos.
        """
        
        analysis_result = self._execute_analysis_with_backup(analysis_prompt)
        
        return {
            'detailed_profile': analysis_result,
            'confidence_score': self._calculate_confidence_score(analysis_result),
            'data_quality': 'high' if market_data.get('data_sources', 0) > 5 else 'medium',
            'timestamp': time.time()
        }
    
    def create_mental_drivers(self, input_data: Dict[str, Any], 
                             avatar_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cria sistema de drivers mentais específicos
        Identifica e organiza gatilhos psicológicos para conversão
        """
        logger.info("Criando sistema de drivers mentais")
        
        drivers_prompt = f"""
        Com base no perfil psicológico detalhado, crie um SISTEMA DE DRIVERS MENTAIS:
        
        PRODUTO: {input_data.get('product_name', '')}
        
        PERFIL PSICOLÓGICO:
        {self._extract_avatar_analysis(avatar_data)}
        
        CRIE SISTEMA COMPLETO DE DRIVERS (MÍNIMO 1800 CARACTERES):
        
        1. DRIVER PRIMÁRIO (Mais Poderoso):
        - Nome do driver e descrição psicológica
        - Por que é o mais forte para este avatar
        - Como ativar especificamente
        - Exemplos de aplicação prática
        - Momento ideal de uso
        
        2. DRIVERS SECUNDÁRIOS (3-4 drivers):
        Para cada driver secundário:
        - Nome e fundamento psicológico
        - Situações onde é mais eficaz
        - Combinações com outros drivers
        - Implementação tática
        
        3. DRIVERS DE URGÊNCIA:
        - Quando usar cada driver
        - Sequências de ativação
        - Combinações para máximo impacto
        - Sinais de saturação
        
        4. ANTI-DRIVERS (Evitar):
        - Gatilhos que repelem este avatar
        - Por que são contraproducentes
        - Como evitar ativá-los acidentalmente
        
        5. SISTEMA DE IMPLEMENTAÇÃO:
        - Hierarquia de uso dos drivers
        - Roteiro de aplicação
        - Métricas para medir eficácia
        - Ajustes baseados em resposta
        
        Base-se INTEGRALMENTE no perfil psicológico fornecido.
        """
        
        analysis_result = self._execute_analysis_with_backup(drivers_prompt)
        
        return {
            'driver_system': analysis_result,
            'implementation_ready': True,
            'psychological_foundation': 'strong',
            'timestamp': time.time()
        }
    
    def analyze_objections(self, input_data: Dict[str, Any], 
                          avatar_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Análise completa de objeções e sistema anti-objeção
        Mapeia resistências psicológicas e cria contramedidas
        """
        logger.info("Analisando objeções e criando sistema anti-objeção")
        
        objections_prompt = f"""
        Mapeie TODAS as objeções psicológicas e crie sistema anti-objeção:
        
        PRODUTO: {input_data.get('product_name', '')}
        PREÇO: {input_data.get('price_range', '')}
        
        PERFIL PSICOLÓGICO:
        {self._extract_avatar_analysis(avatar_data)}
        
        MAPEAMENTO COMPLETO DE OBJEÇÕES (MÍNIMO 1600 CARACTERES):
        
        1. OBJEÇÕES CONSCIENTES (Verbalizadas):
        Para cada objeção principal:
        - Objeção específica
        - Origem psicológica da resistência
        - Anti-objeção lógica específica
        - Anti-objeção emocional
        - Momento ideal de abordagem
        - Prova social aplicável
        
        2. OBJEÇÕES INCONSCIENTES (Não verbalizadas):
        - Medos não admitidos
        - Preconceitos ocultos
        - Resistências culturais
        - Bloqueios emocionais
        - Como revelar e tratar cada um
        
        3. SISTEMA DE PREVENÇÃO:
        - Como evitar que objeções surjam
        - Estrutura de apresentação preventiva
        - Elementos que criam confiança prévia
        - Sequência ideal de informações
        
        4. PROTOCOLO DE RESPOSTA:
        - Script para cada objeção principal
        - Técnicas de neutralização emocional
        - Redirecionamento para benefícios
        - Fechamento após objeção tratada
        
        5. MÉTRICAS DE SUCESSO:
        - Como medir eficácia anti-objeção
        - Sinais de objeção neutralizada
        - Indicadores de prontidão para compra
        
        Base-se EXCLUSIVAMENTE no perfil psicológico do avatar.
        """
        
        analysis_result = self._execute_analysis_with_backup(objections_prompt)
        
        return {
            'objection_mapping': analysis_result,
            'prevention_system': 'implemented',
            'response_protocols': 'ready',
            'timestamp': time.time()
        }
    
    def create_provi_system(self, input_data: Dict[str, Any], 
                           drivers_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cria sistema PROVI (Proof of Value Instantaneous)
        Desenvolve provas visuais instantâneas de valor
        """
        logger.info("Criando sistema PROVI para demonstração de valor")
        
        provi_prompt = f"""
        Crie sistema PROVI (Provas Visuais Instantâneas) baseado nos drivers:
        
        PRODUTO: {input_data.get('product_name', '')}
        
        DRIVERS MENTAIS:
        {self._extract_drivers_analysis(drivers_data)}
        
        SISTEMA PROVI COMPLETO (MÍNIMO 1400 CARACTERES):
        
        1. PROVAS VISUAIS PRIMÁRIAS:
        Para cada driver principal:
        - Tipo de prova visual necessária
        - Elementos específicos a incluir
        - Psicologia por trás da eficácia
        - Formato ideal (vídeo, imagem, gráfico)
        - Call-to-action integrado
        
        2. PROVAS SOCIAIS INSTANTÂNEAS:
        - Depoimentos visuais específicos
        - Demonstrações de resultados
        - Comparações visuais com concorrentes
        - Evidências de credibilidade
        
        3. PROVAS DE TRANSFORMAÇÃO:
        - Antes e depois relevantes
        - Linha do tempo de benefícios
        - Progressão visual de valor
        - Impacto emocional demonstrado
        
        4. PROVAS DE AUTORIDADE:
        - Certificações visuais
        - Reconhecimentos mostrados
        - Expertise demonstrada
        - Credenciais relevantes
        
        5. IMPLEMENTAÇÃO PRÁTICA:
        - Sequência ideal de apresentação
        - Momentos de impacto máximo
        - Combinações mais eficazes
        - Testes A/B recomendados
        
        Baseie-se INTEGRALMENTE nos drivers mentais identificados.
        """
        
        analysis_result = self._execute_analysis_with_backup(provi_prompt)
        
        return {
            'provi_system': analysis_result,
            'visual_requirements': 'defined',
            'implementation_guide': 'ready',
            'timestamp': time.time()
        }
    
    def create_prepitch_architecture(self, drivers_data: Dict[str, Any], 
                                   objections_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cria arquitetura de pré-pitch invisível
        Sequência psicológica que prepara para conversão antes da oferta
        """
        logger.info("Criando arquitetura de pré-pitch invisível")
        
        prepitch_prompt = f"""
        Crie ARQUITETURA DE PRÉ-PITCH INVISÍVEL baseada em drivers e objeções:
        
        DRIVERS MENTAIS:
        {self._extract_drivers_analysis(drivers_data)}
        
        MAPEAMENTO DE OBJEÇÕES:
        {self._extract_objections_analysis(objections_data)}
        
        ARQUITETURA COMPLETA (MÍNIMO 1500 CARACTERES):
        
        1. FASE DE AQUECIMENTO:
        - Primeiros touchpoints ideais
        - Conteúdo que ativa drivers sutilmente
        - Como estabelecer autoridade inicial
        - Construção de rapport psicológico
        
        2. FASE DE EDUCAÇÃO:
        - Sequência de informações estratégicas
        - Como educar sem vender
        - Plantio de sementes para drivers futuros
        - Neutralização preventiva de objeções
        
        3. FASE DE ATIVAÇÃO:
        - Momentos de ativação de drivers específicos
        - Escalada emocional controlada
        - Sinais de prontidão para pitch
        - Gatilhos de urgência apropriados
        
        4. FASE DE TRANSIÇÃO:
        - Como migrar do pré-pitch para pitch
        - Sinais que indicam momento certo
        - Bridging emocional eficaz
        - Manutenção do momentum
        
        5. CRONOGRAMA E SEQUÊNCIA:
        - Timeline ideal para cada fase
        - Indicadores de progressão
        - Pontos de decisão críticos
        - Sistemas de fallback
        
        Integre PERFEITAMENTE drivers e anti-objeções.
        """
        
        analysis_result = self._execute_analysis_with_backup(prepitch_prompt)
        
        return {
            'prepitch_architecture': analysis_result,
            'phase_structure': 'complete',
            'integration_status': 'ready',
            'timestamp': time.time()
        }
    
    def _execute_analysis_with_backup(self, prompt: str) -> Dict[str, Any]:
        """Executa análise usando sistema de backup"""
        try:
            # Tentar usar sistema de backup simplificado para análise
            if hasattr(self.backup_manager, 'services_available'):
                
                # Tentar OpenAI primeiro
                if self.backup_manager.services_available.get('openai'):
                    try:
                        from openai import OpenAI
                        client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
                        
                        response = client.chat.completions.create(
                            model="gpt-4o",
                            messages=[{"role": "user", "content": prompt}],
                            max_tokens=3000,
                            temperature=0.7
                        )
                        
                        return {
                            'content': response.choices[0].message.content,
                            'source': 'OpenAI GPT-4o',
                            'quality': 'high'
                        }
                    except Exception as e:
                        logger.warning(f"Erro no OpenAI: {e}")
                
                # Tentar Gemini como backup
                if self.backup_manager.services_available.get('gemini'):
                    try:
                        from google import genai
                        client = genai.Client(api_key=os.environ.get('GEMINI_API_KEY'))
                        
                        response = client.models.generate_content(
                            model="gemini-2.5-flash",
                            contents=prompt
                        )
                        
                        return {
                            'content': response.text,
                            'source': 'Google Gemini',
                            'quality': 'high'
                        }
                    except Exception as e:
                        logger.warning(f"Erro no Gemini: {e}")
            
            # Fallback para análise estruturada
            return self._structured_analysis_fallback(prompt)
            
        except Exception as e:
            logger.error(f"Erro na execução com backup: {e}")
            return self._structured_analysis_fallback(prompt)
    
    def _structured_analysis_fallback(self, prompt: str) -> Dict[str, Any]:
        """Análise estruturada quando IA não está disponível"""
        
        # Extrair contexto do prompt
        context = {
            'product_mentioned': 'produto' in prompt.lower(),
            'market_analysis': 'mercado' in prompt.lower(),
            'psychology_focus': 'psicológico' in prompt.lower(),
            'drivers_focus': 'drivers' in prompt.lower(),
            'objections_focus': 'objeções' in prompt.lower()
        }
        
        if context['market_analysis']:
            content = self._generate_market_analysis_structure()
        elif context['drivers_focus']:
            content = self._generate_drivers_structure()
        elif context['objections_focus']:
            content = self._generate_objections_structure()
        else:
            content = self._generate_general_psychology_structure()
        
        return {
            'content': content,
            'source': 'Structured Analysis',
            'quality': 'medium'
        }
    
    def _generate_market_analysis_structure(self) -> str:
        return """
        ANÁLISE PSICOLÓGICA DE MERCADO
        
        1. PERFIL PSICOLÓGICO DO MERCADO
        - Consumidores brasileiros demonstram comportamento de pesquisa antes da compra
        - Valorização de confiança e credibilidade da marca
        - Influência forte de recomendações pessoais e sociais
        - Sensibilidade a preço equilibrada com percepção de valor
        
        2. ANÁLISE COMPETITIVA PSICOLÓGICA
        - Mercado com múltiplos players disputando atenção
        - Diferenciação baseada em conexão emocional
        - Oportunidades em nichos específicos pouco explorados
        - Necessidade de posicionamento claro e consistente
        
        3. TENDÊNCIAS COMPORTAMENTAIS
        - Crescimento do consumo digital e pesquisa online
        - Busca por conveniência e soluções práticas
        - Valorização de sustentabilidade e responsabilidade social
        - Preferência por experiências personalizadas
        
        4. INSIGHTS ESTRATÉGICOS
        - Foco em benefícios tangíveis e demonstráveis
        - Importância de prova social e depoimentos
        - Necessidade de educação do mercado sobre benefícios
        - Oportunidade de criar relacionamento de longo prazo
        """
    
    def _generate_drivers_structure(self) -> str:
        return """
        SISTEMA DE DRIVERS MENTAIS
        
        1. DRIVER PRIMÁRIO: SEGURANÇA E CONFIANÇA
        - Necessidade fundamental de sentir-se protegido na decisão
        - Ativação através de garantias, certificações e provas sociais
        - Momento ideal: Antes da apresentação da oferta
        - Implementação: Depoimentos, avaliações, histórico da empresa
        
        2. DRIVERS SECUNDÁRIOS:
        
        A) CONVENIÊNCIA E PRATICIDADE
        - Valorização de soluções que simplifiquem a vida
        - Ativação: Demonstrações de facilidade de uso
        - Combinação eficaz com driver de economia de tempo
        
        B) STATUS E RECONHECIMENTO
        - Desejo de ser visto positivamente pelos pares
        - Ativação: Associação com sucesso e prestígio
        - Cuidado para não parecer superficial
        
        C) ECONOMIA E VALOR
        - Necessidade de justificar investimento
        - Ativação: Comparações, ROI, custo-benefício
        - Importante balancear com qualidade
        
        3. DRIVERS DE URGÊNCIA:
        - Escassez limitada e temporária
        - Oportunidades que não se repetem
        - Consequências da inação
        - Benefícios de ação imediata
        
        4. IMPLEMENTAÇÃO SEQUENCIAL:
        - Estabelecer confiança primeiro
        - Demonstrar valor e conveniência
        - Ativar urgência apropriada
        - Manter consistência na mensagem
        """
    
    def _generate_objections_structure(self) -> str:
        return """
        MAPEAMENTO E TRATAMENTO DE OBJEÇÕES
        
        1. OBJEÇÕES CONSCIENTES PRINCIPAIS:
        
        A) "É muito caro"
        - Origem: Falta de percepção de valor
        - Anti-objeção: Demonstração de ROI e comparações
        - Momento: Após estabelecer valor, antes do preço
        - Prova social: Cases de clientes similares
        
        B) "Não conheço a empresa"
        - Origem: Necessidade de segurança e confiança
        - Anti-objeção: Credenciais, certificações, histórico
        - Momento: Início da apresentação
        - Prova social: Depoimentos e avaliações
        
        C) "Preciso pensar"
        - Origem: Medo de tomar decisão errada
        - Anti-objeção: Garantias e processo de teste
        - Momento: Após apresentação completa
        - Prova social: Política de satisfação
        
        2. OBJEÇÕES INCONSCIENTES:
        - Medo de mudança de rotina
        - Preocupação com julgamento de outros
        - Insegurança sobre capacidade de uso
        - Ansiedade sobre comprometimento
        
        3. SISTEMA DE PREVENÇÃO:
        - Abordar benefícios antes de características
        - Usar linguagem do cliente, não técnica
        - Demonstrar facilidade e suporte
        - Oferecer garantias e reversibilidade
        
        4. PROTOCOLO DE RESPOSTA:
        - Escutar completamente a objeção
        - Validar a preocupação do cliente
        - Fornecer informação específica
        - Verificar se objeção foi resolvida
        - Avançar para próximo passo
        """
    
    def _generate_general_psychology_structure(self) -> str:
        return """
        ANÁLISE PSICOLÓGICA GERAL
        
        1. PERFIL COMPORTAMENTAL:
        - Processo de decisão baseado em emoção e lógica
        - Necessidade de validação social e pessoal
        - Influência de experiências passadas
        - Busca por soluções que reflitam identidade
        
        2. MOTIVAÇÕES FUNDAMENTAIS:
        - Segurança e proteção
        - Reconhecimento e status
        - Conveniência e eficiência
        - Economia e valor
        - Realização pessoal
        
        3. BARREIRAS PSICOLÓGICAS:
        - Medo de tomar decisão errada
        - Resistência a mudanças
        - Ceticismo em relação a promessas
        - Preocupação com julgamento social
        
        4. ESTRATÉGIAS DE CONEXÃO:
        - Comunicação clara e honesta
        - Demonstrações práticas de valor
        - Construção gradual de confiança
        - Personalização da abordagem
        - Suporte contínuo e acessível
        """
    
    def _calculate_relevance(self, query: str, content: str) -> float:
        """Calcula relevância entre query e conteúdo"""
        if not content:
            return 0.0
        
        query_words = set(query.lower().split())
        content_words = set(content.lower().split())
        
        intersection = query_words.intersection(content_words)
        if not query_words:
            return 0.0
        
        return len(intersection) / len(query_words)
    
    def _format_market_insights(self, insights: List[Dict[str, Any]]) -> str:
        """Formata insights de mercado para prompt"""
        formatted = []
        for i, insight in enumerate(insights[:8]):
            formatted.append(f"{i+1}. {insight.get('title', '')}: {insight.get('snippet', '')}")
        
        return "\n".join(formatted)
    
    def _extract_market_analysis(self, market_data: Dict[str, Any]) -> str:
        """Extrai análise de mercado para uso em prompts"""
        analysis = market_data.get('analysis', {})
        if isinstance(analysis, dict):
            return analysis.get('content', 'Dados de mercado limitados')
        return str(analysis)[:1000]
    
    def _extract_avatar_analysis(self, avatar_data: Dict[str, Any]) -> str:
        """Extrai análise de avatar para uso em prompts"""
        profile = avatar_data.get('detailed_profile', {})
        if isinstance(profile, dict):
            return profile.get('content', 'Perfil psicológico limitado')
        return str(profile)[:1000]
    
    def _extract_drivers_analysis(self, drivers_data: Dict[str, Any]) -> str:
        """Extrai análise de drivers para uso em prompts"""
        system = drivers_data.get('driver_system', {})
        if isinstance(system, dict):
            return system.get('content', 'Sistema de drivers limitado')
        return str(system)[:1000]
    
    def _extract_objections_analysis(self, objections_data: Dict[str, Any]) -> str:
        """Extrai análise de objeções para uso em prompts"""
        mapping = objections_data.get('objection_mapping', {})
        if isinstance(mapping, dict):
            return mapping.get('content', 'Mapeamento de objeções limitado')
        return str(mapping)[:1000]
    
    def _calculate_confidence_score(self, analysis_result: Dict[str, Any]) -> float:
        """Calcula score de confiança da análise"""
        content = analysis_result.get('content', '')
        
        # Critérios de qualidade
        length_score = min(100, len(content) / 20)  # 20 chars = 1 point
        source_score = 100 if analysis_result.get('source', '').startswith('OpenAI') or analysis_result.get('source', '').startswith('Google') else 60
        
        return (length_score + source_score) / 2
    
    def _fallback_market_analysis(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Análise de mercado estruturada quando dados são limitados"""
        return {
            'content': f"""
            ANÁLISE DE MERCADO ESTRUTURADA
            
            Produto: {input_data.get('product_name', 'N/A')}
            Mercado-alvo: {input_data.get('target_market', 'N/A')}
            
            1. CONTEXTO DE MERCADO:
            - Mercado brasileiro em crescimento digital
            - Consumidores cada vez mais informados
            - Competição crescente em diversos setores
            - Oportunidades em nichos específicos
            
            2. COMPORTAMENTO DO CONSUMIDOR:
            - Pesquisa online antes da compra
            - Valorização de recomendações sociais
            - Sensibilidade a preço vs qualidade
            - Busca por conveniência e praticidade
            
            3. OPORTUNIDADES IDENTIFICADAS:
            - Diferenciação através de experiência
            - Foco em benefícios tangíveis
            - Construção de relacionamento
            - Inovação em atendimento
            """,
            'source': 'Structured Fallback',
            'quality': 'basic'
        }