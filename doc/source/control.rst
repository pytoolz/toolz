Control Flow
============

Programming is hard when we think simultaneously about several concepts.  Good
programming breaks down big problems into small problems and
builds up small solutions into big solutions.  By this practice the
need for simultaneous thought is restricted to only a few elements at a time.

All modern languages provide mechanisms to build data into data structures and
to build functions out of other functions.  The third element of programming,
besides data and functions, is control flow.  Building complex control flow
out of simple control flow presents deeper challenges.


What?
-----

Each element in a computer program is either

-   A variable or value literal like ``x``, ``total``, or ``5``
-   A function or computation like the ``+`` in ``x + 1``, the function ``fib``
    in ``fib(3)``, the method ``split`` in ``line.split(',')``, or the ``=`` in
    ``x = 0``
-   Control flow like ``if``, ``for``, or ``return``

Here is a piece of code; see if you can label each term as either
variable/value, function/computation, or control flow

.. code::

    def fib(n):
        a, b = 0, 1
        for i in range(n):
            a, b = b, a + b
        return b

Programming is hard when we have to juggle many code elements of each type at
the same time.  Good programming is about managing these three elements so that
the developer is only required to think about a handful of them at a time.  For
example we might collect many integer variables into a list of integers or
build a big function out of smaller ones.

We organize our data into **data structures** like lists, dictionaries, or objects
in order to group related data together -- this allows us to manipulate large
collections of related data as if we were only manipulating a single entity.

We **build large functions out of smaller ones**, enabling us to break up a
complex task like doing laundry into a sequence of simpler tasks.

.. code::

    def do_laundry(clothes):
        wet_clothes = wash(clothes)
        dry_clothes = dry(wet_clothes)
        return fold(dry_clothes)

While we have natural ways to manage data and functions, **control flow presents more of a challenge**.
How do we break down complex control flow into simpler pieces that fit in our brain?
How do we encapsulate commonly recurring patterns?

Let's motivate this with an example of a common control structure, applying a
function to each element in a list.  Imagine we want to download the HTML
source for a number of webpages.

.. code::

    from urllib import urlopen

    urls = ['http://www.google.com', 'http://www.wikipedia.com', 'http://www.apple.com']
    html_texts = []
    for item in urls:
        html_texts.append(urlopen(item))

Or maybe we want to compute the Fibonacci numbers on a particular set of
integers

.. code::

    integers = [1, 2, 3, 4, 5]
    fib_integers = []
    for item in integers:
        fib_integers.append(fib(item))

These two unrelated applications share an identical control flow pattern.  They
apply a function (``urlopen`` or ``fib``) onto each element of an input list
(``urls``, or ``integers``), appending the result onto an output list.  Because
this control flow pattern is so common we give it a name, ``map``, and say that
we map a function (like ``urlopen``) onto a list (like ``urls``).

Because Python can treat functions like variables we can encode this control
pattern into a higher-order-function as follows:

.. code::

    def map(function, sequence):
        output = []
        for item in sequence:
            output.append(function(item))
        return output

This allows us to simplify our code above to the following, pithy solutions

.. code::

    html_texts = map(urlopen, urls)
    fib_integers = map(fib, integers)

Experienced Python programmers know that this control pattern is so popular
that it has been elevated to the status of **syntax** with the popular list
comprehension

.. code::

    html_texts = [urlopen(url) for url in urls]


Why?
----

So maybe you already knew about ``map`` and don't use it or maybe you just
prefer list comprehensions.  Why should you keep reading?

Managing Complexity
^^^^^^^^^^^^^^^^^^^

The higher order function ``map`` gives us a name to call a particular control
pattern.  Regardless of whether or not you use a for loop, a list
comprehension, or ``map`` itself, it is useful to recognize the operation
and to give it a name.  Naming control patterns lets us tackle
complex problems at larger scale without burdening our mind with rote details.
It is just as important as bundling data into data structures or building
complex functions out of simple ones.

*Naming control flow patterns enables programmers to manipulate increasingly
complex operations.*

Other Patterns
^^^^^^^^^^^^^^

The function ``map`` has friends.  Advanced programmers may know about
``map``'s siblings, ``filter`` and ``reduce``.  The ``filter`` control pattern
is also handled by list comprehension syntax and ``reduce`` is often replaced
by straight for loops, so if you don't want to use them there is no immediately
practical reason why you would care.

Most programmers however don't know about the many cousins of
``map``/``filter``/``reduce``.  Consider for example the unsung heroine,
``groupby``.  A brief example grouping names by their length follows:

.. code::

    >>> names = ['Alice', 'Bob', 'Charlie', 'Dan', 'Edith', 'Frank']
    >>> groupby(len, names)
    {3: ['Bob', 'Dan'], 5: ['Alice', 'Edith', 'Frank'], 7: ['Charlie']}

``groupby`` collects each element of a list into sublists determined by the value
of a function.  Let's see ``groupby`` in action again, grouping numbers by
evenness.

.. code::

    >>> def iseven(n):
    ...     return n % 2 == 0

    >>> groupby(iseven, [1, 2, 3, 4, 5, 6, 7])
    {True: [2, 4, 6], False: [1, 3, 5, 7]}

If we were to write this second operation out by hand it might look something
like the following:

.. code::

    evens = []
    odds = []
    for item in numbers:
        if iseven(item):
            evens.append(item)
        else:
            odds.append(item)

Most programmers have written code exactly like this over and over again, just
like they may have repeated the ``map`` control pattern.  When we identify code
as a ``groupby`` operation we mentally collapse the detailed manipulation into
a single concept.

Additional Considerations
^^^^^^^^^^^^^^^^^^^^^^^^^

The Toolz library contains dozens of patterns like ``map`` and ``groupby``.
Learning a core set (maybe a dozen) covers the vast majority of common
programming tasks often done by hand.

*A rich vocabulary of core control functions conveys the following benefits:*

-   You identify new patterns
-   You make fewer errors in rote coding
-   You can depend on well tested and benchmarked implementations

But this does not come for free.  As in spoken language the use of a rich
vocabulary can alienate new practitioners.  Most functional languages have
fallen into this trap and are seen as unapproachable and smug.  Python
maintains a low-brow reputation and benefits from it.  Just as with spoken
language the value of using just-the-right-word must be moderated with the
comprehension of the intended audience.
