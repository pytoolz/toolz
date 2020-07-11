Tips and Tricks
===============

Toolz functions can be combined to make functions that, while common, aren't
a part of toolz's standard offerings. This section presents
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

* .. function:: keyjoin(leftkey, leftseq, rightkey, rightseq)

  Inner join two sequences of dictionaries on specified keys, merging matches with right value
  precedence.

  ::

    from itertools import starmap
    from toolz import join, merge

    def keyjoin(leftkey, leftseq, rightkey, rightseq):
        return starmap(merge, join(leftkey, leftseq, rightkey, rightseq))


  Example:

   >>> people = [{'id': 0, 'name': 'Anonymous Guy', 'location': 'Unknown'},
                 {'id': 1, 'name': 'Karan', 'location': 'San Francisco'},
                 {'id': 2, 'name': 'Matthew', 'location': 'Oakland'}]
   >>> hobbies = [{'person_id': 1, 'hobby': 'Tennis'},
                  {'person_id': 1, 'hobby': 'Acting'},
                  {'person_id': 2, 'hobby': 'Biking'}]
   >>> list(keyjoin('id', people, 'person_id', hobbies))
   [{'hobby': 'Tennis',
     'id': 1,
     'location': 'San Francisco',
     'name': 'Karan',
     'person_id': 1},
    {'hobby': 'Acting',
     'id': 1,
     'location': 'San Francisco',
     'name': 'Karan',
     'person_id': 1},
    {'hobby': 'Biking',
     'id': 2,
     'location': 'Oakland',
     'name': 'Matthew',
     'person_id': 2}]

* .. function:: areidentical(\*seqs)

  Determine if sequences are identical element-wise.
  This lazily evaluates the sequences and stops as soon as the result
  is determined.

  ::

    from toolz import diff

    def areidentical(*seqs):
        return not any(diff(*seqs, default=object()))


  Example:

   >>> areidentical([1, 2, 3], (1, 2, 3))
   True

   >>> areidentical([1, 2, 3], [1, 2])
   False
