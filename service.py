__all__ = 'Service',

from types import FunctionType

class ServiceMeta(type):

    def __getattribute__(cls, name):
        if isinstance(super().__getattribute__(name), FunctionType) and name != 'proxy':
            result = super().__getattribute__('proxy')(name, super().__getattribute__)

            if result is not None:
                return result

        return super().__getattribute__(name)

class Service(metaclass = ServiceMeta):

    def __new__(cls, *_, **__):
        raise TypeError('Service class cannot be intialized')

    def proxy(name, getattr):
        '''When you access a function of a service, 
        you get name of a function and attr extractor for current class.
        Primarily designed for usage statistics, metrics, logging, etc

        if result is None: return unmodified value
        else: return result

        You may as well use decorators to achieve this, but this is a more general approach
            that allows modifying objects in batch

        Example:
            
        class MyService(Service):
            def proxy(name, getattr):
                def log(*args, **kwargs):
                    print(*args, **kwargs)

                def with_calls_logging(*args, **kwargs):
                    log(name, *args, **kwargs)
                    return getattr(name)(*args, **kwargs)

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

