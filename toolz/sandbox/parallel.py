from __future__ import annotations

import functools
from typing import TYPE_CHECKING, Callable, Iterable, Sequence, TypeVar, cast

from toolz.itertoolz import partition_all
from toolz.utils import no_default

if TYPE_CHECKING:
    from toolz.itertoolz import BinaryOp
    from toolz.utils import NoDefaultType

_T = TypeVar('_T')


def _reduce(
    func: BinaryOp[_T],
    seq: Iterable[_T],
    initial: _T | None = None,
) -> _T:
    if initial is None:
        return functools.reduce(func, seq)
    return functools.reduce(func, seq, initial)


def fold(
    binop: BinaryOp[_T],
    seq: Sequence[_T],
    default: _T | NoDefaultType = no_default,
    map: Callable = map,
    chunksize: int = 128,
    combine: BinaryOp[_T] | None = None,
) -> _T:
    """
    Reduce without guarantee of ordered reduction.

    inputs:

    ``binop``     - associative operator. The associative property allows us to
                    leverage a parallel map to perform reductions in parallel.
    ``seq``       - a sequence to be aggregated
    ``default``   - an identity element like 0 for ``add`` or 1 for mul

    ``map``       - an implementation of ``map``. This may be parallel and
                    determines how work is distributed.
    ``chunksize`` - Number of elements of ``seq`` that should be handled
                    within a single function call
    ``combine``   - Binary operator to combine two intermediate results.
                    If ``binop`` is of type (total, item) -> total
                    then ``combine`` is of type (total, total) -> total
                    Defaults to ``binop`` for common case of operators like add

    Fold chunks up the collection into blocks of size ``chunksize`` and then
    feeds each of these to calls to ``reduce``. This work is distributed
    with a call to ``map``, gathered back and then refolded to finish the
    computation. In this way ``fold`` specifies only how to chunk up data but
    leaves the distribution of this work to an externally provided ``map``
    function. This function can be sequential or rely on multithreading,
    multiprocessing, or even distributed solutions.

    If ``map`` intends to serialize functions it should be prepared to accept
    and serialize lambdas. Note that the standard ``pickle`` module fails
    here.

    Example
    -------

    >>> # Provide a parallel map to accomplish a parallel sum
    >>> from operator import add
    >>> fold(add, [1, 2, 3, 4], chunksize=2, map=map)
    10
    """
    # assert chunksize > 1
    chunksize = max(chunksize, 1)

    if combine is None:
        combine = binop

    chunks = partition_all(chunksize, seq)

    # Evaluate sequence in chunks via map
    if default == no_default:
        results = map(functools.partial(_reduce, binop), chunks)
    else:
        results = map(
            functools.partial(_reduce, binop, initial=default),
            chunks,
        )

    results = list(results)  # TODO: Support complete laziness

    if len(results) == 1:    # Return completed result
        res = results[0]
    else:                    # Recurse to reaggregate intermediate results
        res = fold(combine, results, map=map, chunksize=chunksize)
    return cast(_T, res)
