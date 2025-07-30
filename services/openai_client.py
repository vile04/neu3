import os
import json
from openai import OpenAI
import logging

class OpenAIClient:
    def __init__(self):
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.model = "gpt-4o"

    def analyze_market_data(self, prompt):
        """Analyze market data using OpenAI"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert market research analyst with deep expertise in consumer psychology, market dynamics, and competitive intelligence. Provide comprehensive, data-driven insights in structured JSON format."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                response_format={"type": "json_object"},
                temperature=0.7,
                max_tokens=4000
            )
            
            content = response.choices[0].message.content
            if content:
                result = json.loads(content)
            else:
                result = {"error": "Empty response from OpenAI"}
            return result
            
        except Exception as e:
            logging.error(f"OpenAI market analysis error: {str(e)}")
            return {"error": f"OpenAI analysis failed: {str(e)}"}

    def analyze_avatar_psychology(self, prompt):
        """Deep psychological avatar analysis"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a world-class consumer psychologist and behavioral analyst. You specialize in creating detailed psychological profiles that reveal deep motivations, hidden desires, and subconscious decision-making patterns. Your analysis should be so precise that it feels like you're reading someone's mind."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                response_format={"type": "json_object"},
                temperature=0.8,
                max_tokens=4000
            )
            
            content = response.choices[0].message.content
            if content:
                result = json.loads(content)
            else:
                result = {"error": "Empty response from OpenAI"}
            return result
            
        except Exception as e:
            logging.error(f"OpenAI avatar analysis error: {str(e)}")
            return {"error": f"Avatar analysis failed: {str(e)}"}

    def create_mental_drivers(self, prompt):
        """Create customized mental drivers"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert in psychological persuasion and mental anchoring techniques. You create powerful mental drivers that install deep psychological triggers in the target audience's mind. Your drivers should be so effective that they create inevitable behavioral changes."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                response_format={"type": "json_object"},
                temperature=0.9,
                max_tokens=4000
            )
            
            content = response.choices[0].message.content
            if content:
                result = json.loads(content)
            else:
                result = {"error": "Empty response from OpenAI"}
            return result
            
        except Exception as e:
            logging.error(f"OpenAI mental drivers error: {str(e)}")
            return {"error": f"Mental drivers creation failed: {str(e)}"}

    def analyze_objections(self, prompt):
        """Analyze psychological objections"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a master of objection psychology and sales resistance analysis. You can identify not just the surface objections people voice, but the deep psychological roots that drive their resistance. Your analysis reveals the hidden fears, limiting beliefs, and emotional barriers that prevent people from taking action."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                response_format={"type": "json_object"},
                temperature=0.8,
                max_tokens=4000
            )
            
            content = response.choices[0].message.content
            if content:
                result = json.loads(content)
            else:
                result = {"error": "Empty response from OpenAI"}
            return result
            
        except Exception as e:
            logging.error(f"OpenAI objection analysis error: {str(e)}")
            return {"error": f"Objection analysis failed: {str(e)}"}

    def synthesize_insights(self, prompt):
        """Synthesize multiple insights into unified analysis"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert synthesis analyst who can take multiple different analyses and create a unified, coherent insight that captures the best of all inputs while resolving contradictions and highlighting the most important actionable intelligence."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                response_format={"type": "json_object"},
                temperature=0.6,
                max_tokens=3000
            )
            
            content = response.choices[0].message.content
            if content:
                result = json.loads(content)
            else:
                result = {"error": "Empty response from OpenAI"}
            return result
            
        except Exception as e:
            logging.error(f"OpenAI synthesis error: {str(e)}")
            return {"error": f"Synthesis failed: {str(e)}"}

    def generate_comprehensive_text(self, prompt):
        """Generate comprehensive text content"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert content creator specializing in comprehensive, detailed analysis and reporting. Your writing is thorough, well-structured, and provides deep insights that are immediately actionable."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=4000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logging.error(f"OpenAI text generation error: {str(e)}")
            return f"Text generation failed: {str(e)}"
