#!/usr/bin/env python3
"""Шаг 13: Setup Rollback System"""
import logging
logger = logging.getLogger(__name__)

class RollbackSystem:
    """Undo operations"""
    def __init__(self):
        self.rollback_points = []
        logger.info("⏮️ RollbackSystem создан")
    
    def create_rollback_point(self): self.rollback_points.append({})
    def rollback(self): return self.rollback_points.pop() if self.rollback_points else {}
