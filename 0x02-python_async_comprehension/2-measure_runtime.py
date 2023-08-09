#!/usr/bin/env python3
"""
    task 2 module
"""
import asyncio
import time
from importlib import import_module as imp_


async_comprehension = imp_('1-async_comprehension').async_comprehension


async def measure_runtime() -> float:
    """
        runs the async_comprehension 4 times and measures
        the total execution time
    """
    start = time.time()
    await asyncio.gather(*(async_comprehension() for _ in range(4)))
    end = time.time()
    return end - start
