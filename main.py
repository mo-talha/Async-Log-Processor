import asyncio
import random
import time
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List
import json


@dataclass
class LogEntry:
    level: str
    message: str
    source: str
    timestamp: float
    
class RealTimeLogAggregator:
    def __init__(self, num_sources: int = 5, num_workers: int = 3, max_queue_size: int = 1000):
        self.input_queue = asyncio.Queue(maxsize=max_queue_size)
        self.result_queue = asyncio.Queue()
        self.num_soruces = num_sources
        self.num_workers = num_workers