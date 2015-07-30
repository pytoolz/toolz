def raises(err, lamda):
    try:
        lamda()
        return False
    except err:
        return True


@object.__new__
class no_default(object):
    def __new__(self):
        raise TypeError("cannot create 'no_default' instances")

    def __str__(self):
        return '<object no_default>'
    __repr__ = __str__
