import gc
import time
from functools import wraps

# 100% my own code.
# Pass in nanoseconds...
def ftime(ticks, *, unit_type=True):
    units = ['ns', '\u00B5s', 'ms', 's']
    reso = [.1*10**((i*3)+1) for i in range(10)]
    q = len([i for i in reso if ticks > i])
    z = (ticks*1000)/reso[q]
    w = units[q-1]
    if unit_type:
        return f"{z:.2f} {w}"
    return z
# ... and get back an aesthetically pleasing, not-too-long
# automatically converted value, with or without a unit label.


# Hard to claim as my own, if everyone and their mother has made one.
# I drew inspiration from many a timeit decorator.
def timeit(arg=None, repeat:int=1, garbage=False):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kw):
            assert repeat > 0, "Nice try there, buckaroo. Use something above 0."
            # Store state of GC, then disable if indicated.
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
            # Super stupid compacting I did, thinking I was clever. It's too stupid to change.
            s = f"{func.__name__} elapsed: {ftime(te)}" if repeat == 1 else f"{func.__name__} average elapsed: {ftime(avg)} | best (of {repeat:,}): {ftime(min(times))} | worst (of {repeat:,}): {ftime(max(times))}"
            print(s)
            # If user provided the keyword AND the GC was previously enabled, let's turn it back on.
            if garbage and gcold:
                gc.enable()
            return result
        return wrapper
    # Allows us to use @timeit all willy-nilly.
    if callable(arg):
        return decorator(arg)
    elif repeat == 1 and type(arg) == int:
        repeat = arg or 1
    return decorator

# timeit details

# You can use any of @timeit, @timeit(),
# @timeit(repeat=666), or even @timeit(666)

# They all just work.

# @timeit
# def one():
#     return

# @timeit()
# def two():
#     return

# @timeit(repeat=666)
# def three():
#     return

# @timeit(666)
# def four():
#     return

# one()
# two()
# three()
# four()

# Output for these four functions

# one elapsed: 800.00 ns
# two elapsed: 900.00 ns
# three average elapsed: 251.95 ns | best (of 666): 100.00 ns | worst (of 666): 27.50 µs
# four average elapsed: 205.41 ns | best (of 666): 100.00 ns | worst (of 666): 800.00 ns

# ftime() details

# # 500 million nanoseconds. That's about 500 milliseconds?
# print(ftime(549_364_135))
# # >>> 549.36 ms

# # We'll just do a few quick tests...
# ts = time.perf_counter_ns()
# time.sleep(0)
# te = time.perf_counter_ns() - ts
# print(ftime(te))
# # >>> 2.70 µs
# # 2.70 microseconds. Surely we can go faster.
# # (But don't call me Shirley)

# # How about no interruption?
# ts = time.perf_counter_ns()
# te = time.perf_counter_ns() - ts
# print(ftime(te))
# # >>> 400.00 ns
# # I get anywhere between 200 and 1000 nanoseconds.
# # My PC can't do any better than .1 microsecond ticks. (I think that's right.)

# ts = time.perf_counter_ns()
# te = time.perf_counter_ns() - ts
# print(ftime(te, unit_type=False))
# # >>> 900.0
# # And without the label (gets returned as an int, too!)

# It can no longer be said that I haven't commented my code.