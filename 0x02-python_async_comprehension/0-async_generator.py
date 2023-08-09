#!/usr/bin/python3
"""
    task 0 module
"""
import random
import asyncio
from typing import Generator


async def async_generator() -> Generator[float, None, None]:
    """
        generates a sequence of ten numbers
    """
    for _ in range(10):
        await asyncio.sleep(1)
        yield random.random() * 10
        