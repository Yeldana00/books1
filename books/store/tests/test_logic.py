from unittest import TestCase
# from django.test import TestCase
from store.logic import operations


class LogicTestCase(TestCase):
    def test_plus(self):
        result = operations(3, 4, '+')
        self.assertEqual(7, result)

    def test_minus(self):
        result = operations(10, 4, '-')
        self.assertEqual(6, result)

    def test_multi(self):
        result = operations(3, 4, '*')
        self.assertEqual(12, result)
