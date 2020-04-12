import time
from functools import wraps

def ftime(n):
    units = ['ns', '\u00B5s', 'ms', 's']
    reso = [.1*10**((i*3)+1) for i in range(10)]
    q = len([i for i in reso if n > i])
    readable = f"{((n*1000)/reso[q]):.2f} {units[q-1]}"
    return readable

def timeit(arg=None, repeat:int=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kw):
            ts = time.perf_counter_ns()
            result = func(*args, **kw)
            te = time.perf_counter_ns() - ts
            times = [te]
            if repeat > 1:
                for _ in range(repeat):
                    ts = time.perf_counter_ns()
                    result = func(*args, **kw)
                    te = time.perf_counter_ns() - ts
                    times.append(te)
                avg = sum(times)/len(times)
                print(f"{func.__name__} average elapsed: {ftime(avg)} | best (of {repeat}): {ftime(min(times))} | worst (of {repeat}): {ftime(max(times))}")
                return result
            print(f"{func.__name__} elapsed: {ftime(te)}")
            return result
        return wrapper
    if callable(arg):
        return decorator(arg)
    return decorator
