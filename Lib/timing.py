import time
import logging


def logSpeed(func):

    # added arguments inside the inner1,
    # if function takes any arguments,
    # can be added like this.
    def inner1(*args, **kwargs):
 
        # storing time before function execution
        begin = time.perf_counter()

        temp = func(*args, **kwargs)


        total = time.perf_counter() - begin
        logging.info(f"Function \"{func.__name__:<20}\" ran in {total:>20} seconds")

        if temp is not None:
            return temp
 
    return inner1