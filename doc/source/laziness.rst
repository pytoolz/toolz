Laziness
========

Lazy iterators evaluate only when necessary.  They allow us to semantically
manipulate large amounts of data while keeping very little of it actually in
memory.  They act like lists but don't take up space.


Example - A Tale of Two Cities
------------------------------

We open a file containing the text of the classic text "A Tale of Two Cities"
by Charles Dickens[1_].

.. code::

    >>> book = open('tale-of-two-cities.txt')

Much like a secondary school student, Python owns and opens the book without
reading a single line of the text.  The object ``book`` is a lazy iterator!
Python will give us a line of the text only when we explicitly ask it to do so

.. code::

    >>> next(book)
    "It was the best of times,"

    >>> next(book)
    "it was the worst of times,"

and so on.  Each time we call ``next`` on ``book`` we burn through another line
of the text and the ``book`` iterator marches slowly onwards through the text.


Computation
-----------

We can lazily operate on lazy iterators without doing any actual computation.
For example let's read the book in upper case

.. code::

    >>> from toolz import map  # toolz' map is lazy by default

    >>> loud_book = map(str.upper, book)

    >>> next(loud_book)
    "IT WAS THE AGE OF WISDOM,"
    >>> next(loud_book)
    "IT WAS THE AGE OF FOOLISHNESS,"

It is as if we applied the function ``str.upper`` onto every line of the book;
yet the first line completes instantaneously.  Instead Python does the
uppercasing work only when it becomes necessary, i.e.  when you call ``next``
to ask for another line.


Reductions
----------

You can operate on lazy iterators just as you would with lists, tuples, or
sets.  You can use them in for loops as in


.. code::

    for line in loud_book:
        ...

You can instantiate them all into memory by calling them with the constructors
``list``, or ``tuple``.

.. code::

    loud_book = list(loud_book)

Of course if they are very large then this might be unwise.  Often we use
laziness to avoid loading large datasets into memory at once.  Many
computations on large datasets don't require access to all of the data at a
single time.  In particular *reductions* (like sum) often take large amounts of
sequential data (like [1, 2, 3, 4]) and produce much more manageable results
(like 10) and can do so just by viewing the data a little bit at a time.  For
example we can count all of the letters in the Tale of Two Cities trivially
using functions from ``toolz``

.. code::

    >>> from toolz import concat, frequencies
    >>> letters = frequencies(concat(loud_book))
    { 'A': 48036,
      'B': 8402,
      'C': 13812,
      'D': 28000,
      'E': 74624,
      ...

In this case ``frequencies`` is a sort of reduction.  At no time were more than
a few hundred bytes of Tale of Two Cities necessarily in memory.  We could just
have easily done this computation on the entire Gutenberg collection or on
Wikipedia.  In this case we are limited by the size and speed of our hard drive
and not by the capacity of our memory.

.. [1] http://www.gutenberg.org/cache/epub/98/pg98.txt
