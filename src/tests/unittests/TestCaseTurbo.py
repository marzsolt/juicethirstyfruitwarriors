import unittest

HAS_ATTR_MESSAGE = '{} should have an attribute {}'


# heavily based on:
# https://stackoverflow.com/questions/48078636/pythons-unittest-lacks-an-asserthasattr-method-what-should-i-use-instead
class TestCaseTurbo(unittest.TestCase):

    def assertHasAttr(self, obj, attribute_name, message=None):
        if not hasattr(obj, attribute_name):
            if message is not None:
                self.fail(message)
            else:
                self.fail(HAS_ATTR_MESSAGE.format(obj, attribute_name))
