#!/usr/bin/env python3
"""Шаг 11: Setup Logging Infrastructure"""
import logging
logger = logging.getLogger(__name__)

class ActionLogger:
    """DEBUG, INFO, WARNING, ERROR levels"""
    def __init__(self):
        self.logs = []
        logger.info("📝 ActionLogger создан")
    
    def log(self, level, message): 
        self.logs.append({'level': level, 'message': message})
