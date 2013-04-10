import logging
import unittest
import inspect
from types import FunctionType, MethodType, UnboundMethodType


from kuyruk.loader import resolve, get_fully_qualified_function_name


logger = logging.getLogger(__name__)


def get_weather():
    return 'rainy'


class Car(object):

    @staticmethod
    def calculate_tax():
        return 3

    @classmethod
    def get_brand(cls):
        return 'Ford'

    def get_color(self):
        return 'red'


def _print(obj):
    try:
        self = obj.__self__
    except:
        self = None

    try:
        cls = obj.__self__.__name__
    except:
        cls = None

    print type(obj), 'name:', obj.__name__, obj
    print 'FunctionType:', isinstance(obj, FunctionType)
    print 'MethodType:', isinstance(obj, MethodType)
    print 'UnboundMethodType:', isinstance(obj, UnboundMethodType)
    print 'ismethod:', inspect.ismethod(obj)
    print '__self__:', self
    print 'class:', cls


_print(get_weather)
_print(Car.calculate_tax)
_print(Car.get_brand)
_print(Car.get_color)


class LoaderTestCase(unittest.TestCase):

    def test_loader(self):
        _assert('kuyruk.test.test_loader.get_weather', get_weather)
        _assert('kuyruk.test.test_loader.Car.calculate_tax', Car.calculate_tax)
        _assert('kuyruk.test.test_loader.Car.get_brand', Car.get_brand)
        _assert('kuyruk.test.test_loader.Car.get_color', Car.get_color)

    def test_get_name(self):
        assert get_fully_qualified_function_name(get_weather) == 'kuyruk.test.test_loader.get_weather'
        assert get_fully_qualified_function_name(Car.get_brand) == 'kuyruk.test.test_loader.Car.get_brand'


def _assert(s, f):
    resolved = resolve(s)
    _print(resolved)
    _print(f)
    assert resolved == f, 'Cannot resolve: %s' % s
