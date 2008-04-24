__all__ = ['deque', 'defaultdict', 'NamedTuple']

## from _collections import deque, defaultdict
from operator import itemgetter as _itemgetter
import sys as _sys

def NamedTuple(typename, s, verbose=False):
    """Returns a new subclass of tuple with named fields.

    >>> Point = NamedTuple('Point', 'x y')
    >>> Point.__doc__                   # docstring for the new class
    'Point(x, y)'
    >>> p = Point(11, y=22)             # instantiate with positional args or keywords
    >>> p[0] + p[1]                     # works just like the tuple (11, 22)
    33
    >>> x, y = p                        # unpacks just like a tuple
    >>> x, y
    (11, 22)
    >>> p.x + p.y                       # fields also accessable by name
    33
    >>> d = p.__asdict__()              # convert to a dictionary
    >>> d['x']
    11
    >>> Point(**d)                      # convert from a dictionary
    Point(x=11, y=22)
    >>> p.__replace__('x', 100)         # __replace__() is like str.replace() but targets a named field
    Point(x=100, y=22)

    """

    field_names = tuple(s.replace(',', ' ').split())    # names separated by spaces and/or commas
    if not ''.join((typename,) + field_names).replace('_', '').isalnum():
        raise ValueError('Type names and field names can only contain alphanumeric characters and underscores')
    if any(name.startswith('__') and name.endswith('__') for name in field_names):
        raise ValueError('Field names cannot start and end with double underscores')
    argtxt = repr(field_names).replace("'", "")[1:-1]   # tuple repr without parens or quotes
    reprtxt = ', '.join('%s=%%r' % name for name in field_names)
    template = '''class %(typename)s(tuple):
        '%(typename)s(%(argtxt)s)'
        __slots__ = ()
        __fields__ = %(field_names)r
        def __new__(cls, %(argtxt)s):
            return tuple.__new__(cls, (%(argtxt)s))
        def __repr__(self):
            return '%(typename)s(%(reprtxt)s)' %% self
        def __asdict__(self, dict=dict, zip=zip):
            'Return a new dict mapping field names to their values'
            return dict(zip(%(field_names)r, self))
        def __replace__(self, field, value, dict=dict, zip=zip):
            'Return a new %(typename)s object replacing one field with a new value'
            return %(typename)s(**dict(zip(%(field_names)r, self) + [(field, value)]))  \n''' % locals()
    for i, name in enumerate(field_names):
        template += '        %s = property(itemgetter(%d))\n' % (name, i)
    if verbose:
        print template
    m = dict(itemgetter=_itemgetter)
    exec template in m
    result = m[typename]
    if hasattr(_sys, '_getframe'):
        result.__module__ = _sys._getframe(1).f_globals['__name__']
    return result






if __name__ == '__main__':
    # verify that instances can be pickled
    from cPickle import loads, dumps
    Point = NamedTuple('Point', 'x, y', True)
    p = Point(x=10, y=20)
    assert p == loads(dumps(p))

    import doctest
    TestResults = NamedTuple('TestResults', 'failed attempted')
    print TestResults(*doctest.testmod())