#!/usr/bin/env python3
"""
    task 2 module
"""
import time
import asyncio


wait_n = __import__('1-concurrent_corountines').wait_n


def measure_time(n: int, max_delay: int) -> float:
    """
        measures the total execution time
    """
    start = time.time()
    asyncio.run(wait_n(n, max_delay))
    return (time.time() - start) / n
