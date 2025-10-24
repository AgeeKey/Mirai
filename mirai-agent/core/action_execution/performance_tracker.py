#!/usr/bin/env python3
"""Шаг 10: Initialize Performance Tracking"""
import logging
logger = logging.getLogger(__name__)

class PerformanceTracker:
    """Time, resources, success rate"""
    def __init__(self):
        self.metrics = {'total': 0, 'successful': 0}
        logger.info("📈 PerformanceTracker создан")
    
    def track(self, success): 
        self.metrics['total'] += 1
        if success: self.metrics['successful'] += 1
    
    def get_metrics(self): return self.metrics
