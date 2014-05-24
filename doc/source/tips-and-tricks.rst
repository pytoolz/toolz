Tips and Tricks
===============

Toolz functions can be combined to make functions that, while common, aren't
a part of toolz's standard library. This section presents
a few of these recipes.


* .. function:: pick(whitelist, dictionary)

  Return a subset of the provided dictionary with keys contained in the
  whitelist.

  ::

    from toolz import keyfilter

    def pick(whitelist, d):
        return keyfilter(lambda k: k in whitelist, d)


  Example:

    >>> alphabet = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
    >>> pick(['a', 'b'], alphabet)
    {'a': 1, 'b': 2}


* .. function:: omit(blacklist, dictionary)

  Return a subset of the provided dictionary with keys *not* contained in the
  blacklist.

  ::

    from toolz import keyfilter

    def omit(blacklist, d):
        return keyfilter(lambda k: k not in blacklist, d)


  Example:

    >>> alphabet = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
    >>> omit(['a', 'b'], alphabet)
    {'c': 3, 'd': 4}


* .. function:: compact(iterable)

  Filter an iterable on "truthy" values.

  ::

    from toolz import filter

    def compact(iter):
      return filter(None, iter)


  Example:

    >>> results = [0, 1, 2, None, 3, False]
    >>> list(compact(results))
    [1, 2, 3]
