from .openai_client import OpenAIClient
from .gemini_client import GeminiClient
import json

class ObjectionAnalysisService:
    def __init__(self):
        self.openai_client = OpenAIClient()
        self.gemini_client = GeminiClient()
        
        # Universal objections framework
        self.universal_objections = {
            "time_objections": {
                "surface": "Não tenho tempo",
                "hidden_roots": ["Não é prioridade", "Medo de compromisso", "Perfeccionismo"],
                "neutralization": "Reframe como importância vs tempo"
            },
            "money_objections": {
                "surface": "Não tenho dinheiro",
                "hidden_roots": ["Prioridades desalinhadas", "Medo de perda", "Desvalorização do resultado"],
                "neutralization": "Demonstrar custo de oportunidade"
            },
            "trust_objections": {
                "surface": "Preciso pensar",
                "hidden_roots": ["Experiências passadas negativas", "Medo de ser enganado", "Baixa autoestima"],
                "neutralization": "Construir autoridade e reduzir risco"
            },
            "hidden_objections": {
                "autossuficiencia": "Acho que consigo sozinho",
                "fraqueza": "Aceitar ajuda é admitir fracasso",
                "medo_mudanca": "Não tenho pressa",
                "prioridades": "Não é dinheiro mas prioridade",
                "autoestima": "Não confio em mim mesmo"
            }
        }

    def analyze_objections(self, input_data, avatar_data):
        """Comprehensive objection analysis with counter-strategies"""
        try:
            objection_analysis_prompt = f"""
            You are a master of objection psychology and sales resistance analysis. You can identify not just 
            the surface objections people voice, but the deep psychological roots that drive their resistance.

            Analyze the following context and create a comprehensive objection analysis system:

            PRODUCT CONTEXT:
            Product: {input_data.get('product_name')}
            Description: {input_data.get('product_description')}
            Target Market: {input_data.get('target_market')}
            Price Range: {input_data.get('price_range')}

            AVATAR PSYCHOLOGY:
            {json.dumps(avatar_data, indent=2)}

            UNIVERSAL OBJECTIONS FRAMEWORK:
            {json.dumps(self.universal_objections, indent=2)}

            Create a comprehensive objection analysis including:

            FASE 1: MAPEAMENTO EMOCIONAL GERAL
            - Temperatura emocional dominante do avatar
            - Nível de vulnerabilidade demonstrado
            - Padrões de linguagem e resistência
            - Sinais de abertura vs resistência à mudança

            FASE 2: IDENTIFICAÇÃO DAS DORES PRIMÁRIAS
            - Intensidade emocional das dores mencionadas
            - Frequência e personalização das dores
            - Urgência vs conformismo
            - Histórico de tentativas e frustrações

            FASE 3: DIAGNÓSTICO DE OBJEÇÕES ESPECÍFICAS

            For each objection category, analyze:

            OBJEÇÕES DE TEMPO:
            - Frases específicas usadas para justificar falta de tempo
            - Atividades mencionadas como prioritárias
            - Sinais de procrastinação vs genuína falta de tempo
            - Como descrevem sua rotina atual

            TRATAMENTO ESPECÍFICO:
            - Drives mentais para elevar prioridade
            - Histórias de consequência de inação
            - Reformulação de "tempo" como "importância"
            - Cálculo de custo de oportunidade

            OBJEÇÕES DE DINHEIRO:
            - Como se referem à questão financeira
            - Outras áreas onde investem/gastam
            - Sinais de dificuldade genuína vs prioridade desalinhada
            - Como justificam gastos em outras áreas

            TRATAMENTO ESPECÍFICO:
            - Técnica "piorar a vida" aplicada
            - Comparações de investimento (educação vs consumo)
            - Histórias de ROI de outros clientes similares
            - Ressignificação: gasto vs investimento vs custo de não agir

            OBJEÇÕES DE CONFIANÇA:
            - Em quem/o que demonstram desconfiança
            - Experiências passadas negativas mencionadas
            - Como se referem a autoridades do nicho
            - Sinais de desconfiança em si mesmos

            TRATAMENTO ESPECÍFICO:
            - Provas sociais específicas para este perfil
            - Garantias que removem riscos percebidos
            - Autoridade construída através de conhecimento técnico
            - Validação de suas preocupações como legítimas

            FASE 4: OBJEÇÕES OCULTAS IDENTIFICADAS

            For each hidden objection, analyze:

            AUTOSSUFICIÊNCIA DETECTADA:
            - Sinais: Menções de "tentar sozinho", resistência a ajuda
            - Perfil típico: Pessoas com formação, experiência, ego profissional
            - Raiz emocional: Medo de parecer incompetente
            - CONTRA-ATAQUE: Histórias de experts que precisaram de mentoria

            AJUDA COMO FRAQUEZA:
            - Sinais: Minimização de problemas, resistência a expor vulnerabilidade
            - Perfil típico: Líderes, pessoas com imagem a zelar
            - Raiz emocional: Medo de julgamento, perda de status
            - CONTRA-ATAQUE: Reposicionamento como "aceleração"

            MEDO DO NOVO/MUDANÇA:
            - Sinais: "Quando for a hora certa", procrastinação disfarçada
            - Perfil típico: Pessoas estagnadas mas "confortáveis"
            - Raiz emocional: Ansiedade sobre nova realidade
            - CONTRA-ATAQUE: Histórias de arrependimento + consequências futuras

            PRIORIDADES DESEQUILIBRADAS:
            - Sinais: Gastos em outras áreas, justificativas contraditórias
            - Perfil típico: Gastam em lazer mas "não têm dinheiro" para evolução
            - Raiz emocional: Não reconhece educação como prioridade
            - CONTRA-ATAQUE: Comparação cruel + cálculo de oportunidade perdida

            AUTOESTIMA DESTRUÍDA:
            - Sinais: "Já tentei antes", histórico de fracassos, vitimização
            - Perfil típico: Múltiplas tentativas fracassadas
            - Raiz emocional: "Sou eu o problema", medo de mais fracasso
            - CONTRA-ATAQUE: Cases de pessoas "piores" que conseguiram

            FASE 5: ARSENAL DE DRIVES ANTI-OBJEÇÃO

            Create specific mental drives for objection destruction:

            DRIVES DE ELEVAÇÃO DE PRIORIDADE (Tempo):
            - Cálculo da Sangria
            - Consequência Exponencial  
            - Janela de Oportunidade

            DRIVES DE JUSTIFICAÇÃO DE INVESTIMENTO (Dinheiro):
            - Comparação Cruel
            - ROI Absurdo
            - Custo de Oportunidade Gigante

            DRIVES DE CONSTRUÇÃO DE CONFIANÇA:
            - Autoridade Técnica Inquestionável
            - Prova Social Qualificada
            - Garantia Agressiva

            DRIVES PARA OBJEÇÕES OCULTAS:
            - O Expert que Precisou de Expert
            - Aceleração vs Tentativa
            - Reframe de Inteligência
            - Histórias de Heróis Vulneráveis
            - Dor da Estagnação

            For each drive, include:
            - Template de ativação
            - Aplicação específica ao avatar
            - Exemplo customizado
            - Momento ideal de uso
            - Frases de ancoragem

            Format as comprehensive JSON with detailed implementation strategies.
            """

            # Get objection analysis from OpenAI
            objection_analysis = self.openai_client.analyze_objections(objection_analysis_prompt)
            
            # Enhance with Gemini insights
            enhancement_prompt = f"""
            Enhance this objection analysis with additional psychological insights and counter-strategies:

            {json.dumps(objection_analysis, indent=2)}

            Add:
            1. Advanced psychological neutralization techniques
            2. Preemptive objection prevention strategies
            3. Emotional objection handling approaches
            4. Cultural and demographic specific considerations
            5. Advanced reframe techniques for resistant personalities

            Format as detailed JSON with practical implementation guidance.
            """

            enhanced_analysis = self.gemini_client.analyze_avatar_psychology(enhancement_prompt)
            
            # Create comprehensive objection system
            complete_system = {
                "objection_analysis": objection_analysis,
                "enhanced_insights": enhanced_analysis,
                "implementation_framework": self._create_implementation_framework(),
                "neutralization_scripts": self._create_neutralization_scripts(objection_analysis),
                "tracking_system": self._create_objection_tracking_system()
            }
            
            return complete_system
            
        except Exception as e:
            return {"error": f"Objection analysis failed: {str(e)}"}

    def _create_implementation_framework(self):
        """Create implementation framework for objection handling"""
        return {
            "prevention_strategies": {
                "preemptive_addressing": "Address objections before they're voiced through content",
                "mental_preparation": "Install supporting beliefs that prevent objections",
                "social_proof_loading": "Provide evidence that counters common objections",
                "authority_establishment": "Build credibility to reduce skepticism"
            },
            "response_protocols": {
                "listen_fully": "Never interrupt or dismiss objections",
                "acknowledge_validity": "Validate concerns before addressing them",
                "ask_clarifying_questions": "Understand the root concern",
                "provide_specific_evidence": "Use concrete proof rather than generalizations",
                "check_satisfaction": "Ensure the objection is fully resolved"
            },
            "escalation_procedures": {
                "multiple_objections": "Address systematically, don't overwhelm",
                "emotional_objections": "Handle feelings before facts",
                "logical_objections": "Provide data and evidence",
                "hidden_objections": "Use indirect approaches and stories"
            }
        }

    def _create_neutralization_scripts(self, objection_data):
        """Create specific scripts for objection neutralization"""
        scripts = {
            "time_objection_scripts": [
                "I understand time is precious. That's exactly why this works - it's designed for busy people like you.",
                "The question isn't whether you have time, but whether you can afford not to make time for this.",
                "What if I told you this could actually give you back more time than it takes?"
            ],
            "money_objection_scripts": [
                "I appreciate you being honest about your budget concerns. Let me ask you this...",
                "The real question is: what's it costing you NOT to solve this problem?",
                "This isn't an expense, it's an investment. Let me show you the math."
            ],
            "trust_objection_scripts": [
                "I respect that you're being careful. That shows good judgment.",
                "What specific concerns do you have? I'd rather address them directly.",
                "Here's what others in your exact situation said before they got results..."
            ],
            "hidden_objection_scripts": [
                "Many successful people I work with initially thought they could handle this alone...",
                "The strongest people I know are the ones who recognize when to get help.",
                "Staying where you are isn't actually safer - it's the riskiest choice of all."
            ]
        }
        
        return scripts

    def _create_objection_tracking_system(self):
        """Create system for tracking and analyzing objections"""
        return {
            "objection_categories": [
                "Time/Priority",
                "Money/Investment", 
                "Trust/Credibility",
                "Authority/Competence",
                "Fear/Risk",
                "Past Experience",
                "Decision Process"
            ],
            "tracking_metrics": [
                "Objection frequency by category",
                "Resolution success rate",
                "Time to resolution",
                "Follow-up objections",
                "Conversion after objection handling"
            ],
            "optimization_indicators": [
                "Most common objections (need better prevention)",
                "Hardest to resolve objections (need better scripts)",
                "Objections that kill deals (need priority focus)",
                "Successful resolution patterns (replicate approach)"
            ]
        }

    def validate_objection_strategies(self, objection_data, avatar_data):
        """Validate objection handling strategies against avatar psychology"""
        try:
            validation_prompt = f"""
            Validate the effectiveness of these objection handling strategies against the target avatar:

            OBJECTION STRATEGIES:
            {json.dumps(objection_data, indent=2)}

            AVATAR PSYCHOLOGY:
            {json.dumps(avatar_data, indent=2)}

            Analyze:
            1. Strategy Alignment: How well strategies match avatar communication style
            2. Psychological Resonance: Whether approaches address core emotional drivers
            3. Resistance Prediction: Likelihood of creating additional resistance
            4. Trust Building: Whether strategies enhance or diminish credibility
            5. Effectiveness Probability: Success likelihood for each strategy
            6. Improvement Recommendations: Specific optimizations for better results

            Format as detailed JSON analysis.
            """
            
            validation = self.openai_client.synthesize_insights(validation_prompt)
            return validation
            
        except Exception as e:
            return {"error": f"Objection validation failed: {str(e)}"}
