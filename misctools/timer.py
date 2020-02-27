import time
from functools import wraps

microseconds = u"\u00B5" + 's'


def timeit(arg=None, repeat=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if repeat is None:
                ts = time.perf_counter_ns()
                result = func(*args, **kwargs)
                te = time.perf_counter_ns() - ts
                if te > 1000000000:
                    tte = te/1000000000
                    unit = 's'
                elif te > 1000000:
                    tte = te/1000000
                    unit = 'ms'
                elif te > 1000:
                    tte = te/1000
                    unit = '\u00b5s'
                else:
                    tte = te
                    unit = 'ns'
                print(f"'{func.__name__}' elapsed: {tte:.2f} {unit}")
            else:
                times = []
                for _ in range(repeat):
                    ts = time.perf_counter_ns()
                    result = func(*args, **kwargs)
                    te = time.perf_counter_ns() - ts
                    times.append(te)
                avg = (sum(times)/len(times))
                if avg > 1000000000:
                    tavg = avg/1000000000
                    best = min(times)/1000000000
                    worst = max(times)/1000000000
                    unit = 's'
                elif avg > 1000000:
                    tavg = avg/1000000
                    best = min(times)/1000000
                    worst = max(times)/1000000
                    unit = 'ms'
                elif avg > 1000:
                    tavg = avg/1000
                    best = min(times)/1000
                    worst = max(times)/1000
                    unit = '\u00b5'
                else:
                    tavg = avg
                    best = min(times)
                    worst = max(times)
                    unit = 'ns'
                print(f"'{func.__name__}' results:\n---\nAverage of {repeat}: {tavg:.2f} {unit}\nBest of {repeat}: {best:.2f} {unit}\nWorst of {repeat}: {worst:.2f} {unit}\n")
            return result
        return wrapper
    if callable(arg):
        return decorator(arg)
    else:
        return decorator
