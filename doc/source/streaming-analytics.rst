Streaming Analytics
===================

The toolz functions can be composed to analyze large streaming datasets.
Toolz supports common analytics patterns like the selection, grouping,
reduction, and joining of data through pure composable functions.  These
functions often have analogs to familiar operations in other data analytics
platforms like SQL or Pandas.


Selecting with ``map`` and ``filter``
-------------------------------------

Simple projection and linear selection from a sequence is acheived through the
standard functions ``map`` and ``filter``.

.. code::

   SELECT name, balance
   FROM accounts
   WHERE balance > 150

These functions correspond to the SQL commands ``SELECT`` and ``WHERE``.

.. code::

   >>> accounts = [(1, 'Alice', 100, 'F'),  # id, name, balance, gender
   ...             (2, 'Bob', 200, 'M'),
   ...             (3, 'Charlie', 150, 'M'),
   ...             (4, 'Dennis', 50, 'M'),
   ...             (5, 'Edith', 300, 'F')]

   >>> pipe(accounts, filter(lambda (id, name, balance, gender): balance > 150),
   ...                map(get([1, 2])),
   ...                list)

Of course, these operations are also well supported with standard
list/generator expressions syntax.  This syntax is more often used and
generally considered to be more readable.

.. code::

   >>> [(name, balance) for (id, name, balance, gender) in accounts
   ...                  if balance > 150]


Grouping with ``groupby`` and ``reduceby``
------------------------------------------

We separate split-apply-combine operations into the following two concepts

1.  Split the dataset into groups by some property
2.  Reduce each of the groups with some synopsis

Toolz supports this common workflow with a simple in-memory solution and with a
more sophisticated streaming solution.


In Memory
^^^^^^^^^

The in-memory solution depends on the functions `groupby`_ to split, and
`valmap`_ to apply/combine.

.. code::

   SELECT gender, sum(balance)
   FROM accounts
   GROUPBY gender

We first show these two functions piece by piece to show the intermediate
groups.

.. code::

   >>> groupby(get(3), accounts)
   {'F': [(1, 'Alice', 100, 'F'), (5, 'Edith', 300, 'F')],
    'M': [(2, 'Bob', 200, 'M'), (3, 'Charlie', 150, 'M'), (4, 'Dennis', 50, 'M')]}

   >>> valmap(compose(sum, map(get(2))), _)
   {'F': 400, 'M': 400}


Then we chain them together into a single computation

.. code::
   >>> pipe(accounts, groupby(get(3)),
   ...                valmap(compose(sum, map(get(2)))))
   {'F': 400, 'M': 400}


Streaming
^^^^^^^^^

The ``groupby`` function collects the entire dataset in memory into a
dictionary.  While convenient, the ``groupby`` operation is *not streaming* and
so this approach is limited to what can comfortably fit into memory.

Toolz acheives streaming split-apply-combine with `reduceby`_ which performs a
simultaneous reduction on each group as elements stream in.  To understand this
section you should first be familiar with the builtin funciton ``reduce``.

The ``reduceby`` operation takes a key function, like ``groupby`` and a binary
operator like ``add`` or ``lesser = lambda acc, x: acc if acc < x else x``.  It
is unable to accept full reduction operations like ``sum`` or ``min`` as these
would require access to the entire group at once.  Here is a simple example:

.. code::

   >>> def iseven(n):
   ...     return n % 2 == 0

   >>> def add(x, y):
   ...     return x + y

   >>> reduceby(iseven, add, [1, 2, 3, 4])
   {True: 6, False: 4}


The challenge to using ``reduceby`` often lies in the construction of a
suitable binary operator.  Here is the solution for our accounts example:

.. code::

   >>> binop = lambda acc, (id, name, bal, gend): acc + bal
   >>> initial_value = 0

   >>> reduceby(get(3), binop, accounts, initial_value)
   {'F': 400, 'M': 400}


This construction supports ``accounts`` datasets that could be much larger than
available memory.  Only the reduced result must be able to fit comfortably in
memory and this is rarely an issue, even for very large computations.


Semi-Streaming ``join``
-----------------------

We register multiple datasets together with `join`_.  Consider a second
dataset storing addresses by ID

.. code::

   >>> addresses = [(1, '123 Main Street'),  # id, address
   ...              (2, '5 Adams Way'),
   ...              (5, '34 Rue St Michel')]

We can join this dataset against our accounts dataset by specifying attributes
which register different elements with each other; in this case they share a
common first column, id.


.. code::

   SELECT accounts.name, addresses.address
   FROM accounts, addresses
   WHERE accounts.id = addresses.id

.. code::

   >>> result = join(first, first, accounts, addresses)

   >>> for ((_, name, _, _), (_, addr)) in result:
   ...     print((name, addr))
   ('Alice', '123 Main Street')
   ('Bob', '5 Adams Way')
   ('Edith', '34 Rue St Michel')

Join takes four main arguments, a left and right key function and a left and
right sequence.  It returns a sequence of pairs of matching items.  In the
example above we unpack this tuple to get the fields that we want (``name`` and
``address``) from the result.

Join on arbitrary functions / data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Those familiar with SQL are accustomed to this sort of join on columns.  We
note that a functional join need not operate on tuples and that key functions
need not get particular columns.  In the example below we match numbers from two collections so that exactly one is even and one is odd.

.. code::

   >>> iseven = lambda x: x % 2 == 0
   >>> isodd  = lambda x: x % 2 == 1

   >>> list(join(iseven, isodd, [1, 2, 3, 4], [7, 8, 9]))
   [(2, 7), (4, 7), (1, 8), (3, 8), (2, 9), (4, 9)]


Semi-Streaming Join
^^^^^^^^^^^^^^^^^^^

The Toolz Join operation fully evaluates the LEFT sequence and streams the
RIGHT sequence through memory.  Thus, if streaming support is desired the
larger of the two sequences should always occupy the right side of the join.


Algorithmic Complexity
^^^^^^^^^^^^^^^^^^^^^^

The semi-streaming join operation in ``toolz`` is asymptotically optimal.
Computationally it is linear in the size of the input + output.  In terms of
storage the left sequence must fit in memory but the right sequence is free to
stream.


More complex Example
^^^^^^^^^^^^^^^^^^^^

The accounts example above composes two one-to-one relationships; there was
exactly one name per ID and one address per ID.  This need not be the case.
The join abstraction is sufficiently flexible to join one-to-many or even
many-to-many relationships.  The following example finds a city/person pairs where that person has a friend who has a residence in that city.  This is an example of joining two many-to-many relationships because a person may have many friends and because a friend may have many residences.


.. code::

   >>> friends = [('Alice', 'Edith'),
   ...            ('Alice', 'Zhao'),
   ...            ('Edith', 'Alice'),
   ...            ('Zhao', 'Alice'),
   ...            ('Zhao', 'Edith')]

   >>> cities = [('Alice', 'NYC'),
   ...           ('Alice', 'Chicago'),
   ...           ('Dan', 'Syndey'),
   ...           ('Edith', 'Paris'),
   ...           ('Edith', 'Berlin'),
   ...           ('Zhao', 'Shanghai')]

   >>> # Vacation opportunities
   >>> # In what cities do people have friends?
   >>> result = join(second, first, friends, cities)
   >>> for ((a, b), (c, d)) in sorted(unique(result)):
   ...     print((a, d))
   ('Alice', 'Berlin')
   ('Alice', 'Paris')
   ('Alice', 'Shanghai')
   ('Edith', 'Chicago')
   ('Edith', 'NYC')
   ('Zhao', 'Chicago')
   ('Zhao', 'NYC')
   ('Zhao', 'Berlin')
   ('Zhao', 'Paris')

Join is computationally powerful

*   It is expressive enough to cover a wide set of analytics operations
*   It runs in linear time relative to the size of the input and output
*   Only the left sequence must fit in memory


Disclaimer
----------

Toolz is a general purpose functional standard library, not a library for data
analytics.  While there are some obvious benefits (streaming, composition, ...)
users interested in data analytics might be better served by using projects
specific to data analytics like Pandas or SQLAlchemy.


.. _groupby: http://toolz.readthedocs.org/en/latest/api.html#toolz.itertoolz.groupby
.. _join: http://toolz.readthedocs.org/en/latest/api.html#toolz.itertoolz.join
.. _reduceby: http://toolz.readthedocs.org/en/latest/api.html#toolz.itertoolz.reduceby
.. _valmap: http://toolz.readthedocs.org/en/latest/api.html#toolz.itertoolz.valmap
