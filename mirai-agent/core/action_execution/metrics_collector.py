#!/usr/bin/env python3
"""Шаг 12: Initialize Metrics Collection"""
import logging
logger = logging.getLogger(__name__)

class MetricsCollector:
    """Aggregated statistics"""
    def __init__(self):
        self.metrics = {}
        logger.info("📊 MetricsCollector создан")
    
    def collect(self, metric_name, value): 
        self.metrics[metric_name] = value
    
    def get_all(self): return self.metrics
