from .gemini_client import GeminiClient
from .openai_client import OpenAIClient
import json

class ProviSystemService:
    def __init__(self):
        self.gemini_client = GeminiClient()
        self.openai_client = OpenAIClient()

    def create_provi_arsenal(self, input_data, drivers_data):
        """Create comprehensive PROVI (Provas Visuais Instantâneas) system"""
        try:
            provi_creation_prompt = f"""
            You are the DIRECTOR SUPREMO DE EXPERIÊNCIAS TRANSFORMADORAS. Your mission is to analyze 
            the sales/launch context and create AUTOMATICALLY a complete arsenal of PROVIs that transform 
            ALL abstract concepts into unforgettable physical experiences.

            CONTEXT ANALYSIS:
            Product: {input_data.get('product_name')}
            Description: {input_data.get('product_description')}
            Target Market: {input_data.get('target_market')}
            Price Range: {input_data.get('price_range')}

            MENTAL DRIVERS TO PROVE:
            {json.dumps(drivers_data, indent=2)}

            FASE 1: ESCANEAMENTO PROFUNDO
            Identify all abstract concepts that need to be proven:
            - Mental drivers mentioned
            - Objections to be destroyed
            - Method principles  
            - Promised transformations
            - Beliefs to be broken
            - Urgencies to be created

            FASE 2: CRIAÇÃO MASSIVA DE PROVIS
            For EACH concept identified, create complete PROVIs following this structure:

            PROVI #X: [IMPACTFUL NAME]
            ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

            CONCEITO-ALVO: [What needs to be installed/destroyed]
            CATEGORIA: [Urgency/Belief/Objection/Transformation/Method]
            PRIORIDADE: [Critical/High/Medium]
            MOMENTO IDEAL: [When to execute in event]

            🎯 OBJETIVO PSICOLÓGICO
            [What specific mental change we want]

            🔬 EXPERIMENTO ESCOLHIDO
            [Clear description of physical demonstration]

            📐 ANALOGIA PERFEITA
            "Just like [experiment] → You [life application]"

            📝 ROTEIRO COMPLETO
            ┌─ SETUP (30s)
            │  [Introduction phrase that creates expectation]
            │  [Physical preparation of experiment]
            │
            ├─ EXECUÇÃO (30-90s)  
            │  [Step 1: Specific action]
            │  [Step 2: Tension moment]
            │  [Step 3: Visual revelation]
            │
            ├─ CLÍMAX (15s)
            │  [The exact "AHA!" moment]
            │  [Expected audience reaction]
            │
            └─ BRIDGE (30s)
               [Direct connection to their life]
               [Powerful rhetorical question]
               [Subliminal action command]

            🛠️ MATERIAIS
            - [Item 1: exact specification]
            - [Item 2: where to get it]
            - [Item 3: possible substitutes]

            ⚡ VARIAÇÕES
            - ONLINE: [Camera adaptation]
            - LARGE AUDIENCE: [Amplified version]
            - INTIMATE: [Simplified version]

            🚨 GESTÃO DE RISCOS
            - CAN FAIL IF: [Situations]
            - PLAN B: [Ready alternative]
            - TURN ERROR: [How to use failure in favor]

            💬 FRASES DE IMPACTO
            - During: "[Phrase that increases tension]"
            - Revelation: "[Phrase at aha moment]"
            - Anchoring: "[Phrase that stays in memory]"

            🎭 DRAMATIZAÇÃO EXTRA (optional)
            [Theatrical elements to amplify impact]

            Create 10-15 complete PROVIs prioritizing the most critical concepts.
            Be CREATIVE, BOLD, and MEMORABLE. Each PROVI should be so impactful that it becomes 
            THE STORY that defines the event.

            Format as detailed JSON with complete implementation guidance.
            """

            # Create PROVIs using Gemini for creativity
            provi_arsenal = self.gemini_client.create_visual_proofs(provi_creation_prompt)
            
            # Enhance with OpenAI analysis
            enhancement_prompt = f"""
            Enhance and optimize this PROVI system for maximum psychological impact:

            {json.dumps(provi_arsenal, indent=2)}

            Provide enhancements including:
            1. Risk assessment and mitigation strategies
            2. Psychological impact optimization
            3. Sequence optimization for maximum effect
            4. Alternative variations for different contexts
            5. Implementation troubleshooting guide

            Format as comprehensive JSON with detailed guidance.
            """
            
            enhanced_provis = self.openai_client.synthesize_insights(enhancement_prompt)
            
            # Combine original and enhanced versions
            complete_system = {
                "original_provis": provi_arsenal,
                "enhanced_analysis": enhanced_provis,
                "implementation_guide": self._create_implementation_guide(),
                "material_checklist": self._create_material_checklist(provi_arsenal)
            }
            
            return complete_system
            
        except Exception as e:
            return {"error": f"PROVI system creation failed: {str(e)}"}

    def _create_implementation_guide(self):
        """Create comprehensive implementation guide for PROVIs"""
        return {
            "preparation_checklist": [
                "Review all PROVI scripts and memorize key phrases",
                "Gather and test all required materials",
                "Practice timing and execution in safe environment",
                "Prepare backup materials and contingency plans",
                "Set up recording/documentation systems for optimization"
            ],
            "execution_principles": [
                "Always test PROVIs beforehand to ensure they work",
                "Have backup plans ready for every demonstration",
                "Use failures as learning opportunities and pivot gracefully",
                "Maintain high energy and confidence throughout",
                "Connect every PROVI directly to audience's experience"
            ],
            "timing_optimization": [
                "Start with medium-impact PROVIs to build momentum",
                "Save highest-impact demonstrations for key decision moments",
                "Allow time for audience processing between PROVIs",
                "Use callbacks to previous PROVIs throughout presentation",
                "End with urgency-creating or action-driving demonstrations"
            ],
            "audience_management": [
                "Read audience energy and adjust PROVI intensity accordingly",
                "Involve audience members when possible for engagement",
                "Address skepticism directly and use it to fuel demonstrations",
                "Create anticipation before each PROVI execution",
                "Use PROVI outcomes to reinforce key messages"
            ]
        }

    def _create_material_checklist(self, provi_data):
        """Create comprehensive material checklist for all PROVIs"""
        materials = {
            "basic_supplies": [
                "Flip chart paper and markers",
                "Clear containers of various sizes",
                "Colored water and food coloring",
                "Timer/stopwatch",
                "Measuring tools (ruler, scale)",
                "Magnifying glass",
                "Simple tools (hammer, screwdriver, etc.)"
            ],
            "demonstration_items": [
                "Playing cards",
                "Dice",
                "Coins",
                "Rubber bands",
                "Paper clips",
                "Balloons",
                "String/rope",
                "Magnets"
            ],
            "visual_aids": [
                "Printed charts and graphs",
                "Before/after photos",
                "Calculator",
                "Whiteboard/easel",
                "Pointer",
                "Props for analogies"
            ],
            "backup_supplies": [
                "Extra materials for each demonstration",
                "Alternative props for failed demonstrations",
                "Cleaning supplies for messy experiments",
                "Extension cords and batteries",
                "Spare markers and paper"
            ]
        }
        
        # Extract specific materials from PROVI data if available
        if isinstance(provi_data, dict) and 'materials' in str(provi_data):
            materials["custom_materials"] = ["Specific materials listed in individual PROVI specifications"]
        
        return materials

    def validate_provi_effectiveness(self, provi_data, avatar_data):
        """Validate PROVI effectiveness against target psychology"""
        try:
            validation_prompt = f"""
            Evaluate the effectiveness of this PROVI system against the target avatar psychology:

            PROVI SYSTEM:
            {json.dumps(provi_data, indent=2)}

            TARGET AVATAR:
            {json.dumps(avatar_data, indent=2)}

            Analyze and provide:
            1. Resonance Assessment: How well PROVIs align with avatar preferences
            2. Comprehension Level: Whether demonstrations match avatar sophistication
            3. Emotional Impact: Likelihood of creating desired emotional responses
            4. Cultural Sensitivity: Appropriateness for target demographic
            5. Practical Feasibility: Ease of implementation and execution
            6. Risk Analysis: Potential failure points and mitigation strategies
            7. Optimization Recommendations: Improvements for maximum impact

            Format as detailed JSON analysis.
            """
            
            validation = self.openai_client.synthesize_insights(validation_prompt)
            return validation
            
        except Exception as e:
            return {"error": f"PROVI validation failed: {str(e)}"}
