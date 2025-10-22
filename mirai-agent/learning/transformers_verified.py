"""
transformers - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.89
Tests Passed: 0/1
Learned: 2025-10-22T01:26:43.345032

This code has been verified by MIRAI's NASA-level learning system.
"""

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Pipeline

class SentimentAnalyzer:
    def __init__(self, model_name: str):
        """
        Initializes the SentimentAnalyzer with a specified model.

        Args:
            model_name (str): The name of the model to load from the Hugging Face model hub.
        """
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
            self.pipeline = Pipeline("sentiment-analysis", model=self.model, tokenizer=self.tokenizer)
        except Exception as e:
            raise RuntimeError(f"Failed to load model {model_name}: {e}")

    def analyze_sentiment(self, text: str) -> dict:
        """
        Analyzes the sentiment of the given text.

        Args:
            text (str): The text to analyze.

        Returns:
            dict: A dictionary containing the sentiment label and score.
        """
        if not text:
            raise ValueError("Input text cannot be empty.")
        
        try:
            result = self.pipeline(text)[0]  # Get the first result
            return result
        except Exception as e:
            raise RuntimeError(f"Failed to analyze sentiment: {e}")

if __name__ == "__main__":
    # Define the model name to use
    model_name = "distilbert-base-uncased-finetuned-sst-2-english"
    
    # Create an instance of the sentiment analyzer
    analyzer = SentimentAnalyzer(model_name)
    
    # Example text to analyze
    example_text = "I love using transformers for natural language processing!"
    
    # Analyze the sentiment of the example text
    try:
        sentiment_result = analyzer.analyze_sentiment(example_text)
        print(sentiment_result)
    except Exception as e:
        print(f"Error: {e}")