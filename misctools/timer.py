import time
from functools import wraps


def timeit(arg=None, repeat=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            times = []
            for _ in range(repeat):
                ts = time.time()
                if repeat > 1:
                    ts = time.perf_counter_ns()
                result = func(*args, **kwargs)
                if repeat > 1:
                    times.append(time.perf_counter_ns() - ts)
                else:
                    times.append(time.time() - ts)
            tavg = (sum(times)/len(times))
            single, multi = ['s', 's', 's', 'ms', 'ms', 'ms', '\u00b5s', '\u00b5s', '\u00b5s', 'ns', 'ns', 'ns'], ['ns', 'ns', 'ns', '\u00b5s', '\u00b5s', '\u00b5s', 'ms', 'ms', 'ms', 's', 's', 's']
            best, worst = min(times), max(times)
            while tavg > 10:
                tavg, best, worst = (i / 10 for i in (tavg, best, worst))
                if len(single) + len(multi) > 2:
                    single.pop(0)
                    multi.pop(0)
            msg = f"'{func.__name__}' elapsed: {tavg:.2f} {single[0]}"
            if repeat > 1:
                msg = f"'{func.__name__}' results:\n---\nAverage (of {repeat}): {tavg:.2f} {multi[0]}\nBest (of {repeat}): {best:.2f} {multi[0]}\nWorst (of {repeat}): {worst:.2f} {multi[0]}\n"
            print(msg)
            return result
        return wrapper
    if callable(arg):
        return decorator(arg)
    else:
        return decorator
