def timer_wrapper(function_to_time, verbose = False):
    """
    This is a wrapper function that serves as a decorator
    for other functions that informs us how long (in seconds)
    it takes for those functions to run.

    ----- FUNCTION FLOW -----
    (1): Try to import the native module "Time."
    (2): Start the timer.
    (3): Run the function.
    (4): End the timer when the variable "function_result" has
        been obtained.
    (5): Compute the difference in end time from start time.
    (6): Log the output, which states how long the function took 
        to run.
    -------------------------
    """

    # (1): Try to import the native module "Time":
    try:
        import time
    except Exception as E:
        print(f"> Error running timer wrapper:\n> {E}")
        return 0

    def wrapper(*args, **kwargs):

        # (2): Start the timer.
        start_time = time.time()
        if verbose:
            print(f"> Function \"{function_to_time.__name__}\" began running {start_time}.")

        # (3): Run the function.
        function_result = function_to_time(*args, **kwargs)
    
        # (4): End the timer.
        end_time = time.time()
        if verbose:
            print(f"> Function \"{function_to_time.__name__}\" began running {start_time}.")

        # (5): Compute the difference.
        elapsed_time = end_time - start_time

        # (6): Log the output.
        print(f"> Function \"{function_to_time.__name__}\" took {elapsed_time:.6f} seconds to run.")
        
        return function_result

    return wrapper