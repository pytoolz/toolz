#          /            0               if i is 0
# fib(i) = |            1               if i is 1
#          \ fib(i - 1) + fib(i - 2)    otherwise


# This is intuitive but VERY slow
def fib(n):
    """ Functional definition of Fibonacci numbers """
    if n == 0 or n == 1:
        return n
    else:
        return fib(n - 1) + fib(n - 2)


def fib_imperative(n):
    """ Imperative definition of Fibonacci numbers """
    a, b = 0, 1
    for i in range(n):
        a, b = b, a + b
    return b


from toolz import memoize

# Oh wait, it's fast again
fib = memoize(fib)
