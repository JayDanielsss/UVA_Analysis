# Native Packages | NumPy
import time

# Native Packages | NumPy
from typing import Callable, Any, Tuple

def measure_time(func: Callable, *args: Any, **kwargs: Any) -> Tuple[float, Any]:
    """
    # Description:
    Measures the execution time of a function.

    # Parameters:
    
    func (Callable): The function to measure.
    *args (Any): Positional arguments to pass to the function.
    **kwargs (Any): Keyword arguments to pass to the function.

    # Returns:

    Tuple[float, Any]: A tuple containing the elapsed time in seconds and the function's return value.
    """
    start_time = time.time()
    result = func(*args, **kwargs)
    end_time = time.time()
    elapsed_time = end_time - start_time
    return elapsed_time, result