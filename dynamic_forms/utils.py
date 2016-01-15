import inspect
import types


def is_old_style_action(func):
    if isinstance(func, types.FunctionType):
        # it's a regular function
        argspec = inspect.getargspec(func)
        return len(argspec.args) == 2
    else:
        # it's class with __call__()
        argspec = inspect.getargspec(func.__call__)
        return len(argspec.args) == 3  # mind the 'self' arg


class RemovedIn05Warning(DeprecationWarning):
    pass


class RemovedIn06Warning(PendingDeprecationWarning):
    pass
