from functools import wraps
from time import perf_counter, perf_counter_ns

microseconds = u"\u00B5" + 's'

def timeit(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        ts = perf_counter()
        result = f(*args, **kwargs)
        te = (perf_counter()-ts)*1000
        if te < 1:
            te *= 1000
            print(f'Method ({f.__name__}) elapsed: {te:.01f} {microseconds}')
        else:
            print(f"Method ({f.__name__}) elapsed: {te:.02f} ms")

        return result
    return wrapper


def bestof(f):
    @wraps(f)
    def wrapper(*args, **kw):
        ts = perf_counter()
        result = f(*args, **kw)
        te = perf_counter()-ts
        x = int(1/te)
        if te > 5:
            return result
        elif te > 1:
            x = 3
        times = []
        for i in range(1, x+1):
            ts = perf_counter_ns()
            result = f(*args, **kw)
            te = perf_counter_ns()-ts
            times.append(te)
        avg = (sum(times)/len(times))
        if avg > 1000000:
            avg = avg / 1000
            print(f"Method ({f.__name__}) average (best of {x}):\n  {avg:.01f} {microseconds}")
        elif avg > 1000:
            avg = avg / 1000000
            print(f"Method ({f.__name__}) average (best of {x}):\n  {avg:.02f} ms")
        elif avg > 1:
            avg = avg / 1000000000
            print(f"Method ({f.__name__}) average (best of {x}):\n  {avg:.02f} seconds")
        return result
    return wrapper
