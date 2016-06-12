import sys
import types
from importlib import import_module


class TlzLoader(object):
    """ Finds and loads modules when added to sys.meta_path"""
    def _load_toolz(self, fullname):
        package, dot, submodules = fullname.partition('.')
        module_name = ''.join(['cytoolz', dot, submodules])
        try:
            module = import_module(module_name)
        except ImportError:
            module_name = ''.join(['toolz', dot, submodules])
            module = import_module(module_name)
        return module

    def find_module(self, fullname, path=None):  # pragma: py3 no cover
        package, dot, submodules = fullname.partition('.')
        if package == 'tlz':
            return self

    def load_module(self, fullname):  # pragma: py3 no cover
        if fullname in sys.modules:  # pragma: no cover
            return sys.modules[fullname]
        spec = TlzSpec(fullname, self)
        module = self.create_module(spec)
        sys.modules[fullname] = module
        self.exec_module(module)
        return module

    def find_spec(self, fullname, path, target=None):  # pragma: py2 no cover
        package, dot, submodules = fullname.partition('.')
        if package == 'tlz':
            return TlzSpec(fullname, self)

    def create_module(self, spec):
        module = types.ModuleType(spec.name)
        return module

    def exec_module(self, module):
        toolz_module = self._load_toolz(module.__name__)
        d = dict(toolz_module.__dict__, **module.__dict__)
        module.__dict__.update(d)
        package = toolz_module.__dict__['__package__']
        if package is not None:
            package, dot, submodules = package.partition('.')
            module.__dict__['__package__'] = ''.join(['tlz', dot, submodules])

        for k, v in toolz_module.__dict__.items():
            if (
                isinstance(v, types.ModuleType)
                and v.__package__ == toolz_module.__name__
            ):
                package, dot, submodules = v.__name__.partition('.')
                module_name = ''.join(['tlz', dot, submodules])
                submodule = import_module(module_name)
                module.__dict__[k] = submodule


class TlzSpec(object):
    def __init__(self, name, loader):
        self.name = name
        self.loader = loader
        self.origin = None
        self.submodule_search_locations = []
        self.loader_state = None
        self.cached = None
        self.parent = None
        self.has_location = False


sys.meta_path.append(TlzLoader())
