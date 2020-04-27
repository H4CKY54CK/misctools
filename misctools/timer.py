import gc
import time
from functools import wraps

def ftime(nanoseconds, *, units=True):
    units = ['ns', '\u00B5s', 'ms', 's']
    reso = [.1*10**((i*3)+1) for i in range(10)]
    q = len([i for i in reso if nanoseconds > i])
    z = (nanoseconds*1000)/reso[q]
    w = units[q-1]
    if units:
        return f"{z:.2f} {w}"
    return z

def timeit(arg=None, repeat:int=1, garbage=False):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kw):
            # assert repeat > 0, "Nice try there, buckaroo. Use something above 0."
            gcold = gc.isenabled()
            if garbage:
                gc.disable()    
            times = []
            for _ in range(repeat or 1):
                ts = time.perf_counter_ns()
                result = func(*args, **kw)
                te = time.perf_counter_ns() - ts
                times.append(te)
            avg = sum(times)/repeat
            s = f"{func.__name__} elapsed: {ftime(te)}" if repeat == 1 else f"{func.__name__} average elapsed: {ftime(avg)} | best (of {repeat:,}): {ftime(min(times))} | worst (of {repeat:,}): {ftime(max(times))}"
            print(s)
            if garbage and gcold:
                gc.enable()
            return result
        return wrapper
    if callable(arg):
        return decorator(arg)
    elif repeat == 1 and type(arg) == int:
        repeat = arg or 1
    return decorator
