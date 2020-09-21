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

The function ``powers`` is impure for two reasons.  First, it depends on a
global variable, ``exponent``, which can change [*]_.  Second, it changes the
input ``L`` which may have external state.  Consider the following execution:

.. code::

    >>> data = [1, 2, 3]
    >>> result = powers(data)

    >>> print(result)
    [1, 4, 9]
    >>> print(data)
    [1, 4, 9]

We see that ``powers`` affected the variable ``data``.  Users of our function
might be surprised by this.  Usually we expect our inputs to be unchanged.

Another problem occurs when we run this code in a different context:

.. code::

    >>> data = [1, 2, 3]
    >>> result = powers(data)
    >>> print(result)
    [1, 8, 27]

When we give ``powers`` the same inputs we receive different outputs; how could
this be?  Someone must have changed the value of ``exponent`` to be ``3``,
producing cubes rather than squares.  At first this flexibility may seem like a
feature and indeed in many cases it may be.  The cost for this flexibility is
that we need to keep track of the ``exponent`` variable separately whenever we
use ``powers``.  As we use more functions these extra variables become a
burden.

.. [*] A function depending on a global value can be pure if the value never
       changes, i.e. is immutable.

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
