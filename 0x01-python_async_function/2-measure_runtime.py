#!/usr/bin/env python3
"""
    task 2 module
"""
import time
import asyncio


wait_n = __import__('1-concurrent_coroutines').wait_n


def measure_time(n: int, max_delay: int) -> float:
    """
        measures the total execution time
    """
    start = time.time()
    asyncio.run(wait_n(n, max_delay))
    end = time.time()

    total_time = end - start
    avg_time_per_oper = total_time / n
    return avg_time_per_oper
