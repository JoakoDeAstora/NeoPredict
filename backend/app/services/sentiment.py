from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch

class SentimentService:
    def __init__(self):
        # Using a Spanish financial sentiment model or generic Spanish sentiment
        # 'pysentimiento/robertuito-sentiment-analysis' is good for general spanish
        # 'dccuchile/bert-base-spanish-wwm-uncased' is base BETO
        # For this specific task, we'll use a finetuned model if available or a robust spanish one.
        self.model_name = "pysentimiento/robertuito-sentiment-analysis" 
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
        self.pipeline = pipeline("sentiment-analysis", model=self.model, tokenizer=self.tokenizer)

    def analyze_text(self, text: str, ticker: str = None):
        """
        Returns a sentiment score and label.
        Incorporates 'Cluster-Based' keyword dictionary if ticker is provided.
        """
        # 1. Base Model Sentiment
        max_len = 512
        chunks = [text[i:i+max_len] for i in range(0, len(text), max_len)]
        
        scores = []
        for chunk in chunks:
            result = self.pipeline(chunk)[0]
            label = result['label']
            score = result['score']
            
            numeric_val = 0
            if label == 'POS': numeric_val = 1 * score
            elif label == 'NEG': numeric_val = -1 * score
            else: numeric_val = 0
            scores.append(numeric_val)
            
        base_score = sum(scores) / len(scores) if scores else 0
        
        # 2. Cluster/Dictionary Adjustment
        if ticker:
            from app.config import CLUSTERS_CONFIG
            config = CLUSTERS_CONFIG.get(ticker)
            if config:
                keyword_adjust = 0.0
                text_lower = text.lower()
                for word, effect in config.sentiment_keywords.items():
                    if word.lower() in text_lower:
                        if effect == 'positive': keyword_adjust += 0.1
                        elif effect == 'negative': keyword_adjust -= 0.1
                        elif effect == 'negative_if_high': keyword_adjust -= 0.05 # Context dependent, simplified here
                
                # Weighted fusion of Model + Dictionary
                final_score = (base_score * 0.7) + (keyword_adjust * 0.3)
                return max(-1.0, min(1.0, final_score)) # Clamp
                
        return base_score

    def get_embedding(self, text: str):
        """
        Returns the CLS token embedding for the Hybrid Model.
        """
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
        with torch.no_grad():
            outputs = self.model.base_model(**inputs)
        # CLS token is [0][:, 0, :]
        return outputs.last_hidden_state[:, 0, :]
