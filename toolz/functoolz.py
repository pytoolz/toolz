from __future__ import annotations

import contextlib
import inspect
import sys
from functools import partial, reduce
from importlib import import_module
from operator import attrgetter, not_
from types import MethodType
from typing import TYPE_CHECKING, Any, Generic, TypeVar, cast, overload

if sys.version_info < (3, 10):
    from typing_extensions import ParamSpec
else:
    from typing import ParamSpec

from .utils import no_default

_S = TypeVar('_S')
_T = TypeVar('_T')
_U = TypeVar('_U')
_Instance = TypeVar('_Instance')
_P = ParamSpec('_P')

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping, Sequence
    from types import NotImplementedType

    from typing_extensions import Literal, TypeGuard, TypeVarTuple, Unpack

    _Ts = TypeVarTuple('_Ts')

    Getter = Callable[[_Instance], _T]
    Setter = Callable[[_Instance, _T], None]
    Deleter = Callable[[_Instance], None]
    InstancePropertyState = tuple[
        Getter[_Instance, _T] | None,
        Setter[_Instance, _T] | None,
        Deleter[_Instance] | None,
        str | None,
        _T,
    ]
    TransformOp = Callable[[_T], _S]
    TupleTransformBack = tuple[
        Callable[[Unpack[_Ts], _S], _T],
        Unpack[_Ts],
    ]  # >= py311
    TupleTransformFront = tuple[
        Callable[[_S, Unpack[_Ts]], _T],
        Unpack[_Ts],
    ]  # >= py311
    _CurryState = tuple


__all__ = ('identity', 'apply', 'thread_first', 'thread_last', 'memoize',
           'compose', 'compose_left', 'pipe', 'complement', 'juxt', 'do',
           'curry', 'flip', 'excepts')

PYPY = hasattr(sys, 'pypy_version_info')


def identity(x: _T) -> _T:
    """ Identity function. Return x

    >>> identity(3)
    3
    """
    return x


def apply(func: Callable[..., _T], /, *args: Any, **kwargs: Any) -> _T:
    """ Applies a function and returns the results

    >>> def double(x): return 2*x
    >>> def inc(x):    return x + 1
    >>> apply(double, 5)
    10

    >>> tuple(map(apply, [double, inc, double], [10, 500, 8000]))
    (20, 501, 16000)
    """
    return func(*args, **kwargs)


def thread_first(val: Any, *forms: TransformOp | TupleTransformFront) -> Any:
    """ Thread value through a sequence of functions/forms

    >>> def double(x): return 2*x
    >>> def inc(x):    return x + 1
    >>> thread_first(1, inc, double)
    4

    If the function expects more than one input you can specify those inputs
    in a tuple.  The value is used as the first input.

    >>> def add(x, y): return x + y
    >>> def pow(x, y): return x**y
    >>> thread_first(1, (add, 4), (pow, 2))  # pow(add(1, 4), 2)
    25

    So in general
        thread_first(x, f, (g, y, z))
    expands to
        g(f(x), y, z)

    See Also:
        thread_last
    """

    @overload
    def evalform_front(val: _S, form: TransformOp[_S, _T]) -> _T: ...

    @overload
    def evalform_front(
        val: _S, form: TupleTransformFront[_S, Unpack[_Ts], _T]
    ) -> _T: ...

    def evalform_front(
        val: _S,
        form: TransformOp[_S, _T] | TupleTransformFront[_S, Unpack[_Ts], _T],
    ) -> _T:
        if callable(form):
            return form(val)
        # if isinstance(form, tuple):
        func, args = form[0], form[1:]
        all_args = (val, *args)
        return func(*all_args)

    return reduce(evalform_front, forms, val)  # type: ignore[arg-type]


def thread_last(val: Any, *forms: TransformOp | TupleTransformBack) -> Any:
    """ Thread value through a sequence of functions/forms

    >>> def double(x): return 2*x
    >>> def inc(x):    return x + 1
    >>> thread_last(1, inc, double)
    4

    If the function expects more than one input you can specify those inputs
    in a tuple.  The value is used as the last input.

    >>> def add(x, y): return x + y
    >>> def pow(x, y): return x**y
    >>> thread_last(1, (add, 4), (pow, 2))  # pow(2, add(4, 1))
    32

    So in general
        thread_last(x, f, (g, y, z))
    expands to
        g(y, z, f(x))

    >>> def iseven(x):
    ...     return x % 2 == 0
    >>> list(thread_last([1, 2, 3], (map, inc), (filter, iseven)))
    [2, 4]

    See Also:
        thread_first
    """

    @overload
    def evalform_back(val: _S, form: TransformOp[_S, _T]) -> _T: ...

    @overload
    def evalform_back(
        val: _S, form: TupleTransformBack[Unpack[_Ts], _S, _T]
    ) -> _T: ...

    def evalform_back(
        val: _S,
        form: TransformOp[_S, _T] | TupleTransformBack[Unpack[_Ts], _S, _T],
    ) -> _T:
        if callable(form):
            return form(val)
        # if isinstance(form, tuple):
        func, args = form[0], form[1:]
        all_args = (*args, val)
        return func(*all_args)

    return reduce(evalform_back, forms, val)  # type: ignore[arg-type]


@overload
def instanceproperty(
    fget: Getter[_Instance, _T],
    fset: Setter[_Instance, _T] | None = ...,
    fdel: Deleter[_Instance] | None = ...,
    doc: str | None = ...,
    classval: _T | None = ...,
) -> InstanceProperty[_Instance, _T]: ...


@overload
def instanceproperty(
    fget: Literal[None] | None = None,
    fset: Setter[_Instance, _T] | None = ...,
    fdel: Deleter[_Instance] | None = ...,
    doc: str | None = ...,
    classval: _T | None = ...,
) -> Callable[[Getter[_Instance, _T]], InstanceProperty[_Instance, _T]]: ...


def instanceproperty(
    fget: Getter[_Instance, _T] | None = None,
    fset: Setter[_Instance, _T] | None = None,
    fdel: Deleter[_Instance] | None = None,
    doc: str | None = None,
    classval: _T | None = None,
) -> (
    InstanceProperty[_Instance, _T]
    | Callable[[Getter[_Instance, _T]], InstanceProperty[_Instance, _T]]
):
    """ Like @property, but returns ``classval`` when used as a class attribute

    >>> class MyClass(object):
    ...     '''The class docstring'''
    ...     @instanceproperty(classval=__doc__)
    ...     def __doc__(self):
    ...         return 'An object docstring'
    ...     @instanceproperty
    ...     def val(self):
    ...         return 42
    ...
    >>> MyClass.__doc__
    'The class docstring'
    >>> MyClass.val is None
    True
    >>> obj = MyClass()
    >>> obj.__doc__
    'An object docstring'
    >>> obj.val
    42
    """
    if fget is None:
        return partial(
            instanceproperty, fset=fset, fdel=fdel, doc=doc, classval=classval
        )
    return InstanceProperty(
        fget=fget, fset=fset, fdel=fdel, doc=doc, classval=classval
    )


class InstanceProperty(Generic[_Instance, _T], property):
    """ Like @property, but returns ``classval`` when used as a class attribute

    Should not be used directly.  Use ``instanceproperty`` instead.
    """

    def __init__(
        self,
        fget: Getter[_Instance, _T] | None = None,
        fset: Setter[_Instance, _T] | None = None,
        fdel: Deleter[_Instance] | None = None,
        doc: str | None = None,
        classval: _T | None = None,
    ) -> None:
        self.classval = classval
        property.__init__(self, fget=fget, fset=fset, fdel=fdel, doc=doc)

    @overload
    def __get__(self, obj: None, type: type | None = ...) -> _T | None: ...

    @overload
    def __get__(self, obj: _Instance, type: type | None = ...) -> _T: ...

    def __get__(
        self, obj: _Instance | None, type: type | None = None
    ) -> _T | None:
        if obj is None:
            return self.classval
        return cast(_T, property.__get__(self, obj, type))

    def __reduce__(
        self,
    ) -> tuple[type[InstanceProperty], InstancePropertyState]:
        state = (self.fget, self.fset, self.fdel, self.__doc__, self.classval)
        return InstanceProperty, state


def is_partial_function(func: Callable) -> TypeGuard[partial]:
    if (
        hasattr(func, 'func')
        and hasattr(func, 'args')
        and hasattr(func, 'keywords')
        and isinstance(func.args, tuple)
    ):
        return True
    return False


class curry(Generic[_T]):
    """ Curry a callable function

    Enables partial application of arguments through calling a function with an
    incomplete set of arguments.

    >>> def mul(x, y):
    ...     return x * y
    >>> mul = curry(mul)

    >>> double = mul(2)
    >>> double(10)
    20

    Also supports keyword arguments

    >>> @curry  # Can use curry as a decorator
    ... def f(x, y, a=10):
    ...     return a * (x + y)

    >>> add = f(a=1)
    >>> add(2, 3)
    5

    See Also:
        toolz.curried - namespace of curried functions
                        https://toolz.readthedocs.io/en/latest/curry.html
    """

    def __init__(
        self,
        # TODO: type hint that the returned value of a `partial` is _T
        func: curry[_T] | partial | Callable[..., _T],
        /,  # `func` is positional only, cannot be passed as keyword
        *args: Any,
        **kwargs: Any,
    ) -> None:
        if not callable(func):
            raise TypeError('Input must be callable')

        # curry- or functools.partial-like object?  Unpack and merge arguments
        if is_partial_function(func):
            _kwargs = {}
            if func.keywords:
                _kwargs.update(func.keywords)
            _kwargs.update(kwargs)
            kwargs = _kwargs
            args = func.args + args
            func = func.func

        if kwargs:
            self._partial = partial(func, *args, **kwargs)
        else:
            self._partial = partial(func, *args)

        self.__doc__ = getattr(func, '__doc__', None)
        self.__name__ = getattr(func, '__name__', '<curry>')
        self.__module__ = getattr(func, '__module__', '')
        self.__qualname__ = getattr(func, '__qualname__', '')
        self._sigspec: inspect.Signature | None = None
        self._has_unknown_args: bool | None = None

    @instanceproperty
    def func(self) -> Callable[..., _T]:
        return self._partial.func

    @instanceproperty
    def __signature__(self) -> inspect.Signature:
        sig = inspect.signature(self.func)
        args = self.args or ()
        keywords = self.keywords or {}
        if is_partial_args(self.func, args, keywords, sig) is False:
            raise TypeError('curry object has incorrect arguments')

        params = list(sig.parameters.values())
        skip = 0
        for param in params[: len(args)]:
            if param.kind == param.VAR_POSITIONAL:
                break
            skip += 1

        kwonly = False
        newparams = []
        for param in params[skip:]:
            kind = param.kind
            default = param.default
            if kind == param.VAR_KEYWORD:
                pass
            elif kind == param.VAR_POSITIONAL:
                if kwonly:
                    continue
            elif param.name in keywords:
                default = keywords[param.name]
                kind = param.KEYWORD_ONLY
                kwonly = True
            else:
                if kwonly:
                    kind = param.KEYWORD_ONLY
                if default is param.empty:
                    default = no_default
            newparams.append(param.replace(default=default, kind=kind))

        return sig.replace(parameters=newparams)

    @instanceproperty
    def args(self) -> tuple[Any, ...]:
        return self._partial.args

    @instanceproperty
    def keywords(self) -> dict[str, Any]:
        return self._partial.keywords

    @instanceproperty
    def func_name(self) -> str:
        return self.__name__

    def __str__(self) -> str:
        return str(self.func)

    def __repr__(self) -> str:
        return repr(self.func)

    def __hash__(self) -> int:
        return hash(
            (
                self.func,
                self.args,
                frozenset(self.keywords.items()) if self.keywords else None,
            )
        )

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, curry)
            and self.func == other.func
            and self.args == other.args
            and self.keywords == other.keywords
        )

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __call__(self, *args: Any, **kwargs: Any) -> _T | curry[_T]:
        try:
            return self.call(*args, **kwargs)
        except TypeError as exc:
            if self._should_curry(args, kwargs, exc):
                return self.bind(*args, **kwargs)
            raise

    def _should_curry(
        self,
        args: tuple[Any, ...],
        kwargs: Mapping,
        exc: Exception | None = None,  # noqa: ARG002
    ) -> bool:
        func = self.func
        args = self.args + args
        if self.keywords:
            kwargs = dict(self.keywords, **kwargs)
        if self._sigspec is None:
            sigspec = self._sigspec = _sigs.signature_or_spec(func)
            self._has_unknown_args = has_varargs(func, sigspec) is not False
        else:
            sigspec = self._sigspec

        if is_partial_args(func, args, kwargs, sigspec) is False:
            # Nothing can make the call valid
            return False
        if self._has_unknown_args:
            # The call may be valid and raised a TypeError, but we curry
            # anyway because the function may have `*args`.  This is useful
            # for decorators with signature `func(*args, **kwargs)`.
            return True
        if not is_valid_args(func, args, kwargs, sigspec):
            # Adding more arguments may make the call valid
            return True
        # There was a genuine TypeError
        return False

    def bind(self, *args: Any, **kwargs: Any) -> curry[_T]:
        return type(self)(self, *args, **kwargs)

    def call(self, *args: Any, **kwargs: Any) -> _T:
        return cast(_T, self._partial(*args, **kwargs))

    def __get__(self, instance: object, owner: type) -> curry[_T]:
        if instance is None:
            return self
        return curry(self, instance)

    def __reduce__(self) -> tuple[Callable, _CurryState]:
        func = self.func
        modname = getattr(func, '__module__', '')
        qualname = getattr(func, '__qualname__', '')
        if qualname is None:  # pragma: no cover
            qualname = getattr(func, '__name__', '')
        is_decorated = None
        if modname and qualname:
            attrs = []
            obj = import_module(modname)
            for attr in qualname.split('.'):
                if isinstance(obj, curry):
                    attrs.append('func')
                    obj = obj.func  # type: ignore[assignment]
                obj = getattr(obj, attr, None)  # type: ignore[assignment]
                if obj is None:
                    break
                attrs.append(attr)
            if isinstance(obj, curry) and obj.func is func:
                is_decorated = obj is self
                qualname = '.'.join(attrs)
                func = f'{modname}:{qualname}'  # type: ignore[assignment]

        # functools.partial objects can't be pickled
        userdict = tuple(
            (k, v)
            for k, v in self.__dict__.items()
            if k not in ('_partial', '_sigspec')
        )
        state = (
            type(self),
            func,
            self.args,
            self.keywords,
            userdict,
            is_decorated,
        )
        return _restore_curry, state


def _restore_curry(
    cls: type[curry[_T]],
    func: str | Callable[..., _T],
    args: tuple[Any, ...],
    kwargs: dict[str, Any],
    userdict: Mapping[str, Any],
    is_decorated: bool,
) -> curry[_T]:
    if isinstance(func, str):
        modname, qualname = func.rsplit(':', 1)
        obj = import_module(modname)
        for attr in qualname.split('.'):
            obj = getattr(obj, attr)
        if is_decorated:
            return obj  # type: ignore[return-value]
        func = obj.func
    # TODO: check that func is callable
    func = cast('Callable[..., _T]', func)
    obj = cls(func, *args, **(kwargs or {}))  # type: ignore[assignment]
    obj.__dict__.update(userdict)
    return obj  # type: ignore[return-value]


@curry
def memoize(
    func: Callable[..., _T],
    cache: dict[Any, _T] | None = None,
    key: Callable[[tuple, Mapping], Any] | None = None,
) -> Callable[..., _T]:
    """ Cache a function's result for speedy future evaluation

    Considerations:
        Trades memory for speed.
        Only use on pure functions.

    >>> def add(x, y): return x + y
    >>> add = memoize(add)

    Or use as a decorator

    >>> @memoize
    ... def add(x, y):
    ...     return x + y

    Use the ``cache`` keyword to provide a dict-like object as an initial cache

    >>> @memoize(cache={(1, 2): 3})
    ... def add(x, y):
    ...     return x + y

    Note that the above works as a decorator because ``memoize`` is curried.

    It is also possible to provide a ``key(args, kwargs)`` function that
    calculates keys used for the cache, which receives an ``args`` tuple and
    ``kwargs`` dict as input, and must return a hashable value.  However,
    the default key function should be sufficient most of the time.

    >>> # Use key function that ignores extraneous keyword arguments
    >>> @memoize(key=lambda args, kwargs: args)
    ... def add(x, y, verbose=False):
    ...     if verbose:
    ...         print('Calculating %s + %s' % (x, y))
    ...     return x + y
    """
    if cache is None:
        cache = {}

    try:
        may_have_kwargs = has_keywords(func) is not False
        # Is unary function (single arg, no variadic argument or keywords)?
        is_unary = is_arity(1, func)
    except TypeError:  # pragma: no cover
        may_have_kwargs = True
        is_unary = False

    if key is None:
        if is_unary:

            def key(args: tuple, kwargs: Mapping) -> Any:  # noqa: ARG001
                return args[0]
        elif may_have_kwargs:

            def key(args: tuple, kwargs: Mapping) -> Any:
                return (
                    args or None,
                    frozenset(kwargs.items()) if kwargs else None,
                )
        else:

            def key(args: tuple, kwargs: Mapping) -> Any:  # noqa: ARG001
                return args

    def memof(*args: Any, **kwargs: Any) -> _T:
        k = key(args, kwargs)
        try:
            return cache[k]
        except TypeError as err:
            msg = 'Arguments to memoized function must be hashable'
            raise TypeError(msg) from err
        except KeyError:
            cache[k] = result = func(*args, **kwargs)
            return result

    with contextlib.suppress(AttributeError):
        memof.__name__ = func.__name__
    memof.__doc__ = func.__doc__
    memof.__wrapped__ = func  # type: ignore[attr-defined]
    return memof


# TODO: requires a mypy plugin to type check a function chain
# see `returns.pipeline.flow`
class Compose:
    """ A composition of functions

    See Also:
        compose
    """

    __slots__ = ['first', 'funcs']

    def __init__(self, funcs: Sequence[Callable]) -> None:
        funcs = tuple(reversed(funcs))
        self.first: Callable = funcs[0]
        self.funcs: tuple[Callable, ...] = funcs[1:]

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        ret = self.first(*args, **kwargs)
        for f in self.funcs:
            ret = f(ret)
        return ret

    def __getstate__(self) -> tuple[Callable, tuple[Callable, ...]]:
        return self.first, self.funcs

    def __setstate__(
        self, state: tuple[Callable, tuple[Callable, ...]]
    ) -> None:
        self.first, self.funcs = state

    @instanceproperty(classval=__doc__)
    def __doc__(self) -> str:  # type: ignore[override]
        def composed_doc(*fs: Callable) -> str:
            """Generate a docstring for the composition of fs.
            """
            if not fs:
                # Argument name for the docstring.
                return '*args, **kwargs'

            f = fs[0].__name__
            g_or_args = composed_doc(*fs[1:])
            return f'{f}({g_or_args})'

        try:
            body = composed_doc(*reversed((self.first, *self.funcs)))
            return f'lambda *args, **kwargs: {body}'
        except AttributeError:
            # One of our callables does not have a `__name__`, whatever.
            return 'A composition of functions'

    @property
    def __name__(self) -> str:
        try:
            return '_of_'.join(
                f.__name__ for f in reversed((self.first, *self.funcs))
            )
        except AttributeError:
            return 'Compose'

    def __repr__(self) -> str:
        name = self.__class__.__name__
        funcs = tuple(reversed((self.first, *self.funcs)))
        return f'{name}{funcs!r}'

    def __eq__(self, other: Any) -> bool | NotImplementedType:
        if isinstance(other, Compose):
            return other.first == self.first and other.funcs == self.funcs
        return NotImplemented

    def __ne__(self, other: Any) -> bool | NotImplementedType:
        equality = self.__eq__(other)
        return NotImplemented if equality is NotImplemented else not equality

    def __hash__(self) -> int:
        return hash(self.first) ^ hash(self.funcs)

    # Mimic the descriptor behavior of python functions.
    # i.e. let Compose be called as a method when bound to a class.
    # adapted from
    # docs.python.org/3/howto/descriptor.html#functions-and-methods
    def __get__(self, obj: object, objtype: type | None = None) -> Any:
        return self if obj is None else MethodType(self, obj)

    # introspection with Signature is only possible from py3.3+
    @instanceproperty
    def __signature__(self) -> inspect.Signature:
        base = inspect.signature(self.first)
        last = inspect.signature(self.funcs[-1])
        return base.replace(return_annotation=last.return_annotation)

    __wrapped__ = instanceproperty(attrgetter('first'))


def compose(*funcs: Callable) -> Callable | Compose:
    """ Compose functions to operate in series.

    Returns a function that applies other functions in sequence.

    Functions are applied from right to left so that
    ``compose(f, g, h)(x, y)`` is the same as ``f(g(h(x, y)))``.

    If no arguments are provided, the identity function (f(x) = x) is returned.

    >>> inc = lambda i: i + 1
    >>> compose(str, inc)(3)
    '4'

    See Also:
        compose_left
        pipe
    """
    if not funcs:
        return identity
    if len(funcs) == 1:
        return funcs[0]
    return Compose(funcs)


def compose_left(*funcs: Callable) -> Callable | Compose:
    """ Compose functions to operate in series.

    Returns a function that applies other functions in sequence.

    Functions are applied from left to right so that
    ``compose_left(f, g, h)(x, y)`` is the same as ``h(g(f(x, y)))``.

    If no arguments are provided, the identity function (f(x) = x) is returned.

    >>> inc = lambda i: i + 1
    >>> compose_left(inc, str)(3)
    '4'

    See Also:
        compose
        pipe
    """
    return compose(*reversed(funcs))


def pipe(data: Any, *funcs: Callable) -> Any:
    """ Pipe a value through a sequence of functions

    I.e. ``pipe(data, f, g, h)`` is equivalent to ``h(g(f(data)))``

    We think of the value as progressing through a pipe of several
    transformations, much like pipes in UNIX

    ``$ cat data | f | g | h``

    >>> double = lambda i: 2 * i
    >>> pipe(3, double, str)
    '6'

    See Also:
        compose
        compose_left
        thread_first
        thread_last
    """
    for func in funcs:
        data = func(data)
    return data


def complement(func: Callable[[Any], bool]) -> Compose:
    """ Convert a predicate function to its logical complement.

    In other words, return a function that, for inputs that normally
    yield True, yields False, and vice-versa.

    >>> def iseven(n): return n % 2 == 0
    >>> isodd = complement(iseven)
    >>> iseven(2)
    True
    >>> isodd(2)
    False
    """
    return cast(Compose, compose(not_, func))


class juxt(Generic[_P, _T]):
    """ Creates a function that calls several functions with the same arguments

    Takes several functions and returns a function that applies its arguments
    to each of those functions then returns a tuple of the results.

    Name comes from juxtaposition: the fact of two things being seen or placed
    close together with contrasting effect.

    >>> inc = lambda x: x + 1
    >>> double = lambda x: x * 2
    >>> juxt(inc, double)(10)
    (11, 20)
    >>> juxt([inc, double])(10)
    (11, 20)
    """

    __slots__ = ['funcs']

    def __init__(self, *funcs: Callable[_P, _T]) -> None:
        if len(funcs) == 1 and not callable(funcs[0]):
            funcs = funcs[0]
        self.funcs: tuple[Callable[_P, _T], ...] = tuple(funcs)

    def __call__(self, *args: _P.args, **kwargs: _P.kwargs) -> tuple[_T, ...]:
        return tuple(func(*args, **kwargs) for func in self.funcs)

    def __getstate__(self) -> tuple[Callable[_P, _T], ...]:
        return self.funcs

    def __setstate__(self, state: tuple[Callable[_P, _T], ...]) -> None:
        self.funcs = state


def do(func: Callable[[_T], Any], x: _T) -> _T:
    """ Runs ``func`` on ``x``, returns ``x``

    Because the results of ``func`` are not returned, only the side
    effects of ``func`` are relevant.

    Logging functions can be made by composing ``do`` with a storage function
    like ``list.append`` or ``file.write``

    >>> from toolz import compose
    >>> from toolz.curried import do

    >>> log = []
    >>> inc = lambda x: x + 1
    >>> inc = compose(inc, do(log.append))
    >>> inc(1)
    2
    >>> inc(11)
    12
    >>> log
    [1, 11]
    """
    func(x)
    return x


@curry
def flip(func: Callable[[_S, _T], _U], a: _T, b: _S) -> _U:
    """ Call the function call with the arguments flipped

    This function is curried.

    >>> def div(a, b):
    ...     return a // b
    ...
    >>> flip(div, 2, 6)
    3
    >>> div_by_two = flip(div, 2)
    >>> div_by_two(4)
    2

    This is particularly useful for built in functions and functions defined
    in C extensions that accept positional only arguments. For example:
    isinstance, issubclass.

    >>> data = [1, 'a', 'b', 2, 1.5, object(), 3]
    >>> only_ints = list(filter(flip(isinstance, int), data))
    >>> only_ints
    [1, 2, 3]
    """
    return func(b, a)


def return_none(exc: Exception) -> Literal[None]:  # noqa: ARG001
    """ Returns None.
    """
    return None


class excepts(Generic[_P, _T]):
    """A wrapper around a function to catch exceptions and
    dispatch to a handler.

    This is like a functional try/except block, in the same way that
    ifexprs are functional if/else blocks.

    Examples
    --------
    >>> excepting = excepts(
    ...     ValueError,
    ...     lambda a: [1, 2].index(a),
    ...     lambda _: -1,
    ... )
    >>> excepting(1)
    0
    >>> excepting(3)
    -1

    Multiple exceptions and default except clause.

    >>> excepting = excepts((IndexError, KeyError), lambda a: a[0])
    >>> excepting([])
    >>> excepting([1])
    1
    >>> excepting({})
    >>> excepting({0: 1})
    1
    """

    exc: type[Exception] | tuple[type[Exception], ...]
    func: Callable[_P, _T]
    handler: Callable[[Exception], _T | None]

    def __init__(
        self,
        exc: type[Exception] | tuple[type[Exception], ...],
        func: Callable[_P, _T],
        handler: Callable[[Exception], _T | None] | None = None,
    ) -> None:
        self.exc = exc
        self.func = func
        self.handler = handler or return_none

    def __call__(self, *args: _P.args, **kwargs: _P.kwargs) -> _T | None:
        try:
            return self.func(*args, **kwargs)
        except self.exc as e:
            return self.handler(e)

    @instanceproperty(classval=__doc__)
    def __doc__(self) -> str:  # type: ignore[override]
        from textwrap import dedent

        exc = self.exc
        try:
            if isinstance(exc, tuple):
                names = ', '.join(map(attrgetter('__name__'), exc))
                exc_name = f'({names})'
            else:
                exc_name = exc.__name__

            return dedent(
                """\
                A wrapper around {inst.func.__name__!r} that will except:
                {exc}
                and handle any exceptions with {inst.handler.__name__!r}.

                Docs for {inst.func.__name__!r}:
                {inst.func.__doc__}

                Docs for {inst.handler.__name__!r}:
                {inst.handler.__doc__}
                """
            ).format(
                inst=self,
                exc=exc_name,
            )
        except AttributeError:
            return str(type(self).__doc__)

    @property
    def __name__(self) -> str:
        exc = self.exc
        try:
            if isinstance(exc, tuple):
                exc_name = '_or_'.join(map(attrgetter('__name__'), exc))
            else:
                exc_name = exc.__name__
            return f'{self.func.__name__}_excepting_{exc_name}'
        except AttributeError:
            return 'excepting'


def _has_signature_get(func: Callable) -> bool:
    if func not in _sigs.signatures:
        return False
    if not hasattr(func, '__signature__') or not hasattr(
        func.__signature__, '__get__'
    ):
        return False
    return True


def _check_sigspec_orig(
    sigspec: inspect.Signature | None,
    func: Callable,
    builtin_func: Callable[..., _S],
    *builtin_args: Any,
) -> tuple[None, _S | bool | None] | tuple[inspect.Signature, None]:
    if sigspec is None:
        try:
            sigspec = inspect.signature(func)
        except (ValueError, TypeError) as e:
            if isinstance(e, ValueError):
                return None, builtin_func(*builtin_args)
            if _has_signature_get(func):
                val = builtin_func(*builtin_args)
                return None, val
            return None, False
    return sigspec, None


if PYPY:  # pragma: no cover

    def _check_sigspec(
        sigspec: inspect.Signature | None,
        func: Callable,
        builtin_func: Callable[..., _S],
        *builtin_args: Any,
    ) -> tuple[None, _S | bool | None] | tuple[inspect.Signature, None]:
        # PyPy may lie, so use our registry for builtins instead
        if func in _sigs.signatures:
            val = builtin_func(*builtin_args)
            return None, val
        return _check_sigspec_orig(sigspec, func, builtin_func, *builtin_args)

else:
    _check_sigspec = _check_sigspec_orig


_check_sigspec.__doc__ = """ \
Private function to aid in introspection compatibly across Python versions.

If a callable doesn't have a signature (Python 3) or an argspec (Python 2),
the signature registry in toolz._signatures is used.
"""


def num_required_args(
    func: Callable,
    sigspec: inspect.Signature | None = None,
) -> int | bool | None:
    sigspec, rv = _check_sigspec(sigspec, func, _sigs._num_required_args, func)
    if sigspec is None:
        return rv
    return sum(
        1
        for p in sigspec.parameters.values()
        if p.default is p.empty
        and p.kind in (p.POSITIONAL_OR_KEYWORD, p.POSITIONAL_ONLY)
    )


def has_varargs(
    func: Callable,
    sigspec: inspect.Signature | None = None,
) -> bool | None:
    sigspec, rv = _check_sigspec(sigspec, func, _sigs._has_varargs, func)
    if sigspec is None:
        return rv
    return any(p.kind == p.VAR_POSITIONAL for p in sigspec.parameters.values())


def has_keywords(
    func: Callable,
    sigspec: inspect.Signature | None = None,
) -> bool | None:
    sigspec, rv = _check_sigspec(sigspec, func, _sigs._has_keywords, func)
    if sigspec is None:
        return rv
    return any(
        p.default is not p.empty or p.kind in (p.KEYWORD_ONLY, p.VAR_KEYWORD)
        for p in sigspec.parameters.values()
    )


def is_valid_args(
    func: Callable,
    args: tuple[Any, ...],
    kwargs: Mapping[str, Any],
    sigspec: inspect.Signature | None = None,
) -> bool | None:
    sigspec, rv = _check_sigspec(
        sigspec, func, _sigs._is_valid_args, func, args, kwargs
    )
    if sigspec is None:
        return rv
    try:
        sigspec.bind(*args, **kwargs)
    except TypeError:
        return False
    return True


def is_partial_args(
    func: Callable,
    args: tuple[Any, ...],
    kwargs: Mapping[str, Any],
    sigspec: inspect.Signature | None = None,
) -> bool | None:
    sigspec, rv = _check_sigspec(
        sigspec, func, _sigs._is_partial_args, func, args, kwargs
    )
    if sigspec is None:
        return rv
    try:
        sigspec.bind_partial(*args, **kwargs)
    except TypeError:
        return False
    return True


def is_arity(
    n: int,
    func: Callable,
    sigspec: inspect.Signature | None = None,
) -> bool | None:
    """ Does a function have only n positional arguments?

    This function relies on introspection and does not call the function.
    Returns None if validity can't be determined.

    >>> def f(x):
    ...     return x
    >>> is_arity(1, f)
    True
    >>> def g(x, y=1):
    ...     return x + y
    >>> is_arity(1, g)
    False
    """
    sigspec, rv = _check_sigspec(sigspec, func, _sigs._is_arity, n, func)
    if sigspec is None:
        return rv
    num = num_required_args(func, sigspec)
    if num is not None:
        num = num == n
        if not num:
            return False
    varargs = has_varargs(func, sigspec)
    if varargs:
        return False
    keywords = has_keywords(func, sigspec)
    if keywords:
        return False
    if num is None or varargs is None or keywords is None:  # pragma: no cover
        return None
    return True


num_required_args.__doc__ = """ \
Number of required positional arguments

    This function relies on introspection and does not call the function.
    Returns None if validity can't be determined.

    >>> def f(x, y, z=3):
    ...     return x + y + z
    >>> num_required_args(f)
    2
    >>> def g(*args, **kwargs):
    ...     pass
    >>> num_required_args(g)
    0
    """

has_varargs.__doc__ = """ \
Does a function have variadic positional arguments?

    This function relies on introspection and does not call the function.
    Returns None if validity can't be determined.

    >>> def f(*args):
    ...    return args
    >>> has_varargs(f)
    True
    >>> def g(**kwargs):
    ...    return kwargs
    >>> has_varargs(g)
    False
    """

has_keywords.__doc__ = """ \
Does a function have keyword arguments?

    This function relies on introspection and does not call the function.
    Returns None if validity can't be determined.

    >>> def f(x, y=0):
    ...     return x + y

    >>> has_keywords(f)
    True
    """

is_valid_args.__doc__ = """ \
Is ``func(*args, **kwargs)`` a valid function call?

    This function relies on introspection and does not call the function.
    Returns None if validity can't be determined.

    >>> def add(x, y):
    ...     return x + y

    >>> is_valid_args(add, (1,), {})
    False
    >>> is_valid_args(add, (1, 2), {})
    True
    >>> is_valid_args(map, (), {})
    False

    **Implementation notes**
    Python 2 relies on ``inspect.getargspec``, which only works for
    user-defined functions.  Python 3 uses ``inspect.signature``, which
    works for many more types of callables.

    Many builtins in the standard library are also supported.
    """

is_partial_args.__doc__ = """ \
Can partial(func, *args, **kwargs)(*args2, **kwargs2) be a valid call?

    Returns True *only* if the call is valid or if it is possible for the
    call to become valid by adding more positional or keyword arguments.

    This function relies on introspection and does not call the function.
    Returns None if validity can't be determined.

    >>> def add(x, y):
    ...     return x + y

    >>> is_partial_args(add, (1,), {})
    True
    >>> is_partial_args(add, (1, 2), {})
    True
    >>> is_partial_args(add, (1, 2, 3), {})
    False
    >>> is_partial_args(map, (), {})
    True

    **Implementation notes**
    Python 2 relies on ``inspect.getargspec``, which only works for
    user-defined functions.  Python 3 uses ``inspect.signature``, which
    works for many more types of callables.

    Many builtins in the standard library are also supported.
    """

from . import _signatures as _sigs  # noqa: E402
