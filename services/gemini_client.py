import os
import json
import logging
from google import genai
from google.genai import types

class GeminiClient:
    def __init__(self):
        self.client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
        self.model = "gemini-2.5-pro"

    def analyze_market_data(self, prompt):
        """Analyze market data using Gemini"""
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=[
                    types.Content(
                        role="user",
                        parts=[types.Part(text=prompt)]
                    )
                ],
                config=types.GenerateContentConfig(
                    system_instruction="You are an expert market research analyst with deep expertise in consumer psychology, market dynamics, and competitive intelligence. Provide comprehensive, data-driven insights in structured JSON format.",
                    response_mime_type="application/json",
                    temperature=0.7
                )
            )
            
            if response.text:
                result = json.loads(response.text)
                return result
            else:
                return {"error": "Empty response from Gemini"}
                
        except Exception as e:
            logging.error(f"Gemini market analysis error: {str(e)}")
            return {"error": f"Gemini analysis failed: {str(e)}"}

    def analyze_avatar_psychology(self, prompt):
        """Deep psychological avatar analysis"""
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=[
                    types.Content(
                        role="user", 
                        parts=[types.Part(text=prompt)]
                    )
                ],
                config=types.GenerateContentConfig(
                    system_instruction="You are a world-class consumer psychologist and behavioral analyst. You specialize in creating detailed psychological profiles that reveal deep motivations, hidden desires, and subconscious decision-making patterns. Your analysis should be so precise that it feels like you're reading someone's mind.",
                    response_mime_type="application/json",
                    temperature=0.8
                )
            )
            
            if response.text:
                result = json.loads(response.text)
                return result
            else:
                return {"error": "Empty response from Gemini"}
                
        except Exception as e:
            logging.error(f"Gemini avatar analysis error: {str(e)}")
            return {"error": f"Avatar analysis failed: {str(e)}"}

    def create_visual_proofs(self, prompt):
        """Create visual proof systems (PROVIs)"""
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=[
                    types.Content(
                        role="user",
                        parts=[types.Part(text=prompt)]
                    )
                ],
                config=types.GenerateContentConfig(
                    system_instruction="You are the DIRECTOR SUPREMO DE EXPERIÊNCIAS TRANSFORMADORAS. Your mission is to analyze ANY sales/launch context and automatically create a complete arsenal of PROVIs that transform ALL abstract concepts into unforgettable physical experiences. You are creative, bold, and memorable.",
                    response_mime_type="application/json",
                    temperature=0.9
                )
            )
            
            if response.text:
                result = json.loads(response.text)
                return result
            else:
                return {"error": "Empty response from Gemini"}
                
        except Exception as e:
            logging.error(f"Gemini visual proofs error: {str(e)}")
            return {"error": f"Visual proofs creation failed: {str(e)}"}

    def create_prepitch_architecture(self, prompt):
        """Create pre-pitch invisible architecture"""
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=[
                    types.Content(
                        role="user",
                        parts=[types.Part(text=prompt)]
                    )
                ],
                config=types.GenerateContentConfig(
                    system_instruction="You are the Master of Invisible Pre-Pitch, specialist in creating psychological installation sequences that make prospects BEG for the offer before you even present it. Your mission: Take the mental drivers already created and orchestrate a SYMPHONY OF PSYCHOLOGICAL TENSION that prepares the mental terrain so precisely that the sale becomes just a formality.",
                    response_mime_type="application/json",
                    temperature=0.8
                )
            )
            
            if response.text:
                result = json.loads(response.text)
                return result
            else:
                return {"error": "Empty response from Gemini"}
                
        except Exception as e:
            logging.error(f"Gemini pre-pitch architecture error: {str(e)}")
            return {"error": f"Pre-pitch architecture creation failed: {str(e)}"}

    def generate_comprehensive_text(self, prompt):
        """Generate comprehensive text content"""
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=[
                    types.Content(
                        role="user",
                        parts=[types.Part(text=prompt)]
                    )
                ],
                config=types.GenerateContentConfig(
                    system_instruction="You are an expert content creator specializing in comprehensive, detailed analysis and reporting. Your writing is thorough, well-structured, and provides deep insights that are immediately actionable.",
                    temperature=0.7
                )
            )
            
            return response.text if response.text else "Text generation failed"
                
        except Exception as e:
            logging.error(f"Gemini text generation error: {str(e)}")
            return f"Text generation failed: {str(e)}"
