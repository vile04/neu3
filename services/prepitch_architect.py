from .openai_client import OpenAIClient
from .gemini_client import GeminiClient
import json

class PrePitchArchitectService:
    def __init__(self):
        self.openai_client = OpenAIClient()
        self.gemini_client = GeminiClient()

    def create_prepitch_sequence(self, drivers_data, objections_data):
        """Create comprehensive pre-pitch invisible architecture"""
        try:
            prepitch_prompt = f"""
            You are the Master of Invisible Pre-Pitch, specialist in creating psychological installation 
            sequences that make prospects BEG for the offer before you even present it.

            Your mission: Take the mental drivers already created and orchestrate a SYMPHONY OF 
            PSYCHOLOGICAL TENSION that prepares the mental terrain so precisely that the sale becomes 
            just a formality.

            MENTAL DRIVERS AVAILABLE:
            {json.dumps(drivers_data, indent=2)}

            OBJECTION INTELLIGENCE:
            {json.dumps(objections_data, indent=2)}

            Create a comprehensive pre-pitch invisible architecture following this structure:

            FASE 1: ORQUESTRAÇÃO EMOCIONAL (70% do tempo)

            OBJETIVO: Criar uma MONTANHA-RUSSA EMOCIONAL que:
            - Desperta consciência da dor
            - Amplifica o desejo latente  
            - Instala urgência visceral
            - Ativa os drivers em sequência estratégica

            SEQUÊNCIA PSICOLÓGICA:
            1. QUEBRA → Destruir a ilusão confortável
            2. EXPOSIÇÃO → Revelar a ferida real
            3. INDIGNAÇÃO → Criar revolta produtiva
            4. VISLUMBRE → Mostrar o possível
            5. TENSÃO → Amplificar o gap
            6. NECESSIDADE → Tornar a mudança inevitável

            FASE 2: JUSTIFICAÇÃO LÓGICA (30% do tempo)

            OBJETIVO: Dar ao cérebro racional as PROVAS que ele precisa para validar a decisão 
            emocional já tomada

            ELEMENTOS ESSENCIAIS:
            - Números e estatísticas irrefutáveis
            - Cálculos de ROI conservadores
            - Demonstrações passo a passo
            - Cases com métricas específicas
            - Garantias que eliminam risco

            ETAPA 1: ANÁLISE E SELEÇÃO DE DRIVERS

            From the available drivers, select and organize:

            1. IDENTIFICAR OS 5-7 DRIVERS PRINCIPAIS
            - Quais atacam as objeções mais fortes?
            - Quais geram mais tensão emocional?
            - Quais se conectam melhor em sequência?

            2. MAPEAR ORDEM PSICOLÓGICA IDEAL
            - Começar com consciência (Diagnóstico/Oportunidade)
            - Evoluir para desejo (Ambição/Troféu)
            - Criar pressão (Urgência/Custo)
            - Oferecer caminho (Método/Mentor)
            - Forçar decisão (Coragem/Binária)

            3. DEFINIR MOMENTOS DE ATIVAÇÃO
            - Onde cada driver será instalado/ativado
            - Quanto tempo dedicar a cada um
            - Como fazer transições suaves

            ETAPA 2: CRIAÇÃO DO ROTEIRO COMPLETO

            Create complete scripts for different formats:

            PRÉ-PITCH PARA WEBINÁRIO (60-90 min)
            - Pré-pitch: 15-20 minutos antes do pitch
            - Foco: Urgência e método
            - Velocidade: Rápida, dinâmica

            PRÉ-PITCH PARA EVENTO PRESENCIAL (1-3 dias)
            - Pré-pitch: Distribuído ao longo do evento
            - Foco: Transformação profunda
            - Velocidade: Construção gradual

            PRÉ-PITCH PARA CPL (3 aulas)
            - Pré-pitch: Final da aula 3
            - Foco: Consolidação e decisão
            - Velocidade: Crescente

            PRÉ-PITCH PARA LIVES DE AQUECIMENTO
            - Pré-pitch: Sementes em cada live
            - Foco: Preparação subliminar
            - Velocidade: Sutil

            For each format, create:

            PRÉ-PITCH PARA [FORMATO]
            ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

            📍 CONTEXTO
            - Formato: [Webinar/Evento/CPL/Live]
            - Duração: [Tempo total disponível]
            - Momento: [Quando acontece no funil]
            - Estado mental esperado: [Como chegam]

            🎯 OBJETIVO ESPECÍFICO
            [Que transformação mental queremos ao final]

            🎭 ROTEIRO COMPLETO

            ── ABERTURA (X minutos) ──────────
            DRIVER: [Nome do Driver]
            INSTALAÇÃO: [Como introduzir]
            NARRATIVA: "[História/analogia específica]"
            PERGUNTA ÂNCORA: "[Pergunta que fica ecoando]"

            ── DESENVOLVIMENTO (X minutos) ────
            [Repeat structure for each driver]

            ── TRANSIÇÃO PARA LÓGICA (X min) ─
            PONTE: "[Frase que conecta emoção com lógica]"

            ── PROVA LÓGICA (X minutos) ──────
            NÚMEROS: [Estatísticas/dados]
            CÁLCULO: [ROI demonstrado]
            CASES: [Exemplos com métricas]
            DEMONSTRAÇÃO: [Passo a passo visual]

            ── FECHAMENTO PRÉ-PITCH (X min) ──
            DRIVER FINAL: [Urgência/Decisão]
            TRANSIÇÃO: "[Como levar ao pitch sem parecer]"
            ESTADO FINAL: [Como devem estar mentalmente]

            💬 SCRIPTS ESPECÍFICOS
            [Frases exatas para momentos cruciais]

            ⚡ ELEMENTOS DE TENSÃO
            [Como manter engajamento alto]

            🎯 MÉTRICAS DE SUCESSO
            [Como saber se funcionou]

            TEMPLATES PRONTOS:

            TEMPLATE 1: ABERTURA PADRÃO
            "Deixa eu te fazer uma pergunta difícil...
            [DRIVER DE DIAGNÓSTICO]
            
            Sabe por que isso dói tanto ouvir?
            Porque no fundo você sabe que é verdade.
            
            E sabe o que é pior?
            [DRIVER DE CUSTO INVISÍVEL]
            
            Mas calma, não vim aqui só pra abrir feridas...
            [TRANSIÇÃO PARA ESPERANÇA]"

            TEMPLATE 2: TRANSIÇÃO EMOÇÃO→LÓGICA
            "Eu sei que você está sentindo isso agora...
            Aquela mistura de indignação com esperança.
            
            Mas seu cérebro racional está gritando:
            'Será que funciona mesmo?'
            
            Então deixa eu te mostrar os números...
            [ENTRAR NA PROVA LÓGICA]"

            TEMPLATE 3: FECHAMENTO PRÉ-PITCH
            "Agora você tem duas escolhas:
            [DRIVER DE DECISÃO BINÁRIA]
            
            Eu vou te mostrar exatamente como fazer isso...
            Mas antes, preciso saber:
            Você está pronto para parar de [dor] e começar a [desejo]?
            
            [PAUSA DRAMÁTICA]
            
            Então presta atenção no que vem agora..."

            ELEMENTOS AVANÇADOS:

            TÉCNICAS DE AMPLIFICAÇÃO:
            1. Contrastes extremos (antes miserável vs depois glorioso)
            2. Provas sociais estratégicas (case igual ao avatar)
            3. Urgência crescente (sutil → explosiva)

            SINAIS DE SUCESSO:
            - Durante: Silêncio absoluto, perguntas sobre "quando abre"
            - Após: Ansiedade para oferta, "já quero comprar"

            The pré-pitch should be so powerful that the prospect arrives at the offer moment 
            already convinced, just waiting to know HOW to buy, not IF they should buy.

            Format as comprehensive JSON with complete implementation guidance.
            """

            # Create pre-pitch architecture using Gemini
            prepitch_architecture = self.gemini_client.create_prepitch_architecture(prepitch_prompt)
            
            # Enhance with OpenAI optimization
            optimization_prompt = f"""
            Optimize this pre-pitch architecture for maximum psychological impact and conversion:

            {json.dumps(prepitch_architecture, indent=2)}

            Provide optimizations including:
            1. Psychological sequence refinement for optimal flow
            2. Timing optimization for maximum impact
            3. Transition smoothness between emotional and logical phases
            4. Resistance handling during pre-pitch execution
            5. Adaptation strategies for different audience responses
            6. Measurement and optimization frameworks

            Format as detailed JSON with practical implementation guidance.
            """
            
            optimized_architecture = self.openai_client.synthesize_insights(optimization_prompt)
            
            # Create complete pre-pitch system
            complete_system = {
                "core_architecture": prepitch_architecture,
                "optimization_framework": optimized_architecture,
                "implementation_guide": self._create_implementation_guide(),
                "format_adaptations": self._create_format_adaptations(),
                "success_metrics": self._create_success_metrics()
            }
            
            return complete_system
            
        except Exception as e:
            return {"error": f"Pre-pitch architecture creation failed: {str(e)}"}

    def _create_implementation_guide(self):
        """Create comprehensive implementation guide"""
        return {
            "preparation_phase": {
                "script_mastery": "Memorize key transitions and anchor phrases",
                "timing_practice": "Rehearse timing for each segment",
                "contingency_planning": "Prepare for audience resistance or low energy",
                "material_preparation": "Gather all supporting materials and proof elements"
            },
            "execution_principles": {
                "energy_management": "Start high energy and build progressively",
                "audience_reading": "Constantly gauge emotional temperature",
                "flexibility": "Adapt timing and intensity based on response",
                "commitment": "Don't back down from psychological pressure"
            },
            "transition_mastery": {
                "emotional_to_logical": "Acknowledge feelings before presenting facts",
                "driver_to_driver": "Use callback phrases to connect concepts",
                "resistance_handling": "Use resistance as fuel for next driver",
                "building_momentum": "Each element should amplify the next"
            },
            "troubleshooting": {
                "low_energy_audience": "Increase interaction and personal examples",
                "high_resistance": "Acknowledge resistance and use it productively",
                "technical_failures": "Have backup materials and methods ready",
                "time_constraints": "Know which elements are essential vs optional"
            }
        }

    def _create_format_adaptations(self):
        """Create adaptations for different presentation formats"""
        return {
            "webinar_60_min": {
                "pre_pitch_duration": "12-15 minutes",
                "key_focus": "Urgency and method demonstration",
                "energy_level": "High intensity, fast pace",
                "interaction": "Chat questions and polls",
                "transition_to_pitch": "Direct and immediate"
            },
            "webinar_90_min": {
                "pre_pitch_duration": "18-22 minutes", 
                "key_focus": "Deep pain awareness and solution preview",
                "energy_level": "Building intensity with peaks",
                "interaction": "More detailed Q&A integration",
                "transition_to_pitch": "Natural evolution"
            },
            "live_event_1_day": {
                "pre_pitch_duration": "Distributed throughout day",
                "key_focus": "Progressive psychological installation",
                "energy_level": "Sustained building with breaks",
                "interaction": "High audience participation",
                "transition_to_pitch": "Climactic moment"
            },
            "cpl_sequence": {
                "pre_pitch_duration": "Final 20 minutes of last class",
                "key_focus": "Consolidation and decision forcing",
                "energy_level": "Crescendo to maximum intensity",
                "interaction": "Personal commitment exercises",
                "transition_to_pitch": "Inevitable conclusion"
            },
            "social_media_series": {
                "pre_pitch_duration": "Multiple posts over days/weeks",
                "key_focus": "Subliminal preparation and awareness",
                "energy_level": "Gradual building across content",
                "interaction": "Comments and shares",
                "transition_to_pitch": "Natural progression"
            }
        }

    def _create_success_metrics(self):
        """Create metrics for measuring pre-pitch effectiveness"""
        return {
            "real_time_indicators": {
                "engagement_metrics": [
                    "Attention level (silence, focus)",
                    "Physical responses (leaning in, nodding)",
                    "Verbal responses (agreement sounds)",
                    "Question quality (deeper, more specific)"
                ],
                "emotional_indicators": [
                    "Facial expressions (concern, excitement)",
                    "Body language (tension, relief)",
                    "Voice tone (urgency, eagerness)",
                    "Participation level (voluntary sharing)"
                ]
            },
            "post_sequence_metrics": {
                "psychological_state": [
                    "Eagerness for solution",
                    "Reduced skepticism", 
                    "Increased urgency",
                    "Enhanced trust"
                ],
                "behavioral_indicators": [
                    "Questions about next steps",
                    "Requests for pricing/availability",
                    "Elimination of major objections",
                    "Forward-looking language"
                ]
            },
            "conversion_metrics": {
                "immediate_response": [
                    "Offer presentation receptivity",
                    "Objection frequency reduction",
                    "Decision speed increase",
                    "Price resistance decrease"
                ],
                "final_outcomes": [
                    "Conversion rate improvement",
                    "Average deal size increase",
                    "Sales cycle length reduction",
                    "Customer satisfaction enhancement"
                ]
            }
        }

    def validate_prepitch_effectiveness(self, prepitch_data, drivers_data, objections_data):
        """Validate pre-pitch architecture effectiveness"""
        try:
            validation_prompt = f"""
            Validate the effectiveness of this pre-pitch architecture:

            PRE-PITCH ARCHITECTURE:
            {json.dumps(prepitch_data, indent=2)}

            MENTAL DRIVERS:
            {json.dumps(drivers_data, indent=2)}

            OBJECTION ANALYSIS:
            {json.dumps(objections_data, indent=2)}

            Analyze:
            1. Psychological Flow: Whether the sequence creates optimal emotional progression
            2. Driver Integration: How well mental drivers are woven into the sequence
            3. Objection Prevention: Whether the sequence prevents or neutralizes objections
            4. Timing Optimization: Whether pacing and duration are appropriate
            5. Transition Quality: How smoothly elements connect and build
            6. Resistance Management: How well potential resistance is handled
            7. Conversion Readiness: Whether prospects will be optimally prepared

            Format as detailed JSON analysis with specific recommendations.
            """
            
            validation = self.openai_client.synthesize_insights(validation_prompt)
            return validation
            
        except Exception as e:
            return {"error": f"Pre-pitch validation failed: {str(e)}"}
