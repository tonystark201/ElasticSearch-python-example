import functools
import time


def boundary(func):
    @functools.wraps(func)
    def inner(*args,**kwargs):
        print("=" * 30 + f" [Begin invoke {func.__name__} api] " + "=" * 30)
        result = func(*args,**kwargs)
        print("=" * 30 + f" [End invoke {func.__name__} api] " + "=" * 30)
        return result
    return inner

def timer(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} take {(end_time-start_time)*1000}ms")
        return result
    return inner