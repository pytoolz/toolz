Parallelism
===========

PyToolz tries to support other parallel processing libraries.  It does this
by ensuring easy serialization of ``toolz`` functions and providing
architecture-agnostic parallel algorithms.

In practice ``toolz`` is developed against ``multiprocessing`` and
``ipyparallel``.


Serialization
-------------

Multiprocessing or distributed computing requires the transmission of functions
between different processes or computers.  This is done through serializing the
function into text, sending that text over a wire, and deserializing the text
back into a function.  To the extent possible PyToolz functions are compatible
with the standard serialization library ``pickle``.

The ``pickle`` library often fails for complex functions including lambdas,
closures, and class methods.  When this occurs we recommend the alternative
serialization library ``dill``.


Example with parallel map
-------------------------

Most parallel processing tasks may be significantly accelerated using only a
parallel map operation.  A number of high quality parallel map operations exist
in other libraries, notably ``multiprocessing``, ``ipyparallel``, and
``threading`` (if your operation is not processor bound).

In the example below we extend our wordcounting solution with a parallel map.
We show how one can progress in development from sequential, to
multiprocessing, to distributed computation all with the same domain code.


.. code::

    from toolz.curried import map
    from toolz import frequencies, compose, concat, merge_with

    def stem(word):
        """ Stem word to primitive form

        >>> stem("Hello!")
        'hello'
        """
        return word.lower().rstrip(",.!)-*_?:;$'-\"").lstrip("-*'\"(_$'")


    wordcount = compose(frequencies, map(stem), concat, map(str.split), open)

    if __name__ == '__main__':
        # Filenames for thousands of books from which we'd like to count words
        filenames = ['Book_%d.txt'%i for i in range(10000)]

        # Start with sequential map for development
        # pmap = map

        # Advance to Multiprocessing map for heavy computation on single machine
        # from multiprocessing import Pool
        # p = Pool(8)
        # pmap = p.map

        # Finish with distributed parallel map for big data
        from ipyparallel import Client
        p = Client()[:]
        pmap = p.map_sync

        total = merge_with(sum, pmap(wordcount, filenames))

This smooth transition is possible because

1.  The ``map`` abstraction is a simple function call and so can be replaced.
    By contrast, this transformation would be difficult if we had written our code with a
    for loop or list comprehension.
2.  The operation ``wordcount`` is separate from the parallel solution.
3.  The task is embarrassingly parallel, needing only a very simple parallel
    strategy.  Fortunately this is the common case.


Parallel Algorithms
-------------------

PyToolz does not implement parallel processing systems.  It does however
provide parallel algorithms that can extend existing parallel systems.  Our
general solution is to build algorithms that operate around a user-supplied
parallel map function.

In particular we provide a parallel ``fold`` in ``toolz.sandbox.parallel.fold``.
This fold can work equally well with ``multiprocessing.Pool.map``,
``threading.Pool.map``, or ``ipyparallel``'s ``map_async``.
