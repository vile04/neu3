from .openai_client import OpenAIClient
from .gemini_client import GeminiClient
import json

class MentalDriversService:
    def __init__(self):
        self.openai_client = OpenAIClient()
        self.gemini_client = GeminiClient()
        
        # 19 Universal Mental Drivers Framework
        self.universal_drivers = {
            "ferida_exposta": {
                "trigger": "Dor não resolvida",
                "mechanism": "Trazer à consciência o que foi reprimido",
                "activation": "Você ainda [comportamento doloroso] mesmo sabendo que [consequência]?"
            },
            "trofeu_secreto": {
                "trigger": "Desejo inconfessável",
                "mechanism": "Validar ambições 'proibidas'",
                "activation": "Não é sobre dinheiro, é sobre [desejo real oculto]"
            },
            "inveja_produtiva": {
                "trigger": "Comparação com pares",
                "mechanism": "Transformar inveja em combustível",
                "activation": "Enquanto você [situação atual], outros como você [resultado desejado]"
            },
            "relogio_psicologico": {
                "trigger": "Urgência existencial",
                "mechanism": "Tempo como recurso finito",
                "activation": "Quantos [período] você ainda vai [desperdício]?"
            },
            "identidade_aprisionada": {
                "trigger": "Conflito entre quem é e quem poderia ser",
                "mechanism": "Expor a máscara social",
                "activation": "Você não é [rótulo limitante], você é [potencial real]"
            },
            "custo_invisivel": {
                "trigger": "Perda não percebida",
                "mechanism": "Quantificar o preço da inação",
                "activation": "Cada dia sem [solução] custa [perda específica]"
            },
            "ambicao_expandida": {
                "trigger": "Sonhos pequenos demais",
                "mechanism": "Elevar o teto mental de possibilidades",
                "activation": "Se o esforço é o mesmo, por que você está pedindo tão pouco?"
            },
            "diagnostico_brutal": {
                "trigger": "Confronto com a realidade atual",
                "mechanism": "Criar indignação produtiva com status quo",
                "activation": "Olhe seus números/situação. Até quando você vai aceitar isso?"
            },
            "ambiente_vampiro": {
                "trigger": "Consciência do entorno tóxico",
                "mechanism": "Revelar como ambiente atual suga energia/potencial",
                "activation": "Seu ambiente te impulsiona ou te mantém pequeno?"
            },
            "mentor_salvador": {
                "trigger": "Necessidade de orientação externa",
                "mechanism": "Ativar desejo por figura de autoridade que acredita neles",
                "activation": "Você precisa de alguém que veja seu potencial quando você não consegue"
            },
            "coragem_necessaria": {
                "trigger": "Medo paralisante disfarçado",
                "mechanism": "Transformar desculpas em decisões corajosas",
                "activation": "Não é sobre condições perfeitas, é sobre decidir apesar do medo"
            },
            "mecanismo_revelado": {
                "trigger": "Compreensão do 'como'",
                "mechanism": "Desmistificar o complexo",
                "activation": "É simplesmente [analogia simples], não [complicação percebida]"
            },
            "prova_matematica": {
                "trigger": "Certeza numérica",
                "mechanism": "Equação irrefutável",
                "activation": "Se você fizer X por Y dias = Resultado Z garantido"
            },
            "padrao_oculto": {
                "trigger": "Insight revelador",
                "mechanism": "Mostrar o que sempre esteve lá",
                "activation": "Todos que conseguiram [resultado] fizeram [padrão específico]"
            },
            "excecao_possivel": {
                "trigger": "Quebra de limitação",
                "mechanism": "Provar que regras podem ser quebradas",
                "activation": "Diziam que [limitação], mas [prova contrária]"
            },
            "atalho_etico": {
                "trigger": "Eficiência sem culpa",
                "mechanism": "Validar o caminho mais rápido",
                "activation": "Por que sofrer [tempo longo] se existe [atalho comprovado]?"
            },
            "decisao_binaria": {
                "trigger": "Simplificação radical",
                "mechanism": "Eliminar zona cinzenta",
                "activation": "Ou você [ação desejada] ou aceita [consequência dolorosa]"
            },
            "oportunidade_oculta": {
                "trigger": "Vantagem não percebida",
                "mechanism": "Revelar demanda/chance óbvia mas ignorada",
                "activation": "O mercado está gritando por [solução] e ninguém está ouvindo"
            },
            "metodo_vs_sorte": {
                "trigger": "Caos vs sistema",
                "mechanism": "Contrastar tentativa aleatória com caminho estruturado",
                "activation": "Sem método você está cortando mata com foice. Com método, está na autoestrada"
            }
        }

    def create_customized_drivers(self, input_data, avatar_data):
        """Create customized mental drivers based on avatar psychology"""
        try:
            customization_prompt = f"""
            You are the Architect of Mental Drivers, an expert in creating psychological anchoring triggers 
            that function as emotional and rational frameworks in the target audience's mind.

            Based on the following information, create a comprehensive customized mental drivers framework:

            PRODUCT INFORMATION:
            Product: {input_data.get('product_name')}
            Description: {input_data.get('product_description')}
            Target Market: {input_data.get('target_market')}
            Price Range: {input_data.get('price_range')}

            AVATAR PSYCHOLOGY:
            {json.dumps(avatar_data, indent=2)}

            UNIVERSAL DRIVERS REFERENCE:
            {json.dumps(self.universal_drivers, indent=2)}

            Create a customized mental drivers framework that includes:

            1. SELECTED DRIVERS: Choose the 7-10 most relevant universal drivers for this specific avatar and product.

            2. CUSTOMIZED ACTIVATIONS: For each selected driver, create specific activation scripts customized to:
               - The avatar's language patterns and preferences
               - The specific product and market context
               - The psychological triggers identified in the avatar analysis

            3. IMPLEMENTATION STRATEGY: For each driver, specify:
               - Optimal installation moment (when to introduce)
               - Specific activation phrases and scripts
               - Supporting evidence and proof elements
               - Reactivation triggers for reinforcement
               - Integration with other drivers

            4. PSYCHOLOGICAL SEQUENCE: Arrange the drivers in optimal psychological progression:
               - Awareness phase drivers (consciousness creation)
               - Desire phase drivers (motivation amplification)
               - Decision phase drivers (action forcing)
               - Direction phase drivers (path provision)

            5. CUSTOMIZATION DETAILS: For each driver, include:
               - Avatar-specific pain points it addresses
               - Custom analogies and metaphors that resonate
               - Specific language patterns and terminology
               - Cultural and demographic considerations
               - Emotional intensity calibration

            Format the response as detailed JSON with comprehensive implementation guidance.
            """
            
            # Get customized drivers from OpenAI
            customized_drivers = self.openai_client.create_mental_drivers(customization_prompt)
            
            return customized_drivers
            
        except Exception as e:
            return {"error": f"Mental drivers creation failed: {str(e)}"}

    def get_driver_combinations(self):
        """Get optimal driver combinations for different scenarios"""
        return {
            "awareness_phase": [
                "oportunidade_oculta",
                "diagnostico_brutal", 
                "ferida_exposta"
            ],
            "desire_phase": [
                "ambicao_expandida",
                "trofeu_secreto",
                "inveja_produtiva"
            ],
            "decision_phase": [
                "relogio_psicologico",
                "custo_invisivel",
                "decisao_binaria"
            ],
            "direction_phase": [
                "metodo_vs_sorte",
                "mentor_salvador",
                "coragem_necessaria"
            ]
        }

    def validate_driver_effectiveness(self, drivers_data, avatar_data):
        """Validate the effectiveness of created drivers against avatar psychology"""
        try:
            validation_prompt = f"""
            Analyze the effectiveness of these mental drivers against the target avatar psychology:

            MENTAL DRIVERS:
            {json.dumps(drivers_data, indent=2)}

            AVATAR PSYCHOLOGY:
            {json.dumps(avatar_data, indent=2)}

            Provide a detailed validation analysis including:

            1. RESONANCE ASSESSMENT: How well each driver aligns with avatar psychology
            2. TRIGGER EFFECTIVENESS: Likelihood each driver will create desired response
            3. SEQUENCE OPTIMIZATION: Whether the driver sequence creates optimal progression
            4. GAP IDENTIFICATION: Missing psychological elements that should be addressed
            5. IMPROVEMENT RECOMMENDATIONS: Specific suggestions for enhancement

            Format as structured JSON with detailed analysis.
            """
            
            validation_result = self.openai_client.synthesize_insights(validation_prompt)
            return validation_result
            
        except Exception as e:
            return {"error": f"Driver validation failed: {str(e)}"}
