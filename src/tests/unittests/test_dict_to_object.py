import unittest
from parameterized import parameterized  # because it's fancy
from src.tests.unittests.TestCaseTurbo import TestCaseTurbo
from src.utils.domi_utils import dict_to_object as dto


class TestDictToObject(TestCaseTurbo):
    @parameterized.expand([
        ("simple point", ["x", "y"], [10, 12]),
        ("empty", [], []),
        ("string and bool values", ["str", "bool"], ["Domi Domi Domi", False]),
        ("list and None values", ["list", "null"], [[1, 2, 3], None])
    ])
    def test_dict_to_object_basic(self, name, keys, values):
        """
        Test that some basic dictionaries can be converted
        """
        # create dict to be tested
        zip_obj = zip(keys, values)
        dict_obj = dict(zip_obj)

        # tested function
        result = dto(dict_obj)

        # checking
        for k, v in zip(keys, values):
            self.assertHasAttr(result, k)  # checking if attribute generated
            self.assertEqual(getattr(result, k), v)  # checking if attribute has correct value

    @parameterized.expand([
        ("list", ["x", "y"]),
        ("None", None),
        ("bool", True),
        ("string", "Laci Laci Laci"),
        ("Number", 12.34)
    ])
    def test_dict_to_object_exception(self, name, not_dict):
        """
        Test that for non-dicts we get a nice TypeError
        """
        with self.assertRaises(TypeError):
            dto(not_dict)

    def test_dict_to_object_nested(self):
        """
        Test that nested dicts can be converted too
        """
        d = {
            "nested": {"x": 4}
        }
        result = dto(d)
        self.assertHasAttr(result.nested, "x")  # checking if attribute generated
        self.assertEqual(result.nested.x, 4)  # checking if attribute has correct value

    def test_dict_to_object_nested_compex(self):
        """
        Test that really nested dicts can be converted as well
        """
        d = {
            "array": [{"x": 4, "y": 10}, {"x": 2.4, "y": 0}, {"x": 1/3, "y": 10000}]
        }
        result = dto(d)
        self.assertHasAttr(result, "array")  # checking if attribute generated
        self.assertEqual(len(result.array), 3)  # checking array length
        self.assertHasAttr(result.array[2], "x")  # checking if attribute generated
        self.assertAlmostEqual(result.array[2].x, 1/3)  # checking value, floats are sometimes tricky :)
