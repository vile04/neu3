import os
import requests
import json
import logging

class HuggingFaceClient:
    def __init__(self):
        self.api_key = os.environ.get("HUGGINGFACE_API_KEY")
        self.headers = {"Authorization": f"Bearer {self.api_key}"}
        self.base_url = "https://api-inference.huggingface.co/models"

    def analyze_sentiment(self, text):
        """Analyze sentiment using HuggingFace models"""
        try:
            url = f"{self.base_url}/cardiffnlp/twitter-roberta-base-sentiment-latest"
            payload = {"inputs": text}
            
            response = requests.post(url, headers=self.headers, json=payload)
            result = response.json()
            
            if isinstance(result, list) and len(result) > 0:
                sentiments = result[0]
                # Convert to standardized format
                sentiment_mapping = {
                    'LABEL_0': 'negative',
                    'LABEL_1': 'neutral', 
                    'LABEL_2': 'positive'
                }
                
                processed = []
                for sentiment in sentiments:
                    processed.append({
                        'label': sentiment_mapping.get(sentiment['label'], sentiment['label']),
                        'score': sentiment['score']
                    })
                
                return processed
            
            return result
            
        except Exception as e:
            logging.error(f"HuggingFace sentiment analysis error: {str(e)}")
            return {"error": f"Sentiment analysis failed: {str(e)}"}

    def extract_keywords(self, text):
        """Extract keywords and key phrases"""
        try:
            # Use a keyword extraction model
            url = f"{self.base_url}/yanekyuk/bert-keyword-extractor"
            payload = {"inputs": text}
            
            response = requests.post(url, headers=self.headers, json=payload)
            result = response.json()
            
            return result
            
        except Exception as e:
            logging.error(f"HuggingFace keyword extraction error: {str(e)}")
            return {"error": f"Keyword extraction failed: {str(e)}"}

    def classify_text(self, text, categories=None):
        """Classify text into categories"""
        try:
            if categories is None:
                categories = [
                    "business", "technology", "marketing", "psychology", 
                    "finance", "education", "health", "lifestyle"
                ]
            
            url = f"{self.base_url}/facebook/bart-large-mnli"
            
            # Create hypothesis for classification
            hypotheses = [f"This text is about {category}" for category in categories]
            
            results = []
            for hypothesis in hypotheses:
                payload = {
                    "inputs": {
                        "premise": text,
                        "hypothesis": hypothesis
                    }
                }
                
                response = requests.post(url, headers=self.headers, json=payload)
                result = response.json()
                results.append(result)
            
            return results
            
        except Exception as e:
            logging.error(f"HuggingFace text classification error: {str(e)}")
            return {"error": f"Text classification failed: {str(e)}"}

    def summarize_text(self, text, max_length=200):
        """Summarize long text"""
        try:
            url = f"{self.base_url}/facebook/bart-large-cnn"
            payload = {
                "inputs": text,
                "parameters": {
                    "max_length": max_length,
                    "min_length": 50,
                    "do_sample": False
                }
            }
            
            response = requests.post(url, headers=self.headers, json=payload)
            result = response.json()
            
            if isinstance(result, list) and len(result) > 0:
                return result[0].get('summary_text', text[:max_length])
            
            return result
            
        except Exception as e:
            logging.error(f"HuggingFace summarization error: {str(e)}")
            return {"error": f"Summarization failed: {str(e)}"}

    def analyze_emotions(self, text):
        """Analyze emotional content"""
        try:
            url = f"{self.base_url}/j-hartmann/emotion-english-distilroberta-base"
            payload = {"inputs": text}
            
            response = requests.post(url, headers=self.headers, json=payload)
            result = response.json()
            
            return result
            
        except Exception as e:
            logging.error(f"HuggingFace emotion analysis error: {str(e)}")
            return {"error": f"Emotion analysis failed: {str(e)}"}

    def generate_text(self, prompt, max_length=500):
        """Generate text content"""
        try:
            url = f"{self.base_url}/gpt2"
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_length": max_length,
                    "temperature": 0.7,
                    "do_sample": True
                }
            }
            
            response = requests.post(url, headers=self.headers, json=payload)
            result = response.json()
            
            if isinstance(result, list) and len(result) > 0:
                return result[0].get('generated_text', prompt)
            
            return result
            
        except Exception as e:
            logging.error(f"HuggingFace text generation error: {str(e)}")
            return {"error": f"Text generation failed: {str(e)}"}
