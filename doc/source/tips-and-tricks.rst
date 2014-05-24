Tips and Tricks
===============

Toolz functions can be combined to yield other functions that, while commonly used, aren't
a part of toolz's standard library. This section presents
a few of these recipes.


* .. function:: pick(whitelist, dictionary)

  Return a subset of the provided dictionary with keys contained in the
  whitelist.

  ::

    from toolz import keyfilter

    def pick(whitelist, d):
        return keyfilter(lambda k: k in whitelist, d)



* .. function:: omit(blacklist, dictionary)

  Return a subset of the provided dictionary with keys *not* contained in the
  blacklist.

  ::

    from toolz import keyfilter, complement

    def pick(blacklist, d):
        return keyfilter(lambda k: k not in blacklist, d)


* .. function:: compact(iterable)

  Filter an iterable on "truthy" values.

  ::

    from toolz import filter

    def compact(iterable):
      return filter(None, iterable)
