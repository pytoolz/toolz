Function Purity
===============

We call a function *pure* if it meets the following criteria

1.  It does not depend on hidden state, or equivalently it only depends on its
    inputs.
2.  Evaluation of the function does not cause side effects

In short the internal work of a pure function is isolated from the rest of the
program.

Examples
--------

This is made clear by two examples:

.. code::

    # A pure function
    def min(x, y):
        if x < y:
            return x
        else:
            return y


    # An impure function
    exponent = 2

    def powers(L):
        for i in range(len(L)):
            L[i] = L[i]**exponent
        return L

The function ``min`` is pure.  It always produces the same result given the
same inputs and it doesn't affect any external variable.

The function ``powers`` is impure for the following two reasons:

1.  It depends on the global variable ``exponent``
2.  It changes the input ``L`` which may have external state.  
    
Consider the following execution:

.. code::

    >>> data = [1, 2, 3]
    >>> result = powers(data)

    >>> print result
    [1, 4, 9]
    >>> print data
    [1, 4, 9]

We see that ``powers`` affected the variable ``data``.  Users of our function
might be surprised by this.  Usually we expect our inputs to be unchanged.

Another problem occurs when we run this code in a different context:

.. code::

    >>> data = [1, 2, 3]
    >>> result = powers(L)
    >>> print result
    [1, 8, 27]

When we give ``powers`` the same inputs we receive different outputs; how could
this be?  Someone must have changed the value of ``exponent`` to be ``3``,
producing cubes rather than squares.  At first this flexibility may seem like a
feature and indeed in many cases it may be.  The cost for this flexibility is
that we need to keep track of the ``exponent`` variable separately whenever we
use ``powers``.  As we use more functions these extra variables become a
burden.


State
-----

Impure functions are often more efficient but also require that the programmer
"keep track" of the state of several variables.  Keeping track of this state
becomes increasingly difficult as programs grow in size.  By eschewing state
programmers are able to conceptually scale out to solve much larger problems.
The loss of performance is often negligible compared to the freedom to trust
that your functions work as expected on your inputs.

Maintaining state provides efficiency at the cost of surprises.  Pure
functions produce no surprises and so lighten the mental load of the
programmer.


Testing
-------

As an added bonus, testing pure functions is substantially simpler than testing
impure ones.  A programmer who has tried to test functions that include
randomness will know this first-hand.


Power of Predictability
-----------------------

It is easier to build general transformations around pure functions.  General transformations like parallel programming systems often need to assume that simultaneously running processes don't affect each other during operation.  Because pure functions don't affect external state this condition is guaranteed.

Another, more demonstrable function transformation is *memoization*, also called caching.  Memoization caches input-output pairs of a function so that, if the function is called twice with the same inputs then the output of the first execution is returned immediately.  Naively we would memoize a function as follows

.. code::

    cache = dict()
    def f(input):
        if input in cache:
            return cache[input]
        
        else:
            # Perform normal execution of f
            result = ...
            cache[input] = result
            return result

This trades memory usage (we store accumulated results) for computational speed
(a dictionary lookup is probably faster than our function execution.)  This
only works if a function predictably returns the same values given the same
inputs; this is guaranteed if the function is pure.

Fortunately this transformation can be formed into the higher order function
``memoize``.


.. code::

    def f(input):
        return ...

    from toolz import memoize

    f = memoize(f)


Example -- Memoizing Fibonacci
------------------------------

The Fibonacci numbers ``0, 1, 1, 2, 3, 5, 8, 13, 21, ...`` are often defined by
one of the two following methods

.. code::

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


    # Less intuitive but quite fast
    def fib_imperative(n):
        """ Imperative definition of Fibonacci numbers """
        a, b = 0, 1
        for i in range(n):
            a, b = b, a + b
        return b

The first solution, ``fib``, matches the mathematical definition well but
suffers from terrible computational complexity.  The second algorithm,
``fib_imperative``, is quite fast but is not intuitive from the mathematical
definition.  The intuitive/slow solution can be saved by caching intermediate
results, thus avoiding a ruinous call tree.

.. code::

    from toolz import memoize
    fib = memoize(fib)

Lets look at some timings


.. code::

    >>> timeit fib_imperative(30)
    100000 loops, best of 3: 8.42 µs per loop

    >>> timeit fib(30)                              # without memoization
    1 loops, best of 3: 1.51 s per loop

    >>> cache = dict()
    >>> fib = memoize(fib, cache)                   # explicitly create cache

    >>> timeit cache.clear(); fib(30)               # with memoization
    10000 loops, best of 3: 160 µs per loop

While the functional and memoized result ``160us`` is not nearly as fast as the
imperative ``8us`` it's still *much* faster than the naive functional solution
of ``1.5s``.  Additionally, it is often *fast enough* for most applications.
