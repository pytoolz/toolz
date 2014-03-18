#          /            0               if i is 0
# fib(i) = |            1               if i is 1
#          \ fib(i - 1) + fib(i - 2)    otherwise


def fib(n):
    """ Imperative definition of Fibonacci numbers """
    a, b = 0, 1
    for i in range(n):
        a, b = b, a + b
    return a


# This is intuitive but VERY slow
def fib(n):
    """ Functional definition of Fibonacci numbers """
    if n == 0 or n == 1:
        return n
    else:
        return fib(n - 1) + fib(n - 2)

from toolz import memoize

# Oh wait, it's fast again
fib = memoize(fib)


# Provide a cache with initial values to `memoize`
@memoize(cache={0: 0, 1: 1})
def fib(n):
    """ Functional definition of Fibonacci numbers with initial terms cached.

    fib(0) == 0
    fib(1) == 1
    ...
    fib(n) == fib(n - 1) + fib(n - 2)
    """
    return fib(n - 1) + fib(n - 2)
