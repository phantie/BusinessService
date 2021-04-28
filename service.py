__all__ = 'Service',

from types import FunctionType


class ServiceMeta(type):
    def __new__(cls, name, bases, attrs):

        attrs['funcs'] = {k for k, v in attrs.items()
            if isinstance(v, FunctionType) and k != 'proxy'}

        return super().__new__(cls, name, bases, attrs)

    def __getattribute__(cls, name):
        if super().__getattribute__('proxy') and name in super().__getattribute__('funcs'):
            result = super().__getattribute__('proxy')(
                name, super().__getattribute__('__dict__'))

            if result is not None:
                return result

        return super().__getattribute__(name)

class Service(metaclass = ServiceMeta):
    def __new__(cls, *_, **__):
        raise TypeError('Service class cannot be intiated')

    def __repr__(self):
        return f'''{self.__class__.__name__}({
            ', '.join((f'{name}={value!r}'for name, value in self.dependencies.items()))})'''

    def __str__(self):
        return f"{self.__class__.__name__}({', '.join(self.dependencies)})"

    def proxy(name, __dict__):
        '''When you access a function of a service, 
        you get name of a function and dictionary of a class.
        Primarily designed for usage statistics, metrics, logging, etc

        If result returns None -> unmodifed value
        else -> result.
        You might as well use decorators to achieve this, but this is a more general approach
            that allows modifying objects in batch

        Example:
            
        class MyService(Service):
            def proxy(name, __dict__):
                def log(*args, **kwargs):
                    print(*args, **kwargs)

                def with_calls_logging(*args, **kwargs):
                    log(name, *args, **kwargs)
                    return __dict__[name](*args, **kwargs)

                if name in ('foo', 'bar'):
                    return with_calls_logging


            def foo(a, b):
                return a + b
            
            def bar(args):
                return sum(args)

            def baz():
                return 42

        assert MyService.foo(1, 2) == 3             # stdout: foo 1 2
        assert MyService.bar([1, 1, 2, 3, 5]) == 12 # stdout: bar [1, 1, 2, 3, 5]
        assert MyService.baz() == 42                # stdout:
        '''


