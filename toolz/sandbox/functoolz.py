from toolz.functoolz import pipe


def pipeseq(seq, *funcs):
    """ Pipe each value in a sequence through a sequence of functions

    I.e. ``pipeseq(seq, f, g, h)`` is equivalent to each of the following
        pipe(seq, map(f), map(g), map(h))
        pipe(seq, map(map, [f, g, h]))
        map(h, map(g, map(f, seq)))
        map(compose(h, g, f), seq)

    >>> double = lambda i: 2 * i
    >>> list(pipeseq([3, 5, 7], double, str))
    ['6', '10', '14']

    See Also:
        pipe
        compose
        map
        thread_first
        thread_last
    """
    for item in seq:
        yield pipe(item, *funcs)