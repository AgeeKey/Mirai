"""
huggingface-transformers - Verified Learning Artifact

Quality Grade: B
Overall Score: 0.85
Tests Passed: 0/1
Learned: 2025-10-17T16:12:40.085627

This code has been verified by MIRAI's NASA-level learning system.
"""

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

def load_model(model_name: str) -> AutoModelForSequenceClassification:
    """
    Load a pre-trained model for sequence classification.
    
    Args:
        model_name (str): The name of the model to load from Hugging Face Hub.
        
    Returns:
        AutoModelForSequenceClassification: The loaded model.
        
    Raises:
        ValueError: If the model cannot be loaded.
    """
    try:
        model = AutoModelForSequenceClassification.from_pretrained(model_name)
        return model
    except Exception as e:
        raise ValueError(f"Could not load model '{model_name}': {e}")

def load_tokenizer(model_name: str) -> AutoTokenizer:
    """
    Load a pre-trained tokenizer for the specified model.
    
    Args:
        model_name (str): The name of the tokenizer to load from Hugging Face Hub.
        
    Returns:
        AutoTokenizer: The loaded tokenizer.
        
    Raises:
        ValueError: If the tokenizer cannot be loaded.
    """
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        return tokenizer
    except Exception as e:
        raise ValueError(f"Could not load tokenizer '{model_name}': {e}")

def classify_text(model: AutoModelForSequenceClassification, tokenizer: AutoTokenizer, text: str) -> str:
    """
    Classify the input text using the provided model and tokenizer.
    
    Args:
        model (AutoModelForSequenceClassification): The pre-trained model for classification.
        tokenizer (AutoTokenizer): The pre-trained tokenizer for the model.
        text (str): The input text to classify.
        
    Returns:
        str: The predicted class label.
    """
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():  # Disable gradient calculation
        outputs = model(**inputs)
    logits = outputs.logits
    predicted_class = logits.argmax(dim=-1).item()
    return predicted_class

if __name__ == "__main__":
    model_name = "distilbert-base-uncased-finetuned-sst-2-english"
    
    # Load model and tokenizer
    model = load_model(model_name)
    tokenizer = load_tokenizer(model_name)
    
    # Input text to classify
    text = "I love using Hugging Face Transformers!"
    
    # Classify text
    predicted_class = classify_text(model, tokenizer, text)
    print(f"Predicted class: {predicted_class}")